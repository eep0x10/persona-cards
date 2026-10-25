"""Save the healthy Persona Cards image and private deployment inputs for rollback."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import uuid

from verify_snapshot import ARTIFACTS, CONTAINER, digest, inside, inspect_container, run, verify


def create_snapshot(base: Path) -> dict:
    base = base.resolve(strict=True)
    releases = (base / "releases").resolve(strict=True)
    release = (base / "current").resolve(strict=True)
    if not inside(releases, base) or not inside(release, releases) or not re.fullmatch(r"[0-9a-f]{40}", release.name):
        raise ValueError("Current must resolve to a versioned release inside the application releases")
    head = release.name
    container = inspect_container()
    image_ref, image_id = container["Config"]["Image"], container["Image"]
    if image_ref != f"persona-cards:release-{head}":
        raise ValueError("Current release HEAD and running image tag differ")
    image = json.loads(run("docker", "image", "inspect", image_ref))[0]
    if image["Id"] != image_id:
        raise ValueError("Active image tag moved")
    revision_label = (image.get("Config", {}).get("Labels") or {}).get("org.opencontainers.image.revision")
    if revision_label is not None and revision_label != head:
        raise ValueError("Image revision label contradicts release HEAD")
    for name in ("docker-compose.prod.yml", ".env", "runtime-source.tgz"):
        path = release / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or symlinked release input: {name}")
    env_lines = (release / ".env").read_text(encoding="utf-8").splitlines()
    if any(line.strip() and not line.lstrip().startswith("#") and not line.startswith(("PERSONA_IMAGE=", "COMPOSE_PROJECT_NAME=")) for line in env_lines):
        raise ValueError("Application .env contains unexpected keys; do not snapshot a global stack environment")
    if any(line.startswith("COMPOSE_PROJECT_NAME=") and line != "COMPOSE_PROJECT_NAME=personcard" for line in env_lines):
        raise ValueError("Unexpected Compose project name")
    config = json.loads(run("docker", "compose", "-p", "personcard", "--env-file", str(release / ".env"),
                            "-f", str(release / "docker-compose.prod.yml"), "config", "--format", "json"))
    if set(config["services"]) != {"personcard"} or config.get("volumes"):
        raise ValueError("Unexpected services or named volumes")
    service = config["services"]["personcard"]
    if service.get("volumes") or not service.get("read_only") or service.get("image") != image_ref:
        raise ValueError("Compose does not describe the active stateless application")
    if set(service.get("environment", {})) - {"VIRTUAL_HOST", "VIRTUAL_PORT", "CERT_NAME"}:
        raise ValueError("Unexpected application environment keys")
    health = json.loads(run("docker", "exec", CONTAINER, "python", "-c",
                            "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=5).read().decode())"))
    if health.get("status") != "ok":
        raise ValueError("Application HTTP health failed")
    os.umask(0o077)
    snapshots = base / "snapshots"
    snapshots.mkdir(mode=0o700, exist_ok=True)
    if not inside(snapshots.resolve(), base):
        raise ValueError("Snapshots directory leaves application base")
    now = datetime.now(timezone.utc)
    target = snapshots / (now.strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex)
    target.mkdir(mode=0o700)
    for name in ("runtime-source.tgz", "docker-compose.prod.yml"):
        shutil.copyfile(release / name, target / name)
    (target / ".env").write_text(f"PERSONA_IMAGE={image_ref}\n", encoding="utf-8")
    (target / "docker-compose.resolved.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    state = {"container": CONTAINER, "image_ref": image_ref, "image_id": image_id,
             "user": container["Config"]["User"], "read_only": True, "mounts": [],
             "health": health, "networks": list(container["NetworkSettings"]["Networks"])}
    (target / "runtime-state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    run("docker", "image", "save", "--output", str(target / "image.tar"), image_ref)
    manifest = {"version": 1, "project": "persona-cards", "created_at": now.isoformat(),
                "base": str(base), "release_path": str(release), "head": head,
                "image_revision_label": revision_label, "container": CONTAINER,
                "image_ref": image_ref, "image_id": image_id, "mounts": [], "named_volumes": [],
                "server_user_data": "none; characters remain in browser storage",
                "files": {name: {"bytes": (target / name).stat().st_size, "sha256": digest(target / name)}
                          for name in sorted(ARTIFACTS)}}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    # Validate the saved tar and detect release/container changes during export.
    try:
        return verify(target, base)
    except Exception:
        # Keep partial artifacts for diagnosis, but never advertise a completed snapshot.
        (target / "manifest.json").rename(target / "manifest.failed.json")
        raise


def repository_state(base: Path, allowed_heads: set[str]) -> str | None:
    repository = base / "repository"
    if not repository.exists():
        return None
    if not inside(repository.resolve(strict=True), base) or not (repository / ".git").exists():
        raise ValueError("Recovery repository is not a real application checkout")
    if run("git", "-C", str(repository), "status", "--porcelain", "--untracked-files=all"):
        raise ValueError("Recovery refused: repository has local changes; preserve and resolve them first")
    env = repository / ".env"
    if env.exists():
        if env.is_symlink() or any(line.strip() and not line.lstrip().startswith("#") and
                                  not line.startswith(("PERSONA_IMAGE=", "COMPOSE_PROJECT_NAME="))
                                  for line in env.read_text(encoding="utf-8").splitlines()):
            raise ValueError("Recovery repository environment contains unexpected application keys")
    head = run("git", "-C", str(repository), "rev-parse", "HEAD")
    if head not in allowed_heads:
        raise ValueError("Recovery refused: repository HEAD differs from both current and snapshot releases")
    return head


def prepare_rollback(snapshot: Path, base: Path) -> dict:
    """Check Git before any container change and preserve a sanitized incident receipt."""
    base = base.resolve(strict=True)
    checked = verify(snapshot, base, "archive")
    current = (base / "current").resolve(strict=True)
    if not inside(current, (base / "releases").resolve(strict=True)):
        raise ValueError("Current pointer leaves application releases")
    pointer = base / "current"
    if not pointer.is_symlink() and not getattr(pointer, "is_junction", lambda: False)():
        raise ValueError("Current must be a release pointer before recovery")
    before_head = repository_state(base, {checked["head"], current.name})
    if before_head is not None:
        run("git", "-C", str(base / "repository"), "cat-file", "-e", checked["head"] + "^{commit}")
    try:
        active = json.loads(run("docker", "inspect", CONTAINER))[0]
        incident = {"image_ref": active["Config"]["Image"], "image_id": active["Image"],
                    "status": active["State"]["Status"]}
    except (ValueError, KeyError):
        incident = {"status": "container unavailable"}
    os.umask(0o077)
    events = base / "recovery-events"
    events.mkdir(mode=0o700, exist_ok=True)
    if not inside(events.resolve(), base):
        raise ValueError("Recovery receipt directory leaves application base")
    now = datetime.now(timezone.utc)
    receipt = events / (now.strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex + ".json")
    record = {"version": 1, "action": "rollback", "status": "prepared", "created_at": now.isoformat(),
              "base": str(base), "snapshot": checked["snapshot"], "head": checked["head"],
              "current_before": str(current), "repository_head_before": before_head, "incident": incident}
    receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "receipt": str(receipt), "snapshot": checked["snapshot"], "head": checked["head"]}


def finish_rollback(receipt: Path, base: Path) -> dict:
    """Reconcile the clean Git checkout and current pointer after healthy recovery."""
    base = base.resolve(strict=True)
    receipt = receipt.resolve(strict=True)
    if receipt.parent != (base / "recovery-events").resolve(strict=True) or receipt.is_symlink():
        raise ValueError("Invalid recovery receipt path")
    record = json.loads(receipt.read_text(encoding="utf-8"))
    if record.get("base") != str(base) or record.get("status") != "prepared":
        raise ValueError("Recovery receipt is invalid or already completed")
    checked = verify(Path(record["snapshot"]), base, "activated")
    if checked["head"] != record["head"]:
        raise ValueError("Recovery receipt and snapshot HEAD differ")
    target = (base / "releases" / checked["head"]).resolve(strict=True)
    current = base / "current"
    if str(current.resolve(strict=True)) != record["current_before"]:
        raise ValueError("Current release changed during recovery; refusing to overwrite another deployment")
    before_head = record["repository_head_before"]
    actual_head = repository_state(base, {before_head} if before_head else set())
    if actual_head != before_head:
        raise ValueError("Repository changed during recovery")
    if before_head is not None:
        run("git", "-C", str(base / "repository"), "checkout", "--detach", "--no-overwrite-ignore", checked["head"])
        (base / "repository" / ".env").write_text(
            f"COMPOSE_PROJECT_NAME=personcard\nPERSONA_IMAGE={checked['image_ref']}\n", encoding="utf-8")
    if not current.is_symlink() and not getattr(current, "is_junction", lambda: False)():
        raise ValueError("Current is not a release pointer; refusing to replace a directory")
    # Both paths are validated children of the application base; only the pointer
    # is replaced. Release directories and incident artifacts remain untouched.
    temporary = base / (".current-recovery-" + uuid.uuid4().hex)
    temporary.symlink_to(target, target_is_directory=True)
    os.replace(temporary, current)
    record.update(status="restored", completed_at=datetime.now(timezone.utc).isoformat())
    receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "receipt": str(receipt), "current": str(target), "head": checked["head"]}


def verify_release_lock(base: Path, descriptor: int) -> None:
    """An inherited FD is a capability only for this application's lock inode."""
    import fcntl
    base = base.resolve(strict=True)
    path = base / ".release.lock"
    if descriptor < 3 or path.is_symlink():
        raise ValueError("Invalid inherited release lock")
    expected, actual = path.stat(), os.fstat(descriptor)
    if (expected.st_dev, expected.st_ino) != (actual.st_dev, actual.st_ino):
        raise ValueError("Inherited FD is not the application release lock")
    # Same inherited open-file description succeeds; a competing holder fails.
    fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)


