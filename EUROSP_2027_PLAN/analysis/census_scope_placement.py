#!/usr/bin/env python3
"""CPU census (model-free, read-only, exploratory): where do AgentDojo's injection vectors sit relative to the
values that legitimate tasks take from tool results, and does the user's request name the source of those values?

For every user task (suite version v1) the reference solution is replayed in the default environment, with every
injection vector's DEFAULT text wrapped in markers (<<INJ:id>>default<<END:id>>), so the benign content is unchanged
but each attacker-controllable span is visible. For every non-text argument value of a state-changing call that is
not in the user's request but is found in an earlier tool result ("tool-only value", as in census_argument_source.py):

  placement (first that applies, strongest first)
    IN_VECTOR      the value lies inside an attacker-controllable span (the attack text replaces it)
    SAME_RECORD    a span is in the same record (list element / object) that supplies the value
    SAME_RESULT    a span is in the same tool result, in another record
    OTHER_RESULT   a span is only in another tool result read by the reference solution
    NONE           the reference solution reads no attacker-controllable span
  designation
    CALL_NAMED     a string argument of the read call that supplies the value occurs in the user's request
    RECORD_NAMED   a string field of the supplying record occurs in the user's request
    UNNAMED        neither

Output -> census_scope_placement.json
"""
import json, re, collections, warnings, logging, sys
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


