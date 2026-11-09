#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${DIAG_PROJECT_ROOT:-}" ]]; then export STUDY_PROJECT_ROOT="$DIAG_PROJECT_ROOT"; fi
if [[ -n "${STUDY_PROJECT_ROOT:-}" ]]; then PROJECT_DIR="$STUDY_PROJECT_ROOT"
elif [[ -f "$PACKAGE_DIR/../logs/DIAGNOSTIC_GPU3_LATEST" ]]; then PROJECT_DIR="$(cd -- "$PACKAGE_DIR/.." && pwd)"
else PROJECT_DIR="$PACKAGE_DIR"; fi
RUN_ID="$(cat "$PROJECT_DIR/logs/DIAGNOSTIC_GPU3_LATEST")"
echo "Run: $RUN_ID"
if [[ -f "$PROJECT_DIR/results/user_runs/$RUN_ID/status.json" ]]; then cat "$PROJECT_DIR/results/user_runs/$RUN_ID/status.json"; fi
tail -n 30 -f "$PROJECT_DIR/logs/$RUN_ID.log"
