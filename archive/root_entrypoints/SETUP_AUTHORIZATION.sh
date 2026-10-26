#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [[ "${1:-}" != --foreground ]]; then
  mkdir -p logs
  RUN_ID="authorization_setup_$(date -u +%Y%m%dT%H%M%SZ)_$$"
  LOG="$ROOT/logs/$RUN_ID.log"
  nohup bash "$0" --foreground > "$LOG" 2>&1 < /dev/null &
  printf '%s\n' "$!" > "$LOG.pid"
  printf 'PID: %s\nLog: %s\n' "$!" "$LOG"
  exit 0
fi
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
mkdir -p "$ROOT/logs"
STATUS="$ROOT/logs/setup_$(date -u +%Y%m%dT%H%M%SZ)_$$.status"
trap 'rc=$?; printf "exit_code=%s\n" "$rc" > "$STATUS"' EXIT
PYTHON_BIN="${AUTHORIZATION_PYTHON:-python3.12}"
"$PYTHON_BIN" -c 'import sys; assert sys.version_info[:2]==(3,12), "Python 3.12 is required; set AUTHORIZATION_PYTHON to its absolute path"'
"$PYTHON_BIN" -m venv .venv
.venv/bin/python -m pip install -r requirements-authorization-research.lock.txt
.venv/bin/python -m pip check
"$PYTHON_BIN" -m venv .venv-serving
.venv-serving/bin/python -m pip install 'vllm==0.26.0' 'torch==2.11.0' 'ninja==1.13.2'
.venv-serving/bin/python -m pip check
.venv/bin/python -c 'from authorization_study.engine import verify_runtime; verify_runtime(); print("PINNED RESEARCH RUNTIME VERIFIED")'
echo 'SETUP COMPLETE: .venv and .venv-serving'
