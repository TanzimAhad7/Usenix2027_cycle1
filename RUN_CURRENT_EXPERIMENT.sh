#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
exec bash IEEE_SP_Reference_Study_GPU2/RUN_STUDY.sh "$@"
