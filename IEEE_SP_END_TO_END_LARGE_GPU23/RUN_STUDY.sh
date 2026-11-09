#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--help" ]]; then
  echo 'Usage: bash RUN_STUDY.sh [--prepare-only] [--batch-lanes N] [--models qwen gemma] [--gemma-revision <sha>] [--gemma-cache <hub-cache>]'
  echo 'Optional environment: E0_STACK_PYTHON, E0_MODEL_CACHE, E2E_NATIVE_PYTHON'
  exit 0
fi
mkdir -p "$ROOT/logs" "$ROOT/runs"
if [[ "${1:-}" != "--_owned_worker" ]]; then
  run_id="$(date -u +%Y%m%dT%H%M%SZ)_$$_$RANDOM"
  log="$ROOT/logs/$run_id.log"
  nohup bash "$ROOT/RUN_STUDY.sh" --_owned_worker "$run_id" "$@" >"$log" 2>&1 </dev/null &
  echo "PID=$! LOG=$log"
  echo "Progress: bash \"$ROOT/SHOW_PROGRESS.sh\" \"$run_id\""
  exit 0
fi
shift
run_id="$1"
shift
[[ "$run_id" =~ ^[0-9]{8}T[0-9]{6}Z_[0-9]+_[0-9]+$ ]] || exit 2
exec 9>"$ROOT/logs/e0e1_gpu23.lock"
flock -n 9 || { echo "Another end-to-end process owns the study lock"; exit 2; }
printf '%s\n' "$run_id" >"$ROOT/logs/latest"
sha256sum -c "$ROOT/SHA256SUMS" >/dev/null
CACHE="${E0_MODEL_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}"
STACK="${E0_STACK_PYTHON:-}"
qualify_stack() {
  [[ -x "$1" ]] && env -u PYTHONPATH -u PYTHONHOME "$1" -c '
import sys, torch, transformers
assert sys.version_info[:2] == (3,12)
assert torch.__version__.split("+")[0] == "2.11.0" and torch.version.cuda is not None
assert transformers.__version__ == "5.20.2"
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration
' >/dev/null 2>&1
}
if [[ -n "$STACK" ]]; then
  qualify_stack "$STACK" || { echo "E0_STACK_PYTHON failed the CUDA stack check"; exit 2; }
else
  for candidate in "$ROOT"/../IEEE_SP_*/.venv-serving/bin/python; do
    if qualify_stack "$candidate"; then STACK="$candidate"; break; fi
  done
  [[ -n "$STACK" ]] || { echo "Set E0_STACK_PYTHON to the existing Python 3.12 CUDA environment (torch 2.11.0 and Transformers 5.20.2)."; exit 2; }
fi
unset PYTHONPATH PYTHONHOME
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export E0_STACK_ORIGIN="$STACK"
SOURCE_SITE="$("$STACK" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"
if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  [[ ! -e "$ROOT/.venv" ]] || { echo "Incomplete .venv already exists. Use a fresh extraction."; exit 2; }
  "$STACK" -m venv --without-pip "$ROOT/.venv"
  local_site="$("$ROOT/.venv/bin/python" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"
  printf '%s\n' "$SOURCE_SITE" >"$local_site/e0_existing_stack.pth"
  printf '%s\n' "$SOURCE_SITE" >"$ROOT/.venv/e0_stack_origin"
fi
[[ -f "$ROOT/.venv/e0_stack_origin" && "$(<"$ROOT/.venv/e0_stack_origin")" == "$SOURCE_SITE" ]] ||
  { echo "Existing local .venv does not match the selected stack. Use a fresh extraction."; exit 2; }
qualify_stack "$ROOT/.venv/bin/python" || { echo "Local isolated .venv failed the stack check"; exit 2; }
if ! "$ROOT/.venv/bin/python" -c 'import accelerate' >/dev/null 2>&1; then
  UV="$(command -v uv || true)"
  if [[ -z "$UV" && -x "$HOME/.local/bin/uv" ]]; then UV="$HOME/.local/bin/uv"; fi
  if [[ -z "$UV" && -x "$(dirname "$(dirname "$STACK")")/../.tools/uv" ]]; then
    UV="$(dirname "$(dirname "$STACK")")/../.tools/uv"
  fi
  [[ -n "$UV" ]] || { echo "Missing accelerate and uv. See README.md."; exit 2; }
  "$UV" pip install --python "$ROOT/.venv/bin/python" --no-deps 'accelerate==1.12.0'
  "$ROOT/.venv/bin/python" -c 'import accelerate'
fi

NATIVE="${E2E_NATIVE_PYTHON:-}"
qualify_native() {
  [[ -x "$1" ]] && CUDA_VISIBLE_DEVICES="" "$1" -c '
from importlib.metadata import version
from agentdojo.task_suite.load_suites import get_suite
assert version("agentdojo") == "0.1.35"
for suite in ("banking","workspace","slack"):
    get_suite("v1",suite)
' >/dev/null 2>&1
}
if [[ -n "$NATIVE" ]]; then
  qualify_native "$NATIVE" || { echo "E2E_NATIVE_PYTHON must run AgentDojo 0.1.35"; exit 2; }
else
  for candidate in "$ROOT"/../IEEE_SP_R3*/.venv/bin/python "$ROOT"/../IEEE_SP_*/.venv/bin/python "$ROOT/.venv-native/bin/python"; do
    if qualify_native "$candidate"; then NATIVE="$candidate"; break; fi
  done
fi
if [[ -z "$NATIVE" ]]; then
  UV="$(command -v uv || true)"
  if [[ -z "$UV" && -x "$HOME/.local/bin/uv" ]]; then UV="$HOME/.local/bin/uv"; fi
  if [[ -z "$UV" && -x "$(dirname "$(dirname "$STACK")")/../.tools/bin/uv" ]]; then
    UV="$(dirname "$(dirname "$STACK")")/../.tools/bin/uv"
  fi
  [[ -n "$UV" ]] || { echo "Set E2E_NATIVE_PYTHON to the R3 client environment or put uv on PATH."; exit 2; }
  [[ ! -e "$ROOT/.venv-native" || -f "$ROOT/.venv-native/.e2e-owned" ]] ||
    { echo "Preserving an existing unrecognized native environment"; exit 2; }
  if [[ ! -x "$ROOT/.venv-native/bin/python" ]]; then
    "$UV" venv --python 3.10.21 "$ROOT/.venv-native"
    touch "$ROOT/.venv-native/.e2e-owned"
  fi
  NATIVE="$ROOT/.venv-native/bin/python"
  "$UV" pip sync --python "$NATIVE" "$ROOT/native.lock.txt"
  qualify_native "$NATIVE" || { echo "Native environment setup failed"; exit 2; }
fi
NATIVE="$(cd -- "$(dirname -- "$NATIVE")" && pwd)/$(basename -- "$NATIVE")"
export E2E_SETUP_LOG="$ROOT/logs/$run_id.log"

export CUDA_VISIBLE_DEVICES=""
exec "$ROOT/.venv/bin/python" -u "$ROOT/run.py" --run "$ROOT/runs/$run_id" --cache "$CACHE" --native-python "$NATIVE" "$@"
