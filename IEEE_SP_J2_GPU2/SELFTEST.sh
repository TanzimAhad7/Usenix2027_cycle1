#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH DIAG_VARIANT DIAG_MODEL_REVISION E2B_RESUME_DISABLED J2_MOCK_RULE
cd "$PACKAGE_DIR"
python3 -m j2.audit_requests
RELEASE_PYTHON="${J2_RELEASE_PYTHON:-$PACKAGE_DIR/.venv/bin/python}"
if [[ ! -x "$RELEASE_PYTHON" ]]; then bash SETUP.sh release; RELEASE_PYTHON="$PACKAGE_DIR/.venv/bin/python"; fi
"$RELEASE_PYTHON" ENVIRONMENT.py release
"$RELEASE_PYTHON" -m unittest discover -s tests_j2 -v
echo 'CPU source/SDK boundary tests passed. Zero model inference.'
