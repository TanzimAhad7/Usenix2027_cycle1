import json,glob,sys,collections as C,os
plan=json.load(open(sys.argv[1])); epdir=sys.argv[2]; arms=sys.argv[3].split(',')
bases={b['id']:b for b in plan['bases']}
def eq(a,b):
    try: return abs(float(a)-float(b))<1e-9
    except: return str(a).strip()==str(b).strip()
pat=C.Counter(); ex=[]
for f in glob.glob(os.path.join(epdir,'*.json')):
    x=json.load(open(f)); c=x['cell']
    if x['arm'] not in arms or c['flex']!=0 or c['attack']!=0 or c['source']!=1: continue
    b=bases[c['base']]
    w=[e['dispatched'] for e in x['events'] if e.get('dispatched') and e['dispatched']['function']==b['action']]
    if not w: continue
    a=w[0]['args']
    for k,v in b['good'].items():
        if not(k in a and eq(a[k],v)):
            got=a.get(k,'<MISSING>')
            # categorize
            if k in('recipient','recipients','channel'):
                cat='same-normalized' if str(got).lower().strip("[]' ")==str(v).lower().strip("[]' ") else ('sender/self' if str(got) in('DE0000000000',) else ('placeholder/empty' if not got or got in([],'') else 'other-value'))
            elif k=='amount': cat='zero' if eq(got,0) else ('alt' if eq(got,b['alt'].get('amount',-1)) else 'other-amount')
            elif k=='date': cat='other-date'
            else: cat='other'
            pat[(x['arm'],b['family'],k,cat)]+=1
            if len(ex)<14 and x['arm']==arms[-1]: ex.append((c['base'],k,v,got))
for k,v in sorted(pat.items()): print(v,k)
for e in ex: print('  EX',e)
