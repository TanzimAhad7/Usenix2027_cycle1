#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
STATUS="${1:?Status path required}"
trap 'rc=$?; printf "exit_code=%s\n" "$rc" > "$STATUS"' EXIT

unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
export PYTHONNOUSERSITE=1
export CUDA_VISIBLE_DEVICES=""
export UV_PYTHON_INSTALL_DIR="$ROOT/.tools/python"
export UV_CACHE_DIR="$ROOT/.tools/cache"

"$ROOT/.tools/bin/uv" venv \
  --managed-python --python 3.12 --seed .venv-serving

.venv-serving/bin/python -m pip install "vllm==0.26.0"
.venv-serving/bin/python -m pip check
.venv-serving/bin/python -c \
  'import torch, vllm; print("torch:", torch.__version__); print("vLLM:", vllm.__version__)'

.venv-serving/bin/python -m pip freeze \
  > "${STATUS%.status}.packages.txt"

echo "SERVING ENVIRONMENT COMPLETE"
