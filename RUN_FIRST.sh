#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$ROOT/.venv/bin/python"
if ! "$PYTHON_BIN" -c 'import sys; assert sys.version_info >= (3,11)' 2>/dev/null; then
  echo 'Run bash LAUNCH.sh setup setup_new first.' >&2
  exit 2
fi
"$PYTHON_BIN" "$ROOT/scripts/run_native.py" "${1:-local_$(date -u +%Y%m%dT%H%M%SZ)_$$}"
