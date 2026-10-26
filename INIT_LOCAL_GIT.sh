#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -d .git ]]; then git init; fi
git status --short
echo 'Local repository ready. No files staged, commit created, or remote configured.'
