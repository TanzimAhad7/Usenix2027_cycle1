#!/usr/bin/env python3
"""Bridge (8 Nov), guard arm, no attacker: is the detector's flag related to whether the agent's
FIRST PROPOSAL was correct?  Read-only.  Output -> flag_vs_correctness.json"""
import csv, json, collections
from pathlib import Path
csv.field_size_limit(10**9)
X = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/artifact_extracts'); out = {}
def J(s):
    try: return json.loads(s) if s else None
    except Exception: return None
def norm(v): return json.dumps(v, sort_keys=True).lower().strip()
for tag, f in (('gemma', 'bridge_E13_gemma_episodes.csv'), ('qwen', 'bridge_E14_qwen_episodes.csv')):
    R = [r for r in csv.DictReader(open(X/f)) if r['attack'] == '0' and r['flex'] == '0' and r['arm'] == 'scalar']
    o = {}
    for src in ('1', '0'):
        t = collections.Counter(); ex = collections.Counter()
        for r in R:
            if r['source'] != src: continue
            p = J(r['first_proposal_args']); g = J(r['good_args'])
            if not isinstance(p, dict) or not isinstance(g, dict): t[('no_parsed_proposal', r['flagged'])] += 1; continue
            idf, pf = r['identifier_field'], r['parameter_field']
            ok_id = norm(p.get(idf)) == norm(g.get(idf)); ok_p = norm(p.get(pf)) == norm(g.get(pf))
            k = 'proposal_correct' if (ok_id and ok_p) else ('identifier_wrong' if not ok_id else 'parameter_wrong')
            t[(k, 'flagged' if r['flagged'] in ('1', 'True', 'true') else 'not_flagged')] += 1
            if k != 'proposal_correct' and r['flagged'] not in ('1', 'True', 'true'): ex[norm(p.get(idf))[:40] + ' | ' + norm(p.get(pf))[:25]] += 1
        o['identifier_from_tool' if src == '1' else 'identifier_from_user'] = {'proposal_class x flag': {f'{k[0]}|{k[1]}': v for k, v in sorted(t.items())}, 'unflagged_wrong_proposals_top_values': ex.most_common(5)}
    out[tag] = o
json.dump(out, open(Path(__file__).with_name('flag_vs_correctness.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
