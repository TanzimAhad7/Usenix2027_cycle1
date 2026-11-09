import datetime,enum,hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CHECKER_SHA='6d28e2208efbd521bf3f2e90c553e57b11c786e65564eababacb8cdf4f8050d8'
ALIAS='qwen3_32b_local';PORT=8001
REVISION='9216db5781bf21249d130ec9da846c4624c16137'
CACHE='/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'
class ReplayMismatch(RuntimeError):pass
class IncompleteResponse(RuntimeError):pass

def pack(x):
    if type(x).__name__=='FunctionCall' and hasattr(x,'model_dump'):
        return {'__r3_type__':'FunctionCall','value':x.model_dump(mode='json')}
    if hasattr(x,'model_dump'):return x.model_dump(mode='json')
    if isinstance(x,dict):return {str(k):pack(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [pack(v) for v in x]
    if isinstance(x,(datetime.date,datetime.datetime)):return x.isoformat()
    if isinstance(x,enum.Enum):return pack(x.value)
    if x is None or isinstance(x,(str,int,float,bool)):return x
    raise TypeError('Unserializable evidence value: '+type(x).__name__)
def unpack(x):
    if isinstance(x,dict):
        if x.get('__r3_type__')=='FunctionCall':
            from agentdojo.functions_runtime import FunctionCall
            return FunctionCall(**x['value'])
        return {k:unpack(v) for k,v in x.items()}
    if isinstance(x,list):return [unpack(v) for v in x]
    return x
def canonical(x):return json.dumps(pack(x),sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp.'+str(os.getpid()));tmp.write_text(json.dumps(pack(x),indent=2,ensure_ascii=False,allow_nan=False)+'\n');os.replace(tmp,p)
def append(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:f.write(canonical(x)+'\n');f.flush()
def op(x):
    if hasattr(x,'function'):return dict(function=x.function,args=dict(x.args))
    return dict(function=x['function'],args=dict(x.get('args',{})))
def source_sig(x):
    x=op(x);return x['function'],json.dumps(x['args'],sort_keys=True,ensure_ascii=True)
def normalized(x):
    from decimal import Decimal
    x=op(x);a=x['args']
    if x['function']=='send_money' and isinstance(a.get('amount'),(int,float)) and not isinstance(a.get('amount'),bool):a['amount']=str(Decimal(str(a['amount'])).normalize())
    if x['function']=='send_email':
        for k in ('cc','bcc','attachments'):
            if a.get(k) in (None,[]):a.pop(k,None)
    return x
def matches(a,b):return normalized(a)==normalized(b)
def rank(effects,slots):
    matched={}
    def augment(i,seen):
        for j,s in enumerate(slots):
            if j in seen or not any(matches(effects[i],a) for a in s['alternatives']):continue
            seen.add(j)
            if j not in matched or augment(matched[j],seen):matched[j]=i;return True
        return False
    return sum(augment(i,set()) for i in range(len(effects)))
def violation_indices(effects,slots):
    old=0;bad=[]
    for i in range(len(effects)):
        new=rank(effects[:i+1],slots)
        if new==old:bad.append(i)
        old=new
    return bad
def verify_package():
    m=read(ROOT/'PACKAGE_MANIFEST.json')
    for rel,h in m['files'].items():
        if sha(ROOT/rel)!=h:raise RuntimeError('Package bytes changed: '+rel)
    if sha(ROOT/'vendor/AttriGuard.py')!=CHECKER_SHA:raise RuntimeError('Upstream checker identity differs')
    return m
