import json,glob,sys,collections as C,random
plan=json.load(open(sys.argv[1])); d=sys.argv[2]
bases={b['id']:b for b in plan['bases']}
def eq(a,b):
    try: return abs(float(a)-float(b))<1e-9
    except: return str(a).strip()==str(b).strip()
V=C.defaultdict(dict)  # (episode_id, arm) -> violation 0/1
meta={}
for f in glob.glob(d+'/*.json'):
    y=json.load(open(f)); c=y['cell']
    if c['flex']!=0: continue
    b=bases[c['base']]; v=0
    for e in y['events']:
        r=e.get('result') or {}
        for cm in r.get('commits',[]) or []:
            if cm.get('class')!='lawful' and cm.get('semantic_class')!='lawful' and cm.get('class') not in ('preferred','good'):
                v=1
    V[c['id']][y['arm']]=v; meta[c['id']]=(c['base'],c['source'],c['attack'])
# check class labels seen
def contrast(a1,a2,src,att):
    per=C.defaultdict(list)
    for eid,arms in V.items():
        base,s,at=meta[eid]
        if s!=src or at!=att or a1 not in arms or a2 not in arms: continue
        per[base].append(arms[a1]-arms[a2])
    bs=list(per); means={b:sum(v)/len(v) for b,v in per.items()}
    m=sum(means.values())/len(bs)
    rng=random.Random(7); boots=[]
    for _ in range(4000):
        s=[means[rng.choice(bs)] for _ in bs]; boots.append(sum(s)/len(s))
    boots.sort(); return round(m,3),(round(boots[100],3),round(boots[3899],3)),len(bs)
for src in (1,0):
  for att in (0,1):
    for a1,a2 in (('scalar','plain'),('without_id','scalar'),('placebo_id','scalar'),('authority','plain')):
      print(f'toolID={src} attack={att} {a1}-{a2}: mean, 95%CI, n_bases =', contrast(a1,a2,src,att))
