#!/usr/bin/env bash
# Launch N2 unattended (setsid + nohup). Usage:
#   bash RUN_N2.sh                 full run: Qwen3-32B then Gemma-3-27B on physical GPU 3
#   bash RUN_N2.sh --mock          CPU engineering check (reference-solution replay, no model)
#   bash RUN_N2.sh --limit 40      first 40 episodes per profile (smoke run on the GPU)
set -euo pipefail
PKG="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$PKG/logs" "$PKG/runs"
RUN_ID="n2_$(date -u +%Y%m%dT%H%M%SZ)"
for a in "$@"; do [[ "$a" == --mock ]] && RUN_ID="${RUN_ID}_mock"; [[ "$a" == --limit ]] && RUN_ID="${RUN_ID}_smoke"; done
LOG="$PKG/logs/$RUN_ID.log"
setsid nohup bash "$PKG/_inner.sh" "$RUN_ID" "$@" > "$LOG" 2>&1 < /dev/null &
echo "$!" > "$PKG/logs/$RUN_ID.pid"
echo "$RUN_ID" > "$PKG/logs/LATEST"
echo "N2 started: $RUN_ID (pid $(cat "$PKG/logs/$RUN_ID.pid"))"
echo "Log:      $LOG"
echo "Progress: bash $PKG/SHOW_PROGRESS.sh"
echo "Results:  $PKG/runs/$RUN_ID   (bundle in $PKG/bundles/ when finished)"
