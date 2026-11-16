#!/usr/bin/env python3
"""CPU census v2 (model-free, exploratory): the utility CEILING of grounding policies on AgentDojo v1 reference solutions.

For every argument value of every state-changing call in each user task's reference solution:
  kind      AUTHORITY (default) | TEMPORAL (date/time fields) | CONTROL (booleans) | TEXT (body/content/subject/description/title)
  source    REQUEST   value string occurs in the user's request
            TOOL      found in an earlier read result (first supplier recorded):
                        field    TYPED  = equals a whole leaf field (or list element) of the supplying record
                                 EMBED  = occurs inside a longer string field (free text)
                        selector NAMED  = a string argument of the supplying read call occurs in the request
                                 NOARG  = the read call has no string argument (whole collection)
                                 DERIVED= its string arguments are not in the request
                        exposure FIELD  = an attacker-controllable span is in the same field (or the value itself)
                                 RECORD = ... in another field of the same record
                                 RESULT = ... in another record of the same result
                                 NONE   = not in that result
            NEITHER   found nowhere (composed or computed by the agent)
A task PASSES a policy if every AUTHORITY value of its reference solution is admitted by the policy (tasks without a
state-changing call always pass). This is an upper bound on utility for any agent under that policy without asking the user.
"""
import json, re, collections, warnings, logging, sys
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
from agentdojo.task_suite.load_suites import get_suite
from agentdojo.functions_runtime import FunctionsRuntime
READ = ('get_', 'read_', 'search_', 'check_', 'list_', 'find_')
TEXT = {'body', 'content', 'subject', 'description', 'title'}
TEMPORAL = {'date', 'start_time', 'end_time', 'new_start_time', 'new_end_time', 'start_day', 'end_day', 'day', 'time'}
SPAN = re.compile(r'<<inj:([a-z0-9_]+)>>(.*?)<<end:\1>>', re.S | re.I)
strip = lambda s: SPAN.sub(lambda m: m.group(2), s)
def forms(v):
    if isinstance(v, bool): return [str(v).lower()]
    if isinstance(v, float): return list({repr(v), str(int(v)) if v == int(v) else repr(v), f'{v:.2f}'})
    return [str(v).strip().lower()]
def leaves(v):
    if isinstance(v, dict): return [x for y in v.values() for x in leaves(y)]
    if isinstance(v, (list, tuple)): return [x for y in v for x in leaves(y)]
    return [] if v is None or v == '' else [v]
