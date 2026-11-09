#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
python3 -m compileall -q analysis.py bridge design.py experiment.py model.py native.py prepare.py run.py score.py tests
python3 -m unittest discover -s tests -p 'test_*.py' -v
for script in RUN_STUDY.sh SHOW_PROGRESS.sh SWITCH_AND_RUN.sh; do
  bash -n "$script"
done
sha256sum --quiet -c SHA256SUMS
native_python="${E2E_NATIVE_PYTHON:-}"
if [[ -n "$native_python" ]]; then
  PYTHONPATH="$ROOT" "$native_python" tests/native_selfcheck.py
fi
echo "Package checks passed"
