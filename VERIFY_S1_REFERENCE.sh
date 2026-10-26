#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
bash RUN_S1_REFERENCE_GPU3.sh --cpu-only
