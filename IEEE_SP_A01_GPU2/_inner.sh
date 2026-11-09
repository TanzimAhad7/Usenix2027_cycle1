#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_ID="$1"
STAGE="$2"
shift 2
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH DIAG_VARIANT DIAG_MODEL_REVISION E2B_RESUME_DISABLED VIRTUAL_ENV
MODE=live
for ARG in "$@"; do if [[ "$ARG" == --mock ]]; then MODE=mock; fi; done
bootstrap_exit() {
 RC=$?
 if [[ ! -f "$PACKAGE_DIR/logs/$RUN_ID.status" ]]; then
  printf 'BOOTSTRAP_FAILED exit_code=%s\n' "$RC" > "$PACKAGE_DIR/logs/$RUN_ID.status"
  echo 'Bootstrap stopped. Inspect this log; no run was reported as complete.'
 fi
}
trap bootstrap_exit EXIT
mkdir -p "$PACKAGE_DIR/../logs"
exec 7> "$PACKAGE_DIR/../logs/gpu2_sequence.lock"
flock -n 7 || { echo 'Project GPU2 sequence lock occupied. No process stopped.'; exit 2; }
exec 6> "/tmp/ieee_sp_gpu2_${UID}.lock"
flock -n 6 || { echo 'GPU2 sequence lock occupied. No process stopped.'; exit 2; }
exec 9> "$PACKAGE_DIR/logs/gpu2_sequence.lock"
flock -n 9 || { echo 'Package GPU2 lock occupied.'; exit 2; }
if [[ "$MODE" == live ]]; then
 command -v nvidia-smi >/dev/null
 if nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader | grep -F 'GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932'; then
  echo 'GPU2 has active compute processes. No process stopped.'; exit 2
 fi
fi
RELEASE_PYTHON="${A01_RELEASE_PYTHON:-$PACKAGE_DIR/../IEEE_SP_E2b_GPU2/.venv/bin/python}"
if [[ ! -x "$RELEASE_PYTHON" ]]; then
 bash "$PACKAGE_DIR/SETUP.sh" release
 RELEASE_PYTHON="$PACKAGE_DIR/.venv/bin/python"
fi
SERVING_PYTHON="${A01_SERVING_PYTHON:-$PACKAGE_DIR/../IEEE_SP_E2b_GPU2/.venv-serving/bin/python}"
if [[ "$MODE" == live && ! -x "$SERVING_PYTHON" ]]; then
 bash "$PACKAGE_DIR/SETUP.sh" serving
 SERVING_PYTHON="$PACKAGE_DIR/.venv-serving/bin/python"
fi
cd "$PACKAGE_DIR"
"$RELEASE_PYTHON" -u -m a01.controller --stage "$STAGE" --project-root "$PACKAGE_DIR" --run-id "$RUN_ID" \
 --recorded-python "${A01_RECORDED_PYTHON:-$PACKAGE_DIR/../.venv/bin/python}" \
 --serving-python "$SERVING_PYTHON" --lock-fd 9 --workers "${A01_WORKERS:-4}" \
 --cache "${A01_HF_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}" "$@"
