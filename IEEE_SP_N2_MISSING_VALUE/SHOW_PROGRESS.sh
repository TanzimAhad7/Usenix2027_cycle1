#!/usr/bin/env bash
PKG="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_ID="${1:-$(cat "$PKG/logs/LATEST" 2>/dev/null)}"
[[ -z "$RUN_ID" ]] && { echo "No run yet."; exit 0; }
echo "Run: $RUN_ID"
for p in qwen gemma; do
  f="$PKG/runs/$RUN_ID/$p/status.json"
  [[ -f "$f" ]] && python3 -c "import json;d=json.load(open('$f'));print('$p', {k:d.get(k) for k in ('phase','planned','already_done','done','failed','updated')})"
done
echo "--- last log lines ---"; tail -n 5 "$PKG/logs/$RUN_ID.log" 2>/dev/null
