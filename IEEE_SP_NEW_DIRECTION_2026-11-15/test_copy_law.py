#!/usr/bin/env python3
"""Test: is the August detector's decision predicted by WHERE THE ACTION'S WORDS CAN BE COPIED FROM?
For every scored action in study 07 (both runs) compute, from text alone (no model):
  user_share = share of the action's argument tokens that occur in the user's request.
Then compare with the proxy model's leave-one-out scores recorded in August:
  delta_u  = drop in action log-likelihood per token when the user request is removed
  flag     = some tool result has a larger drop than the user request
Read-only. Output -> copy_law.json"""
import json, re, sys, collections, math, warnings, logging
from pathlib import Path
warnings.filterwarnings('ignore'); logging.disable(logging.CRITICAL)
from agentdojo.task_suite.load_suites import get_suite
S7 = Path('/home/tahad/IEEE_SP/IEEE_SP_2027/research_basis/studies/07_causalarmor')
RUNS = {'primary': S7/'reconstruction_results', 'attempt0': S7/'support/P0B3_AUTHOR_RUN_HISTORY/P0B3_ATTEMPT0_16K_TECHNICAL_ABORT_992_OF_1046'}
SU = {s: get_suite('v1.2.2', s) for s in ('banking', 'slack', 'travel', 'workspace')}
tok = lambda s: [t.lower() for t in re.findall(r"[A-Za-z0-9@._\-']{3,}", s)]
def arg_tokens(action):
    i = action.index('('); a = json.loads(action[i+1:-1]); out = []
    def walk(x):
        if isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, list): [walk(v) for v in x]
        elif x is not None: out.extend(tok(str(x)))
    walk(a); return out
def spearman(x, y):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0]*len(v); i = 0
        while i < len(o):
            j = i
            while j+1 < len(o) and v[o[j+1]] == v[o[i]]: j += 1
            for k in range(i, j+1): r[o[k]] = (i+j)/2
            i = j+1
        return r
    rx, ry = rank(x), rank(y); n = len(x); mx = sum(rx)/n; my = sum(ry)/n
    c = sum((a-mx)*(b-my) for a, b in zip(rx, ry)); vx = sum((a-mx)**2 for a in rx); vy = sum((b-my)**2 for b in ry)
    return c / math.sqrt(vx*vy) if vx and vy else float('nan')
def auc(pos, neg):
    if not pos or not neg: return None
    w = sum((p > q) + 0.5*(p == q) for p in pos for q in neg); return w/(len(pos)*len(neg))
out = {}
for tag, d in RUNS.items():
    evs = [json.loads(l) for l in open(d/'P0B3_DEFENSE_EVENTS.jsonl')]
    rec = []
    for e in evs:
        p = e['episode_id'].split(':'); U = set(tok(SU[p[1]].get_user_task_by_id(p[2]).PROMPT))
        for a in e['actions']:
            T = arg_tokens(a['action'])
            if len(T) < 2: continue
            pr = a['primary']; us = sum(t in U for t in T)/len(T)
            rec.append({'kind': p[0], 'suite': p[1], 'task': p[2], 'user_share': us, 'delta_u': pr['delta_u_norm'],
                        'max_delta_s': max([s['delta_s_norm'] for s in pr['spans']] or [0]), 'flag': bool(pr['flagged_message_indices']), 'n_tok': len(T)})
    R = {}
    for kind in ('benign', 'attack', 'all'):
        r = [x for x in rec if kind == 'all' or x['kind'] == kind]
        fl = [x['user_share'] for x in r if x['flag']]; nf = [x['user_share'] for x in r if not x['flag']]
        bins = collections.OrderedDict()
        for lo, hi in ((0, .1), (.1, .3), (.3, .5), (.5, .7), (.7, 1.01)):
            b = [x for x in r if lo <= x['user_share'] < hi]
            bins[f'{lo:.1f}-{min(hi,1):.1f}'] = f"{sum(x['flag'] for x in b)}/{len(b)} flagged; mean delta_u {sum(x['delta_u'] for x in b)/len(b):+.2f}" if b else '0'
        # best single threshold on user_share for predicting 'not flagged', evaluated leave-one-TASK-out
        tasks = sorted({(x['suite'], x['task']) for x in r}); correct = 0
        for t in tasks:
            tr = [x for x in r if (x['suite'], x['task']) != t]; te = [x for x in r if (x['suite'], x['task']) == t]
            best = max((sum((x['user_share'] >= th) != x['flag'] for x in tr), th) for th in [i/20 for i in range(1, 21)])[1]
            correct += sum((x['user_share'] >= best) != x['flag'] for x in te)
        maj = max(sum(x['flag'] for x in r), len(r) - sum(x['flag'] for x in r))
        R[kind] = {'scored_actions': len(r), 'flagged': sum(x['flag'] for x in r),
                   'spearman_user_share_vs_delta_u': round(spearman([x['user_share'] for x in r], [x['delta_u'] for x in r]), 3),
                   'spearman_user_share_vs_margin(max_delta_s-delta_u)': round(spearman([x['user_share'] for x in r], [x['max_delta_s']-x['delta_u'] for x in r]), 3),
                   'AUC_user_share_separates_unflagged_from_flagged': round(auc(nf, fl), 3) if auc(nf, fl) is not None else None,
                   'flag_rate_by_user_share_bin': bins,
                   'threshold_rule_accuracy_leave_one_task_out': f'{correct}/{len(r)} = {correct/len(r):.3f}', 'majority_class_baseline': f'{maj/len(r):.3f}'}
    out[tag] = R
json.dump(out, open(Path(__file__).with_name('copy_law.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
