#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
[[ $# == 0 || ( $# == 1 && "$1" == --mock ) ]] || { echo 'Usage: RUN_STUDY.sh [--mock]'; exit 2; }
python3 "$PACKAGE_DIR/PROCESS.py" check
cd "$PACKAGE_DIR"
python3 -c 'from reference_study.common import verify_package; verify_package(); print("Package verified; GPU 2 only.")'
mkdir -p "$PACKAGE_DIR/logs"
exec 8> "$PACKAGE_DIR/logs/bootstrap.lock"
flock -n 8 || { echo 'J2 is already running. Use SHOW_PROGRESS.sh.'; exit 2; }
RUN_ID="j2_gpu2_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
LOG="$PACKAGE_DIR/logs/$RUN_ID.log"
nohup bash "$PACKAGE_DIR/_inner.sh" "$RUN_ID" "$@" 8<&8 > "$LOG" 2>&1 < /dev/null &
PID=$!
python3 "$PACKAGE_DIR/PROCESS.py" record "$PID" "$PACKAGE_DIR/logs/$RUN_ID.pid.json"
printf '%s\n' "$RUN_ID" > "$PACKAGE_DIR/logs/LATEST_J2"
printf 'J2 PID: %s\nLog: %s\nProgress: bash %q\nResults: %s/results/user_runs/%s\n' "$PID" "$LOG" "$PACKAGE_DIR/SHOW_PROGRESS.sh" "$PACKAGE_DIR" "$RUN_ID"
