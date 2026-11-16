#!/usr/bin/env python3
"""Mine every stored AttriGuard judge record (raw reply, parsed verdict, the released code's fallback prediction) across all
runs. Read-only. Output -> mine_judge_records.json"""
import json, os, re, sys, collections, hashlib
ROOTS = ['results/user_runs', 'IEEE_SP_A01_GPU2/results/user_runs', 'IEEE_SP_E1_GPU3/results/user_runs', 'IEEE_SP_E2b_GPU2/results/user_runs',
         'IEEE_SP_J2_GPU2/results/user_runs', 'IEEE_SP_N1_GPU3/results/user_runs', 'IEEE_SP_R3_GPU2/results/user_runs']
recs, seen, files = [], set(), 0
def walk(o, path, meta):
    if isinstance(o, dict):
        if 'raw' in o and ('reported_survive' in o or 'source_fallback_prediction' in o or 'envelope' in o):
            key = hashlib.sha1((path + json.dumps(o, sort_keys=True, default=str)[:400]).encode()).hexdigest()
            if key not in seen:
                seen.add(key); recs.append(dict(meta, raw=o.get('raw'), envelope=o.get('envelope'), parsed=o.get('parsed'),
                                               reported=o.get('reported_survive'), fallback=o.get('source_fallback_prediction'),
                                               finish=o.get('finish_reason'), interpretable=o.get('interpretable')))
        for k, v in o.items(): walk(v, path + '/' + str(k), meta)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + f'[{i}]', meta)
for root in ROOTS:
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('source', 'model_io', '.venv', '__pycache__')]
        for f in fn:
            if f != 'result.json': continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 30_000_000: continue
                txt = open(p).read()
                if 'judge_diagnostics' not in txt and 'source_fallback_prediction' not in txt: continue
                d = json.loads(txt)
            except Exception: continue
            files += 1
            run = p.split('user_runs/')[1].split('/')[0]
            prof = 'gemma' if '/gemma' in p else 'qwen' if '/qwen' in p else d.get('profile') if isinstance(d, dict) else None
            walk(d, p, dict(run=run, profile=prof, file=p))
print('files with judge records', files, 'records', len(recs))
json.dump(recs, open('EUROSP_2027_PLAN/analysis/mine_judge_records.json', 'w'), default=str)
C = collections.Counter
print('by run family x profile', sorted(C((re.sub(r'_2026.*', '', r['run']), r['profile']) for r in recs).items()))
print('envelope x profile', sorted(C((r['profile'], r['envelope']) for r in recs).items(), key=lambda x: -x[1])[:20])
dis = [r for r in recs if r['reported'] is not None and r['fallback'] is not None and r['reported'] != r['fallback']]
print('parsed verdict != released-code fallback prediction:', len(dis), 'of', sum(r['reported'] is not None and r['fallback'] is not None for r in recs))
print(' direction', C((r['profile'], r['reported'], r['fallback']) for r in dis))
for r in dis[:6]: print('  ', r['profile'], r['run'][:40], repr(r['raw'])[:420])
