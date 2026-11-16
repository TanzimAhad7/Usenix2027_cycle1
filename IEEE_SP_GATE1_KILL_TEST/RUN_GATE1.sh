#!/usr/bin/env bash
# Gate 1 kill test (protocol GATE1_KILL_TEST_V2). See PROTOCOL.md. Physical GPU 3 only.
#
#   bash RUN_GATE1.sh test             # CPU: unit tests, native worlds, both chat templates, checksums (~6 min)
#   bash RUN_GATE1.sh all              # GPU 3, unattended: smoke Qwen+Gemma -> smoke gate -> full Qwen+Gemma
#                                      #   -> two-profile verdict -> evaluation ZIP (code + all runs + log)
#   bash RUN_GATE1.sh smoke            # GPU 3, unattended: smoke Qwen+Gemma only (+ ZIP)
#   bash RUN_GATE1.sh run              # GPU 3, unattended: full Qwen+Gemma only (+ verdict + ZIP)
#   bash RUN_GATE1.sh run gemma        # GPU 3, unattended: full run of one profile (qwen|gemma|both; also for all/smoke)
#   bash RUN_GATE1.sh audit [RUN_DIR...]  # CPU: reanalysis/deep_audit.py on each full run of the latest pipeline
#                                      #   (or on the given run directories) -> reanalysis/out_<run name>/
#   bash RUN_GATE1.sh follow           # follow the latest pipeline log live (Ctrl-C stops following, not the run)
#   bash RUN_GATE1.sh status           # pipeline status, current run progress, last log lines
#   bash RUN_GATE1.sh stop             # stop the latest pipeline (it archives what exists and writes the ZIP)
#
# Pipelines start with `setsid nohup`: they have their own session, ignore hangups, and keep running after
# the terminal, VS Code, SSH or your laptop closes. Profiles run one after the other on GPU 3. If GPU 3 is
# busy, a run waits (up to 12 h) instead of failing; it never stops another process.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
mkdir -p logs runs bundles
CACHE="${E0_MODEL_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}"

qualify_stack() {
  [[ -x "$1" ]] && env -u PYTHONPATH -u PYTHONHOME "$1" -c '
import sys, torch, transformers
assert sys.version_info[:2] == (3,12)
assert torch.__version__.split("+")[0] == "2.11.0" and torch.version.cuda is not None
assert transformers.__version__ == "5.20.2"
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration
import accelerate
' >/dev/null 2>&1
}
stack_python() {
  if [[ -n "${E0_STACK_PYTHON:-}" ]]; then qualify_stack "$E0_STACK_PYTHON" && { printf '%s\n' "$E0_STACK_PYTHON"; return; }
    echo "E0_STACK_PYTHON failed the stack check" >&2; exit 2; fi
  for c in "$ROOT"/../IEEE_SP_END_TO_END_LARGE_GPU23/.venv/bin/python "$ROOT"/../IEEE_SP_*/.venv-serving/bin/python \
           "$ROOT"/../IEEE_SP_*/.venv/bin/python; do
    if qualify_stack "$c"; then printf '%s\n' "$c"; return; fi
  done
  echo "Set E0_STACK_PYTHON to the Python 3.12 / Torch 2.11.0 / Transformers 5.20.2 / Accelerate stack" >&2; exit 2
}
native_python() {
  if [[ -n "${E2E_NATIVE_PYTHON:-}" ]]; then printf '%s\n' "$E2E_NATIVE_PYTHON"; return; fi
  for c in "$ROOT"/../IEEE_SP_R3*/.venv/bin/python "$ROOT"/../IEEE_SP_*/.venv/bin/python; do
    if [[ -x "$c" ]] && CUDA_VISIBLE_DEVICES="" "$c" -c '
from importlib.metadata import version
from agentdojo.task_suite.load_suites import get_suite
assert version("agentdojo") == "0.1.35"
for s in ("banking", "workspace", "slack"): get_suite("v1", s)' >/dev/null 2>&1; then
      printf '%s\n' "$(cd -- "$(dirname -- "$c")" && pwd)/$(basename -- "$c")"; return
    fi
  done
  echo "Set E2E_NATIVE_PYTHON to an AgentDojo 0.1.35 interpreter" >&2; exit 2
}
export_env() {
  unset PYTHONPATH PYTHONHOME
  export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
         TOKENIZERS_PARALLELISM=false CUDA_VISIBLE_DEVICES=""
}
latest() { [[ -f logs/latest ]] || { echo "No pipeline has been started yet"; exit 2; }; cat logs/latest; }

