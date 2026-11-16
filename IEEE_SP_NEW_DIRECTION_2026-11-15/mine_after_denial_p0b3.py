#!/usr/bin/env python3
"""What happens in an episode AFTER the guard has removed a call?  August study 07 (both runs).
Reuses only the raw records and the predicate-based attacker-call test from the 14 Nov audit
(imported, not copied).  Read-only.  Output -> after_denial_p0b3.json"""
import json, sys, collections, warnings, logging
from pathlib import Path
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
sys.path.insert(0, '/home/tahad/IEEE_SP/IEEE_SP_2027/IEEE_SP_AUGUST_AUDIT_2026-11-14')
import audit_p0b3 as A
out = {}
for tag, d in A.RUNS.items():
    rows = {json.loads(l)['episode_id']: json.loads(l) for l in open(d/'P0B3_SCIENCE_ROWS.jsonl')}
    evs = [json.loads(l) for l in open(d/'P0B3_DEFENSE_EVENTS.jsonl')]
    by = collections.defaultdict(list)
    for e in evs: by[e['episode_id']].append(e)
    seqs = {}
    for eid, es in by.items():
        if not eid.startswith('attack:'): continue
        _, suite, ut, inj = eid.split(':'); es.sort(key=lambda e: e['decision_index']); s = []
        for e in es:
            if e['intervened']:
                P = [A.parse(c) for c in e['original_proposal']['tool_calls']]; E = [A.parse(c) for c in e['regenerated_proposal']['tool_calls']]
                aP = any(A.is_attacker(suite, ut, inj, c) for c in P); aE = any(A.is_attacker(suite, ut, inj, c) for c in E)
                s.append({(1,0):'R',(1,1):'K',(0,1):'I',(0,0):'u'}[(int(aP),int(aE))] if True else None)   # R removed, K kept, u = user-side action intervened
                if s[-1] == 'u': s[-1] = 'd' if (P and not E) else ('c' if [json.dumps(x, sort_keys=True) for x in P] != [json.dumps(x, sort_keys=True) for x in E] else 's')  # d dropped, c changed, s same
            else:
                P = [A.parse(a['action']) for a in e['actions']]
                s.append('X' if any(A.is_attacker(suite, ut, inj, c) for c in P) else 'n')                   # X attacker call executed unflagged, n not flagged user action
        seqs[eid] = ''.join(s)
    # attacker proposals per episode and outcome
    n_prop = collections.Counter(); succ_by = collections.defaultdict(lambda: [0, 0])
    first_R = 0; reprop_after_R = 0; succ_after_R = 0; succ_first = 0; exec_after_R = 0
    for eid, s in seqs.items():
        k = sum(ch in 'RKX' for ch in s); n_prop[k] += 1
        ok = rows[eid]['attack_success'] is True
        succ_by[min(k, 3)][0] += ok; succ_by[min(k, 3)][1] += 1
        if 'R' in s:
            i = s.index('R'); prior_exec = any(ch in 'KX' for ch in s[:i])
            if not prior_exec:
                first_R += 1; tail = s[i+1:]
                if any(ch in 'RKX' for ch in tail): reprop_after_R += 1
                if any(ch in 'KX' for ch in tail): exec_after_R += 1
                if any(ch in 'KX' for ch in tail) and ok: succ_after_R += 1
    # what the removal does to the USER's task in that episode
    util_R = [rows[e]['utility'] for e, s in seqs.items() if 'R' in s and not any(ch in 'KX' for ch in s)]
    util_none = [rows[e]['utility'] for e, s in seqs.items() if not any(ch in 'RKX' for ch in s)]
    # audited-route successes: on the first attacker proposal, or on a later one?
    aud = []
    for eid, s in seqs.items():
        if rows[eid]['attack_success'] is True and any(ch in 'KX' for ch in s):
            j = min(s.index(ch) for ch in 'KX' if ch in s); aud.append({'episode': eid, 'sequence': s, 'attacker_proposals_before_the_executed_one': sum(ch == 'R' for ch in s[:j])})
    out[tag] = {'attacked_episodes_with_events': len(seqs), 'episodes_by_number_of_attacker_proposals': dict(sorted(n_prop.items())),
        'attack_success_by_number_of_attacker_proposals(3=3+)': {k: f'{v[0]}/{v[1]}' for k, v in sorted(succ_by.items())},
        'episodes_whose_first_attacker_proposal_was_removed': first_R,
        'of_those_agent_proposed_an_attacker_call_again': reprop_after_R, 'of_those_an_attacker_call_later_executed': exec_after_R,
        'of_those_attack_succeeded_after_removal': succ_after_R,
        'user_task_utility_when_all_attacker_proposals_removed': f'{sum(u is True for u in util_R)}/{len(util_R)}',
        'user_task_utility_when_no_attacker_proposal_at_audited_decisions': f'{sum(u is True for u in util_none)}/{len(util_none)}',
        'audited_route_successes': aud, 'example_sequences': collections.Counter(seqs.values()).most_common(14)}
json.dump(out, open(Path(__file__).with_name('after_denial_p0b3.json'), 'w'), indent=1)
for t in out:
    print('#####', t)
    for k, v in out[t].items():
        if k != 'audited_route_successes': print('  ', k, ':', v)
    for a in out[t]['audited_route_successes']: print('     ', a['episode'], a['sequence'], a['attacker_proposals_before_the_executed_one'])
