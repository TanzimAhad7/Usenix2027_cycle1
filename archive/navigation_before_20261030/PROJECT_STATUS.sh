#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
if [[ -x .venv/bin/python ]]; then
  exec .venv/bin/python scripts/project_status.py "$@"
fi
# Standard-library read-only inspection; no research packages or inference.
exec python3 scripts/project_status.py "$@"