def run_rollback(snapshot: Path, base: Path, descriptor: int | None = None) -> int:
    import fcntl
    base = base.resolve(strict=True)
    owned = descriptor is None
    if owned:
        path = base / ".release.lock"
        descriptor = os.open(path, os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
        fcntl.flock(descriptor, fcntl.LOCK_EX)
    try:
        verify_release_lock(base, descriptor)
        return subprocess.run(["bash", str(Path(__file__).with_name("rollback.sh")),
                               "--locked-fd", str(descriptor), str(snapshot)],
                              pass_fds=(descriptor,)).returncode
    finally:
        if owned:
            os.close(descriptor)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=Path("/home/deploy/persona-cards"))
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--prepare-rollback", type=Path)
    action.add_argument("--finish-rollback", type=Path)
    action.add_argument("--run-rollback", type=Path)
    parser.add_argument("--lock-fd", type=int, help="Internal inherited application lock descriptor")
    args = parser.parse_args()
    try:
        if args.lock_fd is not None and not args.run_rollback:
            parser.error("--lock-fd is only valid for the rollback runner")
        if args.run_rollback:
            raise SystemExit(run_rollback(args.run_rollback, args.base, args.lock_fd))
        if args.prepare_rollback:
            result = prepare_rollback(args.prepare_rollback, args.base)
        elif args.finish_rollback:
            result = finish_rollback(args.finish_rollback, args.base)
        else:
            result = create_snapshot(args.base)
        print(json.dumps(result))
    except (ValueError, KeyError, OSError, tarfile.TarError, json.JSONDecodeError) as error:
        parser.exit(1, f"Snapshot failed: {error}\n")


if __name__ == "__main__":
    main()
