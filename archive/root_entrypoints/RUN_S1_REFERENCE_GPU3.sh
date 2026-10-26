#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
mkdir -p logs results/user_runs
if [[ "${1:-}" != "--worker" ]]; then
  run_id="s1_reference_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
  log="$ROOT/logs/$run_id.log"
  nohup bash "$ROOT/RUN_S1_REFERENCE_GPU3.sh" --worker "$run_id" "$@" > "$log" 2>&1 < /dev/null &
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
if [[ ! "$run_id" =~ ^[A-Za-z0-9_-]+$ ]]; then echo "Invalid run ID"; exit 1; fi
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
trap 'rc=$?; if [[ ! -f "logs/$run_id.status" ]]; then printf "exit_code=%s\nstatus=BOOTSTRAP_FAILED\n" "$rc" > "logs/$run_id.status"; fi' EXIT
if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  echo "Missing existing $ROOT/.venv/bin/python. No install or environment replacement attempted."
  exit 1
fi
exec "$ROOT/.venv/bin/python" -u -m s1_reference_study.bootstrap --root "$ROOT" --run-id "$run_id" "$@"
