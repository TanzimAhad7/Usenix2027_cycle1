#!/usr/bin/env bash
# S0 V2 launcher (PROTOCOL.md). Physical GPU 3 by default, GPU 2 only via --gpu 2 (both UUID-pinned);
# unattended runs via setsid + nohup.
#   bash RUN_S0.sh verify [--online]                         CPU checks (+ free OpenRouter listing with --online)
#   bash RUN_S0.sh freeze                                    CPU, once: freeze inputs (refuses to overwrite)
#   bash RUN_S0.sh open [both|qwen|gemma] [--gpu 2|3]        GPU (default 3; 2 only if chosen): continuity gate +
#                                                            R0,Q0,Q1 (qwen), G0,G1 (gemma)
#   bash RUN_S0.sh gemini --budget-usd X --max-calls N       PAID API (F0,F1): needs approvals/gemini_approval.json
#   bash RUN_S0.sh follow | status | stop                    the latest background pipeline
#   bash RUN_S0.sh score RUN [RUN...]                        CPU: automatic scores + blinded adjudication export
#   bash RUN_S0.sh analyze RUN [RUN...] [--adjudication F]   CPU: decision bands
#   bash RUN_S0.sh bundle RUN [RUN...]                       ZIP for evaluation
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
declare -A GPU_UUIDS=([2]="GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932" [3]="GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6")
CPU_PY="$ROOT/../.venv/bin/python"                                  # project .venv (AgentDojo 0.1.35)
STACK_PY="$ROOT/../IEEE_SP_END_TO_END_LARGE_GPU23/.venv/bin/python"   # the Gate 2 qualified model stack
mkdir -p logs runs analysis

export_env() {
  unset PYTHONPATH PYTHONHOME
  export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
         TOKENIZERS_PARALLELISM=false CUDA_VISIBLE_DEVICES=""
}
check_stack() {
  CUDA_VISIBLE_DEVICES="" "$STACK_PY" -c '
import sys, torch, transformers
assert sys.version_info[:2] == (3, 12) and torch.__version__.split("+")[0] == "2.11.0"
assert transformers.__version__ == "5.20.2"' || { echo "Model stack check failed: $STACK_PY"; exit 2; }
  "$CPU_PY" -c 'from importlib.metadata import version; assert version("agentdojo") == "0.1.35"' \
    || { echo "Project .venv lacks AgentDojo 0.1.35: $CPU_PY"; exit 2; }
}
gpu_idle() {  # $1 = physical index
  local apps; apps="$(nvidia-smi -i "$1" --query-compute-apps=pid,used_memory --format=csv,noheader)"
  [[ "$(nvidia-smi -i "$1" --query-gpu=uuid --format=csv,noheader)" == "${GPU_UUIDS[$1]}" ]] || { echo "GPU $1 UUID changed"; exit 2; }
  if [[ -n "$apps" ]]; then echo "GPU $1 is busy (not touching it): $apps"; exit 2; fi
}
latest() { [[ -f logs/latest ]] || { echo "No pipeline started yet"; exit 2; }; cat logs/latest; }
stamp() { date -u +%Y%m%dT%H%M%SZ; }