def dump(o):
    if hasattr(o, 'model_dump'): return o.model_dump(mode='json')
    if isinstance(o, dict): return {str(k): dump(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [dump(x) for x in o]
    return o
def records(out):
    d = dump(out)
    return d if isinstance(d, list) and d else [d]
def fields(rec, path=''):
    """Yield (path, leaf) for every scalar leaf of a record."""
    if isinstance(rec, dict):
        for k, v in rec.items(): yield from fields(v, f'{path}.{k}' if path else str(k))
    elif isinstance(rec, (list, tuple)):
        for v in rec: yield from fields(v, path + '[]')
    elif rec is not None and rec != '': yield path, rec
def locate(rec, f_clean):
    """Where in the record is the value? Returns (TYPED|EMBED|None, field path, field has span)."""
    best = None
    for path, leaf in fields(rec):
        s = str(leaf).lower(); plain = strip(s).strip(); lf = [strip(x) for x in forms(leaf)] if not isinstance(leaf, str) else [plain]
        if any(x in lf for x in f_clean) or plain in f_clean:
            return 'TYPED', path, bool(SPAN.search(s))
        if any(x and x in plain for x in f_clean) and best is None:
            best = ('EMBED', path, bool(SPAN.search(s)))
    return best or (None, None, False)
rows, tasks = [], {}
for sname in ('banking', 'slack', 'travel', 'workspace'):
    suite = get_suite('v1', sname); rt = FunctionsRuntime(suite.tools)
    wrapped = {k: f'<<INJ:{k}>>{v}<<END:{k}>>' for k, v in suite.get_injection_vector_defaults().items()}
    for tid, task in suite.user_tasks.items():
        env = suite.load_and_inject_default_environment(wrapped); prompt = task.PROMPT.lower(); reads = []; trows = []
        gt = task.ground_truth(env)
        for c in gt:
            args = dict(c.args)
            if not c.function.startswith(READ):
                for k, v in args.items():
                    for leaf in leaves(v):
                        kind = 'TEXT' if k in TEXT else 'TEMPORAL' if k in TEMPORAL else 'CONTROL' if isinstance(leaf, bool) else 'AUTHORITY'
                        f_clean = [strip(x) for x in forms(leaf) if x]
                        row = dict(suite=sname, task=tid, function=c.function, field=k, value=strip(str(leaf))[:60], kind=kind,
                                   value_has_span=bool(SPAN.search(str(leaf))))
                        if any(x in prompt for x in f_clean): row['source'] = 'REQUEST'
                        else:
                            hit = None
                            for r in reads:
                                for ri, rec in enumerate(r['raw']):
                                    how, path, fspan = locate(rec, f_clean)
                                    if how and (hit is None or (how == 'TYPED' and hit[2] != 'TYPED')):
                                        hit = (r, ri, how, path, fspan)
                                if hit and hit[2] == 'TYPED': break
                            if hit is None: row['source'] = 'NEITHER'
                            else:
                                r, ri, how, path, fspan = hit
                                rec_span = bool(SPAN.search(json.dumps(r['raw'][ri], default=str)))
                                res_span = bool(SPAN.search(json.dumps(r['raw'], default=str)))
                                sargs = [a for a in leaves(r['args']) if isinstance(a, str)]
                                sel = 'NOARG' if not sargs else 'NAMED' if any(len(a) >= 3 and a.lower() in prompt for a in sargs) else 'DERIVED'
                                row.update(source='TOOL', how=how, supplier=r['function'], supplier_field=path, selector=sel,
                                           exposure='FIELD' if (fspan or row['value_has_span']) else 'RECORD' if rec_span else 'RESULT' if res_span else 'NONE',
                                           n_records=len(r['raw']))
                        trows.append(row)
            try: out, err = rt.run_function(env, c.function, args)
            except Exception as e: out = None
            if c.function.startswith(READ) and out is not None:
                reads.append(dict(function=c.function, args=dump(args), raw=records(out)))
        tasks[f'{sname}:{tid}'] = dict(state_changing=any(not c.function.startswith(READ) for c in gt), n_values=len(trows))
        rows += trows
A = [r for r in rows if r['kind'] == 'AUTHORITY']
C = collections.Counter
by_task = collections.defaultdict(list)
for r in A: by_task[f"{r['suite']}:{r['task']}"].append(r)
def admitted(r, policy):
    if r['source'] == 'REQUEST': return True
    if r['source'] == 'NEITHER': return policy == 'ALL'
    t, s = r['how'] == 'TYPED', r['selector']
    return {'R': False,
            'R+TYPED_NAMED': t and s == 'NAMED',
            'R+TYPED_NAMED_OR_NOARG': t and s in ('NAMED', 'NOARG'),
            'R+TYPED_ANY': t,
            'R+ANY_NAMED': s == 'NAMED',
            'R+ANY_NAMED_OR_NOARG': s in ('NAMED', 'NOARG'),
            'R+ANY_TOOL': True, 'ALL': True}[policy]
POL = ['R', 'R+TYPED_NAMED', 'R+TYPED_NAMED_OR_NOARG', 'R+TYPED_ANY', 'R+ANY_NAMED', 'R+ANY_NAMED_OR_NOARG', 'R+ANY_TOOL', 'ALL']
ceil = {}
for p in POL:
    ok = [t for t in tasks if all(admitted(r, p) for r in by_task.get(t, []))]
    adm = [r for r in A if r['source'] == 'TOOL' and admitted(r, p)]
    ceil[p] = dict(tasks_passing=len(ok), of=len(tasks), share=round(len(ok) / len(tasks), 3),
                   state_changing_passing=sum(tasks[t]['state_changing'] for t in ok),
                   by_suite={s: f"{sum(t.startswith(s) for t in ok)}/{sum(t.startswith(s) for t in tasks)}" for s in ('banking', 'slack', 'travel', 'workspace')},
                   tool_values_admitted=len(adm), admitted_exposure=dict(C(r['exposure'] for r in adm)))
summary = dict(all_values_by_kind=dict(C(r['kind'] for r in rows)), authority_by_source=dict(C(r['source'] for r in A)),
               tool_authority_how_x_selector={f'{a}|{b}': n for (a, b), n in sorted(C((r['how'], r['selector']) for r in A if r['source'] == 'TOOL').items())},
               tool_authority_exposure=dict(C(r['exposure'] for r in A if r['source'] == 'TOOL')),
               tool_authority_how_x_exposure={f'{a}|{b}': n for (a, b), n in sorted(C((r['how'], r['exposure']) for r in A if r['source'] == 'TOOL').items())},
               neither_authority_fields=dict(C(r['field'] for r in A if r['source'] == 'NEITHER')),
               ceilings=ceil)
json.dump(dict(summary=summary, rows=rows, tasks=tasks), open(sys.argv[1] if len(sys.argv) > 1 else 'census_grounding_ceiling.json', 'w'), indent=1, default=str)
print(json.dumps(summary, indent=1))
for r in A:
    if r['source'] == 'TOOL': print(f"  {r['suite']:9s} {r['task']:13s} {r['function']}.{r['field']}={r['value'][:26]!r:28s} <- {r['supplier']}.{r['supplier_field']} [{r['how']}; {r['selector']}; exposure {r['exposure']}]")
for r in A:
    if r['source'] == 'NEITHER': print(f"  NEITHER   {r['suite']:9s} {r['task']:13s} {r['function']}.{r['field']}={r['value'][:40]!r}")
