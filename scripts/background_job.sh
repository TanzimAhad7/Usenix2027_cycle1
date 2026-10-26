#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="$1"; RUN_ID="$2"; GPU="${3:-}"
trap 'CODE=$?; printf "exit_code=%s\nfinished_utc=%s\n" "$CODE" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$ROOT/logs/$RUN_ID.status"' EXIT
cd "$ROOT"
printf 'mode=%s run=%s started_utc=%s\n' "$MODE" "$RUN_ID" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
case "$MODE" in
 setup) export CUDA_VISIBLE_DEVICES=""; bash "$ROOT/SETUP.sh" ;;
 components) export CUDA_VISIBLE_DEVICES=""; bash "$ROOT/scripts/project_components.sh" "$RUN_ID" ;;
 historical) bash "$ROOT/scripts/historical_job.sh" "$RUN_ID" ;;
 figures) bash "$ROOT/scripts/figures_job.sh" "$RUN_ID" ;;
 protocols) bash "$ROOT/scripts/protocols_job.sh" ;;
 models) bash "$ROOT/RUN_MODELS.sh" "$RUN_ID" "$GPU" ;;
 *) exit 2 ;;
esac
