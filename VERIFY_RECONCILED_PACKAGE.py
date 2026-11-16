#!/usr/bin/env python3
"""Portable integrity/allocation check. No model, environment install or GPU."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
data=json.loads((root/'RECONCILED_PACKAGE_MANIFEST.json').read_text())
for name,expected in data['files'].items():
    p=root/name
    if not p.is_file():raise SystemExit('Missing file: '+name)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise SystemExit('Modified file: '+name)
protocol=json.loads((root/'reconciled_study/assets/NEXT_EXPERIMENT_ALLOCATION.json').read_text())
slots=protocol['slots']
assert len(slots)==len({s['slot_id'] for s in slots})==156
assert sum(s['workflow'] and s['activation']=='MANDATORY' for s in slots)==120
assert sum(s['activation']!='MANDATORY' for s in slots)==12
assert sum(not s['workflow'] for s in slots)==24
print('PASS: package hashes; 120 mandatory workflows, up to 12 repeats, 24 fixed conditions. No inference executed.')
