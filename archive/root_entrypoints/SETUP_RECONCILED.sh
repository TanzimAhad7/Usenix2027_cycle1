#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
mkdir -p .tools logs
if [[ ! -x .venv/bin/python ]]; then
  python_bin="$(command -v python3.12 || true)"
  if [[ -z "$python_bin" ]]; then
    if [[ ! -x .tools/bin/uv ]]; then
      curl -LsSf https://astral.sh/uv/install.sh -o .tools/uv-install.sh
      UV_UNMANAGED_INSTALL="$ROOT/.tools/bin" sh .tools/uv-install.sh
    fi
    export UV_PYTHON_INSTALL_DIR="$ROOT/.tools/python" UV_CACHE_DIR="$ROOT/.tools/cache"
    .tools/bin/uv python install 3.12
    .tools/bin/uv venv --managed-python --python 3.12 --seed .venv
  else
    "$python_bin" -m venv .venv
  fi
fi
.venv/bin/python -c 'import sys; assert sys.version_info >= (3,11), sys.version'
.venv/bin/python -m pip install -r requirements-reconciled.lock.txt
.venv/bin/python -m pip check
.venv/bin/python -c 'from reconciled_study.legacy_a.engine import verify_runtime; verify_runtime(); print("Pinned research runtime verified")'
if [[ "${1:-}" == "--all" ]]; then
  if [[ ! -x .venv-serving/bin/python ]]; then .venv/bin/python -m venv .venv-serving; fi
  .venv-serving/bin/python -m pip install 'vllm==0.26.0' ninja
  .venv-serving/bin/python -m pip check
fi
echo "Research setup complete. Existing serving venv remains required for the full GPU run."
