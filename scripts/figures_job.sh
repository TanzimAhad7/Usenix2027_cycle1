#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUN_ID="$1"
OUT="$ROOT/results/user_runs/$RUN_ID"
mkdir -p "$(dirname "$OUT")"
mkdir "$OUT"
export PATH="$ROOT/.venv/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
export MPLBACKEND=Agg
export CUDA_VISIBLE_DEVICES=""
export USENIX_GPU_LIST=2,3
export ARTIFACT_ROOT="$ROOT/research_basis"
export WORK_ROOT="$ROOT"
export RUN_ROOT="$OUT"
bash "$ARTIFACT_ROOT/scripts/reproduction/stages/12_figures.sh"
"$ROOT/.venv/bin/python" - "$OUT" <<'REPORT'
import json,sys
from pathlib import Path
out=Path(sys.argv[1])
rows=json.loads((out/'results/12_figures/FIGURE_REGENERATION_REPORT.json').read_text())
different=[r['figure'] for r in rows if r['rendered_150dpi_identical'] is False]
unknown=[r['figure'] for r in rows if r['rendered_150dpi_identical'] is None]
status={'status':'GENERATED_WITH_RENDER_DIFFERENCES' if different else 'GENERATED_RENDER_COMPARISON_INCOMPLETE' if unknown else 'GENERATED_RENDER_MATCH',
        'render_differences':different,'render_comparison_unavailable':unknown,'figure_1':'Frozen PDF copied; no supplied producer',
        'scope':'Original producers executed against frozen data. Original stage PASS means files produced, not all figures visually identical or new scientific results.'}
(out/'display_status.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status))
REPORT
