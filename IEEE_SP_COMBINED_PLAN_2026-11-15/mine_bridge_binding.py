#!/usr/bin/env python3
"""Bridge (8 Nov) and final experiment (8 Nov), re-read for ONE question:
when the authorized identifier is / is not in the agent's view, what does the agent commit?
Read-only on /home/tahad/IEEE_SP/IEEE_SP_2027/artifact_extracts/*.csv.  Output -> bridge_binding.json"""
import csv, json, collections, sys
from pathlib import Path
csv.field_size_limit(10**9)
X = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/artifact_extracts')
out = {}
def J(s):
    try: return json.loads(s) if s else None
    except Exception: return s
for tag, f in (('gemma_E13', 'bridge_E13_gemma_episodes.csv'), ('qwen_E14', 'bridge_E14_qwen_episodes.csv')):
    R = list(csv.DictReader(open(X/f)))
    o = {'episodes': len(R), 'arms': dict(collections.Counter(r['arm'] for r in R))}
    # restrict to clean (no attack), strict permission, tool-supplied identifier
    def sel(r, arm): return r['arm'] == arm and r['attack'] == '0' and r['flex'] == '0' and r['source'] == '1'
    def outcome(r):
        cc = r['commit_classes']
        if not cc or cc in ('[]', ''): return 'nothing_committed'
        c = J(cc); c = c if isinstance(c, list) else [c]
        if any('out_of_contract' in str(x) or 'forbidden' in str(x) for x in c): return 'wrong_committed'
        if any('authorized' in str(x) or 'lawful' in str(x) or 'good' in str(x) for x in c): return 'authorized_committed'
        return 'other:' + str(c)[:40]
    o['commit_class_vocabulary'] = dict(collections.Counter(r['commit_classes'] for r in R).most_common(8))
    tab = {}
    for arm in ('plain', 'scalar', 'without_id', 'placebo_id', 'authority'):
        S = [r for r in R if sel(r, arm)]
        t = collections.Counter((('id_kept' if r['identifier_retained'] in ('1', 'True', 'true') else ('id_lost' if r['identifier_retained'] in ('0', 'False', 'false') else 'not_sanitized')), outcome(r)) for r in S)
        tab[arm] = {f'{k[0]}|{k[1]}': v for k, v in sorted(t.items())}
    o['clean_strict_tool_id_cells: view x outcome'] = tab
    # what is the substituted identifier when wrong?  compare first_commit_args[identifier_field] with good/alt and with a small set of ambient values
    sub = collections.Counter(); ex = []
    for r in R:
        if not sel(r, 'scalar') or outcome(r) != 'wrong_committed': continue
        a = J(r['first_commit_args']) or {}; g = J(r['good_args']) or {}; fld = r['identifier_field']
        v = a.get(fld) if isinstance(a, dict) else None
        same_id = (v == g.get(fld)) if isinstance(g, dict) else None
        kind = 'identifier_correct_other_field_wrong' if same_id else ('identifier_empty' if v in (None, '', []) else 'identifier_substituted')
        sub[(r['family'], kind)] += 1
        if kind == 'identifier_substituted' and len(ex) < 12: ex.append({'family': r['family'], 'field': fld, 'committed': v, 'authorized': g.get(fld)})
    o['scalar_wrong_commits_by_kind'] = {f'{k[0]}|{k[1]}': v for k, v in sorted(sub.items())}
    vals = collections.Counter()
    for r in R:
        if sel(r, 'scalar') and outcome(r) == 'wrong_committed':
            a = J(r['first_commit_args']) or {}; v = a.get(r['identifier_field']) if isinstance(a, dict) else None
            vals[json.dumps(v)[:60]] += 1
    o['most_common_committed_identifier_values_in_wrong_commits'] = vals.most_common(8)
    o['examples'] = ex
    out[tag] = o
# final experiment, live part (Qwen), parsed rows only
R = list(csv.DictReader(open(X/'final_E2L_qwen_records.csv')))
o = {'records': len(R), 'status': dict(collections.Counter(r['status'] for r in R))}
for arm in ('bypass', 'same_context', 'scalar', 'preserve'):
    o[f'arm_{arm}_status'] = dict(collections.Counter(r[f'arm_{arm}_status'] for r in R))
P = [r for r in R if r['arm_scalar_status'] not in ('', 'unparsed', 'UNPARSED') and r['arm_bypass_outcome']]
o['rows_with_bypass_outcome'] = len(P)
for arm in ('bypass', 'same_context', 'scalar', 'preserve'):
    o[f'arm_{arm}_outcome_by_edit'] = {e: dict(collections.Counter(r[f'arm_{arm}_outcome'] for r in R if r['edit'] == e and r[f'arm_{arm}_outcome'])) for e in sorted({r['edit'] for r in R})}
out['final_E2L_qwen'] = o
json.dump(out, open(Path(__file__).with_name('bridge_binding.json'), 'w'), indent=1)
print(json.dumps(out, indent=1)[:9000])
