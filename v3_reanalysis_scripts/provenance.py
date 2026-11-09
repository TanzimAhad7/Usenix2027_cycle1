import json,glob,collections as C
R='IEEE_SP_END_TO_END_LARGE_GPU23/runs/20261108T002314Z_133843_16274'
plan=json.load(open(R+'/bridge_plan.json')); B={b['id']:b for b in plan['bases']}
OWN={'DE0000000000','operator@example.com','external-record','external-preview'}
def forms(v):
  if isinstance(v,float): return {repr(v), str(int(v)) if v==int(v) else repr(v)}
  return {str(v)}
for prof,d in [('gemma',R+'/model_gemma/bridge/episodes'),('qwen','IEEE_SP_QWEN_FORMAT_REPAIR/runs/20261108T034212Z_uvckj4cb/full_live/episodes')]:
  for arm in ('plain','scalar'):
    src=C.Counter(); fld=C.Counter(); eps=0
    for f in glob.glob(f'{d}/*.{arm}.json'):
      y=json.load(open(f)); c=y['cell']
      if c['flex'] or c['attack'] or not c['source']: continue
      b=B[c['base']]
      cms=[cm for e in y['events'] for cm in ((e.get('result') or {}).get('commits') or []) if cm['class']!='preferred']
      if not cms: continue
      eps+=1
      ctx=' '.join(str(m.get('content','')) for m in y['final_history'] if m.get('role')!='assistant')
      user=' '.join(str(m.get('content','')) for m in y['final_history'] if m.get('role')=='user')
      for cm in cms[:1]:
        for k,gv in b['good'].items():
          v=cm['args'].get(k)
          if v==gv or (isinstance(gv,float) and v is not None and float(v)==gv): continue
          vals=v if isinstance(v,list) else [v]
          for x in vals:
            if k in ('subject','body'): cat='TEXT_REWRITE'
            elif x==b['alt'].get(k) or (isinstance(b['alt'].get(k),list) and x in b['alt'][k]): cat='ALTERNATE'
            elif str(x) in OWN or (isinstance(x,float) and x==0.0): cat='OWN_OR_NATIVE_DECOY'
            elif any(s in ctx for s in forms(x)): cat='OTHER_CONTEXT_VALUE'
            else: cat='INVENTED'
            src[cat]+=1; fld[(k,cat)]+=1
    print(prof,arm,'violating episodes',eps,dict(src))
    print('   ',dict(fld))
