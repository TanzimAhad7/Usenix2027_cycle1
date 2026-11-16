#!/usr/bin/env python3
"""CPU census: in the benchmark's OWN reference solutions, how much of each state-changing call's arguments
is stated in the user's request, and how much has to come from tool results?
For every AgentDojo user task (v1 and v1.2.2), take ground_truth(default environment); for every call to a
state-changing tool compute user_share = share of argument words (same tokenizer as test_copy_law.py) found
in the user's PROMPT. Model-free, read-only. Output -> census_ground_truth.json
State-changing = tool name does not start with a read prefix. The list of tool names per class is written out
so the split can be checked by eye."""
import json, re, collections, warnings, logging
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
from agentdojo.task_suite.load_suites import get_suite
tok = lambda s: [t.lower() for t in re.findall(r"[A-Za-z0-9@._\-']{3,}", s)]
READ = ('get_', 'read_', 'search_', 'check_', 'list_', 'find_')
def arg_tokens(args):
    out = []
    def walk(x):
        if isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, (list, tuple)): [walk(v) for v in x]
        elif x is not None: out.extend(tok(str(x)))
    walk(args); return out
res = {}
for ver in ('v1', 'v1.2.2'):
    rows, names = [], collections.Counter()
    for sname in ('banking', 'slack', 'travel', 'workspace'):
        suite = get_suite(ver, sname)
        for tid, task in suite.user_tasks.items():
            env = suite.load_and_inject_default_environment({})
            try: gt = task.ground_truth(env)
            except Exception as e:
                rows.append({'suite': sname, 'task': tid, 'error': repr(e)[:80]}); continue
            U = set(tok(task.PROMPT)); writes = []
            for c in gt:
                state = not c.function.startswith(READ); names[(c.function, state)] += 1
                if not state: continue
                T = arg_tokens(dict(c.args))
                writes.append({'function': c.function, 'n_tok': len(T),
                               'user_share': (sum(t in U for t in T) / len(T)) if T else None})
            rows.append({'suite': sname, 'task': tid, 'n_calls': len(gt), 'writes': writes})
    W = [w | {'suite': r['suite'], 'task': r['task']} for r in rows for w in r.get('writes', []) if w['user_share'] is not None and w['n_tok'] >= 2]
    bins = collections.OrderedDict()
    for lo, hi in ((0, .1), (.1, .3), (.3, .5), (.5, .7), (.7, 1.01)):
        bins[f'{lo:.1f}-{min(hi, 1):.1f}'] = sum(lo <= w['user_share'] < hi for w in W)
    tasks_with_write = [r for r in rows if r.get('writes')]
    def task_min(r):
        v = [w['user_share'] for w in r['writes'] if w['user_share'] is not None and w['n_tok'] >= 2]
        return min(v) if v else None
    tm = [(r['suite'], r['task'], task_min(r)) for r in tasks_with_write if task_min(r) is not None]
    by_suite = collections.OrderedDict()
    for s in ('banking', 'slack', 'travel', 'workspace'):
        ws = [w for w in W if w['suite'] == s]
        by_suite[s] = {'state_changing_calls': len(ws), 'below_0.5': sum(w['user_share'] < .5 for w in ws),
                       'below_0.7': sum(w['user_share'] < .7 for w in ws)}
    res[ver] = {'user_tasks': len(rows), 'errors': sum('error' in r for r in rows),
                'tasks_with_state_changing_call': len(tasks_with_write),
                'state_changing_calls_scored': len(W), 'bins_user_share': bins,
                'calls_below_0.5': sum(w['user_share'] < .5 for w in W), 'calls_below_0.7': sum(w['user_share'] < .7 for w in W),
                'tasks_whose_least_stated_write_is_below_0.5': sum(m < .5 for *_, m in tm),
                'tasks_whose_least_stated_write_is_below_0.7': sum(m < .7 for *_, m in tm),
                'tasks_scored': len(tm), 'by_suite': by_suite,
                'tool_names_state_changing': sorted(n for (n, s) in names if s),
                'tool_names_read': sorted(n for (n, s) in names if not s), 'rows': rows}
json.dump(res, open('census_ground_truth.json', 'w'), indent=1)
for ver, r in res.items():
    print(ver, {k: v for k, v in r.items() if k not in ('rows', 'tool_names_state_changing', 'tool_names_read')})
print('STATE-CHANGING:', res['v1']['tool_names_state_changing']); print('READ:', res['v1']['tool_names_read'])
