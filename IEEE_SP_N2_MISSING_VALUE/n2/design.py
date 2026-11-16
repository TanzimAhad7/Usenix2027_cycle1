"""N2 design: conditions built from the frozen S0 natural population (CPU, deterministic).

Unit = one delegated value (suite, task, function, key, value) from S0's `tasks[].delegated`.
Arms per unit: SILENT, PLACEHOLDER, ERROR. Per task: INTACT (shared by all of the task's units).
Draws: one greedy draw (temperature 0) and SAMPLED_DRAWS sampled draws (temperature 0.7, top_p 0.95).
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S0_INPUTS = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/IEEE_SP_S0_SANITIZER_FIDELITY/inputs/s0_inputs.json')
S0_SHA256 = None  # recorded at build time, checked at run time
VALUE_ARMS = ('SILENT', 'PLACEHOLDER', 'ERROR')
SAMPLED_DRAWS = 4
DRAWS = [dict(draw=0, temperature=0.0, top_p=1.0, seed=20261115)] + [
    dict(draw=i, temperature=0.7, top_p=0.95, seed=20261115 + i) for i in range(1, SAMPLED_DRAWS + 1)]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build():
    s0 = json.loads(S0_INPUTS.read_text())
    # The frozen S0 population is the 45 items (29 tasks); `tasks` also lists the 5 tasks S0 excluded.
    in_population = {(it['suite'], it['task'], v['key'], v['value']) for it in s0['items'] for v in it['carried_values']}
    units, seen = [], set()
    for t in s0['tasks']:
        for d in t['delegated']:
            key = (t['suite'], t['task'], d['key'], d['value'])
            if key in seen or key not in in_population:
                continue
            seen.add(key)
            forms = sorted({*d['forms']['exact'], *d['forms']['equivalent']}, key=lambda f: (-len(f), f))
            units.append(dict(unit=f"{t['suite']}.{t['task']}.{d['key']}.{len(units):02d}", suite=t['suite'], task=t['task'],
                              prompt=t['prompt'], function=d['function'], key=d['key'], value=d['value'], forms=forms,
                              n_sources=len(d['sources'])))
    # All reference-solution values of each unit's (function, key) in its task: a committed value equal to one of
    # them is a legitimate value for ANOTHER part of the task, not a wrong value.
    from agentdojo.task_suite.load_suites import get_suite
    for u in units:
        suite = get_suite('v1', u['suite']); task = suite.get_user_task_by_id(u['task'])
        env = task.init_environment(suite.load_and_inject_default_environment({}))
        vals = []
        for c in task.ground_truth(env):
            if c.function == u['function'] and u['key'] in c.args:
                v = c.args[u['key']]
                vals += [str(x) for x in (v if isinstance(v, (list, tuple)) else [v])]
        u['gt_values'] = sorted(set(vals))
    tasks = sorted({(u['suite'], u['task']) for u in units})
    episodes = []
    for draw in DRAWS:
        for suite, task in tasks:
            episodes.append(dict(id=f"{suite}.{task}.INTACT.d{draw['draw']}", suite=suite, task=task, arm='INTACT',
                                 unit=None, **draw))
        for u in units:
            for arm in VALUE_ARMS:
                episodes.append(dict(id=f"{u['unit']}.{arm}.d{draw['draw']}", suite=u['suite'], task=u['task'], arm=arm,
                                     unit=u['unit'], **draw))
    design = dict(protocol='N2_MISSING_VALUE_V1', s0_inputs=str(S0_INPUTS), s0_inputs_sha256=sha(S0_INPUTS),
                  agentdojo_suite_version='v1', units=units, tasks=[f'{s}.{t}' for s, t in tasks],
                  arms=['INTACT', *VALUE_ARMS], draws=DRAWS, episodes=episodes,
                  counts=dict(units=len(units), tasks=len(tasks), episodes_per_profile=len(episodes)))
    design['design_sha256'] = hashlib.sha256(json.dumps(design, sort_keys=True).encode()).hexdigest()
    return design


if __name__ == '__main__':
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'inputs' / 'design.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    d = build()
    out.write_text(json.dumps(d, indent=1) + '\n')
    print(json.dumps(d['counts']), d['design_sha256'])
