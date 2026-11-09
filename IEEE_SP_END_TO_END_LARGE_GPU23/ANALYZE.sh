#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$#" -ne 1 ]]; then echo 'Usage: bash ANALYZE.sh /path/to/extracted-run'; exit 2; fi
RUN="$(cd -- "$1" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
cd "$ROOT"
python3 "$ROOT/analyze.py" "$RUN"
python3 -c 'import sys; from pathlib import Path; from bridge.report import analyze_bridge; analyze_bridge(Path(sys.argv[1]))' "$RUN"