cmd="${1:-help}"; shift || true
case "$cmd" in
  test)
    sha256sum --quiet -c SHA256SUMS
    export_env
    STACK="$(stack_python)"; NATIVE="$(native_python)"
    GATE1_NATIVE="$NATIVE" GATE1_CACHE="$CACHE" "$STACK" -m unittest discover -s tests -p 'test_*.py' -v
    bash -n RUN_GATE1.sh
    echo "Gate 1 package checks passed" ;;
  all|smoke|run)
    sel="${1:-both}"
    case "$sel" in both) profs="qwen gemma" ;; qwen|gemma) profs="$sel" ;;
      *) echo "Profile must be both, qwen or gemma" >&2; exit 2 ;; esac
    sha256sum --quiet -c SHA256SUMS
    export_env
    STACK="$(stack_python)"; NATIVE="$(native_python)"
    stamp="$(date -u +%Y%m%dT%H%M%SZ)_gate1_${cmd}$([[ "$sel" == both ]] || printf '_%s' "$sel")"
    log="$ROOT/logs/$stamp.log"
    # shellcheck disable=SC2086
    E0_STACK_ORIGIN="$STACK" setsid nohup "$STACK" -u pipeline.py --mode "$cmd" --profiles $profs --stamp "$stamp" --log "$log" \
      --cache "$CACHE" --native-python "$NATIVE" >"$log" 2>&1 </dev/null &
    printf '%s\n' "$stamp" > logs/latest
    for _ in 1 2 3 4 5 6 7 8 9 10; do [[ -s "logs/$stamp.pid" ]] && break; sleep 1; done
    pid="$(cat "logs/$stamp.pid" 2>/dev/null || true)"   # written by pipeline.py: its process group id
    if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then echo "Pipeline exited immediately; see $log"; tail -20 "$log"; exit 1; fi
    cat <<EOF
Started Gate 1 pipeline ($cmd, profiles: $profs) on physical GPU 3, detached (setsid + nohup).
  PIPELINE  $stamp
  PID       $pid
  LOG       $log
Follow it:  bash RUN_GATE1.sh follow        (or: tail -F $log)
Status:     bash RUN_GATE1.sh status
Result ZIP: $ROOT/bundles/gate1_${stamp}_evaluation.zip  (written when the pipeline ends)
EOF
    ;;
  follow)
    stamp="$(latest)"; exec tail -n 50 -F "logs/$stamp.log" ;;
  status)
    stamp="$(latest)"
    pid="$(cat "logs/$stamp.pid" 2>/dev/null || true)"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then echo "PIPELINE $stamp: RUNNING (PID $pid)"; else echo "PIPELINE $stamp: NOT RUNNING"; fi
    [[ -f "logs/${stamp}_pipeline_status.json" ]] && python3 -c "
import json,sys; s=json.load(open(sys.argv[1]))
print('phase:', s.get('phase'), '| updated:', s.get('updated_utc'))
for k,v in s.get('runs',{}).items(): print('  run', k, v)
for k in ('smoke_gate','verdict','bundle','bundle_light'):
    if k in s: print(' ', k+':', s[k])" "logs/${stamp}_pipeline_status.json"
    for f in runs/"$stamp"_*/model_*/progress.json; do [[ -f "$f" ]] && { echo "progress $f:"; cat "$f"; echo; }; done
    echo "--- last log lines ($ROOT/logs/$stamp.log)"; tail -n 8 "logs/$stamp.log" ;;
  audit)
    export_env; STACK="$(stack_python)"
    if [[ $# -gt 0 ]]; then dirs=("$@"); else
      stamp="$(latest)"; dirs=()
      for d in runs/"$stamp"_qwen runs/"$stamp"_gemma; do [[ -d "$d" ]] && dirs+=("$d"); done
    fi
    [[ ${#dirs[@]} -gt 0 ]] || { echo "No full run directories found"; exit 2; }
    for d in "${dirs[@]}"; do
      out="reanalysis/out_$(basename -- "$d")"
      "$STACK" reanalysis/deep_audit.py "$d" --out "$out" && echo "Audit of $d written to $ROOT/$out"
    done ;;
  stop)
    stamp="$(latest)"; pid="$(cat "logs/$stamp.pid")"
    if kill -0 "$pid" 2>/dev/null; then
      kill -TERM -- "-$pid" && echo "Sent SIGTERM to pipeline $stamp (process group $pid). It archives and writes the ZIP."
    else echo "Pipeline $stamp is not running"; fi ;;
  *)
    sed -n '2,20p' "$0" ;;
esac
