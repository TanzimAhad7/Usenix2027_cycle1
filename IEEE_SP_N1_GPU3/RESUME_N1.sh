#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN="$(cat "$P/logs/LATEST_N1")"
# RUN_N1 reserves a new ID; only terminal parent blocks are copied byte-for-byte.
bash "$P/RUN_N1.sh" --resume-parent "$P/results/user_runs/$RUN" "$@"
