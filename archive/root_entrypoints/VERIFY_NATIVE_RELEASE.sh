#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
./.venv/bin/python -c 'from pathlib import Path; from release_native_study.sequence import verify_package; verify_package(Path.cwd()); print("Package hashes verified")'
echo 'For logged CPU assurance only: bash RUN_NATIVE_RELEASE_GPU3.sh --cpu-only'
