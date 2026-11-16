#!/usr/bin/env python3
"""Bridge (8 Nov): split every 'other_out_of_contract' first commit by WHICH field differs from the authorized call,
after normalising punctuation/case/whitespace.  Guard arm and no-guard arm, no attacker, strict permission,
tool-supplied identifier.  Read-only.  Output -> reopen_bridge_fields.json"""
import csv, json, re, collections
from pathlib import Path
csv.field_size_limit(10**9)
X = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/artifact_extracts')
TEXT = {'subject', 'body'}
def J(s):
    try: return json.loads(s) if s else None
    except Exception: return None
soft = lambda v: re.sub(r'[\W_]+', ' ', json.dumps(v, sort_keys=True).lower()).strip()
def kind(commit, good):
    if not isinstance(commit, dict) or not isinstance(good, dict): return 'no_commit_args'
    diff = [k for k in sorted(set(commit) | set(good)) if json.dumps(commit.get(k), sort_keys=True) != json.dumps(good.get(k), sort_keys=True)]
    if not diff: return 'exact'
    softdiff = [k for k in diff if soft(commit.get(k)) != soft(good.get(k))]
    if not softdiff: return 'punctuation_or_case_only'
    nontext = [k for k in softdiff if k not in TEXT]
    if nontext: return 'identity_or_numeric:' + ','.join(nontext)
    return 'free_text_differs'
out = {}
for tag, f in (('gemma', 'bridge_E13_gemma_episodes.csv'), ('qwen', 'bridge_E14_qwen_episodes.csv')):
    R = [r for r in csv.DictReader(open(X/f)) if r['attack'] == '0' and r['flex'] == '0' and r['source'] == '1']
    o = {}
    for arm in ('plain', 'scalar'):
        t = collections.defaultdict(collections.Counter)
        for r in R:
            if r['arm'] != arm: continue
            wrong = 'out_of_contract' in r['commit_classes'] or 'forbidden' in r['commit_classes']
            i, p = r['identifier_retained'], r['parameter_retained']
            view = 'no_guard' if arm == 'plain' else ('not_sanitized' if i == '' else ('nothing_lost' if (i, p) == ('1', '1') else 'some_value_lost'))
            if not r['commit_classes'] or r['commit_classes'] in ('[]',): t[view]['nothing_committed'] += 1; continue
            if not wrong: t[view]['authorized'] += 1; continue
            k = kind(J(r['first_commit_args']), J(r['good_args'])); t[view]['WRONG:' + k.split(':')[0]] += 1
            if k.startswith('identity'):
                for fld in k.split(':')[1].split(','): t[view]['  field:' + fld] += 1
        o[arm] = {k: dict(v) for k, v in sorted(t.items())}
    out[tag] = o
json.dump(out, open(Path(__file__).with_name('reopen_bridge_fields.json'), 'w'), indent=1)
for m in out:
    for arm in out[m]:
        for view, v in out[m][arm].items(): print(m, arm, view, v)
