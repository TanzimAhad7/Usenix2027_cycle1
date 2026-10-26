#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
[[ -x .venv/bin/python ]] || { echo 'Missing project .venv/bin/python'; exit 2; }
[[ -x .venv-serving/bin/python ]] || { echo 'Missing existing .venv-serving/bin/python'; exit 2; }
mkdir -p logs
RUN_ID="gpu3_sequence_$(date -u +%Y%m%dT%H%M%SZ)_$$"
LOG="$ROOT/logs/$RUN_ID.log"
nohup "$ROOT/.venv/bin/python" -u "$ROOT/automation_gpu3/sequence.py" --root "$ROOT" --run-id "$RUN_ID" > "$LOG" 2>&1 < /dev/null &
PID=$!
printf '%s\n' "$PID" > "$ROOT/logs/$RUN_ID.pid"
printf 'PID: %s\nLog: %s\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$ROOT" "$RUN_ID"
echo "View progress: tail -f '$LOG'"
