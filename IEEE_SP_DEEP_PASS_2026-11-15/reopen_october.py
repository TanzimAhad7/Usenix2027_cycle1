#!/usr/bin/env python3
"""Reopen, at row level, the October-November AttriGuard runs that the 15 Nov pass had not reopened.
Read-only. Output -> reopen_october.json.  Each block recomputes the table the 9 Nov register reported,
and classifies 'violations' by which fields differ from the nearest allowed action:
  text_only   = only subject/body/content/description differ (a wording mismatch under an exact-string contract)
  identity    = recipient / amount / channel / date / user / file etc. differ (a real wrong value)
  capacity    = matches an allowed action but the allowance was already used (an extra copy)"""
import json, csv, collections
from pathlib import Path
B = Path('/home/tahad/IEEE_SP/IEEE_SP_2027'); U = B/'results/user_runs'
TEXT = {'subject', 'body', 'content', 'description', 'message', 'title'}
out = {}
def vclass(v):
    if v.get('matches_original_but_capacity_unavailable'): return 'capacity'
    diffs = v.get('nearest_allowed_argument_differences') or []
    if not diffs: return 'no_allowed_action_of_this_kind'
    best = min(diffs, key=lambda d: (not set(d['changed_fields']) <= TEXT, len(d['changed_fields'])))
    return 'text_only' if set(best['changed_fields']) <= TEXT else 'identity:' + ','.join(sorted(set(best['changed_fields']) - TEXT))

# ---- 1. the 688-workflow campaign (344 per model)
camp = {}
for tag, p in (('qwen', U/'parallel_reference_gpu23_20261026T133503Z_1032615_10605/models/qwen/analysis/autonomous_ledger.json'),
               ('gemma', U/'gemma_recovery_20261027T015503Z_3488767_27655/analysis/autonomous_ledger.json')):
    L = json.load(open(p)); o = {'workflows': len(L), 'qualified': sum(bool(x.get('qualified')) for x in L)}
    t = collections.defaultdict(collections.Counter); vc = collections.defaultdict(collections.Counter); wf_real = collections.defaultdict(lambda: [0, 0])
    for x in L:
        t[x['policy']][x['outcome']] += 1
        kinds = [vclass(v).split(':')[0] for v in x['violations']]
        for k in kinds: vc[(x['carrier'], x['policy'])][k] += 1
        key = (x['carrier'], x['policy']); wf_real[key][1] += 1
        wf_real[key][0] += any(k in ('identity', 'capacity', 'no_allowed_action_of_this_kind') for k in kinds)
    o['outcome_by_policy'] = {k: dict(v) for k, v in sorted(t.items())}
    o['violation_records_by_carrier_policy_and_kind'] = {f'{k[0]}/{k[1]}': dict(v) for k, v in sorted(vc.items())}
    o['workflows_with_a_non_text_violation'] = {f'{k[0]}/{k[1]}': f'{v[0]}/{v[1]}' for k, v in sorted(wf_real.items())}
    o['workflows_whose_only_violations_are_text'] = sum(1 for x in L if x['violations'] and all(vclass(v) == 'text_only' for v in x['violations']))
    o['workflows_with_any_violation'] = sum(1 for x in L if x['violations'])
    camp[tag] = o
out['campaign_688'] = camp

# ---- 2. reference study, autonomous part (P3)
L = json.load(open(U/'reference_study_gpu2_20261031T010415Z_3263984_11556/analysis/P3_NATIVE_LEDGER.json'))
t = collections.defaultdict(collections.Counter)
for x in L:
    k = (x['profile'], x['carrier'], x['policy'])
    t[k]['n'] += 1; t[k]['qualified'] += bool(x['qualified']); t[k]['forbidden_after_exposure'] += (x.get('post_forbidden') or 0) > 0
    t[k]['violation'] += bool(x['violation']); t[k][x['outcome'] or x['status']] += 1
out['reference_study_P3'] = {'|'.join(k): dict(v) for k, v in sorted(t.items())}

# ---- 3. E1 owner-permission study
R = list(csv.DictReader(open(B/'IEEE_SP_E1_GPU3/results/user_runs/e1_gpu3_20261102T165724Z_3488373_18361/analysis/cells.csv')))
t = collections.defaultdict(lambda: [0, 0])
for r in R:
    k = (r['profile'], r['criterion'], r['policy'], r['candidate'], r['reference'], 'expected_' + r['expected_permission'])
    t[k][0] += r['operative_allowed'] == 'True'; t[k][1] += 1
