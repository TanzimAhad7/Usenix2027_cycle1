#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
if [[ -x .venv/bin/python ]]; then
  exec .venv/bin/python scripts/verify_repository_current.py "$@"
fi
# This verifier imports only the standard-library protocol/package functions.
exec python3 scripts/verify_repository_current.py "$@"
