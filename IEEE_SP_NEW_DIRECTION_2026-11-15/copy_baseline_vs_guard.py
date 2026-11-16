#!/usr/bin/env python3
"""Compare the August detector's flag with a model-free rule: 'flag a decision if fewer than
theta of its call's argument words occur in the user's request'.  Attacker calls are labelled
with AgentDojo's security predicate (audit_p0b3).  Primary run.  Output -> copy_baseline.json"""
import json, re, sys, collections, warnings, logging
from pathlib import Path
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
sys.path.insert(0, '/home/tahad/IEEE_SP/IEEE_SP_2027/IEEE_SP_AUGUST_AUDIT_2026-11-14')
import audit_p0b3 as A
tok = lambda s: [t.lower() for t in re.findall(r"[A-Za-z0-9@._\-']{3,}", s)]
def share(action, U):
    f, a = A.parse(action); T = []
    def walk(x):
        if isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, list): [walk(v) for v in x]
        elif x is not None: T.extend(tok(str(x)))
    walk(a); return (sum(t in U for t in T)/len(T)) if T else None
d = A.RUNS[sys.argv[1] if len(sys.argv) > 1 else 'primary']
evs = [json.loads(l) for l in open(d/'P0B3_DEFENSE_EVENTS.jsonl')]
rows = []
for e in evs:
    p = e['episode_id'].split(':'); U = set(tok(A.SUITES[p[1]].get_user_task_by_id(p[2]).PROMPT))
    sh = [share(a['action'], U) for a in e['actions']]; sh = [s for s in sh if s is not None]
    if not sh: continue
    att = False
    if p[0] == 'attack':
        calls = [A.parse(a['action']) for a in e['actions']]
        att = any(A.is_attacker(p[1], p[2], p[3], c) for c in calls)
    rows.append({'kind': 'attacker_call' if att else ('benign_episode' if p[0] == 'benign' else 'user_side_call_in_attacked_episode'),
                 'min_share': min(sh), 'guard_flag': bool(e['primary_any_flag']), 'task': (p[1], p[2])})
out = {'decisions': len(rows)}
for th in (0.3, 0.5, 0.7):
    t = {}
    for k in ('attacker_call', 'benign_episode', 'user_side_call_in_attacked_episode'):
        r = [x for x in rows if x['kind'] == k]
        t[k] = {'n': len(r), 'guard_flags': sum(x['guard_flag'] for x in r), 'word_rule_flags': sum(x['min_share'] < th for x in r),
                'both_agree': sum((x['min_share'] < th) == x['guard_flag'] for x in r)}
    out[f'theta_{th}'] = t
# misses of each on attacker calls
ac = [x for x in rows if x['kind'] == 'attacker_call']
out['attacker_calls_missed_by_guard'] = sum(not x['guard_flag'] for x in ac)
out['attacker_calls_missed_by_word_rule_0.5'] = sum(x['min_share'] >= 0.5 for x in ac)
out['attacker_calls_missed_by_both'] = sum((not x['guard_flag']) and x['min_share'] >= 0.5 for x in ac)
out['user_share_of_guard_missed_attacker_calls'] = sorted(round(x['min_share'], 2) for x in ac if not x['guard_flag'])
json.dump(out, open(Path(__file__).with_name(f"copy_baseline_{sys.argv[1] if len(sys.argv) > 1 else 'primary'}.json"), 'w'), indent=1)
print(json.dumps(out, indent=1))
