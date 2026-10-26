#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo 'ERROR: python3 is required' >&2; exit 2; }
python3 scripts/verify_project.py
