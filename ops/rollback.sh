#!/usr/bin/env bash
set -euo pipefail

# Explicit recovery of an integrity-verified snapshot; never removes containers or data.
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [ "$#" -eq 1 ]; then
  exec python3 "$script_dir/snapshot.py" --run-rollback "$1"
elif [ "$#" -eq 3 ] && [ "$2" = '--lock-fd' ]; then
  exec python3 "$script_dir/snapshot.py" --run-rollback "$1" --lock-fd "$3"
elif [ "$#" -eq 3 ] && [ "$1" = '--locked-fd' ]; then
  lock_fd="$2"
  snapshot="$3"
else
  printf '%s\n' 'Usage: rollback.sh /home/deploy/persona-cards/snapshots/<snapshot>' >&2
  exit 2
fi
# Even the internal entry must prove the inherited descriptor before touching state.
python3 - "$script_dir" "$lock_fd" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from snapshot import verify_release_lock
verify_release_lock(Path('/home/deploy/persona-cards'),int(sys.argv[2]))
PY
preparation="$(python3 "$script_dir/snapshot.py" --prepare-rollback "$snapshot")"
printf '%s\n' "$preparation"
receipt="$(printf '%s' "$preparation" | python3 -c 'import json,sys;print(json.load(sys.stdin)["receipt"])')"
docker image load --input "$snapshot/image.tar"
python3 "$script_dir/verify_snapshot.py" --snapshot "$snapshot" --phase loaded
docker compose -p personcard -f "$snapshot/docker-compose.prod.yml" --env-file "$snapshot/.env" up -d --no-build --wait personcard
python3 "$script_dir/verify_snapshot.py" --snapshot "$snapshot" --phase activated
python3 - "$snapshot" <<'PY'
import json, subprocess, sys, urllib.request
from pathlib import Path
expected = json.loads((Path(sys.argv[1]) / 'runtime-state.json').read_text())['health']
command = ['docker','exec','personcard-personcard-1','python','-c',
           "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=5).read().decode())"]
internal = json.loads(subprocess.check_output(command))
request=urllib.request.Request('https://personcard.runictools.com/api/health',headers={'User-Agent':'Persona-Cards-Release-Check/5.2'})
with urllib.request.urlopen(request, timeout=20) as response:
    public = json.load(response)
if internal != expected or public != expected:
    raise SystemExit('Rollback image restored, but internal/public application health differs from the snapshot')
print(json.dumps({'ok': True, 'action': 'rollback', 'health': public}))
PY
python3 "$script_dir/snapshot.py" --finish-rollback "$receipt"
