#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$P/../IEEE_SP_E1_GPU3}"
python3 "$P/APPLY_FIX.py" "$TARGET"
bash "$TARGET/RUN_E1.sh"
