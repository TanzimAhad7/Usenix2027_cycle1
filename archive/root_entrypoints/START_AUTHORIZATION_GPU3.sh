#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1 CUDA_VISIBLE_DEVICES=""
export PATH="$ROOT/.venv-serving/bin:$PATH"
[[ -x "$ROOT/.venv/bin/python" ]] || { echo 'Missing .venv/bin/python; see SETUP_AUTHORIZATION.sh'; exit 2; }
[[ -x "$ROOT/.venv-serving/bin/python" ]] || { echo 'Missing .venv-serving/bin/python; see SETUP_AUTHORIZATION.sh'; exit 2; }
mkdir -p logs
RUN_ID="authorization_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$_$RANDOM"
LOG="$ROOT/logs/$RUN_ID.log"
nohup "$ROOT/.venv/bin/python" -u -m authorization_study.sequence --root "$ROOT" --run-id "$RUN_ID" "$@" > "$LOG" 2>&1 < /dev/null &
PID=$!
printf '%s\n' "$PID" > "$ROOT/logs/$RUN_ID.pid"
printf 'PID: %s\nLog: %s\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$ROOT" "$RUN_ID"
printf "Progress: tail -f '%s'\n" "$LOG"
