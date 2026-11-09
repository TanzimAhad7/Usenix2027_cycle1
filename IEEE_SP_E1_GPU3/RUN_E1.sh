#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$PACKAGE_DIR/logs"
# Reserve the package before publishing LATEST so a second click cannot replace it.
exec 8> "$PACKAGE_DIR/logs/bootstrap.lock"
if ! flock -n 8; then echo 'E1 is already starting or running. Use SHOW_PROGRESS.sh.'; exit 2; fi
RUN_ID="e1_gpu3_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
LOG="$PACKAGE_DIR/logs/$RUN_ID.log"
nohup bash "$PACKAGE_DIR/_inner.sh" "$RUN_ID" "$@" 8<&8 > "$LOG" 2>&1 < /dev/null &
PID=$!
python3 "$PACKAGE_DIR/PROCESS.py" record "$PID" "$PACKAGE_DIR/logs/$RUN_ID.pid.json"
printf '%s\n' "$RUN_ID" > "$PACKAGE_DIR/logs/LATEST_E1"
printf 'E1 PID: %s\nLog: %s\nProgress: bash %q\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$PACKAGE_DIR/SHOW_PROGRESS.sh" "$PACKAGE_DIR" "$RUN_ID"
