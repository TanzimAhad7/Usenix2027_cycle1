#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
if [[ "${1:-}" == --help ]]; then
  python3 run.py --help
  echo 'Launcher options before runner arguments: --foreground, --run-id EXISTING_ID'
  echo 'Launcher environment: E2E_NATIVE_PYTHON, E0_STACK_PYTHON, E0_MODEL_CACHE'
  exit 0
fi
mkdir -p logs runs
worker=0
foreground=0
run_id=""
while (( $# )); do
  case "$1" in
    --worker) worker=1; run_id="${2:?Missing run ID}"; shift 2 ;;
    --foreground) foreground=1; shift ;;
    --run-id) run_id="${2:?Missing run ID}"; shift 2 ;;
    *) break ;;
  esac
done
if [[ -z "$run_id" ]]; then run_id="$(date -u +%Y%m%dT%H%M%SZ)_$$_$RANDOM"; fi
[[ "$run_id" =~ ^[0-9]{8}T[0-9]{6}Z_[0-9]+_[0-9]+$ ]] || { echo "Invalid run ID"; exit 2; }
log="$ROOT/logs/$run_id.log"
if (( !worker && !foreground )); then
  nohup bash "$ROOT/RUN_STUDY.sh" --worker "$run_id" "$@" >>"$log" 2>&1 </dev/null &
  printf 'RUN_ID=%s PID=%s\nLOG=%s\n' "$run_id" "$!" "$log"
  printf 'Progress: bash %q %q\n' "$ROOT/SHOW_PROGRESS.sh" "$run_id"
  exit 0
fi
exec 9>"$ROOT/logs/study.lock"
flock -n 9 || { echo "Another process owns this package's study lock"; exit 2; }
printf '%s\n' "$run_id" >"$ROOT/logs/latest"
sha256sum --quiet -c SHA256SUMS
stage=qualify
engine=local
previous=""
for arg in "$@"; do
  case "$previous" in --stage) stage="$arg";; --engine) engine="$arg";; esac
  case "$arg" in --stage=*) stage="${arg#*=}";; --engine=*) engine="${arg#*=}";;
    --out|--out=*|--profile|--profile=*) echo "Use --run-id to select the output directory"; exit 2;;
  esac
  previous="$arg"
done
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=""
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
python=python3
native_args=()
qualify_native() {
  [[ -x "$1" ]] && "$1" -c '
from importlib.metadata import version
from agentdojo.task_suite.load_suites import get_suite
assert version("agentdojo") == "0.1.35"
for suite in ("banking", "workspace"): get_suite("v1", suite)
' >/dev/null 2>&1
}
if [[ "$stage" != analyze ]]; then
  native="${E2E_NATIVE_PYTHON:-}"
  if [[ -z "$native" ]]; then
    for candidate in "$ROOT"/../IEEE_SP_R3*/.venv/bin/python "$ROOT"/../IEEE_SP_*/.venv/bin/python "$ROOT"/.venv-native/bin/python; do
      if qualify_native "$candidate"; then native="$candidate"; break; fi
    done
  fi
  if [[ -z "$native" ]]; then
    uv_bin="$(command -v uv || true)"
    if [[ -z "$uv_bin" && -x "$HOME/.local/bin/uv" ]]; then uv_bin="$HOME/.local/bin/uv"; fi
    [[ -n "$uv_bin" ]] || { echo "Set E2E_NATIVE_PYTHON to the existing AgentDojo 0.1.35 interpreter"; exit 2; }
    [[ ! -e .venv-native || -f .venv-native/.study-owned ]] ||
      { echo "Existing .venv-native has no ownership marker"; exit 2; }
    if [[ ! -x .venv-native/bin/python ]]; then
      "$uv_bin" venv --python 3.10 .venv-native
      touch .venv-native/.study-owned
    fi
    native="$ROOT/.venv-native/bin/python"
    "$uv_bin" pip sync --python "$native" native.lock.txt
  fi
  qualify_native "$native" || { echo "Native interpreter failed AgentDojo 0.1.35 validation"; exit 2; }
  native_args=(--native-python "$native")
fi
if [[ "$engine" == local && "$stage" != qualify && "$stage" != analyze ]]; then
  qualify_stack() {
    [[ -x "$1" ]] && "$1" -c '
import sys, torch, transformers, accelerate
assert sys.version_info[:2] == (3,12)
assert torch.__version__.split("+")[0] == "2.11.0" and torch.version.cuda is not None
assert transformers.__version__ == "5.20.2"
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration
' >/dev/null 2>&1
  }
  stack="${E0_STACK_PYTHON:-}"
  if [[ -z "$stack" ]]; then
    for candidate in "$ROOT"/../IEEE_SP_*/.venv-serving/bin/python "$ROOT"/../IEEE_SP_*/.venv/bin/python; do
      if qualify_stack "$candidate"; then stack="$candidate"; break; fi
    done
  fi
  [[ -n "$stack" ]] && qualify_stack "$stack" || {
    echo "Set E0_STACK_PYTHON to the Python 3.12 CUDA stack with Torch 2.11.0, Transformers 5.20.2 and Accelerate"; exit 2;
  }
  origin="$("$stack" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"
  if [[ ! -x .venv/bin/python ]]; then
    [[ ! -e .venv ]] || { echo "Incomplete local environment. Use a fresh extraction."; exit 2; }
    "$stack" -m venv --without-pip "$ROOT/.venv"
    site="$("$ROOT/.venv/bin/python" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"
    "$stack" -c 'import sysconfig; print("import site; site.addsitedir(" + repr(sysconfig.get_path("purelib")) + ")")' \
      >"$site/study_stack.pth"
    printf '%s\n' "$origin" >"$ROOT/.venv/study_stack_origin"
  fi
  [[ -f .venv/study_stack_origin && "$(<.venv/study_stack_origin)" == "$origin" ]] ||
    { echo "Local environment was built from a different stack"; exit 2; }
  python="$ROOT/.venv/bin/python"
  qualify_stack "$python" || { echo "Local .venv validation failed"; exit 2; }
fi
exec "$python" -u run.py --out "$ROOT/runs/$run_id" --archive "${native_args[@]}" \
  --cache "${E0_MODEL_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}" "$@"
