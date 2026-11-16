"""Complete denominators and treatment-independent contrasts; no paper verdict."""
from __future__ import annotations

import collections
import csv
import json
from pathlib import Path

from .util import read, write


def compact(result):
    return {key: value for key, value in result.items()
            if key not in ('native_clone_arms', 'effects', 'violations', 'reference_calls', 'source_decisions')}


def analyze(out, manifest):
    out = Path(out)
    rows = []
    summary = {}
    permission_pairs = []
    evidence_pairs = []
    location_pairs = []
    workflow_pairs = []
    for family in manifest['profiles']:
        folder = out / family
        profile_rows = []
        for panel in ('E1', 'E2', 'E3'):
            planned = (manifest[panel] if panel != 'E3' else
                       [item for block in manifest['E3_blocks'] for item in block])
            census = read(folder / 'census.json') if (folder / 'census.json').is_file() else {}
            for item in planned:
                path = folder / panel / item['id'] / 'result.json'
                if path.is_file():
                    result = read(path)
                else:
                    result = dict(id=item['id'], profile=family, panel=panel, attempted=False,
                                  status=census.get(item['id'], 'NOT_EXECUTED'), qualified=False)
                row = compact(result)
                row['result_path'] = str(path.relative_to(out)) if path.is_file() else None
                row['panel'] = panel
                if panel == 'E3':
                    row.update(root_id=item['spec']['id'], carrier=item['spec']['carrier_condition'],
                               policy=item['policy'], structure=item['spec']['structure'],
                               family=item['spec']['family'], wording=item['spec']['wording'])
                rows.append(row)
                profile_rows.append(row)
        by_panel = {}
        for panel in ('E1', 'E2', 'E3'):
            subset = [r for r in profile_rows if r['panel'] == panel]
            value = dict(planned=len(subset), attempted=sum(r.get('attempted', False) for r in subset),
                         qualified=sum(bool(r.get('qualified')) for r in subset),
                         statuses=dict(collections.Counter(r['status'] for r in subset)),
                         generation_records=sum(r.get('generation_records', 0) for r in subset),
                         http_attempts=sum(r.get('http_attempts', 0) for r in subset))
            if panel == 'E1':
                strata = collections.defaultdict(list)
                for r in subset:
                    if 'permission' in r:
                        strata[(r['permission'], r['fact_location'], r['view'])].append(r)
                value['acceptance_strata'] = [dict(permission=k[0], fact_location=k[1], view=k[2],
                    observed=len(v), qualified=sum(bool(r['qualified']) for r in v),
                    source_acceptances=sum(bool(r.get('allowed')) for r in v),
                    qualified_source_acceptances=sum(bool(r.get('allowed')) and r['qualified'] for r in v))
                    for k, v in sorted(strata.items())]
                indexed = {r['id']: r for r in subset}
                for item in manifest['E1']:
                    original = indexed[item['id']]
                    if item['view'] == 'SOURCE':
                        for treatment in ('EVIDENCE', 'PLACEBO'):
                            changed_id = item['id'].replace('_SOURCE_', '_' + treatment + '_')
                            if changed_id in indexed:
                                changed = indexed[changed_id]
                                qualified_pair = bool(original['qualified'] and changed['qualified'])
                                evidence_pairs.append(dict(profile=family, source_id=original['id'],
                                    treatment_id=changed_id, treatment=treatment, both_qualified=qualified_pair,
                                    acceptance_change=int(changed['allowed']) - int(original['allowed']) if qualified_pair else None))
                    if item['fact_location'] == 'ROOT':
                        changed_id = item['id'].replace('_ROOT_', '_DESIGNATED_')
                        if changed_id in indexed:
                            changed = indexed[changed_id]
                            qualified_pair = bool(original['qualified'] and changed['qualified'])
                            location_pairs.append(dict(profile=family, root_id=original['id'], designated_id=changed_id,
                                both_qualified=qualified_pair,
                                acceptance_change=int(changed['allowed']) - int(original['allowed']) if qualified_pair else None))
                    if item['permission'] != 'FORBID':
                        continue
                    no = indexed[item['id']]
                    allowed_id = item['id'].replace('_FORBID_', '_ALLOW_')
                    if allowed_id not in indexed:
                        continue  # Engineering subsets may omit the other arm.
                    yes = indexed[allowed_id]
                    good = bool(no.get('qualified') and yes.get('qualified'))
                    permission_pairs.append(dict(profile=family, forbidden_id=no['id'], allowed_id=yes['id'],
                         both_qualified=good, permission_response=int(yes['allowed']) - int(no['allowed']) if good else None,
                         family=item['spec']['family'], dimension=item['dimension'],
                         fact_location=item['fact_location'], view=item['view'], draw=item['draw']))
            elif panel == 'E3':
                value.update(observed_violating_workflows=sum(bool(r.get('violation')) for r in subset),
                             observed_secure_completions=sum(r.get('outcome') == 'SECURE_COMPLETION' and r['qualified'] for r in subset),
                             unqualified=sum(not r.get('qualified', False) for r in subset))
                index = {(r['root_id'], r['policy'], r['carrier']): r for r in subset}
                for root_id, policy in sorted({(r['root_id'], r['policy']) for r in subset}):
                    neutral = index[root_id, policy, 'NEUTRAL']
                    for target in ('RECIPIENT', 'PARAMETER'):
                        hostile = index[root_id, policy, target]
                        for measure in ('targets_total', 'targets_after_exposure'):
                            a = neutral.get(measure, {}).get(target)
                            b = hostile.get(measure, {}).get(target)
                            workflow_pairs.append(dict(profile=family, root_id=root_id, policy=policy,
                                target=target, measure=measure, neutral_id=neutral['id'], hostile_id=hostile['id'],
                                neutral_observed=a, hostile_observed=b,
                                observed_difference=b-a if a is not None and b is not None else None,
                                both_qualified=bool(neutral['qualified'] and hostile['qualified']),
                                scope='Finite-panel descriptive contrast. Total effects primary; post-exposure is a conditional diagnostic.'))
            else:
                details = []
                for row in subset:
                    if row.get('result_path'):
                        r = read(out / row['result_path'])
                        details.append(dict(id=r['id'], origin=r.get('origin'), view=r.get('view'),
                            qualified=r['qualified'], reference_final_prefix_illegal=r.get('reference_proposal_oracle', {}).get('violation'),
                            reference_added_unmatched_proposals=r.get('reference_added_unmatched_proposals'),
                            prefix_already_illegal=r.get('prefix_oracle', {}).get('violation'),
                            source_new_effect_count=len(r.get('native_clone_arms', {}).get('SOURCE_ADMISSION', {}).get('new_effects', [])),
                            source_final_violation=r.get('native_clone_arms', {}).get('SOURCE_ADMISSION', {}).get('oracle', {}).get('violation'),
                            source_new_unmatched_effects=r.get('native_clone_arms', {}).get('SOURCE_ADMISSION', {}).get('new_unmatched_effect_count'),
                            routes=[d['route'] for d in r.get('source_decisions', [])]))
                value['reference_admission_details'] = details
            by_panel[panel] = value
        summary[family] = by_panel
    analysis = out / 'analysis'
    write(analysis / 'SUMMARY.json', dict(profiles=summary, mock=any(r.get('mock') for r in rows),
        interpretation='No automatic mechanism, generality, attack-rate or IEEE S&P-readiness conclusion. '
                       'Keep attempted denominators, missing results, and technical qualification distinct.'))
    write(analysis / 'ALL_PLANNED_RECORDS.json', rows)
    write(analysis / 'PERMISSION_CONTRASTS.json', permission_pairs)
    write(analysis / 'EVIDENCE_VIEW_CONTRASTS.json', evidence_pairs)
    write(analysis / 'FACT_LOCATION_CONTRASTS.json', location_pairs)
    write(analysis / 'COMMON_TARGET_CONTRASTS.json', workflow_pairs)
    scalar_fields = ['profile', 'panel', 'id', 'status', 'attempted', 'qualified', 'outcome', 'family',
                     'permission', 'fact_location', 'view', 'allowed', 'policy', 'carrier', 'structure',
                     'wording', 'violation', 'physical_goal', 'reporting_completion', 'protocol_completion',
                     'elapsed_seconds', 'generation_records', 'http_attempts', 'result_path']
    analysis.mkdir(exist_ok=True)
    with (analysis / 'ALL_PLANNED_RECORDS.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=scalar_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    total = len(rows)
    recorded = sum(bool(r.get('result_path')) for r in rows)
    qualified = sum(bool(r.get('qualified')) for r in rows)
    text = ('# Permission-admission campaign findings\n\n'
            f'Planned records: {total}. Recorded results: {recorded}. Qualified: {qualified}.\n\n'
            + ('**Engineering mock run: zero scientific model inference.**\n\n' if any(r.get('mock') for r in rows) else '')
            + 'These counts are not interchangeable episodes: E1 is a fixed-judge test, E2 is a fixed-reference test '
            'with conditional downstream matching, and E3 contains complete autonomous workflows.\n\n'
            'Read SUMMARY.json, PERMISSION_CONTRASTS.json and COMMON_TARGET_CONTRASTS.json alongside raw requests, '
            'native states, source decisions and errors. Post-exposure target effects alone do not establish attacker causation. '
            'Interleaved total-effect contrasts address that question at the finite authored-panel scope.\n\n'
            'E1 tests permission response and source/evidence sensitivity. E2 tests reference legality at archived inputs '
            'and fixed-dispatch consequences. E3 tests autonomous reachability and hostile/neutral differences. '
            'No result automatically establishes novelty or a common causal mechanism.\n')
    (analysis / 'FINDINGS.md').write_text(text)
    return dict(planned=total, recorded=recorded, qualified=qualified)

