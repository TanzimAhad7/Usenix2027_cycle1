#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
PY="${A01_RELEASE_PYTHON:-$P/.venv/bin/python}"
[[ -x "$PY" ]] || { echo 'Set A01_RELEASE_PYTHON to an isolated AgentDojo0.1.35/OpenAI2.x interpreter, or run SETUP.sh release.'; exit 2; }
cd "$P"
"$PY" -m unittest discover -s tests_a01 -v
