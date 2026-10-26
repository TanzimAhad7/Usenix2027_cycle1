#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
mkdir -p logs results/user_runs
if [[ "${1:-}" != "--worker" ]]; then
  run_id="reconciled_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
  log="$ROOT/logs/$run_id.log"
  nohup bash "$ROOT/RUN_RECONCILED_GPU3.sh" --worker "$run_id" "$@" > "$log" 2>&1 < /dev/null &
  worker_pid=$!
  echo "$worker_pid" > "$log.pid"
  echo "PID: $worker_pid"
  echo "Log: $log"
  echo "Status: $ROOT/logs/$run_id.status"
  echo "Results: $ROOT/results/user_runs/$run_id"
  echo "Progress: tail -f '$log'"
  exit 0
fi
shift
run_id="$1"
shift
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
trap 'rc=$?; if [[ ! -f "logs/$run_id.status" ]]; then printf "exit_code=%s\nstatus=BOOTSTRAP_FAILED\n" "$rc" > "logs/$run_id.status"; fi' EXIT
if [[ ! -x "$ROOT/.venv/bin/python" ]] || ! "$ROOT/.venv/bin/python" -c 'import agentdojo' >/dev/null 2>&1; then bash SETUP_RECONCILED.sh --research-only; fi
needs_serving=1
for arg in "$@"; do if [[ "$arg" == "--cpu-only" || "$arg" == "--mock" ]]; then needs_serving=0; fi; done
if [[ "$needs_serving" == "1" && ! -x "$ROOT/.venv-serving/bin/python" ]]; then bash SETUP_RECONCILED.sh --all; fi
"$ROOT/.venv/bin/python" -c 'import sys; assert sys.version_info >= (3,11); import agentdojo'
"$ROOT/.venv/bin/python" -c 'from reconciled_study.sequence import main; from reconciled_study.protocol import protocol; protocol()'
exec "$ROOT/.venv/bin/python" -u -m reconciled_study.sequence --root "$ROOT" --run-id "$run_id" "$@"
