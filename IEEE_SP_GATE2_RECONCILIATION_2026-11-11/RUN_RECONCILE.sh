#!/usr/bin/env bash
# Reproduce the Gate 2 post-run reconciliation (CPU only, read-only on runs/; ~6 min).
# Outputs: reconciliation.json, {qwen,gemma}/{analysis_v2.2.json,report_v2.2.txt,episodes_v2.2.csv,B_dossiers.json}
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PKG="$HERE/../IEEE_SP_GATE2_VALUE_SELECTION"
PY="${PY:-$HERE/../IEEE_SP_R3_GPU2/.venv/bin/python}"   # Python >= 3.10 (zip strict / removeprefix)
RUN_Q="$PKG/runs/20261111T185944Z_gate2_all_both_qwen"
RUN_G="$PKG/runs/20261111T185944Z_gate2_all_both_gemma"
before="$(sha256sum "$RUN_Q/analysis.json" "$RUN_G/analysis.json")"
"$PY" -I "$HERE/make_v22.py" "$PKG/analyze.py" "$HERE/analyze_v22.py"
"$PY" -I "$HERE/reconcile.py" "$PKG" "$RUN_Q" "$RUN_G" "$HERE" | tee "$HERE/reconcile_stdout.txt"
after="$(sha256sum "$RUN_Q/analysis.json" "$RUN_G/analysis.json")"
[ "$before" = "$after" ] && echo "run artifacts unchanged" || { echo "RUN ARTIFACTS CHANGED"; exit 1; }
(cd "$HERE" && find . -type f ! -name SHA256SUMS ! -path './__pycache__/*' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
echo "done: $HERE/reconciliation.json"
