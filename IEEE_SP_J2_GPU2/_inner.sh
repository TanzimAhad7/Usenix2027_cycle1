#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_ID="$1"; shift
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH DIAG_VARIANT DIAG_MODEL_REVISION E2B_RESUME_DISABLED VIRTUAL_ENV
MODE=live
if [[ "${1:-}" == --mock ]]; then MODE=mock; fi
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
flock -n 7 || { echo 'Project GPU 2 sequence lock occupied; no process stopped.'; exit 2; }
exec 6> "/tmp/ieee_sp_gpu2_${UID}.lock"
flock -n 6 || { echo 'GPU 2 sequence lock occupied; no process stopped.'; exit 2; }
exec 9> "$PACKAGE_DIR/logs/gpu2_sequence.lock"
flock -n 9 || { echo 'Package GPU 2 lock occupied.'; exit 2; }
if [[ "$MODE" == live ]]; then
 command -v nvidia-smi >/dev/null
 GPU_UUID="$(nvidia-smi -i 2 --query-gpu=uuid --format=csv,noheader | tr -d '[:space:]')"
 [[ "$GPU_UUID" == GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932 ]] || { echo 'Physical GPU 2 UUID differs from the recorded server. No device selected.'; exit 2; }
 if nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader | grep -Fq "$GPU_UUID"; then
  echo 'GPU 2 has active compute processes; no process stopped.'; exit 2
 fi
fi
RELEASE_PYTHON="${J2_RELEASE_PYTHON:-}"
if [[ -n "$RELEASE_PYTHON" ]]; then
 "$RELEASE_PYTHON" "$PACKAGE_DIR/ENVIRONMENT.py" release
else
 for CANDIDATE in "$PACKAGE_DIR/.venv/bin/python" "$PACKAGE_DIR/../IEEE_SP_J1_GPU2/.venv/bin/python" "$PACKAGE_DIR/../IEEE_SP_A01_GPU2/.venv/bin/python" "$PACKAGE_DIR/../IEEE_SP_E2b_GPU2/.venv/bin/python"; do
  if [[ -x "$CANDIDATE" ]] && "$CANDIDATE" "$PACKAGE_DIR/ENVIRONMENT.py" release --quiet; then RELEASE_PYTHON="$CANDIDATE"; break; fi
 done
 if [[ -z "$RELEASE_PYTHON" ]]; then bash "$PACKAGE_DIR/SETUP.sh" release; RELEASE_PYTHON="$PACKAGE_DIR/.venv/bin/python"; fi
fi
SERVING_PYTHON="${J2_SERVING_PYTHON:-}"
if [[ "$MODE" == live ]]; then
 if [[ -n "$SERVING_PYTHON" ]]; then
  "$SERVING_PYTHON" "$PACKAGE_DIR/ENVIRONMENT.py" serving
 else
  for CANDIDATE in "$PACKAGE_DIR/.venv-serving/bin/python" "$PACKAGE_DIR/../IEEE_SP_J1_GPU2/.venv-serving/bin/python" "$PACKAGE_DIR/../IEEE_SP_A01_GPU2/.venv-serving/bin/python" "$PACKAGE_DIR/../IEEE_SP_E2b_GPU2/.venv-serving/bin/python"; do
   if [[ -x "$CANDIDATE" ]] && "$CANDIDATE" "$PACKAGE_DIR/ENVIRONMENT.py" serving --quiet; then SERVING_PYTHON="$CANDIDATE"; break; fi
  done
  if [[ -z "$SERVING_PYTHON" ]]; then bash "$PACKAGE_DIR/SETUP.sh" serving; SERVING_PYTHON="$PACKAGE_DIR/.venv-serving/bin/python"; fi
 fi
else SERVING_PYTHON="$RELEASE_PYTHON"; fi
cd "$PACKAGE_DIR"
"$RELEASE_PYTHON" -u -m j2.controller --project-root "$PACKAGE_DIR" --run-id "$RUN_ID" \
 --serving-python "$SERVING_PYTHON" --lock-fd 9 --workers "${J2_WORKERS:-4}" \
 --cache "${J2_HF_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}" "$@"
