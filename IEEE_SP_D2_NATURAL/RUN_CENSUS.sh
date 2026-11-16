#!/usr/bin/env bash
# D2 step 1: freeze the eligibility census of the unmodified AgentDojo v1 user tasks (CPU, no model).
#   bash RUN_CENSUS.sh            -> census_frozen.json (refuses to overwrite) + census_frozen.json.sha256
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
[[ ! -e census_frozen.json ]] || { echo "census_frozen.json exists; the census is frozen. Move it aside to redo."; exit 2; }
NATIVE="${E2E_NATIVE_PYTHON:-}"
if [[ -z "$NATIVE" ]]; then
  for c in "$ROOT"/../IEEE_SP_R3*/.venv/bin/python "$ROOT"/../IEEE_SP_*/.venv/bin/python; do
    if [[ -x "$c" ]] && CUDA_VISIBLE_DEVICES="" "$c" -c 'from importlib.metadata import version; assert version("agentdojo")=="0.1.35"' >/dev/null 2>&1; then
      NATIVE="$c"; break
    fi
  done
fi
[[ -n "$NATIVE" ]] || { echo "Set E2E_NATIVE_PYTHON to an AgentDojo 0.1.35 interpreter"; exit 2; }
unset PYTHONPATH PYTHONHOME
CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$NATIVE" census.py --out census_frozen.json
sha256sum census_frozen.json census.py > census_frozen.json.sha256
echo "Frozen: $ROOT/census_frozen.json"
