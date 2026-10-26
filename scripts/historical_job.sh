#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
export CUDA_VISIBLE_DEVICES=""
"$ROOT/.venv/bin/python" "$ROOT/scripts/historical_audit.py" --out "$ROOT/results/user_runs/$1"
