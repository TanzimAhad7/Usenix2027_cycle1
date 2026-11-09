#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
mkdir -p "$ROOT/logs"
exec 9>"$ROOT/logs/.r3_gpu2.lock"
flock -n 9 || { echo 'An R3 controller/setup already owns the GPU2 lock. Existing work preserved.'; exit 2; }
WORKERS="${R3_WORKERS:-4}"
[[ "$WORKERS" == 1 || "$WORKERS" == 2 || "$WORKERS" == 4 ]] || { echo 'R3_WORKERS must be 1, 2 or 4'; exit 2; }
CACHE="${R3_MODEL_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}"
[[ -d "$CACHE/models--Qwen--Qwen3-32B" ]] || { echo "Missing Qwen3 cache: $CACHE/models--Qwen--Qwen3-32B. No models will be downloaded or substituted."; exit 2; }
bash "$ROOT/SETUP.sh" client
SERVING="${R3_SERVING_PYTHON:-}"
if [[ -n "$SERVING" ]]; then
 [[ -x "$SERVING" ]] && "$SERVING" "$ROOT/ENVIRONMENT.py" serving --quiet || { echo 'The explicitly selected serving interpreter is incompatible; it was not modified.'; exit 2; }
else
 for CANDIDATE in "$ROOT/.venv-serving/bin/python" "$ROOT/../IEEE_SP_J2_GPU2/.venv-serving/bin/python" "$ROOT/../IEEE_SP_A01_GPU2/.venv-serving/bin/python" "$ROOT/../IEEE_SP_E1_GPU3/.venv-serving/bin/python" "$ROOT/../.venv/bin/python"; do
  if [[ -x "$CANDIDATE" ]] && "$CANDIDATE" "$ROOT/ENVIRONMENT.py" serving --quiet; then SERVING="$CANDIDATE"; break; fi
 done
 if [[ -z "$SERVING" ]]; then bash "$ROOT/SETUP.sh" serving; SERVING="$ROOT/.venv-serving/bin/python"; fi
fi
RUN_ID="r3_gpu2_$(date -u +%Y%m%dT%H%M%SZ)_$$_$RANDOM"
LOG="$ROOT/logs/$RUN_ID.log"
nohup "$ROOT/.venv/bin/python" -u -m r3.controller --project-root "$ROOT" --run-id "$RUN_ID" --serving-python "$SERVING" --cache "$CACHE" --lock-fd 9 --workers "$WORKERS" > "$LOG" 2>&1 < /dev/null &
PID=$!
"$ROOT/.venv/bin/python" - "$ROOT" "$RUN_ID" "$PID" "$LOG" <<'PY'
import json,sys,time
from pathlib import Path
from r3.serving_base import proc_start
root,run,pid,log=sys.argv[1:];pid=int(pid)
(root_path:=Path(root)/'logs/latest.json').write_text(json.dumps(dict(run_id=run,pid=pid,start=proc_start(pid),log=log,results=str(Path(root)/'results/user_runs'/run)),indent=2)+'\n')
PY
exec 9>&-
printf 'R3 PID: %s\nLog: %s\nProgress: bash %s/SHOW_PROGRESS.sh\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$ROOT" "$ROOT" "$RUN_ID"
