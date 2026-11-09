#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${STUDY_PROJECT_ROOT:-}" ]]; then PROJECT_DIR="$STUDY_PROJECT_ROOT"
elif [[ -x "$PACKAGE_DIR/../.venv/bin/python" ]]; then PROJECT_DIR="$(cd -- "$PACKAGE_DIR/.." && pwd)"
else PROJECT_DIR="$PACKAGE_DIR"; fi
mkdir -p "$PROJECT_DIR/.tools"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
MODE="${1:-research}"
if [[ "$MODE" != 'research' && "$MODE" != 'serving' ]]; then echo 'Usage: bash SETUP.sh research|serving'; exit 2; fi
VENV_DIR="$PROJECT_DIR/.venv"
if [[ "$MODE" == 'serving' ]]; then VENV_DIR="$PROJECT_DIR/.venv-serving"; fi
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  PYTHON_BIN=''
  for CANDIDATE in "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/.venv-serving/bin/python" python3.12 python3.13 python3; do
    if command -v "$CANDIDATE" >/dev/null 2>&1 && "$CANDIDATE" -c 'import sys;assert sys.version_info>=(3,11)' >/dev/null 2>&1; then PYTHON_BIN="$CANDIDATE"; break; fi
  done
  if [[ -n "$PYTHON_BIN" ]]; then
    "$PYTHON_BIN" -m venv "$VENV_DIR"
  else
    UV="$PROJECT_DIR/.tools/bin/uv"
    if [[ ! -x "$UV" ]]; then
      curl -LsSf https://astral.sh/uv/install.sh -o "$PROJECT_DIR/.tools/uv-install.sh"
      UV_UNMANAGED_INSTALL="$PROJECT_DIR/.tools/bin" sh "$PROJECT_DIR/.tools/uv-install.sh"
    fi
    export UV_PYTHON_INSTALL_DIR="$PROJECT_DIR/.tools/python" UV_CACHE_DIR="$PROJECT_DIR/.tools/cache"
    "$UV" python install 3.12
    "$UV" venv --managed-python --python 3.12 --seed "$VENV_DIR"
  fi
fi
if [[ "$MODE" == 'research' ]]; then
  if ! "$VENV_DIR/bin/python" - <<'PY'
import sys,importlib.metadata as m
assert sys.prefix!=sys.base_prefix and sys.version_info>=(3,11)
for n,v in {'agentdojo':'0.1.35','openai':'3.35.1','pydantic':'2.14.1','httpx':'0.28.1','tenacity':'9.1.4'}.items():assert m.version(n)==v,(n,m.version(n),v)
import yaml
PY
  then
    "$VENV_DIR/bin/python" -m pip install -r "$PACKAGE_DIR/requirements-research.lock.txt"
  fi
  "$VENV_DIR/bin/python" -m pip check
else
  if ! "$VENV_DIR/bin/python" - <<'PY'
import sys,importlib.metadata as m
assert sys.prefix!=sys.base_prefix
assert m.version('vllm')=='0.26.0'
assert m.version('torch').startswith('2.11.0')
assert m.version('ninja')
PY
  then
    "$VENV_DIR/bin/python" -m pip install 'vllm==0.26.0' 'torch==2.11.0' 'ninja==1.13.2'
  fi
fi
echo "Environment ready: $VENV_DIR"
