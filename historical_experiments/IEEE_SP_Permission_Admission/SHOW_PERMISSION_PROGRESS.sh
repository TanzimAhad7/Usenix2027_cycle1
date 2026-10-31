#!/usr/bin/env bash
set -euo pipefail
BUNDLE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -d "$BUNDLE/.venv" ]]; then PROJECT_ROOT="$BUNDLE"; else PROJECT_ROOT="$(dirname "$BUNDLE")"; fi
PROJECT_ROOT="${PERMISSION_PROJECT_ROOT:-$PROJECT_ROOT}"
latest="$(find "$PROJECT_ROOT/logs" -maxdepth 1 -name 'permission_admission_*.log' -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
if [[ -z "$latest" ]]; then echo 'No permission campaign log found.'; exit 1; fi
echo "Log: $latest"
if [[ -f "$latest.pid" ]]; then ps -p "$(cat "$latest.pid")" -o pid,etime,stat,args || true; fi
tail -n 35 -f "$latest"

