#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${STUDY_PROJECT_ROOT:-}" ]]; then PROJECT_DIR="$STUDY_PROJECT_ROOT"
elif [[ -f "$PACKAGE_DIR/../logs/REFERENCE_STUDY_LATEST" ]]; then PROJECT_DIR="$(cd -- "$PACKAGE_DIR/.." && pwd)"
else PROJECT_DIR="$PACKAGE_DIR"; fi
RUN_ID="$(cat "$PROJECT_DIR/logs/REFERENCE_STUDY_LATEST")"
echo "Run: $RUN_ID"
if [[ -f "$PROJECT_DIR/results/user_runs/$RUN_ID/status.json" ]]; then cat "$PROJECT_DIR/results/user_runs/$RUN_ID/status.json"; fi
tail -n 30 -f "$PROJECT_DIR/logs/$RUN_ID.log"
