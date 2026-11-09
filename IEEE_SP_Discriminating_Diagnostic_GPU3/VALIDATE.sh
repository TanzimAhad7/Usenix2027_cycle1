#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${DIAG_PROJECT_ROOT:-${STUDY_PROJECT_ROOT:-$(cd -- "$PACKAGE_DIR/.." && pwd)}}"
export STUDY_PROJECT_ROOT="$PROJECT_DIR" CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
bash "$PACKAGE_DIR/SETUP.sh" research
cd "$PACKAGE_DIR"
"$PROJECT_DIR/.venv/bin/python" -m diagnostic.qualification --out "$PROJECT_DIR/results/diagnostic_validation_$(date -u +%Y%m%dT%H%M%SZ)_$$"
