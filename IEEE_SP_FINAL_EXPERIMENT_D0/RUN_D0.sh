#!/usr/bin/env bash
# D0 entry point for SP-GUARD-WRITE-20261108-V1 under amendment D0-20261109.
#
#   bash RUN_D0.sh test                      # CPU: unit tests, native self-check, checksums
#   bash RUN_D0.sh recover-qwen              # CPU: recover the censored Qwen E1R of run 20261108T232225Z_3654860_31695
#   bash RUN_D0.sh pilot  qwen|gemma         # GPU: reduced smoke plan (real models), then run pilot_check.py
#   bash RUN_D0.sh full   qwen|gemma         # GPU: full frozen plan (calibration, E1R, E2L)
#   bash RUN_D0.sh check  RUN_ID qwen|gemma  # CPU: parse-census gate for a finished run
#   bash RUN_D0.sh status [RUN_ID]           # progress of a run
#
# GPU: physical GPU 3 only, for both profiles (run them one after the other). Runs start under
# setsid + nohup and survive terminal, SSH or laptop shutdown. Follow: tail -F logs/RUN_ID.log
# Model runs start under nohup through RUN_STUDY.sh and print RUN_ID, PID and log path.
# Nothing here stops another process; the runner refuses a GPU that already has compute jobs.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
OLD_RUN="$ROOT/../IEEE_SP_FINAL_EXPERIMENT_GPU3_SHARED_PREFILL/runs/20261108T232225Z_3654860_31695"

native_python() {
  if [[ -n "${E2E_NATIVE_PYTHON:-}" ]]; then printf '%s\n' "$E2E_NATIVE_PYTHON"; return; fi
  for candidate in "$ROOT"/../IEEE_SP_R3*/.venv/bin/python "$ROOT"/../IEEE_SP_*/.venv/bin/python; do
    if [[ -x "$candidate" ]] && "$candidate" -c '
from importlib.metadata import version
from agentdojo.task_suite.load_suites import get_suite
assert version("agentdojo") == "0.1.35"
for s in ("banking", "workspace"): get_suite("v1", s)' >/dev/null 2>&1; then
      printf '%s\n' "$candidate"; return
    fi
  done
  echo "Set E2E_NATIVE_PYTHON to an AgentDojo 0.1.35 interpreter" >&2; exit 2
}

gpu_for() {
  case "$1" in
    qwen|gemma) printf '%s\n' 3 ;;
    *) echo "Profile must be qwen or gemma" >&2; exit 2 ;;
  esac
}

cmd="${1:-help}"; shift || true
case "$cmd" in
  test)
    E2E_NATIVE_PYTHON="$(native_python)" bash TEST_PACKAGE.sh ;;
  recover-qwen)
    sha256sum --quiet -c SHA256SUMS
    mkdir -p logs
    log="logs/recover_qwen_$(date -u +%Y%m%dT%H%M%SZ).log"
    setsid nohup python3 -u recover_e1r.py --run "$OLD_RUN" --profile qwen --native-python "$(native_python)" \
      >"$log" 2>&1 </dev/null &
    printf 'PID=%s\nLOG=%s\nOutput: %s/recovered/%s/qwen/\n' "$!" "$log" "$ROOT" "$(basename "$OLD_RUN")" ;;
  pilot|full)
    profile="${1:?Usage: bash RUN_D0.sh $cmd qwen|gemma}"
    gpu="$(gpu_for "$profile")"
    extra=()
    [[ "$cmd" == pilot ]] && extra=(--smoke)
    E2E_NATIVE_PYTHON="$(native_python)" bash RUN_STUDY.sh --stage all --engine local \
      --profiles "$profile" --gpu "$gpu" ${extra[@]+"${extra[@]}"}
    echo "When it finishes: bash RUN_D0.sh check RUN_ID $profile" ;;
  check)
    run_id="${1:?Usage: bash RUN_D0.sh check RUN_ID qwen|gemma}"; profile="${2:?profile}"
    python3 pilot_check.py "runs/$run_id" "$profile" ;;
  status)
    bash SHOW_PROGRESS.sh "$@" ;;
  *)
    sed -n '2,13p' "$0" ;;
esac
