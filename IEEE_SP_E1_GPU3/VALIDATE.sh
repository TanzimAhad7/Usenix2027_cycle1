#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PY="${E1_RESEARCH_PYTHON:-$P/.venv/bin/python}"
OUT="${1:-$P/validation/local_$(date -u +%Y%m%dT%H%M%SZ)}"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH DIAG_VARIANT DIAG_MODEL_REVISION
cd "$P"
for FAMILY in qwen gemma; do
 "$PY" -m e1.qualification --family "$FAMILY" --out "$OUT/$FAMILY/source_native"
 "$PY" -m e1.engineering_checks --family "$FAMILY" --out "$OUT/$FAMILY/edge_cases"
done
