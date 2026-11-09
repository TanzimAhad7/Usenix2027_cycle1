#!/usr/bin/env bash
set -euo pipefail
bundle="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project="$PWD"
if [[ "${1:-}" == --worker ]]; then
  shift
  project="$1"
  shift
  export CUDA_VISIBLE_DEVICES='' PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 GIT_TERMINAL_PROMPT=0
  unset PYTHONPATH PYTHONHOME
  status_file="$1"
  shift
  trap 'rc=$?; printf "exit_code=%s\n" "$rc" > "$status_file"' EXIT
  python3 "$bundle/publish_update.py" --project-root "$project" "$@"
  exit
fi
if [[ "${1:-}" == --help ]]; then
  printf '%s\n' 'Run from your experiment project: bash IEEE_SP_Repository_Update/APPLY_AND_PUSH.sh [--stage-only] [--remote URL] [--branch NAME] [--skip-live-results]'
  exit
fi
if [[ -L "$project/logs" ]]; then
  printf '%s\n' 'Refusing symlink logs directory' >&2
  exit 1
fi
mkdir -p "$project/logs"
ident="repository_update_$(date -u +%Y%m%dT%H%M%SZ)_$$_${RANDOM}"
log="$project/logs/$ident.log"
status_file="$project/logs/$ident.status"
nohup bash "$bundle/APPLY_AND_PUSH.sh" --worker "$project" "$status_file" "$@" > "$log" 2>&1 < /dev/null &
printf 'PID: %s\nLog: %s\nStatus: %s\n' "$!" "$log" "$status_file"
printf 'Watch: tail -f %q\n' "$log"
