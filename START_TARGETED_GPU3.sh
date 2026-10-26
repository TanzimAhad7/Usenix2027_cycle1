#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES=""
export PATH="$ROOT/.venv-serving/bin:$PATH"
[[ -x .venv/bin/python && -x .venv-serving/bin/python ]] || { echo 'Existing .venv or .venv-serving missing. No packages were changed.'; exit 2; }
if [[ $# -gt 0 ]]; then
  if [[ "$1" == '--exhaustion' && $# -eq 1 ]]; then :
  elif [[ "$1" == '--exhaustion-from' && $# -eq 2 ]]; then :
  else echo 'Usage: bash START_TARGETED_GPU3.sh [--exhaustion | --exhaustion-from COMPLETED_RUN_DIRECTORY]'; exit 2
  fi
fi
mkdir -p logs
RUN_ID="targeted_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$"
LOG="$ROOT/logs/$RUN_ID.log"
printf 'Targeted experiment bootstrap: physical GPU 3 only; existing venvs; logs and raw artifacts enabled.\n' > "$LOG"
nohup "$ROOT/.venv/bin/python" -u -m targeted_gpu3.sequence --root "$ROOT" --run-id "$RUN_ID" \
  --cache "${IEEE_SP_MODEL_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}" "$@" >> "$LOG" 2>&1 < /dev/null &
PID=$!
printf '%s\n' "$PID" > "$ROOT/logs/$RUN_ID.pid"
printf 'PID: %s\nLog: %s\nStatus: %s/logs/%s.status\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$ROOT" "$RUN_ID" "$ROOT" "$RUN_ID"
printf 'Progress: tail -f "%s"\n' "$LOG"