out['E1'] = {'rows': len(R), 'strictly_qualified': sum(r['qualified'] == 'True' for r in R), 'accepted/n': {'|'.join(k): f'{v[0]}/{v[1]}' for k, v in sorted(t.items())}}

# ---- 4. E2b criterion study
L = json.load(open(B/'IEEE_SP_E2b_GPU2/results/user_runs/e2b_gpu2_20261103T154635Z_4024580_22095/analysis/logical_positions.json'))
t = collections.defaultdict(lambda: [0, 0])
for x in L:
    k = (x['profile'], x['criterion'], x['axis'], x['direction'], x['policy'], x['candidate'], x['reference'])
    t[k][0] += bool(x['operative_allowed']); t[k][1] += 1
out['E2b'] = {'rows': len(L), 'accepted/n': {'|'.join(map(str, k)): f'{v[0]}/{v[1]}' for k, v in sorted(t.items())}}

# ---- 5. A1
R = list(csv.DictReader(open(B/'IEEE_SP_A01_GPU2/results/user_runs/a01_A1_gpu2_20261104T151112Z_2439930_15034/analysis/primitive_cells.csv')))
t = collections.defaultdict(lambda: [0, 0, 0])
for r in R:
    k = (r['profile'], r['criterion'], r['policy'], r['field'], 'permitted_' + r['permitted'])
    t[k][0] += r['allowed'] == 'True'; t[k][1] += r['violation'] == 'True'; t[k][2] += 1
out['A1'] = {'rows': len(R), 'accepted,violations/n': {'|'.join(k): f'{v[0]},{v[1]}/{v[2]}' for k, v in sorted(t.items())}}

# ---- 6. J1
C = json.load(open('/home/tahad/IEEE_SP/IEEE_SP_J1_GPU2/results/user_runs/j1_r2_gpu2_20261104T230250Z_3925546_4052/analysis/cells.json'))['cells']
t = collections.defaultdict(lambda: [0, 0, 0, 0])
for c in C:
    if c['phase'] != 'MAIN': continue
    k = (c['profile'], c['criterion'], c['reference'])
    t[k][0] += c['validated_unauthorized_commits']; t[k][1] += c['forbidden_scheduled']; t[k][2] += c['validated_lawful_acceptance']; t[k][3] += c['lawful_scheduled']
out['J1'] = {'|'.join(k): f'forbidden admitted {v[0]}/{v[1]}; lawful accepted {v[2]}/{v[3]}' for k, v in sorted(t.items())}

# ---- 7. J2
P = json.load(open(B/'IEEE_SP_J2_GPU2/results/user_runs/j2_gpu2_20261105T045123Z_808555_2296/analysis/pattern_comparisons.json'))
out['J2'] = {x['profile']: sorted(((f.get('rule') or f.get('name')), f.get('matches') if 'matches' in f else f.get('fit'), f.get('n') or f.get('total')) for f in x['rule_fits'])[:8] for x in P['by_profile']}
out['J2_raw_first'] = P['by_profile'][0]['rule_fits'][:2]

# ---- 8. R3
S = json.load(open(B/'IEEE_SP_R3_GPU2/results/user_runs/r3_gpu2_20261106T183207Z_3487220_25309/SUMMARY.json'))
out['R3'] = [{k: g[k] for k in ('kind', 'setting', 'scheduled', 'attempted', 'qualified', 'observed_violating', 'target_after_exposure', 'lawful_effect_completion')} for g in S['groups']]
json.dump(out, open(Path(__file__).with_name('reopen_october.json'), 'w'), indent=1, default=str)

c = out['campaign_688']
for m in ('qwen', 'gemma'):
    print('### 688 campaign', m, c[m]['workflows'], 'qualified', c[m]['qualified']); print('  outcome', c[m]['outcome_by_policy'])
    print('  workflows with any violation', c[m]['workflows_with_any_violation'], '| only text mismatches', c[m]['workflows_whose_only_violations_are_text'])
    print('  non-text violation workflows by carrier/policy', c[m]['workflows_with_a_non_text_violation'])
    print('  violation records by kind', c[m]['violation_records_by_carrier_policy_and_kind'])
print('### P3'); [print('  ', k, v) for k, v in out['reference_study_P3'].items()]
print('### J1'); [print('  ', k, v) for k, v in out['J1'].items()]
print('### J2', json.dumps(out['J2_raw_first'])[:500])
print('### R3'); [print('  ', g) for g in out['R3']]
