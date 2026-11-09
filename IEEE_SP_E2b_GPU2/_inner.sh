#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_ID="$1"; shift
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH DIAG_VARIANT DIAG_MODEL_REVISION E1_RESUME_PARENT E2B_RESUME_DISABLED
echo "E2B bootstrap: $RUN_ID; source setup hides all GPUs. Live inference uses GPU2 only."
MODE=live
for ARG in "$@"; do if [[ "$ARG" == --mock || "$ARG" == --cpu-only ]]; then MODE=cpu; fi; done
bootstrap_exit() {
 RC=$?
 if [[ ! -f "$PACKAGE_DIR/logs/$RUN_ID.status" ]]; then
  python3 "$PACKAGE_DIR/BOOTSTRAP_FAILURE.py" "$PACKAGE_DIR" "$RUN_ID" "$RC" || true
 fi
}
trap bootstrap_exit EXIT
# Also coordinate with the existing project's GPU2 lock. Preserve all older jobs.
mkdir -p "$PACKAGE_DIR/../logs"
exec 7> "$PACKAGE_DIR/../logs/gpu2_sequence.lock"
flock -n 7 || { echo 'BLOCKED_CONCURRENT_SEQUENCE: existing project GPU2 sequence owns its lock.'; exit 2; }
exec 6> "/tmp/ieee_sp_gpu2_${UID}.lock"
flock -n 6 || { echo 'BLOCKED_CONCURRENT_SEQUENCE: another E2B GPU2 sequence owns its lock.'; exit 2; }
exec 9> "$PACKAGE_DIR/logs/gpu2_sequence.lock"
flock -n 9 || { echo 'BLOCKED_CONCURRENT_SEQUENCE: package sequence lock occupied.'; exit 2; }
if [[ "$MODE" == live ]]; then
 if ! command -v nvidia-smi >/dev/null; then echo 'nvidia-smi is unavailable; no live launch.'; exit 2; fi
 GPU_UUID='GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932'
 if nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader | grep -F "$GPU_UUID"; then
  echo 'GPU2 has active compute processes. No process was stopped. Try again when your run finishes.'; exit 2
 fi
fi
if [[ -n "${E2B_RESEARCH_PYTHON:-}" && "$MODE" == cpu ]]; then
 # Explicit override is for validation/reuse only; no dependency installs in that environment.
 RESEARCH_PYTHON="$E2B_RESEARCH_PYTHON"
else
 bash "$PACKAGE_DIR/SETUP.sh" research
 RESEARCH_PYTHON="$PACKAGE_DIR/.venv/bin/python"
fi
if [[ "$MODE" == live ]]; then bash "$PACKAGE_DIR/SETUP.sh" serving; fi
cd "$PACKAGE_DIR"
"$RESEARCH_PYTHON" -u -m e2b.controller --project-root "$PACKAGE_DIR" --run-id "$RUN_ID" \
 --serving-python "$PACKAGE_DIR/.venv-serving/bin/python" --lock-fd 9 \
 --cache "${E2B_HF_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}" \
 --workers "${E2B_WORKERS:-8}" "$@"
