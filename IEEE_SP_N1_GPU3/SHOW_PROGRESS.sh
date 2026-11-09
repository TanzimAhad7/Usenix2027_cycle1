#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "$P/logs/LATEST_N1" ]]; then echo 'No N1 run has been launched.'; exit 0; fi
RUN="$(cat "$P/logs/LATEST_N1")"
if [[ -f "$P/results/user_runs/$RUN/status.json" ]]; then cat "$P/results/user_runs/$RUN/status.json"; fi
printf '\nLatest log: %s\n' "$P/logs/$RUN.log"
tail -n 35 "$P/logs/$RUN.log"
