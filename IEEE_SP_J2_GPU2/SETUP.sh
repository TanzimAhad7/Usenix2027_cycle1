#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
MODE="${1:-release}"
[[ "$MODE" == release || "$MODE" == serving ]] || { echo 'Usage: SETUP.sh release|serving'; exit 2; }
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
if [[ "$MODE" == release ]]; then ENV_DIR="$PACKAGE_DIR/.venv"; PYTHON_VERSION=3.10.21
else ENV_DIR="$PACKAGE_DIR/.venv-serving"; PYTHON_VERSION=3.12; fi
MARKER="$ENV_DIR/.j2-owned-environment"
if [[ -x "$ENV_DIR/bin/python" ]]; then
 if "$ENV_DIR/bin/python" "$PACKAGE_DIR/ENVIRONMENT.py" "$MODE" --quiet; then
  echo "Environment already compatible; reused without changes: $ENV_DIR"; exit 0
 fi
 [[ -f "$MARKER" ]] || { echo "Preserving incompatible existing environment: $ENV_DIR. Extract to a fresh directory."; exit 2; }
else
 [[ ! -d "$ENV_DIR" || -f "$MARKER" ]] || { echo "Preserving unrecognized environment directory: $ENV_DIR"; exit 2; }
 "$UV" python install "$PYTHON_VERSION"
 "$UV" venv --managed-python --python "$PYTHON_VERSION" --seed "$ENV_DIR"
 printf '%s\n' 'IEEE_SP_J2_GPU2 owns this isolated setup' > "$MARKER"
fi
if [[ "$MODE" == release ]]; then
 "$UV" pip sync --python "$ENV_DIR/bin/python" "$PACKAGE_DIR/lineage/release.lock.txt"
else
 "$UV" pip install --python "$ENV_DIR/bin/python" 'vllm==0.26.0' 'torch==2.11.0' 'ninja==1.13.2'
fi
"$ENV_DIR/bin/python" -m pip check
"$ENV_DIR/bin/python" "$PACKAGE_DIR/ENVIRONMENT.py" "$MODE"
"$ENV_DIR/bin/python" -m pip freeze > "$PACKAGE_DIR/.tools/$MODE.freeze.txt"
echo "Environment ready: $ENV_DIR"
