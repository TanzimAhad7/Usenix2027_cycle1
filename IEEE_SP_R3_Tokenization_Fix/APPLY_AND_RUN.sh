#!/usr/bin/env bash
set -euo pipefail
FIX_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:-$FIX_DIR/../IEEE_SP_R3_GPU2}"
PYTHON="$PROJECT/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON=python3
"$PYTHON" "$FIX_DIR/APPLY_FIX.py" --project-root "$PROJECT"
bash "$PROJECT/RUN_STUDY.sh"
