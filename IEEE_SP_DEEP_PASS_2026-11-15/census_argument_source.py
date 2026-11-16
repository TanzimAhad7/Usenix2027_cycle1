#!/usr/bin/env python3
"""CPU census, per ARGUMENT: replay each AgentDojo reference solution in the default environment and, for every
argument of every state-changing call, record where its value can be found:
  user    = the value string occurs in the user's request
  tool    = not in the request, but occurs in a tool result returned EARLIER in the same reference solution
  neither = in neither (composed or computed by the agent, or a default)
Free-text fields (body, content, subject, description) are reported separately from the other fields.
Model-free, read-only. Output -> census_argument_source.json"""
import json, collections, warnings, logging
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
from agentdojo.task_suite.load_suites import get_suite
from agentdojo.functions_runtime import FunctionsRuntime
READ = ('get_', 'read_', 'search_', 'check_', 'list_', 'find_')
TEXT = {'body', 'content', 'subject', 'description'}
def forms(v):
    if isinstance(v, bool): return [str(v).lower()]
    if isinstance(v, float): return list({repr(v), str(int(v)) if v == int(v) else repr(v), f'{v:.2f}'})
    return [str(v).strip().lower()]
def leaves(v):
    if isinstance(v, dict): return [x for y in v.values() for x in leaves(y)]
    if isinstance(v, (list, tuple)): return [x for y in v for x in leaves(y)]
    return [] if v is None or v == '' else [v]
res = {}
for ver in ('v1', 'v1.2.2'):
    A, per_task = [], {}
    for sname in ('banking', 'slack', 'travel', 'workspace'):
        suite = get_suite(ver, sname); rt = FunctionsRuntime(suite.tools)
        for tid, task in suite.user_tasks.items():
            env = suite.load_and_inject_default_environment({})
            prompt = task.PROMPT.lower(); seen = ''; rows = []
            for c in task.ground_truth(env):
                args = dict(c.args)
                if not c.function.startswith(READ):
                    for k, v in args.items():
                        for leaf in leaves(v):
                            f = forms(leaf)
                            src = 'user' if any(x in prompt for x in f) else 'tool' if any(x in seen for x in f) else 'neither'
                            rows.append({'suite': sname, 'task': tid, 'function': c.function, 'field': k,
                                         'free_text': k in TEXT, 'source': src, 'value': str(leaf)[:60]})
                try:
                    out, err = rt.run_function(env, c.function, args)
                    seen += ' ' + str(out).lower() + ' ' + str(err or '').lower()
                except Exception as e:
                    seen += ''
            A += rows; per_task[(sname, tid)] = rows
    ident = [a for a in A if not a['free_text']]; text = [a for a in A if a['free_text']]
    cnt = lambda rows: dict(collections.Counter(r['source'] for r in rows))
    tasks_w = {k: v for k, v in per_task.items() if v}
    t_tool = sum(any(r['source'] == 'tool' and not r['free_text'] for r in v) for v in tasks_w.values())
    t_all_user = sum(all(r['source'] == 'user' for r in v if not r['free_text']) for v in tasks_w.values())
    by_suite = {s: cnt([a for a in ident if a['suite'] == s]) for s in ('banking', 'slack', 'travel', 'workspace')}
    by_field = collections.defaultdict(collections.Counter)
    for a in ident: by_field[a['field']][a['source']] += 1
    res[ver] = {'user_tasks': len(per_task), 'tasks_with_state_changing_call': len(tasks_w),
                'non_text_argument_values': len(ident), 'non_text_by_source': cnt(ident),
                'free_text_argument_values': len(text), 'free_text_by_source': cnt(text),
                'tasks_with_a_tool_supplied_non_text_value': t_tool,
                'tasks_where_every_non_text_value_is_in_the_request': t_all_user,
                'non_text_by_suite': by_suite, 'non_text_by_field': {k: dict(v) for k, v in sorted(by_field.items())},
                'tool_supplied_tasks': sorted(f'{s}:{t}' for (s, t), v in tasks_w.items() if any(r['source'] == 'tool' and not r['free_text'] for r in v)),
                'neither_examples': [a for a in ident if a['source'] == 'neither'][:40], 'rows': A}
json.dump(res, open('census_argument_source.json', 'w'), indent=1)
for ver, r in res.items():
    print(ver, json.dumps({k: v for k, v in r.items() if k not in ('rows', 'neither_examples', 'tool_supplied_tasks')}))
print(len(res['v1']['tool_supplied_tasks']), res['v1']['tool_supplied_tasks'])
for a in res['v1']['neither_examples'][:25]: print('  neither:', a['suite'], a['task'], a['function'], a['field'], repr(a['value']))
