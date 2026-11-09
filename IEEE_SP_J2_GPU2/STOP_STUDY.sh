#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -gt 0 ]]; then RUN_ID="$1"; else RUN_ID="$(cat "$PACKAGE_DIR/logs/LATEST_J2")"; fi
[[ "$RUN_ID" != */* && -n "$RUN_ID" ]] || { echo 'Invalid run ID'; exit 2; }
python3 "$PACKAGE_DIR/PROCESS.py" stop "$PACKAGE_DIR/logs/$RUN_ID.pid.json"
