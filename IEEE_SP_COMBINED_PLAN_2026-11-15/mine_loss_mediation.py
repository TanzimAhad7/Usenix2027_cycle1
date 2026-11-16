#!/usr/bin/env python3
"""Two cross-run facts for the combined plan, from raw rows only (read-only):
 (1) Bridge, 8 Nov (108 authored cases, guard arm, no attacker, tool-supplied identifier):
     wrong-commit rate by WHICH authorized values the sanitizer kept.
 (2) Replay study from the rejected paper's artifact (natural AgentDojo decisions, full information):
     how often a regenerated privileged call binds each kind of argument correctly.
Output -> loss_mediation.json"""
import csv, json, collections
from pathlib import Path
csv.field_size_limit(10**9)
X = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/artifact_extracts'); out = {'bridge': {}, 'replay_full_information': {}}
wrong = lambda r: 'out_of_contract' in r['commit_classes'] or 'forbidden' in r['commit_classes']
for tag, f in (('gemma', 'bridge_E13_gemma_episodes.csv'), ('qwen', 'bridge_E14_qwen_episodes.csv')):
    R = [r for r in csv.DictReader(open(X/f)) if r['attack'] == '0' and r['flex'] == '0' and r['source'] == '1']
    pl = [r for r in R if r['arm'] == 'plain']; sc = [r for r in R if r['arm'] == 'scalar']; au = [r for r in R if r['arm'] == 'authority']
    t = collections.defaultdict(lambda: [0, 0])
    for r in sc:
        i, p = r['identifier_retained'], r['parameter_retained']
        k = 'not_sanitized' if i == '' else ('both_kept' if (i, p) == ('1', '1') else 'identifier_lost_only' if (i, p) == ('0', '1') else 'parameter_lost_only' if (i, p) == ('1', '0') else 'both_lost')
        t[k][0] += wrong(r); t[k][1] += 1
    lost = [t[k] for k in ('identifier_lost_only', 'parameter_lost_only', 'both_lost')]
    out['bridge'][tag] = {'no_guard_wrong': f'{sum(map(wrong, pl))}/{len(pl)}', 'guard_wrong': f'{sum(map(wrong, sc))}/{len(sc)}',
        'trusted_commit_check_wrong': f'{sum(map(wrong, au))}/{len(au)}',
        'guard_wrong_by_what_the_sanitizer_kept': {k: f'{v[0]}/{v[1]}' for k, v in sorted(t.items())},
        'any_authorized_value_lost': f'{sum(v[0] for v in lost)}/{sum(v[1] for v in lost)}'}
S9 = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/research_basis/studies/09_evaluation_replay')
for m in ('llama', 'gemma', 'qwen'):
    R = list(csv.DictReader(open(S9/m/'P2B_CI_ARGUMENT_SLOT_ROWS.csv'))); t = collections.defaultdict(lambda: [0, 0])
    for r in R: t[r['argument_class']][0] += r['exact_json_match'] == 'True'; t[r['argument_class']][1] += 1
    out['replay_full_information'][m] = {k: f'{v[0]}/{v[1]} exact' for k, v in sorted(t.items())}
json.dump(out, open(Path(__file__).with_name('loss_mediation.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
