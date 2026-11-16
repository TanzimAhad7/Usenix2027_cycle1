#!/usr/bin/env bash
# Started only by RUN_N2.sh (setsid + nohup). Physical GPU 3 only. Never stops another process.
set -uo pipefail
PKG="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_ID="$1"; shift
RUN_DIR="$PKG/runs/$RUN_ID"
PY=/home/tahad/IEEE_SP/IEEE_SP_2027/IEEE_SP_N1_GPU3/.venv/bin/python
export CUDA_VISIBLE_DEVICES="" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONHOME PYTHONPATH
echo "N2 $RUN_ID started $(date -u +%FT%TZ); args: $*"
# Same GPU 3 locks as the N1 package and the project sequence; refuse to start if any is held.
mkdir -p /home/tahad/IEEE_SP/IEEE_SP_2027/logs
exec 7> /home/tahad/IEEE_SP/IEEE_SP_2027/logs/gpu3_sequence.lock
flock -n 7 || { echo 'BLOCKED: the project GPU 3 sequence lock is held. Nothing was started.'; exit 2; }
exec 6> "/tmp/ieee_sp_gpu3_${UID}.lock"
flock -n 6 || { echo 'BLOCKED: another GPU 3 sequence holds its lock. Nothing was started.'; exit 2; }
MOCK=0; for a in "$@"; do [[ "$a" == --mock ]] && MOCK=1; done
if [[ $MOCK == 0 ]]; then
  GPU_UUID='GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
  if nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader | grep -qF "$GPU_UUID"; then
    echo 'BLOCKED: GPU 3 has active compute processes. None was stopped. Try again when they finish.'; exit 2
  fi
fi
cd "$PKG"
"$PY" -u -m n2.controller --run "$RUN_DIR" "$@"
RC=$?
echo "controller exit $RC at $(date -u +%FT%TZ)"
"$PY" -u -m n2.analyze "$RUN_DIR" || echo "analysis failed (episodes are kept)"
mkdir -p "$PKG/bundles"
ZIP="$PKG/bundles/${RUN_ID}_evaluation.zip"
( cd "$PKG" && zip -qr "$ZIP" PROTOCOL.md RUN_N2.sh _inner.sh SHOW_PROGRESS.sh n2 inputs "runs/$RUN_ID" "logs/$RUN_ID.log" -x '*/__pycache__/*' )
echo "BUNDLE $ZIP ($(du -h "$ZIP" | cut -f1))"
echo "N2 $RUN_ID finished $(date -u +%FT%TZ)"
exit $RC
