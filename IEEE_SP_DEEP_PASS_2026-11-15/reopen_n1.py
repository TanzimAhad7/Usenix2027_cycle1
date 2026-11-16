#!/usr/bin/env python3
"""Reopen the AttriGuard reference study (N1, 2 Nov) at row level.
Question: when a reference is labelled unlawful, HOW does it differ from the lawful alternatives?
Classes: punctuation/whitespace/case only; free-text field differs in wording; an identity or numeric
field differs (a real value substitution); different function or extra call.
Read-only.  Output -> reopen_n1.json"""
import json, glob, os, re, collections
from pathlib import Path
R = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/IEEE_SP_N1_GPU3/results/user_runs/n1_gpu3_20261102T002508Z_229688_30263')
TEXT = {'body', 'subject', 'content', 'description', 'message', 'title'}
def soft(v): return re.sub(r'[\W_]+', ' ', json.dumps(v, sort_keys=True).lower()).strip()
def calls(x):
    out = []
    def walk(y):
        if isinstance(y, dict):
            if 'function' in y and isinstance(y.get('args'), dict): out.append((y['function'], y['args']))
            for v in y.values(): walk(v)
        elif isinstance(y, list):
            for v in y: walk(v)
    walk(x); return out
def classify(ref, alts):
    """ref: (function, args); alts: list of (function, args) lawful alternatives across all slots."""
    best = None
    for f, a in alts:
        if f != ref[0]: continue
        diff = [k for k in sorted(set(a) | set(ref[1])) if json.dumps(a.get(k), sort_keys=True) != json.dumps(ref[1].get(k), sort_keys=True)]
        if not diff: return 'exact_match'
        softdiff = [k for k in diff if soft(a.get(k)) != soft(ref[1].get(k))]
        if not softdiff: c = 'punctuation_or_case_only'
        elif all(k in TEXT for k in softdiff): c = 'free_text_wording_differs'
        else: c = 'identity_or_numeric_field_differs:' + ','.join(k for k in softdiff if k not in TEXT)
        rank = {'punctuation_or_case_only': 0, 'free_text_wording_differs': 1}.get(c, 2)
        if best is None or rank < best[0]: best = (rank, c)
    return best[1] if best else 'function_not_among_lawful_alternatives'
out = {}; examples = []
for prof in ('gemma', 'qwen'):
    tab = collections.defaultdict(collections.Counter)
    for d in sorted(glob.glob(str(R/prof/'P1'/'N1_*'))):
        try:
            res = json.load(open(d + '/result.json')); held = json.load(open(d + '/held_input.json'))
        except Exception: continue
        if 'views' not in res: tab[(res.get('directive'), 'NO_VIEWS')][str(res.get('status'))] += 1; continue
        alts = [(alt['function'], alt['args']) for s in held['facts'].get('slots', []) for alt in s.get('alternatives', [])]
        views = res['views'].items() if isinstance(res['views'], dict) else [(v.get('view'), v) for v in res['views']]
        for name, rec in views:
            if not rec.get('qualified'): tab[(res['directive'], name)]['unqualified'] += 1; continue
            if rec.get('reference_no_effectful_call'): tab[(res['directive'], name)]['no_effectful_call'] += 1; continue
            if not rec.get('reference_unmatched_new'): tab[(res['directive'], name)]['lawful'] += 1; continue
            # unlawful: find the reference calls and classify the worst-matching effectful one
            cs = [c for c in calls(rec) if any(c[0] == f for f, _ in alts) or c[0].startswith(('send_', 'schedule_', 'post_', 'create_', 'update_', 'add_', 'invite_'))]
            cl = [classify(c, alts) for c in cs] or ['no_call_found_in_record']
            bad = [c for c in cl if c != 'exact_match'] or cl
            key = sorted(bad, key=lambda z: 0 if z.startswith('identity') else 1 if z.startswith('function') else 2)[0]
            tab[(res['directive'], name)]['UNLAWFUL:' + key.split(':')[0]] += 1
            if len(examples) < 14 and name == 'SOURCE':
                ref = [c for c, k in zip(cs, cl) if k != 'exact_match'][:1]
                examples.append({'profile': prof, 'id': os.path.basename(d), 'class': key, 'reference': ref, 'lawful_alternatives': alts[:2]})
    out[prof] = {f'{k[0]}|{k[1]}': dict(v) for k, v in sorted(tab.items())}
out['examples'] = examples
json.dump(out, open(Path(__file__).with_name('reopen_n1.json'), 'w'), indent=1)
for p in ('gemma', 'qwen'):
    print('###', p)
    for k, v in out[p].items(): print('  ', k, v)
for e in examples: print(e['profile'], e['id'], e['class'], '\n    ref :', json.dumps(e['reference'])[:260], '\n    law :', json.dumps(e['lawful_alternatives'])[:260])
