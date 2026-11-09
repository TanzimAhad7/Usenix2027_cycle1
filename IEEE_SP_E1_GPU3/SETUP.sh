#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
MODE="${1:-research}"
[[ "$MODE" == research || "$MODE" == serving ]] || { echo 'Usage: SETUP.sh research|serving'; exit 2; }
mkdir -p "$PACKAGE_DIR/.tools"
UV="$(command -v uv || true)"
if [[ -z "$UV" ]]; then
 UV="$PACKAGE_DIR/.tools/bin/uv"
 if [[ ! -x "$UV" ]]; then
  curl --fail --location --silent --show-error https://astral.sh/uv/install.sh -o "$PACKAGE_DIR/.tools/uv-install.sh"
  UV_UNMANAGED_INSTALL="$PACKAGE_DIR/.tools/bin" sh "$PACKAGE_DIR/.tools/uv-install.sh"
 fi
fi
export UV_PYTHON_INSTALL_DIR="$PACKAGE_DIR/.tools/python" UV_CACHE_DIR="$PACKAGE_DIR/.tools/cache"
if [[ "$MODE" == research ]]; then ENV_DIR="$PACKAGE_DIR/.venv"; PYTHON_VERSION=3.10
else ENV_DIR="$PACKAGE_DIR/.venv-serving"; PYTHON_VERSION=3.12; fi
if [[ ! -x "$ENV_DIR/bin/python" ]]; then
 "$UV" python install "$PYTHON_VERSION"
 "$UV" venv --managed-python --python "$PYTHON_VERSION" --seed "$ENV_DIR"
fi
"$ENV_DIR/bin/python" - "$PYTHON_VERSION" <<'PY'
import sys
assert sys.prefix != sys.base_prefix
assert sys.version_info[:2] == tuple(map(int,sys.argv[1].split('.'))), 'Existing package environment has a different Python; preserve it and use a separate package directory.'
PY
if [[ "$MODE" == research ]]; then
 "$UV" pip sync --python "$ENV_DIR/bin/python" "$PACKAGE_DIR/requirements-research.lock.txt"
else
 "$UV" pip install --python "$ENV_DIR/bin/python" 'vllm==0.26.0' 'torch==2.11.0' 'ninja==1.13.2'
fi
"$ENV_DIR/bin/python" -m pip check
"$ENV_DIR/bin/python" -m pip freeze > "$PACKAGE_DIR/.tools/$MODE.freeze.txt"
echo "Environment ready: $ENV_DIR"