cmd="${1:-help}"; shift || true
case "$cmd" in
  verify)
    export_env; check_stack
    "$STACK_PY" run_s0.py verify "$@" ;;
  freeze)
    export_env; check_stack
    [[ -f prompts/D1_published_block.txt ]] || { echo "prompts/D1_published_block.txt missing"; exit 2; }
    "$CPU_PY" run_s0.py freeze ;;
  open)
    export_env; check_stack
    PSEL="${1:-both}"; shift || true
    GPU=3; if [[ "${1:-}" == "--gpu" ]]; then GPU="${2:-}"; fi
    [[ -n "${GPU_UUIDS[$GPU]:-}" ]] || { echo "--gpu must be 2 or 3"; exit 2; }
    GPU_UUID="${GPU_UUIDS[$GPU]}"; gpu_idle "$GPU"
    [[ -f inputs/FREEZE.json ]] || { echo "Run: bash RUN_S0.sh freeze"; exit 2; }
    [[ -f prompts/D1_confirmation.json ]] || { echo "Published block not confirmed (PROTOCOL.md 3)"; exit 2; }
    case "$PSEL" in both) P="qwen gemma";; qwen) P="qwen";; gemma) P="gemma";; *) echo "both|qwen|gemma"; exit 2;; esac
    ID="S0_$(stamp)_open"; RUN="$ROOT/runs/$ID"; LOG="$ROOT/logs/$ID.log"; mkdir -p "$RUN"
    echo "$ID" > logs/latest
    setsid nohup bash -c "
      set -uo pipefail
      for prof in $P; do
        echo \"[\$(date -u +%FT%TZ)] START \$prof on physical GPU $GPU ($GPU_UUID)\"
        CUDA_VISIBLE_DEVICES='$GPU_UUID' '$STACK_PY' -u '$ROOT/run_s0.py' open --run '$RUN' --profile \$prof --gpu $GPU \
          || { echo \"[\$(date -u +%FT%TZ)] FAILED \$prof\"; exit 1; }
      done
      '$STACK_PY' -u '$ROOT/run_s0.py' score --runs '$RUN' --out '$RUN/analysis'
      '$STACK_PY' -u '$ROOT/run_s0.py' analyze --runs '$RUN' --out '$RUN/analysis'
      cd '$ROOT' && zip -qr 'runs/$ID.zip' 'runs/$ID' inputs prompts *.py PROTOCOL.md RUN_S0.sh tests
      echo \"[\$(date -u +%FT%TZ)] PIPELINE END \$(sha256sum runs/$ID.zip)\"
    " > "$LOG" 2>&1 < /dev/null &
    echo $! > "logs/$ID.pid"
    echo "Started $ID (pid $(cat logs/$ID.pid)); follow: bash RUN_S0.sh follow" ;;
  gemini)
    export_env; check_stack
    [[ -f inputs/FREEZE.json ]] || { echo "Run: bash RUN_S0.sh freeze"; exit 2; }
    [[ -f approvals/gemini_approval.json ]] || { echo "approvals/gemini_approval.json missing (PROTOCOL.md 9)"; exit 2; }
    [[ -n "${OPENROUTER_API_KEY:-}" ]] || { echo "export OPENROUTER_API_KEY first"; exit 2; }
    ID="S0_$(stamp)_gemini"; RUN="$ROOT/runs/$ID"; LOG="$ROOT/logs/$ID.log"; mkdir -p "$RUN"
    echo "$ID" > logs/latest
    setsid nohup bash -c "
      set -uo pipefail
      '$STACK_PY' -u '$ROOT/run_s0.py' gemini --run '$RUN' --allow-paid-api $* || echo \"[\$(date -u +%FT%TZ)] STOPPED\"
      '$STACK_PY' -u '$ROOT/run_s0.py' score --runs '$RUN' --out '$RUN/analysis'
      cd '$ROOT' && zip -qr 'runs/$ID.zip' 'runs/$ID' inputs prompts *.py PROTOCOL.md RUN_S0.sh
      echo \"[\$(date -u +%FT%TZ)] PIPELINE END \$(sha256sum runs/$ID.zip)\"
    " > "$LOG" 2>&1 < /dev/null &
    echo $! > "logs/$ID.pid"
    echo "Started $ID (pid $(cat logs/$ID.pid)); follow: bash RUN_S0.sh follow" ;;
  follow) tail -n 50 -f "logs/$(latest).log" ;;
  status) ID="$(latest)"; cat "runs/$ID/status.json" 2>/dev/null || true; echo; tail -n 5 "logs/$ID.log" ;;
  stop)
    ID="$(latest)"; PID="$(cat "logs/$ID.pid")"
    kill -TERM -- "-$(ps -o pgid= -p "$PID" | tr -d ' ')" && echo "Stopped $ID (process group of $PID)" ;;
  score)   export_env; "$STACK_PY" run_s0.py score --runs "$@" ;;
  analyze) export_env; "$STACK_PY" run_s0.py analyze --runs "$@" ;;
  bundle)  for r in "$@"; do zip -qr "runs/$(basename "$r").zip" "$r" inputs prompts *.py PROTOCOL.md RUN_S0.sh; done ;;
  *) sed -n '2,11p' "$0" ;;
esac
