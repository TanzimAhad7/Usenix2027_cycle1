#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:?Usage: bash LAUNCH.sh setup|components|historical|figures|protocols|models RUN_ID [2|3]}"
RUN_ID="${2:?Supply a new run ID}"
[[ "$RUN_ID" =~ ^[A-Za-z0-9_-]+$ ]] || { echo 'Invalid run ID' >&2; exit 2; }
case "$MODE" in
  setup|components|historical|figures|protocols) GPU="" ;;
  models) GPU="${3:?Select physical GPU 2 or 3}"; [[ "$GPU" == 2 || "$GPU" == 3 ]] || { echo 'Only GPU 2 or 3 is authorized' >&2; exit 2; } ;;
  *) echo 'Mode must be setup, components, historical, figures, protocols or models' >&2; exit 2 ;;
esac
mkdir -p "$ROOT/logs"
LOG="$ROOT/logs/$RUN_ID.log"
# noclobber protects previous logs, including concurrent attempts.
(set -o noclobber; : > "$LOG") 2>/dev/null || { echo 'Log already exists; choose a new run ID' >&2; exit 2; }
nohup bash "$ROOT/scripts/background_job.sh" "$MODE" "$RUN_ID" "$GPU" > "$LOG" 2>&1 < /dev/null &
JOB_PID=$!
printf '%s\n' "$JOB_PID" > "$ROOT/logs/$RUN_ID.pid"
printf 'Started PID %s\nLog: %s\nStatus: %s\n' "$JOB_PID" "$LOG" "$ROOT/logs/$RUN_ID.status"
