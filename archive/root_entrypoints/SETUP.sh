#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
if [[ -z "${RB_BASE_PYTHON:-}" ]]; then
  if command -v python3.12 >/dev/null; then RB_BASE_PYTHON=python3.12; else RB_BASE_PYTHON=python3; fi
fi
"$RB_BASE_PYTHON" -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11+ required; 3.12 tested"'
"$RB_BASE_PYTHON" -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements-research.lock.txt"
cd "$ROOT/experiments/review_binding"
"$ROOT/.venv/bin/python" -c 'from diagnostic import verify_runtime; verify_runtime(); print("Pinned runtime source verified")'
