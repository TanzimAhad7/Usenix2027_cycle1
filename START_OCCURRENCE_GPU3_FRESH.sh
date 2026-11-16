#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1
export CUDA_VISIBLE_DEVICES=""
export PATH="$ROOT/.venv-serving/bin:$PATH"
[[ -x "$ROOT/.venv/bin/python" && -x "$ROOT/.venv-serving/bin/python" ]] || { echo 'Existing .venv and .venv-serving are required; nothing installed.'; exit 2; }
mkdir -p logs
RUN_ID="occurrence_fresh_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$"
LOG="$ROOT/logs/$RUN_ID.log"
nohup "$ROOT/.venv/bin/python" -u -m occurrence_study.sequence --root "$ROOT" --run-id "$RUN_ID" "$@" > "$LOG" 2>&1 < /dev/null &
PID=$!
printf '%s\n' "$PID" > "$ROOT/logs/$RUN_ID.pid"
printf 'PID: %s\nLog: %s\nStatus: %s/logs/%s.status\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$ROOT" "$RUN_ID" "$ROOT" "$RUN_ID"
printf "View progress: tail -f '%s'\n" "$LOG"
