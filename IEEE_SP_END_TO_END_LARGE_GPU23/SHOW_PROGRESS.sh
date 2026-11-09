#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$#" -eq 1 ]]; then run_id="$1"
elif [[ -f "$ROOT/logs/latest" ]]; then run_id="$(<"$ROOT/logs/latest")"
else echo "No run recorded."; exit 1; fi
[[ "$run_id" =~ ^[0-9]{8}T[0-9]{6}Z_[0-9]+_[0-9]+$ ]] || exit 2
run="$ROOT/runs/$run_id"
printf 'Run %s\n' "$run_id"
for file in "$run"/status.json "$run"/gpu_bindings.json "$run"/profile_timing.json "$run"/model_*/status.json "$run"/model_*/progress.json "$run"/model_*/bridge/progress.json; do
  if [[ -f "$file" ]]; then printf '%s\n' "$file"; cat "$file"; fi
done
for file in "$ROOT/logs/$run_id.log" "$run"/model_*/score.log; do
  if [[ -f "$file" ]]; then printf '\n%s\n' "$file"; tail -n 12 "$file"; fi
done
if [[ -f "$run/REPORT.md" ]]; then printf '\nReport %s\n' "$run/REPORT.md"; fi
if [[ -f "$run.zip" ]]; then printf '\nArchive %s\n' "$run.zip"; fi
