#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ "$#" -gt 1 ]]; then echo 'Usage: bash SHOW_PROGRESS.sh [RUN_ID]'; exit 2; fi
id="${1:-$(cat logs/latest)}"
[[ "$id" =~ ^[0-9]{8}T[0-9]{6}Z_[0-9]+_[0-9]+$ ]] || { echo "Invalid run ID"; exit 2; }
printf '%s\n' "RUN $id"
for p in "runs/$id/status.json" "runs/$id/"*/status.json; do
  if [[ -f "$p" ]]; then printf '%s\n' "$p"; cat -- "$p"; fi
done
if [[ -f "logs/$id.log" ]]; then tail -12 -- "logs/$id.log"; fi
