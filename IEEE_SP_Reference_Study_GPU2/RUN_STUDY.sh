#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${STUDY_PROJECT_ROOT:-}" ]]; then
  PROJECT_DIR="$(cd -- "$STUDY_PROJECT_ROOT" && pwd)"
elif [[ -x "$PACKAGE_DIR/../.venv/bin/python" || -x "$PACKAGE_DIR/../.venv-serving/bin/python" ]]; then
  PROJECT_DIR="$(cd -- "$PACKAGE_DIR/.." && pwd)"
else
  PROJECT_DIR="$PACKAGE_DIR"
fi
mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/results/user_runs"
RUN_ID="reference_study_gpu2_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
LOG="$PROJECT_DIR/logs/$RUN_ID.log"
nohup bash "$PACKAGE_DIR/_inner.sh" "$PROJECT_DIR" "$RUN_ID" "$@" > "$LOG" 2>&1 < /dev/null &
RUN_PID=$!
printf '%s\n' "$RUN_PID" > "$LOG.pid"
python3 - "$RUN_PID" "$LOG.pid.json" <<'PY'
import json,sys
from pathlib import Path
pid=int(sys.argv[1])
try:start=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()[19]
except FileNotFoundError:start=None
Path(sys.argv[2]).write_text(json.dumps(dict(pid=pid,start=start))+'\n')
PY
printf '%s\n' "$RUN_ID" > "$PROJECT_DIR/logs/REFERENCE_STUDY_LATEST"
printf 'PID: %s\nLog: %s\nResults: %s/results/user_runs/%s\n' "$RUN_PID" "$LOG" "$PROJECT_DIR" "$RUN_ID"
printf 'Progress: tail -f %q\n' "$LOG"
