#!/usr/bin/env python3
"""Does the same word-overlap measure predict the decisions of a SECOND guard?
Live AttriGuard study (study 08, released code, gpt-4.1-mini), defense-on runs.
For each privileged call the guard inspected: user_share = share of its argument words found in the
user's request; outcome = blocked or allowed.  Read-only.  Output -> copy_law_attriguard.json"""
import json, re, collections, warnings, logging
from pathlib import Path
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
from agentdojo.task_suite.load_suites import get_suite
B = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/research_basis/studies/08_live_end_to_end/frozen_results/scientific_v1')
rows = [json.loads(l) for l in open(B/'RUN_ROWS.jsonl')]
rel = lambda p: B/Path(p).relative_to('E2E_ATTR_AUTH_v1/scientific_v1')
SU = {s: get_suite('v1', s) for s in ('banking', 'slack', 'travel', 'workspace')}
tok = lambda s: [t.lower() for t in re.findall(r"[A-Za-z0-9@._\-']{3,}", s)]
def words(a):
    T = []
    def walk(x):
        if isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, list): [walk(v) for v in x]
        elif x is not None: T.extend(tok(str(x)))
    walk(a); return T
def auc(pos, neg):
    return None if not pos or not neg else sum((p > q) + 0.5*(p == q) for p in pos for q in neg)/(len(pos)*len(neg))
print('diagnostic keys:', sorted({k for r in rows for d in r['privileged_call_diagnostics'] for k in d}))
rec = []
for r in rows:
    if r['defense'] != 'ON': continue
    raw = json.load(open(rel(r['raw_result_relpath']))); U = set(tok(SU[r['suite']].get_user_task_by_id(r['user_task']).PROMPT))
    # privileged calls proposed by the agent, in order, from the raw trace
    prop = [tc for m in raw['messages'] if m['role'] == 'assistant' and m.get('tool_calls') for tc in m['tool_calls']]
    diag = r['privileged_call_diagnostics']
    for d in diag:
        cand = [tc for tc in prop if tc['function'] == d['function']]
        if not cand: continue
        tc = cand[min(len(cand)-1, sum(1 for x in diag[:diag.index(d)] if x['function'] == d['function']))]
        T = words(tc['args'])
        if len(T) < 2: continue
        rec.append({'ctx': r['context'], 'task': f"{r['suite']}/{r['user_task']}", 'blocked': bool(d.get('blocked')), 'route': d.get('route'),
                    'inspected': d.get('inspected_before_execution'), 'user_share': sum(t in U for t in T)/len(T)})
out = {'privileged_calls_scored': len(rec), 'blocked': sum(x['blocked'] for x in rec), 'routes': dict(collections.Counter(x['route'] for x in rec))}
for ctx in ('CLEAN', 'ALIGNED', 'CONFLICT', 'ALL'):
    r = [x for x in rec if ctx == 'ALL' or x['ctx'] == ctx]
    b = [x['user_share'] for x in r if x['blocked']]; a = [x['user_share'] for x in r if not x['blocked']]
    bins = {}
    for lo, hi in ((0, .1), (.1, .3), (.3, .5), (.5, .7), (.7, 1.01)):
        s = [x for x in r if lo <= x['user_share'] < hi]; bins[f'{lo:.1f}-{min(hi,1):.1f}'] = f"{sum(x['blocked'] for x in s)}/{len(s)}"
    out[ctx] = {'n': len(r), 'blocked': len(b), 'AUC_low_user_share_predicts_block': round(auc(a, b), 3) if auc(a, b) is not None else None, 'blocked_by_user_share_bin': bins}
pt = collections.defaultdict(lambda: [0, 0, 0.0])
for x in rec:
    pt[x['task']][0] += x['blocked']; pt[x['task']][1] += 1; pt[x['task']][2] += x['user_share']
out['per_task_blocked/n/mean_user_share'] = {k: f"{v[0]}/{v[1]} share {v[2]/v[1]:.2f}" for k, v in sorted(pt.items())}
json.dump(out, open(Path(__file__).with_name('copy_law_attriguard.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
