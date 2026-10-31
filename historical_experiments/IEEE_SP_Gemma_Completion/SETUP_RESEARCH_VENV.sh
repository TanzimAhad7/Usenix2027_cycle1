#!/usr/bin/env bash
# Optional for a fresh directory only. Existing project venvs are never replaced.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ "${1:-}" != '--worker' ]]; then
  mkdir -p logs
  log="logs/setup_permission_$(date -u +%Y%m%dT%H%M%SZ)_$$.log"
  nohup bash "$PWD/SETUP_RESEARCH_VENV.sh" --worker > "$log" 2>&1 < /dev/null &
  echo "PID: $!"
  echo "Log: $log"
  exit 0
fi
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
if [[ -e .venv ]]; then
  echo 'An existing .venv is present. No replacement/install was attempted. Use the existing project environment.'
  exit 1
fi
python_bin="${PERMISSION_PYTHON:-python3.12}"
"$python_bin" -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11+ required; 3.12 tested"'
"$python_bin" -m venv .venv
.venv/bin/python -m pip install -r requirements-runtime.txt
.venv/bin/python -m pip check
echo 'Research .venv complete. GPU serving reuses the existing separately qualified .venv-serving.'

