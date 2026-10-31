#!/usr/bin/env bash
set -euo pipefail
BUNDLE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -x "$BUNDLE/.venv/bin/python" ]]; then PROJECT_ROOT="$BUNDLE"; else PROJECT_ROOT="$(dirname "$BUNDLE")"; fi
PROJECT_ROOT="${PERMISSION_PROJECT_ROOT:-$PROJECT_ROOT}"
if [[ ! -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
  echo "Missing $PROJECT_ROOT/.venv/bin/python. Unzip this folder inside your existing IEEE_SP_2027 directory."
  exit 1
fi
mkdir -p "$PROJECT_ROOT/logs" "$PROJECT_ROOT/results/user_runs"
run_id="gemma_completion_gpu2_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
log="$PROJECT_ROOT/logs/$run_id.log"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONPATH PYTHONHOME
cd "$BUNDLE"
nohup "$PROJECT_ROOT/.venv/bin/python" -u -m permission_admission.controller \
  --project-root "$PROJECT_ROOT" --run-id "$run_id" \
  --serving-python "$PROJECT_ROOT/.venv-serving/bin/python" "$@" \
  > "$log" 2>&1 < /dev/null &
pid=$!
echo "$pid" > "$log.pid"
printf 'PID: %s\nLog: %s\nStatus: %s\nResults: %s\n' \
  "$pid" "$log" "$PROJECT_ROOT/logs/$run_id.status" "$PROJECT_ROOT/results/user_runs/$run_id"
printf "Progress: tail -f '%s'\n" "$log"
echo 'Physical GPU 2 only. Gemma only. Qwen results are retained; no Qwen server is launched.'

