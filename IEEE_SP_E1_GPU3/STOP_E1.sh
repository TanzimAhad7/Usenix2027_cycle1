#!/usr/bin/env bash
set -euo pipefail
P="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN="$(cat "$P/logs/LATEST_E1")"
python3 "$P/PROCESS.py" stop "$P/logs/$RUN.pid.json"
