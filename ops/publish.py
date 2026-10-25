"""Publish one already-pushed revision after the registered production preflight."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BASE = "/home/deploy/persona-cards"
SSH_TARGET = "deploy@187.127.28.169"
IDENTITY = Path("C:/Users/eep0x10/.ssh/do_deploy")
PREFLIGHT = "C:/Users/eep0x10/bin/codex-prod-preflight.ps1"
RECEIPT = Path("C:/Users/eep0x10/.codex/state/production-guard/persona-cards.json")
RUNTIME_PATHS = [".dockerignore", "Dockerfile", "docker-compose.prod.yml", ".codex/release-contract.json",
                 "app/package.json", "app/package-lock.json", "app/index.html", "app/vite.config.js",
                 "app/server.py", "app/requirements.lock.txt", "app/src", "app/public",
                 "deck/illustration_sheets_5_2.json", "ops"]


def run(args: list[str], *, input_text: str | None = None) -> str:
    result = subprocess.run(args, cwd=ROOT, input=input_text, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        # Keep command diagnostics bounded, including the actionable error, without
        # ever reading an environment file or dumping process environments.
        raise RuntimeError(f"Command failed ({Path(args[0]).name}): " + (result.stderr or result.stdout)[-1800:])
    return result.stdout.strip()


def git(*args: str) -> str:
    return run(["git", *args])


def check_local(expected: str | None = None) -> str:
    if git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Tracked changes remain; commit them before publication. Untracked drafts are not archived.")
    head = git("rev-parse", "HEAD")
    if expected is not None and head != expected:
        raise ValueError("Local HEAD differs from --expected-revision")
    git("fetch", "--quiet", "origin", "main")
    if git("rev-parse", "origin/main") != head:
        raise ValueError("HEAD must equal origin/main; publish never pushes or resets Git")
    return head


def remote(script: str, *args: str) -> dict:
    command = "python3 - " + shlex.join([BASE, *args])
    output = run(["ssh", "-i", str(IDENTITY), "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                  SSH_TARGET, command], input_text=script)
    return json.loads(output.splitlines()[-1])


COMMON = '''
import fcntl, hashlib, json, os, re, subprocess, sys, tarfile, uuid
from pathlib import Path, PurePosixPath
base=Path(sys.argv[1]).resolve(strict=True)
if str(base)!='/home/deploy/persona-cards': raise ValueError('Unexpected application base')
head=sys.argv[2]
if not re.fullmatch(r'[0-9a-f]{40}',head): raise ValueError('Invalid revision')
release=base/'releases'/head
tag='persona-cards:release-'+head
def run(*args):
 r=subprocess.run(args,capture_output=True,text=True)
 if r.returncode: raise RuntimeError('Remote command failed: '+args[0]+' '+(args[1] if len(args)>1 else ''))
 return r.stdout.strip()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
os.umask(0o077)
'''

PREPARE = COMMON + '''
release.mkdir(parents=True,exist_ok=True)
if not release.resolve().is_relative_to((base/'releases').resolve()): raise ValueError('Release path escaped base')
archive=release/'runtime-source.tgz'
if archive.exists():
 if archive.is_symlink() or sha(archive)!=sys.argv[3]: raise ValueError('Immutable release archive differs; inspect existing release')
 print(json.dumps({'upload':False}))
else:
 upload=release/('.upload-'+uuid.uuid4().hex+'.tgz')
 print(json.dumps({'upload':True,'path':str(upload)}))
'''

BUILD = COMMON + '''
archive=release/'runtime-source.tgz'
if sys.argv[4]:
 upload=Path(sys.argv[4])
 if upload.parent!=release or not upload.name.startswith('.upload-') or upload.is_symlink(): raise ValueError('Invalid upload path')
 if sha(upload)!=sys.argv[3]: raise ValueError('Uploaded archive checksum differs')
 if archive.exists(): raise ValueError('Release archive appeared during upload; refusing overwrite')
 upload.rename(archive)
if sha(archive)!=sys.argv[3]:raise ValueError('Release archive checksum differs')
with tarfile.open(archive,'r:gz') as tar:
 for member in tar.getmembers():
  name=PurePosixPath(member.name)
  if name.is_absolute() or '..' in name.parts or member.issym() or member.islnk() or member.isdev(): raise ValueError('Unsafe runtime source member')
  dest=release/member.name
  if member.isdir(): dest.mkdir(parents=True,exist_ok=True)
  elif member.isfile():
   dest.parent.mkdir(parents=True,exist_ok=True)
   content=tar.extractfile(member)
   if dest.exists():
    if dest.is_symlink() or hashlib.sha256(content.read()).hexdigest()!=sha(dest): raise ValueError('Immutable release source differs')
   else:
    with dest.open('xb') as output:
     import shutil
     shutil.copyfileobj(content,output)
  else:raise ValueError('Unexpected source member type')
env=release/'.env'
expected_env='COMPOSE_PROJECT_NAME=personcard\\nPERSONA_IMAGE='+tag+'\\n'
if env.exists() and env.read_text()!=expected_env:raise ValueError('Immutable release environment differs')
env.write_text(expected_env)
existing=subprocess.run(['docker','image','inspect',tag],capture_output=True,text=True)
if existing.returncode==0:
 image=json.loads(existing.stdout)[0]
 if (image.get('Config',{}).get('Labels') or {}).get('org.opencontainers.image.revision')!=head: raise ValueError('Existing image tag lacks matching immutable revision label')
else:
 evidence=base/'evidence';evidence.mkdir(exist_ok=True)
 log=evidence/('build-'+head+'.log')
 with log.open('a') as output:
  result=subprocess.run(['docker','build','--label','org.opencontainers.image.revision='+head,'-t',tag,str(release)],stdout=output,stderr=subprocess.STDOUT)
 if result.returncode:raise RuntimeError('Build failed; inspect '+str(log))
image=json.loads(run('docker','image','inspect',tag))[0]
print(json.dumps({'ok':True,'image_ref':tag,'image_id':image['Id'],'release':str(release)}))
'''

ACTIVATE = COMMON + '''
snapshot=Path(sys.argv[3])
repository=base/'repository'
ops=release/'ops'
evidence=base/'evidence';evidence.mkdir(exist_ok=True)
lock=(base/'.release.lock').open('a')
fcntl.flock(lock,fcntl.LOCK_EX)
run('python3',str(ops/'verify_snapshot.py'),'--base',str(base),'--snapshot',str(snapshot))
if run('git','-C',str(repository),'status','--porcelain','--untracked-files=all'): raise ValueError('Production Git checkout is dirty; no discard or automatic stash')
run('git','-C',str(repository),'fetch','--quiet','origin','main')
if run('git','-C',str(repository),'rev-parse','FETCH_HEAD')!=head: raise ValueError('Remote origin/main changed before activation')
if run('git','-C',str(repository),'ls-remote','origin','refs/heads/main').split()[0]!=head: raise ValueError('Upstream moved before activation')
image=json.loads(run('docker','image','inspect',tag))[0]
if (image.get('Config',{}).get('Labels') or {}).get('org.opencontainers.image.revision')!=head: raise ValueError('Image revision does not match publication')
previous_head=run('git','-C',str(repository),'rev-parse','HEAD')
current=base/'current'
if not current.is_symlink():raise ValueError('Current is not a release symlink')
previous_target=current.resolve(strict=True)
if not previous_target.is_relative_to((base/'releases').resolve()):raise ValueError('Current escaped releases')
receipt=evidence/('publish-'+head+'.json')
receipt.write_text(json.dumps({'revision':head,'snapshot':str(snapshot),'previous_head':previous_head,'previous_target':str(previous_target),'status':'activating'},indent=2)+'\\n')
switched=False
try:
 run('git','-C',str(repository),'checkout','--detach','--no-overwrite-ignore',head)
 pointer=base/('.current-publish-'+uuid.uuid4().hex)
 pointer.symlink_to(release,target_is_directory=True)
 os.replace(pointer,current);switched=True
 (repository/'.env').write_text('COMPOSE_PROJECT_NAME=personcard\\nPERSONA_IMAGE='+tag+'\\n')
 result=subprocess.run(['docker','compose','-p','personcard','-f',str(repository/'docker-compose.prod.yml'),'--env-file',str(repository/'.env'),'up','-d','--no-build','--wait','personcard'],capture_output=True,text=True)
 (evidence/('activate-'+head+'.log')).write_text(result.stdout+'\\n'+result.stderr)
 if result.returncode:raise RuntimeError('Compose activation failed')
 container=json.loads(run('docker','inspect','personcard-personcard-1'))[0]
 if container['Image']!=image['Id'] or container['State'].get('Health',{}).get('Status')!='healthy':raise ValueError('Activated image or health differs')
 health=json.loads(run('docker','exec','personcard-personcard-1','python','-c',"import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=5).read().decode())"))
 if health!={'status':'ok','version':'5.2','cards':166}:raise ValueError('5.2 application health invariant failed')
 boot=subprocess.run(['docker','logs','--tail','40','personcard-personcard-1'],capture_output=True,text=True)
 (evidence/('boot-'+head+'.log')).write_text(boot.stdout+'\\n'+boot.stderr)
 if boot.returncode:raise RuntimeError('Cannot collect boot logs')
 (evidence/'deployment.txt').write_text(head+'\\n')
 receipt.write_text(json.dumps({'revision':head,'snapshot':str(snapshot),'image_id':image['Id'],'status':'healthy','health':health},indent=2)+'\\n')
 print(json.dumps({'ok':True,'head':head,'health':health,'snapshot':str(snapshot)}))
except Exception:
 if switched:
  with (evidence/('rollback-'+head+'.log')).open('a') as output:
   rollback=subprocess.run(['bash',str(ops/'rollback.sh'),str(snapshot),'--lock-fd',str(lock.fileno())],stdout=output,stderr=subprocess.STDOUT,pass_fds=(lock.fileno(),))
  if rollback.returncode:raise RuntimeError('Activation failed AND automatic rollback failed; inspect rollback log and preserve incident state')
 else:
  if run('git','-C',str(repository),'rev-parse','HEAD')==head and not run('git','-C',str(repository),'status','--porcelain','--untracked-files=all'):
   run('git','-C',str(repository),'checkout','--detach','--no-overwrite-ignore',previous_head)
 raise RuntimeError('Activation failed; previous deployment preserved or recovered, inspect activation/rollback logs')
'''

RECOVER = COMMON + '''
snapshot=sys.argv[3]
with (base/'.release.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 current=(base/'current').resolve(strict=True)
 repository=base/'repository'
 active=json.loads(run('docker','inspect','personcard-personcard-1'))[0]
 if current!=release or run('git','-C',str(repository),'rev-parse','HEAD')!=head or active['Config']['Image']!=tag:
  raise ValueError('Obsolete public-health recovery: another release is active; preserve it and inspect the failed publication')
 if (json.loads(run('docker','image','inspect',tag))[0]['Id'])!=active['Image']:
  raise ValueError('Obsolete public-health recovery: active image ID changed')
 with (base/'evidence'/('rollback-public-'+head+'.log')).open('a') as output:
  result=subprocess.run(['bash',str(release/'ops/rollback.sh'),snapshot,'--lock-fd',str(lock.fileno())],stdout=output,stderr=subprocess.STDOUT,pass_fds=(lock.fileno(),))
 if result.returncode:raise RuntimeError('Public health failed and recovery requires operator inspection')
print(json.dumps({'ok':True,'action':'rollback'}))
'''


def production_preflight() -> Path:
    pwsh = shutil.which("pwsh")
    if pwsh is None:
        raise ValueError("PowerShell 7 is required for the registered production preflight")
    output = run([pwsh, "-NoProfile", "-File", PREFLIGHT, "persona-cards"])
    print(output[-1200:], flush=True)
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8-sig"))
    if receipt.get("status") != "ready" or receipt.get("project") != "persona-cards":
        raise ValueError("Production preflight did not produce a ready receipt")
    if datetime.fromisoformat(receipt["expiresAtUtc"].replace("Z", "+00:00")) <= datetime.now(timezone.utc):
        raise ValueError("Production preflight receipt expired")
    evidence = json.loads(receipt["backupEvidence"])
    snapshot = Path(evidence["snapshot"])
    if not evidence.get("ok") or not str(snapshot).replace("\\", "/").startswith(BASE + "/snapshots/"):
        raise ValueError("Preflight did not verify a restorable application snapshot")
    return snapshot


def public_health(head: str) -> None:
    request=urllib.request.Request("https://personcard.runictools.com/api/health?revision=" + head, headers={"User-Agent":"Persona-Cards-Release-Check/5.2"})
    with urllib.request.urlopen(request, timeout=30) as response:
        if json.load(response) != {"status": "ok", "version": "5.2", "cards": 166}:
            raise ValueError("Public 5.2 health invariant failed")
    request=urllib.request.Request("https://personcard.runictools.com/", headers={"User-Agent":"Persona-Cards-Release-Check/5.2"})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200 or b'<div id="root"></div>' not in response.read():
            raise ValueError("Public frontend shell failed")


def receipt_is_current() -> bool:
    try:
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8-sig"))
        remaining = (datetime.fromisoformat(receipt["expiresAtUtc"].replace("Z", "+00:00")) - datetime.now(timezone.utc)).total_seconds()
        return receipt.get("status") == "ready" and receipt.get("project") == "persona-cards" and remaining > 120
    except (OSError, KeyError, ValueError):
        return False


def publish(expected: str) -> None:
    head = check_local(expected)
    snapshot = production_preflight()
    with tempfile.TemporaryDirectory(prefix="persona-publish-") as directory:
        archive = Path(directory) / "runtime-source.tgz"
        git("archive", "--format=tar.gz", "--output", str(archive), head, "--", *RUNTIME_PATHS)
        checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
        prepared = remote(PREPARE, head, checksum)
        upload_path = prepared.get("path", "")
        if prepared["upload"]:
            run(["scp", "-i", str(IDENTITY), "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                 str(archive), SSH_TARGET + ":" + upload_path])
        print("Runtime source transferred; building immutable image", flush=True)
        built = remote(BUILD, head, checksum, upload_path)
        print(json.dumps(built), flush=True)
        # Repeat the full gates only if the build consumed the receipt's window.
        check_local(head)
        if not receipt_is_current():
            snapshot = production_preflight()
        result = remote(ACTIVATE, head, str(snapshot).replace("\\", "/"))
        try:
            public_health(head)
        except Exception:
            remote(RECOVER, head, str(snapshot).replace("\\", "/"))
            raise RuntimeError("Public health failed; previous deployment recovered")
        print(json.dumps({**result, "public_health": "ok"}), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Requires tracked-clean source at origin/main, registered persona-cards guard/contract, "
        "real production Git checkout, SSH key, remote Docker/web network and a healthy current release. "
        "Never pushes, resets, prunes, removes volumes or bypasses the production preflight."))
    parser.add_argument("--expected-revision", help="Required full 40-character HEAD for publication")
    parser.add_argument("--check-local", action="store_true", help="Check tracked cleanliness and exact origin/main equality only")
    args = parser.parse_args()
    if not args.check_local and not args.expected_revision:
        parser.error("--expected-revision is required for publication")
    if args.expected_revision is not None and not re.fullmatch(r"[0-9a-f]{40}", args.expected_revision):
        parser.error("--expected-revision must be a full lowercase Git SHA")
    try:
        if args.check_local:
            print(json.dumps({"ok": True, "head": check_local(args.expected_revision), "tracked_clean": True}))
        else:
            publish(args.expected_revision)
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f"Publication stopped: {error}\n")


if __name__ == "__main__":
    main()
