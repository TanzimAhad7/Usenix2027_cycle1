#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
PROJECT="${IEEE_SP_PROJECT_ROOT:-$(dirname "$ROOT")}"
if [[ "${1:-}" != "--worker" ]]; then
  for env_name in .venv .venv-serving; do
    [[ -x "$PROJECT/$env_name/bin/python" ]] || { echo "Missing $PROJECT/$env_name/bin/python. Put this folder inside IEEE_SP_2027 or set IEEE_SP_PROJECT_ROOT."; exit 1; }
  done
  mkdir -p "$PROJECT/logs" "$PROJECT/results/user_runs"
  for name in .venv .venv-serving logs results; do
    if [[ -e "$ROOT/$name" || -L "$ROOT/$name" ]]; then
      [[ "$(readlink -f "$ROOT/$name")" == "$(readlink -f "$PROJECT/$name")" ]] || { echo "Unexpected path: $ROOT/$name"; exit 1; }
    else
      ln -s "$PROJECT/$name" "$ROOT/$name"
    fi
  done
  run_id="gemma_recovery_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
  log="$ROOT/logs/$run_id.log"
  nohup bash "$ROOT/RUN_GEMMA_RECOVERY.sh" --worker "$run_id" "$@" > "$log" 2>&1 < /dev/null &
  worker_pid=$!
  echo "$worker_pid" > "$log.pid"
  echo "PID: $worker_pid"
  echo "Log: $PROJECT/logs/$run_id.log"
  echo "Status: $PROJECT/logs/$run_id.status"
  echo "Results: $PROJECT/results/user_runs/$run_id"
  echo "Progress: tail -f '$PROJECT/logs/$run_id.log'"
  exit 0
fi
shift
run_id="$1"
shift
[[ "$run_id" =~ ^[A-Za-z0-9_-]+$ ]] || { echo "Invalid run ID"; exit 1; }
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
export REFERENCE_DISCOVERY_MODEL_FAMILY=gemma
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
trap 'rc=$?; if [[ ! -f "logs/$run_id.status" ]]; then printf "exit_code=%s\nstatus=BOOTSTRAP_FAILED\n" "$rc" > "logs/$run_id.status"; fi' EXIT
"$ROOT/.venv/bin/python" -u -m unittest discover -s recovery_tests -v
exec "$ROOT/.venv/bin/python" -u -m reference_discovery_parallel.bootstrap --root "$ROOT" --run-id "$run_id" "$@"
