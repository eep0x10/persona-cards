"""Verify a Persona Cards snapshot without exposing application environment data."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile

ARTIFACTS = {"image.tar", "runtime-source.tgz", "docker-compose.prod.yml", ".env",
             "docker-compose.resolved.json", "runtime-state.json"}
CONTAINER = "personcard-personcard-1"


def run(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        # Docker/config diagnostics can contain expanded environment values.
        raise ValueError(f"Command failed: {args[0]} {args[1] if len(args)>1 else ''}")
    return result.stdout.strip()


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def inside(path: Path, parent: Path) -> bool:
    return path != parent and path.is_relative_to(parent)


def check_source_tar(path: Path) -> None:
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        names = {m.name.removeprefix("./") for m in members}
        if not {"Dockerfile", "docker-compose.prod.yml", "app/server.py"} <= names:
            raise ValueError("Source archive lacks required application files")
        for member in members:
            name = PurePosixPath(member.name)
            if name.is_absolute() or ".." in name.parts or "\\" in member.name or member.issym() or member.islnk() or member.isdev():
                raise ValueError("Unsafe source archive member")


def check_image_tar(path: Path, image_id: str, image_ref: str) -> None:
    with tarfile.open(path, "r:") as archive:
        handle = archive.extractfile("manifest.json")
        if handle is None:
            raise ValueError("Image archive has no Docker manifest")
        images = [image for image in json.load(handle) if image_ref in (image.get("RepoTags") or [])]
        if len(images) != 1:
            raise ValueError("Image archive does not preserve the active tag")
        config_name = images[0]["Config"]
        if PurePosixPath(config_name).is_absolute() or ".." in PurePosixPath(config_name).parts:
            raise ValueError("Unsafe image config path")
        config = archive.extractfile(config_name)
        if config is None:
            raise ValueError("Image archive configuration missing")
        config_hash = hashlib.sha256(config.read()).hexdigest()
        if config_hash != image_id.removeprefix("sha256:"):
            # Newer Docker/containerd stores may identify an image by OCI manifest
            # digest, while classic Docker uses the configuration digest.
            try:
                blob = archive.extractfile("blobs/sha256/" + image_id.removeprefix("sha256:"))
            except KeyError:
                blob = None
            raw = blob.read() if blob else b""
            if not raw or hashlib.sha256(raw).hexdigest() != image_id.removeprefix("sha256:"):
                raise ValueError("Image archive does not match saved image ID")
            def points_to_config(descriptor: dict, depth: int = 0) -> bool:
                if descriptor.get("config", {}).get("digest") == "sha256:" + config_hash:
                    return True
                if depth >= 3:
                    return False
                # Docker's containerd store may use an OCI index including
                # platform manifests and build attestations as the image ID.
                for child in descriptor.get("manifests", []):
                    child_digest = child.get("digest", "")
                    if not re.fullmatch(r"sha256:[0-9a-f]{64}", child_digest):
                        continue
                    try:
                        member = archive.extractfile("blobs/sha256/" + child_digest.removeprefix("sha256:"))
                    except KeyError:
                        continue
                    content = member.read() if member else b""
                    if content and hashlib.sha256(content).hexdigest() == child_digest.removeprefix("sha256:"):
                        if points_to_config(json.loads(content), depth + 1):
                            return True
                return False
            if not points_to_config(json.loads(raw)):
                raise ValueError("OCI manifest and image configuration differ")
        for layer in images[0].get("Layers", []):
            if PurePosixPath(layer).is_absolute() or ".." in PurePosixPath(layer).parts or not archive.getmember(layer).isfile():
                raise ValueError("Image archive layer is missing or unsafe")


def inspect_container(name: str = CONTAINER) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("Invalid container name")
    item = json.loads(run("docker", "inspect", name))[0]
    if item["State"]["Status"] != "running" or item["State"].get("Health", {}).get("Status") != "healthy":
        raise ValueError("Application container is not running and healthy")
    if item["Mounts"] or not item["HostConfig"]["ReadonlyRootfs"]:
        raise ValueError("Unexpected persistent mounts or writable root filesystem")
    if item["Config"]["User"] not in ("10001", "10001:10001"):
        raise ValueError("Unexpected application runtime user")
    return item


def verify(snapshot: Path, base: Path, phase: str = "current", max_age_minutes: int = 30) -> dict:
    base = base.resolve(strict=True)
    snapshots = (base / "snapshots").resolve(strict=True)
    if not inside(snapshots, base):
        raise ValueError("Snapshot directory leaves application base")
    snapshot = snapshot.resolve(strict=True)
    if not inside(snapshot, snapshots) or snapshot.parent != snapshots:
        raise ValueError("Snapshot must be a direct child of application snapshots")
    manifest_path = snapshot / "manifest.json"
    if manifest_path.is_symlink():
        raise ValueError("Manifest may not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != 1 or manifest.get("project") != "persona-cards" or manifest.get("base") != str(base):
        raise ValueError("Snapshot project/base contract mismatch")
    created = datetime.fromisoformat(manifest["created_at"])
    if created.tzinfo is None:
        raise ValueError("Snapshot timestamp requires timezone")
    age = (datetime.now(timezone.utc) - created).total_seconds()
    if not 1 <= max_age_minutes <= 30 or age < -60 or phase == "current" and age > max_age_minutes * 60:
        raise ValueError("Snapshot is outside the permitted freshness window (maximum 30 minutes)")
    head = manifest["head"]
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("Invalid release HEAD")
    release = Path(manifest["release_path"]).resolve(strict=True)
    if not inside(release, (base / "releases").resolve(strict=True)) or release.name != head:
        raise ValueError("Snapshot release does not match its HEAD")
    image_ref, image_id = manifest["image_ref"], manifest["image_id"]
    if image_ref != f"persona-cards:release-{head}" or not re.fullmatch(r"sha256:[0-9a-f]{64}", image_id):
        raise ValueError("Invalid snapshot image identity")
    if manifest.get("container") != CONTAINER or manifest.get("mounts") != [] or manifest.get("named_volumes") != [] or manifest.get("server_user_data") != "none; characters remain in browser storage":
        raise ValueError("Unexpected server persistence declaration")
    if set(manifest["files"]) != ARTIFACTS:
        raise ValueError("Snapshot artifact allowlist mismatch")
    for name, expected in manifest["files"].items():
        path = snapshot / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size <= 0:
            raise ValueError(f"Missing or unsafe snapshot artifact: {name}")
        if path.stat().st_size != expected["bytes"] or digest(path) != expected["sha256"]:
            raise ValueError(f"Snapshot checksum mismatch: {name}")
    source = release / "runtime-source.tgz"
    if source.is_symlink() or not source.is_file() or digest(source) != manifest["files"]["runtime-source.tgz"]["sha256"]:
        raise ValueError("Original release source no longer matches snapshot")
    if (snapshot / ".env").read_text(encoding="utf-8") != f"PERSONA_IMAGE={image_ref}\n":
        raise ValueError("Snapshot environment must contain only the saved application image")
    check_source_tar(snapshot / "runtime-source.tgz")
    check_image_tar(snapshot / "image.tar", image_id, image_ref)
    if phase in ("current", "activated"):
        container = inspect_container(manifest["container"])
        if container["Image"] != image_id or container["Config"]["Image"] != image_ref:
            raise ValueError("Running container no longer matches snapshot image")
        if phase == "current" and (base / "current").resolve(strict=True) != release:
            raise ValueError("Current release changed since snapshot")
    if phase in ("current", "loaded", "activated"):
        if json.loads(run("docker", "image", "inspect", image_ref))[0]["Id"] != image_id:
            raise ValueError("Docker image tag does not match saved image ID")
    return {"ok": True, "snapshot": str(snapshot), "manifest": str(manifest_path),
            "head": head, "image_ref": image_ref, "image_id": image_id, "phase": phase}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=Path("/home/deploy/persona-cards"))
    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--latest", action="store_true")
    select.add_argument("--snapshot", type=Path)
    parser.add_argument("--phase", choices=["current", "archive", "loaded", "activated"], default="current")
    parser.add_argument("--max-age-minutes", type=int, default=30)
    args = parser.parse_args()
    if args.latest and args.phase != "current":
        parser.error("--latest is only for fresh pre-deploy verification; recovery requires an explicit --snapshot")
    snapshot = args.snapshot
    if args.latest:
        candidates = [p.parent for p in (args.base / "snapshots").glob("*/manifest.json")]
        if not candidates:
            parser.error("No completed snapshots")
        snapshot = max(candidates, key=lambda p: p.name)
    try:
        print(json.dumps(verify(snapshot, args.base, args.phase, args.max_age_minutes)))
    except (ValueError, KeyError, OSError, tarfile.TarError, json.JSONDecodeError) as error:
        parser.exit(1, f"Snapshot verification failed: {error}\n")


if __name__ == "__main__":
    main()
