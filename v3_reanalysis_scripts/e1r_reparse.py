"""Read-only: recover E1R guarded regenerations censored by the <TOOL_CALL> parser regression.
Compares each recovered action with the frozen lawful first action. No simulator execution."""
import json,re,sys,collections
F='IEEE_SP_FINAL_EXPERIMENT_GPU3_SHARED_PREFILL/runs/20261108T232225Z_3654860_31695/qwen/E1R.jsonl'
rx=re.compile(r'<TOOL_CALL>\s*([A-Za-z_]+)\((\{.*\})\)\s*</TOOL_CALL>',re.S)
def norm(a): return {k:(float(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else v) for k,v in a.items()}
C=collections.Counter(); fields=collections.Counter(); fam=collections.Counter()
for line in open(F):
    r=json.loads(line); first=r['first']; fa=norm(first['args'])
    for arm,v in r['arms'].items():
        if v.get('status')!='regeneration_unparsed': continue
        raw=(v.get('regen') or {}).get('raw') or {}
        text=raw.get('text') if isinstance(raw,dict) else None
        m=rx.search(text or '')
        if not m: C[(arm,'unrecoverable')]+=1; continue
        try: args=norm(json.loads(m.group(2)))
        except Exception: C[(arm,'bad_json')]+=1; continue
        if m.group(1)!=first['function']: C[(arm,'other_function')]+=1; continue
        diff=[k for k in set(fa)|set(args) if fa.get(k)!=args.get(k)]
        if not diff: C[(arm,'same_as_lawful')]+=1
        else:
            C[(arm,'changed')]+=1; fam[(arm,r['family'])]+=1
            for k in diff: fields[(arm,k)]+=1
arms=sorted({a for a,_ in C})
for a in arms:
    tot=sum(v for (x,_),v in C.items() if x==a)
    print(f"{a:16s} n={tot:6d} " + ' '.join(f"{k}={C[(a,k)]}" for k in ('same_as_lawful','changed','other_function','bad_json','unrecoverable')))
print('changed fields (scalar):',{k:v for (a,k),v in fields.items() if a=='scalar'})
print('changed fields (force_same):',{k:v for (a,k),v in fields.items() if a=='force_same'})
print('changed by family:',dict(fam))
