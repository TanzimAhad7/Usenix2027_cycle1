"""N2 analysis (CPU, read-only on result.json files). Writes RUN/analysis.json and RUN/report.txt.

Per profile and arm: outcome classes of the target argument, with counts over EXPOSED episodes only
(a removal arm whose agent never received a result containing the value did not receive the treatment).
Paired contrast: for each unit and draw, removal arm minus INTACT on WRONG_COMMIT (any wrong committed value),
with a 95% bootstrap interval over TASKS (units within a task are not independent).
"""
from __future__ import annotations
import json, random, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

ARMS = ('INTACT', 'SILENT', 'PLACEHOLDER', 'ERROR')
OK = ('COMPLETE', 'ITERATION_LIMIT')


def load(run, profile):
    rows = []
    for p in sorted((run / profile / 'episodes').glob('*/result.json')):
        rows.append(json.loads(p.read_text()))
    return rows


def boot(per_task, n=4000, seed=7):
    keys = sorted(per_task)
    if not keys:
        return None
    rng = random.Random(seed)
    means = [statistics.mean(v for k in (rng.choice(keys) for _ in keys) for v in per_task[k]) for _ in range(n)]
    means.sort()
    point = statistics.mean(v for k in keys for v in per_task[k])
    return dict(mean=round(point, 3), ci95=[round(means[int(.025 * n)], 3), round(means[int(.975 * n) - 1], 3)],
                tasks=len(keys), pairs=sum(len(v) for v in per_task.values()))


def analyze_profile(rows, design):
    units = {u['unit']: u for u in design['units']}
    tech = Counter(r.get('status') for r in rows)
    valid = [r for r in rows if r.get('status') in OK]
    intact = {(r['suite'], r['task'], r['draw']): r for r in valid if r['arm'] == 'INTACT'}
    out = dict(episodes=len(rows), status=dict(tech), arms={})
    for arm in ARMS[1:]:
        sel = [r for r in valid if r['arm'] == arm]
        exp = [r for r in sel if r.get('exposed')]
        out['arms'][arm] = dict(n=len(sel), exposed=len(exp), not_exposed=len(sel) - len(exp),
                                target_class=dict(Counter(r['target_class'] for r in exp)),
                                asks_user_heuristic=sum(r['asks_user_heuristic'] for r in exp),
                                reports_missing_heuristic=sum(r['reports_missing_heuristic'] for r in exp),
                                utility=sum(bool(r.get('utility')) for r in exp))
    # INTACT, scored against each unit of its task (same episode reused for every unit of that task)
    out['intact'] = dict(n=sum(r['arm'] == 'INTACT' for r in valid), utility=sum(bool(r.get('utility')) for r in valid if r['arm'] == 'INTACT'),
                         unit_class=dict(Counter(c for r in valid if r['arm'] == 'INTACT' for c in r['unit_class'].values())))
    # intact target classes need re-scoring per unit: done from stored target calls is not possible for other units,
    # so the paired contrast uses utility and the INTACT run's own target calls via re-classification below.
    contrasts = {}
    for arm in ARMS[1:]:
        for endpoint in ('wrong_commit', 'authorized_commit', 'utility'):
            per = defaultdict(list)
            for r in valid:
                if r['arm'] != arm or not r.get('exposed'):
                    continue
                b = intact.get((r['suite'], r['task'], r['draw']))
                if not b:
                    continue
                def val(x, intact_row=False):
                    if endpoint == 'utility':
                        return int(bool(x.get('utility')))
                    cls = x['unit_class'][r['unit']]
                    if endpoint == 'wrong_commit':
                        return int(str(cls).startswith('WRONG_COMMIT'))
                    return int(cls == 'AUTHORIZED_COMMIT')
                per[f"{r['suite']}.{r['task']}"].append(val(r) - val(b, True))
            contrasts[f'{arm}-INTACT|{endpoint}'] = boot(per)
    out['contrasts'] = contrasts
    return out


def main(run):
    run = Path(run)
    design = json.loads((Path(__file__).resolve().parent.parent / 'inputs' / 'design.json').read_text())
    result, lines = dict(design_sha256=design['design_sha256']), []
    for profile in ('qwen', 'gemma'):
        if not (run / profile / 'episodes').is_dir():
            continue
        a = analyze_profile(load(run, profile), design)
        result[profile] = a
        lines.append(f'== {profile}: {a["episodes"]} episodes; status {a["status"]}')
        lines.append(f'   INTACT: {a["intact"]["n"]} runs, utility {a["intact"]["utility"]}, unit classes {a["intact"]["unit_class"]}')
        for arm, v in a['arms'].items():
            lines.append(f'   {arm:11s} n={v["n"]} exposed={v["exposed"]} classes={v["target_class"]} '
                         f'asks={v["asks_user_heuristic"]} reports_missing={v["reports_missing_heuristic"]} utility={v["utility"]}')
        for k, v in a['contrasts'].items():
            lines.append(f'   {k:36s} {v}')
    (run / 'analysis.json').write_text(json.dumps(result, indent=1) + '\n')
    (run / 'report.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main(sys.argv[1])