def dump(o):
    if hasattr(o, 'model_dump'): return o.model_dump()
    if isinstance(o, dict): return {k: dump(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [dump(x) for x in o]
    return o


def records(out):
    """Split a tool result into records: list elements, else the whole object."""
    d = dump(out)
    if isinstance(d, list) and d: return d
    if isinstance(d, dict) and len(d) > 0 and all(isinstance(v, (dict, list)) for v in d.values()) and len(d) > 1:
        return [{k: v} for k, v in d.items()]
    return [d]


SPAN = re.compile(r'<<inj:([a-z0-9_]+)>>(.*?)<<end:\1>>', re.S)


def text(o): return json.dumps(o, default=str, ensure_ascii=False).lower() if not isinstance(o, str) else o.lower()


def strs(o):
    return [x for x in leaves(o) if isinstance(x, str)]


res = {}
for ver in ('v1',):
    rows, task_info = [], {}
    for sname in ('banking', 'slack', 'travel', 'workspace'):
        suite = get_suite(ver, sname); rt = FunctionsRuntime(suite.tools)
        defaults = suite.get_injection_vector_defaults()
        wrapped = {k: f'<<INJ:{k}>>{v}<<END:{k}>>' for k, v in defaults.items()}
        for tid, task in suite.user_tasks.items():
            env = suite.load_and_inject_default_environment(wrapped)
            prompt = task.PROMPT.lower()
            reads = []  # dicts: idx, function, args, recs (list of record texts), raw recs
            try:
                gt = task.ground_truth(env)
            except Exception as e:
                task_info[f'{sname}:{tid}'] = dict(error=str(e)[:200]); continue
            trows = []
            for ci, c in enumerate(gt):
                args = dict(c.args)
                if not c.function.startswith(READ):
                    for k, v in args.items():
                        if k in TEXT: continue
                        for leaf in leaves(v):
                            f = [x for x in forms(leaf) if x]
                            f_clean = [SPAN.sub(lambda m: m.group(2), x) for x in f]
                            if any(x in prompt for x in f_clean): continue  # in the request
                            # where is it supplied?
                            supply = []
                            for r in reads:
                                for ri, rec in enumerate(r['recs']):
                                    plain = SPAN.sub(lambda m: m.group(2), rec)
                                    if any(x in plain for x in f_clean): supply.append((r, ri))
                            if not supply: continue  # neither
                            r0, ri0 = supply[0]  # first result that supplies it
                            rec0 = r0['recs'][ri0]
                            in_vec = [m.group(1) for m in SPAN.finditer(rec0) if any(x in m.group(2) for x in f_clean)]
                            same_rec = [m.group(1) for m in SPAN.finditer(rec0)]
                            same_res = sorted({m.group(1) for rec in r0['recs'] for m in SPAN.finditer(rec)})
                            any_res = sorted({m.group(1) for r in reads for rec in r['recs'] for m in SPAN.finditer(rec)})
                            placement = ('IN_VECTOR' if in_vec else 'SAME_RECORD' if same_rec else 'SAME_RESULT' if same_res
                                         else 'OTHER_RESULT' if any_res else 'NONE')
                            call_named = [a for a in strs(r0['args']) if len(a) >= 3 and a.lower() in prompt]
                            rec_fields = [s for s in strs(r0['raw'][ri0]) if 4 <= len(s) <= 80 and '<<INJ' not in s
                                          and s.lower() not in f_clean and s.lower() in prompt]
                            designation = 'CALL_NAMED' if call_named else 'RECORD_NAMED' if rec_fields else 'UNNAMED'
                            trows.append(dict(suite=sname, task=tid, function=c.function, field=k, value=str(leaf)[:60],
                                              supplied_by=r0['function'], supplied_args=r0['args'], n_records=len(r0['recs']),
                                              n_supplying_results=len({id(s[0]) for s in supply}),
                                              placement=placement, vectors_in_value=in_vec, vectors_same_record=same_rec,
                                              vectors_same_result=same_res, designation=designation,
                                              named_by=(call_named or rec_fields)[:3]))
                try:
                    out, err = rt.run_function(env, c.function, args)
                except Exception as e:
                    out, err = None, str(e)
                if c.function.startswith(READ) and out is not None:
                    raw = records(out)
                    reads.append(dict(idx=ci, function=c.function, args=dump(args), raw=raw, recs=[text(x) for x in raw]))
            seen_vectors = sorted({m.group(1) for r in reads for rec in r['recs'] for m in SPAN.finditer(rec)})
            state_changing = [c.function for c in gt if not c.function.startswith(READ)]
            task_info[f'{sname}:{tid}'] = dict(state_changing=bool(state_changing), vectors_seen=seen_vectors,
                                               tool_only_values=len(trows), prompt=task.PROMPT)
            rows += trows
    C = collections.Counter
    by = lambda key: dict(C(r[key] for r in rows))
    cross = C((r['placement'], r['designation']) for r in rows)
    tasks = collections.defaultdict(list)
    for r in rows: tasks[(r['suite'], r['task'])].append(r)
    order = ['IN_VECTOR', 'SAME_RECORD', 'SAME_RESULT', 'OTHER_RESULT', 'NONE']
    task_worst = C(min((order.index(r['placement']) for r in v)) for v in tasks.values())
    res[ver] = dict(
        tool_only_values=len(rows), tasks_with_tool_only_value=len(tasks),
        placement=by('placement'), designation=by('designation'),
        placement_x_designation={f'{a}|{b}': n for (a, b), n in sorted(cross.items())},
        placement_by_suite={s: dict(C(r['placement'] for r in rows if r['suite'] == s)) for s in ('banking', 'slack', 'travel', 'workspace')},
        designation_by_suite={s: dict(C(r['designation'] for r in rows if r['suite'] == s)) for s in ('banking', 'slack', 'travel', 'workspace')},
        tasks_by_strongest_placement={order[i]: n for i, n in sorted(task_worst.items())},
        state_changing_tasks=sum(t.get('state_changing', False) for t in task_info.values()),
        state_changing_tasks_reading_a_vector=sum(bool(t.get('vectors_seen')) for t in task_info.values() if t.get('state_changing')),
        all_tasks=len(task_info), all_tasks_reading_a_vector=sum(bool(t.get('vectors_seen')) for t in task_info.values()),
        injection_vectors={s: len(get_suite(ver, s).get_injection_vector_defaults()) for s in ('banking', 'slack', 'travel', 'workspace')},
        rows=rows, tasks=task_info)
out = sys.argv[1] if len(sys.argv) > 1 else 'census_scope_placement.json'
json.dump(res, open(out, 'w'), indent=1, default=str)
for ver, r in res.items():
    print(ver, json.dumps({k: v for k, v in r.items() if k not in ('rows', 'tasks')}, indent=1))
    for x in r['rows']:
        print(f"  {x['suite']:9s} {x['task']:13s} {x['function']}.{x['field']}={x['value'][:28]!r:30s} <- {x['supplied_by']}({json.dumps(x['supplied_args'], default=str)[:50]}) "
              f"[{x['placement']}; {x['designation']}; recs={x['n_records']}]")
