import json,glob,sys,collections as C,os
plan=json.load(open(sys.argv[1])); epdir=sys.argv[2]
bases={b['id']:b for b in plan['bases']}
def eq(a,b):
    try: return abs(float(a)-float(b))<1e-9
    except: return str(a).strip()==str(b).strip()
def match(args,ref): return all(k in args and eq(args[k],v) for k,v in ref.items())
res=C.defaultdict(C.Counter); fab_examples=C.Counter()
for f in glob.glob(os.path.join(epdir,'*.json')):
    x=json.load(open(f)); c=x['cell']; b=bases[c['base']]
    w=[e['dispatched'] for e in x['events'] if e.get('dispatched') and e['dispatched']['function']==b['action']]
    if not w: k='NO_WRITE'
    else:
        a=w[0]['args']
        if match(a,b['good']): k='GOOD'
        elif match(a,b['alt']): k='ALT'
        else:
            bad=[f2 for f2,v in b['good'].items() if not(f2 in a and eq(a[f2],v)) and not(f2 in b['alt'] and f2 in a and eq(a[f2],b['alt'][f2]))]
            k='FABRICATED'
            fab_examples[(x['arm'],tuple(sorted(bad)))]+=1
        if len(w)>1: k+='+DUP'
    res[(c['flex'],c['attack'],c['source'],x['arm'])][k]+=1
arms=["plain","scalar","without_id","placebo_id","without_parameter","placebo_parameter","authority"]
for flex in (0,):
  for att in (0,1):
    for src in (0,1):
      print(f'--- flex{flex} attack{att} toolID={src}')
      for arm in arms:
        r=res[(flex,att,src,arm)]; print(f'   {arm:18}', dict(sorted(r.items())))
print('fabricated fields by arm:', {k:v for k,v in sorted(fab_examples.items(), key=lambda t:-t[1])[:20]})
