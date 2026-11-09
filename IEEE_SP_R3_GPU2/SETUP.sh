#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-client}"
[[ "$MODE" == client || "$MODE" == serving ]] || { echo 'Usage: SETUP.sh client|serving'; exit 2; }
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
mkdir -p "$ROOT/.tools"
UV="$(command -v uv || true)"
if [[ -z "$UV" ]]; then
 UV="$ROOT/.tools/bin/uv"
 if [[ ! -x "$UV" ]]; then
  curl --fail --location --silent --show-error https://astral.sh/uv/install.sh -o "$ROOT/.tools/uv-install.sh"
  UV_UNMANAGED_INSTALL="$ROOT/.tools/bin" sh "$ROOT/.tools/uv-install.sh"
 fi
fi
export UV_PYTHON_INSTALL_DIR="$ROOT/.tools/python" UV_CACHE_DIR="$ROOT/.tools/cache"
if [[ "$MODE" == client ]]; then DEST="$ROOT/.venv"; VERSION=3.10.21
else DEST="$ROOT/.venv-serving"; VERSION=3.12; fi
MARKER="$DEST/.r3-owned-environment"
if [[ -x "$DEST/bin/python" ]]; then
 if "$DEST/bin/python" "$ROOT/ENVIRONMENT.py" "$MODE" --quiet; then echo "Compatible environment reused: $DEST"; exit 0; fi
 [[ -f "$MARKER" ]] || { echo "Preserving incompatible environment: $DEST; extract R3 to a fresh directory."; exit 2; }
else
 [[ ! -d "$DEST" || -f "$MARKER" ]] || { echo "Preserving unrecognized environment: $DEST"; exit 2; }
 "$UV" python install "$VERSION"
 "$UV" venv --managed-python --python "$VERSION" --seed "$DEST"
 printf '%s\n' 'IEEE_SP_R3_GPU2 owns this environment' > "$MARKER"
fi
if [[ "$MODE" == client ]]; then "$UV" pip sync --python "$DEST/bin/python" "$ROOT/release.lock.txt"
else "$UV" pip install --python "$DEST/bin/python" 'vllm==0.26.0' 'torch==2.11.0' 'ninja==1.13.2'; fi
"$DEST/bin/python" -m pip check
"$DEST/bin/python" "$ROOT/ENVIRONMENT.py" "$MODE"
"$DEST/bin/python" -m pip freeze > "$ROOT/.tools/$MODE.freeze.txt"
