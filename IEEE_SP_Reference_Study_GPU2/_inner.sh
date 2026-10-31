#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$1"
RUN_ID="$2"
shift 2
export CUDA_VISIBLE_DEVICES=""
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
export STUDY_PROJECT_ROOT="$PROJECT_DIR"
bootstrap_exit() {
  RC=$?
  if [[ ! -f "$PROJECT_DIR/logs/$RUN_ID.status" ]]; then
    printf 'exit_code=%s\nstatus=BOOTSTRAP_FAILED\n' "$RC" > "$PROJECT_DIR/logs/$RUN_ID.status"
    python3 "$PACKAGE_DIR/BOOTSTRAP_ARCHIVE.py" "$PROJECT_DIR" "$RUN_ID" "$RC" || true
  fi
}
trap bootstrap_exit EXIT
exec 9> "$PROJECT_DIR/logs/gpu2_sequence.lock"
if ! flock -n 9; then
  echo 'BLOCKED_CONCURRENT_SEQUENCE: another GPU2 campaign owns the project lock. No environment or GPU process changed.'
  printf 'exit_code=2\nstatus=BLOCKED_CONCURRENT_SEQUENCE\n' > "$PROJECT_DIR/logs/$RUN_ID.status"
  exit 2
fi
echo "Preparing isolated project environment. No GPU is visible during setup."
bash "$PACKAGE_DIR/SETUP.sh" research
MODE='live'
for ARG in "$@"; do
  if [[ "$ARG" == '--mock' || "$ARG" == '--cpu-only' ]]; then MODE='cpu'; fi
done
if [[ "$MODE" == 'live' ]]; then bash "$PACKAGE_DIR/SETUP.sh" serving; fi
cd "$PACKAGE_DIR"
exec "$PROJECT_DIR/.venv/bin/python" -u -m reference_study.controller \
  --project-root "$PROJECT_DIR" --run-id "$RUN_ID" \
  --serving-python "$PROJECT_DIR/.venv-serving/bin/python" \
  --lock-fd 9 \
  --cache "${STUDY_HF_CACHE:-/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache}" \
  --workers "${STUDY_WORKERS:-4}" "$@"
