#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
[[ $# -eq 1 ]] || { echo 'Usage: bash ANALYZE_TARGETED_GPU3.sh results/user_runs/targeted_gpu3_<run>'; exit 2; }
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1 CUDA_VISIBLE_DEVICES=""
mkdir -p logs results/analysis
ID="targeted_audit_$(date -u +%Y%m%dT%H%M%SZ)_$$"
LOG="$ROOT/logs/$ID.log"
nohup "$ROOT/.venv/bin/python" -u -m targeted_gpu3.analyze --run "$1" --out "$ROOT/results/analysis/$ID" > "$LOG" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$ROOT/logs/$ID.pid"
printf 'PID: %s\nLog: %s\nAnalysis: %s/results/analysis/%s\n' "$!" "$LOG" "$ROOT" "$ID"
