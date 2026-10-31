#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${STUDY_PROJECT_ROOT:-}" ]]; then PROJECT_DIR="$STUDY_PROJECT_ROOT"
elif [[ -f "$PACKAGE_DIR/../logs/REFERENCE_STUDY_LATEST" ]]; then PROJECT_DIR="$(cd -- "$PACKAGE_DIR/.." && pwd)"
else PROJECT_DIR="$PACKAGE_DIR"; fi
RUN_ID="$(cat "$PROJECT_DIR/logs/REFERENCE_STUDY_LATEST")"
python3 - "$PROJECT_DIR/logs/$RUN_ID.log.pid.json" <<'PY'
import json,os,signal,sys
from pathlib import Path
p=Path(sys.argv[1]);r=json.loads(p.read_text());pid=r['pid']
try:
 s=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
 cmd=Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b' ').decode()
except FileNotFoundError:
 print('Recorded controller is no longer running.');raise SystemExit(0)
if s[19]!=r['start'] or 'reference_study.controller' not in cmd:
 raise SystemExit('Controller identity not established, or bootstrap is still in progress. No process was signaled.')
os.kill(pid,signal.SIGTERM);print('Stop requested. The owned controller will clean up and archive partial evidence. Follow its log.')
PY
