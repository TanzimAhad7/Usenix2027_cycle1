import json,glob,collections as C,statistics as st,random,sys
R='IEEE_SP_END_TO_END_LARGE_GPU23/runs/20261108T002314Z_133843_16274'
plan=json.load(open(R+'/bridge_plan.json')); B={b['id']:b for b in plan['bases']}
def viol(y): return int(any(cm.get('class') in('other_out_of_contract','forbidden_alternate','duplicate') for e in y['events'] for cm in ((e.get('result') or {}).get('commits') or [])))
def lawful(y): 
  cs=[cm for e in y['events'] for cm in ((e.get('result') or {}).get('commits') or [])]
  return int(len(cs)>0 and all(c['class']=='preferred' for c in cs))
def fmt(v):
  if isinstance(v,float): return [repr(v), str(int(v)) if v==int(v) else repr(v), f'{v:.2f}']
  if isinstance(v,list): return [str(x) for x in v]
  return [str(v)]
for prof,d in [('gemma',R+'/model_gemma/bridge/episodes'),('qwen','IEEE_SP_QWEN_FORMAT_REPAIR/runs/20261108T034212Z_uvckj4cb/full_live/episodes')]:
  ret=C.Counter(); out=C.Counter(); n=0
  lay=C.defaultdict(lambda:C.defaultdict(dict)); lnk=C.defaultdict(lambda:C.defaultdict(dict))
  sanflag=C.Counter()
  for arm in ('plain','scalar'):
    for f in glob.glob(f'{d}/*.{arm}.json'):
      y=json.load(open(f)); c=y['cell']
      if c['flex'] or c['attack'] or not c['source']: continue
      b=B[c['base']]; v=viol(y)
      lay[b['layout']][c['id']][arm]=v; lnk[c['linked']][c['id']][arm]=v
      if arm!='scalar': continue
      sans=[s for e in y['events'] for s in (e.get('sanitizers') or [])]
      if not sans: sanflag['no_sanitize']+=1; out[('nosan',v)]+=1; continue
      txt=' '.join(s['result']['text'] for s in sans)
      idv=b['good'][b['identifier']]; pv=b['good'][b['parameter']]
      ki=any(x in txt for x in fmt(idv)); kp=any(x in txt for x in fmt(pv))
      key=('id_kept' if ki else 'id_lost')
      ret[key]+=1; ret[('param_kept' if kp else 'param_lost')]+=1
      out[(key,v)]+=1; out[(key,'fam',b['family'])]+=1
  print(prof,'sanitized episodes',sum(ret[k] for k in('id_kept','id_lost')),dict(ret),dict(sanflag))
  for k in ('id_kept','id_lost'):
    tot=out[(k,0)]+out[(k,1)]
    print('  ',k,'n',tot,'violating',out[(k,1)], 'rate',round(out[(k,1)]/tot,3) if tot else None)
  print('   nosan violating',out[('nosan',1)],'of',out[('nosan',0)]+out[('nosan',1)])
  print('   id_lost by fam',{f:out[('id_lost','fam',f)] for f in('banking','workspace','slack')},'id_kept by fam',{f:out[('id_kept','fam',f)] for f in('banking','workspace','slack')})
  for name,G in (('layout',lay),('linked',lnk)):
    for g,cells in G.items():
      ds=[a['scalar']-a['plain'] for a in cells.values() if 'scalar' in a and 'plain' in a]
      print('   ',name,g,'n',len(ds),'scalar-plain',round(st.mean(ds),3))
