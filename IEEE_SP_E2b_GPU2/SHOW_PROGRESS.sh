#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "$P/logs/LATEST_E2B" ]]; then echo 'No E2B run has been launched.'; exit 0; fi
RUN="$(cat "$P/logs/LATEST_E2B")"
if [[ -f "$P/results/user_runs/$RUN/status.json" ]]; then cat "$P/results/user_runs/$RUN/status.json"; fi
printf '\nLatest log: %s\n' "$P/logs/$RUN.log"
tail -n 35 "$P/logs/$RUN.log"
