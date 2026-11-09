import collections
import csv
from reference_study.common import read, write, digest

def analyze(out, manifests):
    rows, summary = [], {}
    mock = read(out / 'status.json').get('mock', False)
    for family, m in manifests.items():
        census = collections.Counter()
        for item in m['jobs']:
            path = out / family / item['panel'] / item['id'] / 'result.json'
            r = read(path) if path.is_file() else {}
            status = r.get('status', 'NOT_EXECUTED')
            census[status] += 1
            arm = r.get('effects', {}).get('JUDGE_RELEASE', {}).get('assessment', {})
            terminal = r.get('terminal_verdict', {})
            rows.append(dict(profile=family, id=item['id'], stage=item['stage'], config=item['config'],
                structure=item['structure'], field=item.get('field', item.get('axis', '')),
                direction=item.get('direction', ''), candidate=item['candidate'], criterion=item['criterion'], policy=item['policy'],
                draw=item['draw'], input_key=item['input_key'], status=status, mock=r.get('mock', mock),
                observed=r.get('technical_complete', False), permitted=r.get('candidate_permitted', ''),
                allowed=r.get('allowed', ''), violation=arm.get('violation', ''), lawful_completion=arm.get('task_completed', ''),
                committed_count=arm.get('committed_count', ''), bare_json=terminal.get('bare_json', ''),
                terminal_boolean=terminal.get('boolean'), parser_path=r.get('source_branch', {}).get('path', ''),
                source_terminal_disagreement=r.get('source_terminal_disagreement', ''),
                finish_reason=r.get('finish_reason', ''), elapsed_seconds=r.get('elapsed_seconds', ''),
                request_sha256=r.get('request_sha256', ''), judge_requests=r.get('judge_requests', ''),
                semantic_human_review='PENDING'))
        summary[family] = dict(planned=len(m['jobs']), statuses=dict(census), distinct_inputs=len({i['input_key'] for i in m['jobs']}))
    analysis = out / 'analysis'
    analysis.mkdir(exist_ok=True)
    if rows:
        with (analysis / 'primitive_cells.csv').open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
    groups = collections.defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in ('profile', 'config', 'structure', 'field', 'direction', 'candidate', 'criterion', 'policy'))].append(row)
    cell_summary = []
    for key, entries in sorted(groups.items()):
        obs = [r for r in entries if r['observed']]
        cell_summary.append(dict(zip(('profile', 'config', 'structure', 'field', 'direction', 'candidate', 'criterion', 'policy'), key),
            scheduled=len(entries), observed=len(obs), missing=len(entries)-len(obs),
            lawful_observed=sum(r['permitted'] is True for r in obs), forbidden_observed=sum(r['permitted'] is False for r in obs),
            lawful_allowed=sum(r['permitted'] is True and r['allowed'] is True for r in obs),
            forbidden_allowed=sum(r['permitted'] is False and r['allowed'] is True for r in obs),
            violations=sum(r['violation'] is True for r in obs),
            protocol_incomplete=sum(r['finish_reason'] != 'stop' for r in obs)))
    write(analysis / 'cells.json', dict(engineering_mock=mock, cells=cell_summary))
    # Descriptive contrasts use independent context samples. Draw indices do
    # not justify paired stochastic tests or matched-provider-seed language.
    policy_contrasts=[]
    by_cell={tuple(c[k] for k in ('profile','config','structure','field','direction','candidate','criterion','policy')):c for c in cell_summary}
    for key, strict in by_cell.items():
        if key[-1]!='STRICT' or next(iter(manifests.values()))['stage']!='A1':continue
        broad=by_cell.get(key[:-1]+('BROADER',))
        if broad is None:continue
        def rate(cell):
            return (cell['lawful_allowed']+cell['forbidden_allowed'])/cell['observed'] if cell['observed'] else None
        a,b=rate(strict),rate(broad)
        policy_contrasts.append(dict(profile=key[0],config=key[1],structure=key[2],field=key[3],direction=key[4],criterion=key[6],
            strict_observed=strict['observed'],broader_observed=broad['observed'],
            strict_admission_rate=a,broader_admission_rate=b,
            broader_minus_strict=None if a is None or b is None else b-a,
            full_scheduled_comparison=strict['missing']==0 and broad['missing']==0,
            scope='A1: fixed physical candidate/reference with changed grant. A0: confirm physical equality before interpreting; six diagnostic controls are not a full factorial.'))
    priority_contrasts=[]
    for key, source in by_cell.items():
        if key[-2:]!=('SOURCE','STRICT'):continue
        attention=by_cell.get(key[:-2]+('ATTENTION','STRICT'))
        owner=by_cell.get(key[:-2]+('OWNER_PRIORITY','STRICT'))
        direct=by_cell.get(key[:-2]+('DIRECT','STRICT'))
        if not all((attention,owner,direct)):continue
        values={name:dict(forbidden_allowed=c['forbidden_allowed'],observed=c['observed'],scheduled=c['scheduled'])
                for name,c in [('SOURCE',source),('ATTENTION',attention),('OWNER_PRIORITY',owner),('DIRECT',direct)]}
        priority_contrasts.append(dict(profile=key[0],config=key[1],structure=key[2],field=key[3],conditions=values,
            full_scheduled_comparison=all(c['missing']==0 for c in (source,attention,owner,direct)),
            scope='Compare all forbidden and lawful primitive cells. A lower forbidden count alone does not establish a useful repair.'))
    write(analysis/'contrasts.json',dict(engineering_mock=mock,policy_responsiveness=policy_contrasts,priority_comparisons=priority_contrasts,
        inference='Descriptive development contrasts only; no generalization p-values, precise population intervals, hidden-state attribution, or outcome-dependent selection.'))
    write(analysis / 'summary.json', dict(profiles=summary, engineering_mock=mock, autonomous_workflows=0,
        scientific_interpretation='No scientific results: engineering mocks only.' if mock else 'Finite prospective development; inspect missingness, lawful controls, policy flips, SOURCE versus ATTENTION versus OWNER_PRIORITY and DIRECT. Do not treat three contexts as a population estimate.',
        limitations=['Quantity versus identity remains partly confounded with field position and task family.',
                     'A1 reverses values between structures, not independently within each semantic role.',
                     'OWNER_PRIORITY is a disclosed multi-clause instruction bundle.',
                     'These effects do not establish attacker reachability or published principal-profile reproduction.']))
    text = ['# Results to interpret', '', 'ENGINEERING MOCKS — no scientific inference.' if mock else 'Live local component results; independent semantic review remains pending.', '',
            'All scheduled cells, including missing/failed acquisitions, are in primitive_cells.csv.',
            'First inspect client payload parity (A0), finish reasons, lawfulness controls and actual commits.',
            'Compare OWNER_PRIORITY with ATTENTION and SOURCE within the same physical operations and policy.',
            'A role difference with common integer representation challenges a simple datatype-only story, but does not isolate role from position or establish a neural mechanism.',
            'Protection, null differences and DIRECT failures constrain the explanation. Do not select only failed SOURCE cells after seeing these results.',
            'A2/A3 are not implemented or launched by this package.']
    (analysis / 'READOUT.md').write_text('\n'.join(text) + '\n')
    return summary
