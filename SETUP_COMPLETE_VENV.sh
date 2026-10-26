#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"

mkdir -p logs .tools
RUN_ID="venv_complete_$(date -u +%Y%m%dT%H%M%SZ)_$$"
STATUS="$ROOT/logs/$RUN_ID.status"
trap 'rc=$?; printf "exit_code=%s\n" "$rc" > "$STATUS"' EXIT

export CUDA_VISIBLE_DEVICES=""
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
export PYTHONNOUSERSITE=1
export UV_PYTHON_INSTALL_DIR="$ROOT/.tools/python"
export UV_CACHE_DIR="$ROOT/.tools/cache"

echo "Installing project-local Python tooling..."
curl -LsSf https://astral.sh/uv/install.sh \
  -o "$ROOT/.tools/uv-install.sh"
UV_UNMANAGED_INSTALL="$ROOT/.tools/bin" \
  sh "$ROOT/.tools/uv-install.sh"

UV="$ROOT/.tools/bin/uv"

echo "Installing isolated Python 3.12..."
"$UV" python install 3.12

if [[ -e "$ROOT/.venv" ]]; then
  mv "$ROOT/.venv" "$ROOT/.venv.backup.$RUN_ID"
fi

echo "Creating fresh .venv..."
"$UV" venv --managed-python --python 3.12 --seed "$ROOT/.venv"

echo "Installing every pinned project dependency..."
"$ROOT/.venv/bin/python" -m pip install \
  -r "$ROOT/requirements-research.lock.txt"

echo "Checking dependency consistency..."
"$ROOT/.venv/bin/python" -m pip check

echo "Verifying pinned research runtime..."
(
  cd "$ROOT/experiments/review_binding"
  "$ROOT/.venv/bin/python" -c \
    'from diagnostic import verify_runtime; verify_runtime(); print("Runtime verified")'
)

"$ROOT/.venv/bin/python" --version
"$ROOT/.venv/bin/python" -m pip freeze \
  > "$ROOT/logs/$RUN_ID.packages.txt"

echo "COMPLETE: $ROOT/.venv"
echo "Status: $STATUS"
