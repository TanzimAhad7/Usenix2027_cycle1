#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1
[[ -x .venv/bin/python && -x .venv-serving/bin/python ]] || { echo 'Existing research/serving venv missing'; exit 2; }
export PATH="$ROOT/.venv-serving/bin:$PATH"
mkdir -p logs
RUN_ID="expanded_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$"
LOG="$ROOT/logs/$RUN_ID.log"
nohup "$ROOT/.venv/bin/python" -u "$ROOT/expanded_gpu3/sequence.py" --root "$ROOT" --run-id "$RUN_ID" > "$LOG" 2>&1 < /dev/null &
PID=$!
printf '%s\n' "$PID" > "$ROOT/logs/$RUN_ID.pid"
printf 'PID: %s\nLog: %s\nStatus: %s/logs/%s.status\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$ROOT" "$RUN_ID" "$ROOT" "$RUN_ID"
echo "View progress: tail -f '$LOG'"
