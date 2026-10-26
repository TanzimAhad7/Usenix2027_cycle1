#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
mkdir -p logs
if [[ "${1:-}" != "--worker" ]]; then
  run_id="github_clean_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
  log="$ROOT/logs/$run_id.log"
  nohup bash "$ROOT/PUSH_LIGHT_TO_GITHUB.sh" --worker "$run_id" "$@" > "$log" 2>&1 < /dev/null &
  pid=$!
  echo "$pid" > "$log.pid"
  echo "PID: $pid"
  echo "Log: $log"
  echo "Status: $ROOT/logs/$run_id.status"
  echo "Progress: tail -f '$log'"
  exit 0
fi
shift
run_id="$1"; shift
[[ "$run_id" =~ ^[A-Za-z0-9_-]+$ ]] || { echo 'Invalid run ID'; exit 1; }
trap 'rc=$?; printf "exit_code=%s\n" "$rc" > "logs/$run_id.status"' EXIT
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export REFERENCE_DISCOVERY_MODEL_FAMILY=qwen
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
research_python="${IEEE_SP_RESEARCH_PYTHON:-$ROOT/.venv/bin/python}"
if [[ -z "${IEEE_SP_RESEARCH_PYTHON:-}" && ! -x "$research_python" ]]; then
  research_python="/home/tahad/IEEE_SP/IEEE_SP_2027/.venv/bin/python"
fi
[[ -x "$research_python" ]] || { echo 'Set IEEE_SP_RESEARCH_PYTHON to your existing project .venv/bin/python. No environment installation attempted.'; exit 1; }
"$research_python" -u scripts/publish_clean.py "$@"
