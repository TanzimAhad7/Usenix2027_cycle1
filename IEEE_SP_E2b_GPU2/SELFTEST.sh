#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH DIAG_VARIANT DIAG_MODEL_REVISION E1_RESUME_PARENT E2B_RESUME_DISABLED
if [[ -n "${E2B_RESEARCH_PYTHON:-}" ]]; then PYTHON="$E2B_RESEARCH_PYTHON"
else bash "$P/SETUP.sh" research; PYTHON="$P/.venv/bin/python"; fi
cd "$P"
"$PYTHON" -m unittest discover -s tests -v
OUT="$P/validation/selftest_$(date -u +%Y%m%dT%H%M%SZ)_$$"
for FAMILY in qwen gemma; do
 "$PYTHON" -m e2b.qualification --family "$FAMILY" --out "$OUT/$FAMILY"
 "$PYTHON" -m e2b.prepare_rendering --family "$FAMILY" --out "$OUT/${FAMILY}_prepared"
done
echo "CPU checks passed: $OUT"
