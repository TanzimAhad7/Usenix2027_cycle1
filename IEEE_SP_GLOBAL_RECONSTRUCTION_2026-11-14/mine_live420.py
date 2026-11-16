#!/usr/bin/env python3
"""Read-only: A/N/V/Z split of the rejected paper's 420-run live AttriGuard study
(agent gpt-4.1-mini, released AttriGuard code, 14 natural AgentDojo tasks x 3 contexts x ON/OFF x 5).
A = authorized protected effect realised (PAEF=1)
Z = the selected unauthorized (attacker) effect realised
V = some other state-changing privileged effect committed, PAEF=0, Z=0   (wrong effect, not the attacker's)
N = no state-changing call committed                                    (safe failure)
Output -> live420_anv.json"""
import json, collections, random
from pathlib import Path
P = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/research_basis/studies/08_live_end_to_end/frozen_results/scientific_v1/RUN_ROWS.jsonl')
rows = [json.loads(l) for l in open(P)]
def cls(r):
    c = r['PAEF_components']
    if r['Z'] == 1: return 'Z'
    if r['PAEF'] == 1: return 'A'
    if c['successful_state_changing_call_count'] == 0: return 'N'
    return 'V'
tab = collections.defaultdict(collections.Counter); per = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for r in rows:
    k = (r['context'], r['defense']); tab[k][cls(r)] += 1; per[r['case_id']][k][cls(r)] += 1
out = {'cells': {f'{k[0]}/{k[1]}': dict(v) for k, v in sorted(tab.items())}}
# paired task-level ON-OFF differences with task bootstrap
random.seed(20261114); cases = sorted(per)
def diff(ctx, c, cs):
    return sum(per[x][(ctx,'ON')][c] - per[x][(ctx,'OFF')][c] for x in cs) / (5*len(cs))
out['on_minus_off'] = {}
for ctx in ('CLEAN','ALIGNED','CONFLICT'):
    for c in 'ANVZ':
        d = diff(ctx, c, cases)
        bs = sorted(diff(ctx, c, [random.choice(cases) for _ in cases]) for _ in range(10000))
        out['on_minus_off'][f'{ctx}:{c}'] = [round(d,4), round(bs[250],4), round(bs[9750],4)]
# what are the V rows?
V = [r for r in rows if cls(r) == 'V']
out['V_rows'] = [{'case': r['case_id'], 'task': f"{r['suite']}/{r['user_task']}", 'ctx': r['context'], 'def': r['defense'], 'utility': r['utility'],
                  'state_changing': r['PAEF_components']['successful_state_changing_call_count'],
                  'target_matching': r['PAEF_components']['target_matching_successful_call_count'],
                  'calls': [(c['function'], c['args']) for c in r['successful_calls'] if c['function'] not in ('read_file',)][:6],
                  'blocked': [d['function'] for d in r['privileged_call_diagnostics'] if d.get('blocked')]} for r in V]
out['V_by_cell'] = dict(collections.Counter(f"{r['context']}/{r['defense']}" for r in V))
out['V_by_task'] = dict(collections.Counter(f"{r['suite']}/{r['user_task']}" for r in V))
out['utility_true_but_not_A'] = dict(collections.Counter((cls(r), r['context'], r['defense']) .__str__() for r in rows if r['utility']==1 and cls(r)!='A'))
json.dump(out, open(Path(__file__).with_name('live420_anv.json'), 'w'), indent=1, default=str)
print(json.dumps(out['cells'], indent=1)); print(json.dumps(out['on_minus_off'], indent=1))
print(out['V_by_cell']); print(out['V_by_task']); print(out['utility_true_but_not_A'])
for v in out['V_rows'][:40]: print(v['task'], v['ctx'], v['def'], 'util', v['utility'], 'sc', v['state_changing'], 'tm', v['target_matching'], 'blocked', v['blocked'], json.dumps(v['calls'])[:330])
