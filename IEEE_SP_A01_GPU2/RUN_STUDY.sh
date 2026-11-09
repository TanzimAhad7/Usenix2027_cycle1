#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
STAGE="${1:-A1}"
[[ "$STAGE" == A0 || "$STAGE" == A1 ]] || { echo 'Usage: RUN_STUDY.sh A1|A0 [--mock]'; exit 2; }
if [[ $# -gt 0 ]]; then shift; fi
python3 "$PACKAGE_DIR/PROCESS.py" check
mkdir -p "$PACKAGE_DIR/logs"
exec 8> "$PACKAGE_DIR/logs/bootstrap.lock"
flock -n 8 || { echo 'A01 is already running. Use SHOW_PROGRESS.sh.'; exit 2; }
RUN_ID="a01_${STAGE}_gpu2_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
LOG="$PACKAGE_DIR/logs/$RUN_ID.log"
nohup bash "$PACKAGE_DIR/_inner.sh" "$RUN_ID" "$STAGE" "$@" 8<&8 > "$LOG" 2>&1 < /dev/null &
PID=$!
python3 "$PACKAGE_DIR/PROCESS.py" record "$PID" "$PACKAGE_DIR/logs/$RUN_ID.pid.json"
printf '%s\n' "$RUN_ID" > "$PACKAGE_DIR/logs/LATEST_A01"
printf 'A01 PID: %s\nLog: %s\nProgress: bash %q\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$PACKAGE_DIR/SHOW_PROGRESS.sh" "$PACKAGE_DIR" "$RUN_ID"
