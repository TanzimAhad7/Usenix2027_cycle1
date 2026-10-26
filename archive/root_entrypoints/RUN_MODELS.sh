#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$ROOT/.venv/bin/python"
RUN_ID="${1:?Supply run ID}"
GPU="${2:?Select physical GPU 2 or 3}"
[[ "$RUN_ID" =~ ^[A-Za-z0-9_-]+$ ]] || { echo 'Invalid run ID' >&2; exit 2; }
case "$GPU" in
 2) MODEL="${QWEN_MODEL_ID:?Set exact served Qwen ID}"; ATTESTATION="${QWEN_ATTESTATION:?Set absolute deployment attestation path}"; PORT=18080 ;;
 3) MODEL="${GEMMA_MODEL_ID:?Set exact served Gemma ID}"; ATTESTATION="${GEMMA_ATTESTATION:?Set absolute deployment attestation path}"; PORT=18081 ;;
 *) echo 'Only physical GPU 2 or 3 is authorized' >&2; exit 2 ;;
esac
[[ -x "$PYTHON_BIN" ]] || { echo 'Run the setup launcher first' >&2; exit 2; }
[[ "$ATTESTATION" == /* && -f "$ATTESTATION" ]] || { echo 'Attestation must be an existing absolute path' >&2; exit 2; }
OUT="$ROOT/results/user_runs/$RUN_ID"
mkdir -p "$(dirname "$OUT")"
mkdir "$OUT"
# Server ownership is observed independently of client CUDA visibility.
"$PYTHON_BIN" "$ROOT/scripts/qualify_gpu.py" --gpu "$GPU" --port "$PORT" > "$OUT/gpu_preflight.json"
"$PYTHON_BIN" - "$ATTESTATION" "$GPU" <<'CHECK'
import json,sys
x=json.load(open(sys.argv[1]))
if str(x.get('gpu_index')) != sys.argv[2]:raise SystemExit('Attestation GPU index differs from selected physical GPU')
CHECK
export CUDA_VISIBLE_DEVICES=""
cd "$ROOT/experiments/review_binding"
"$PYTHON_BIN" autonomous.py --base-url "http://127.0.0.1:$PORT/v1" --model "$MODEL" --attestation "$ATTESTATION" --repeats 1 --out "$OUT/model" > "$OUT/model.log" 2>&1
