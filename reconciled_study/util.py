from __future__ import annotations
import hashlib,json,os
from pathlib import Path
from types import SimpleNamespace

PACKAGE=Path(__file__).resolve().parent
ASSETS=PACKAGE/'assets'

def plain(x):
    if hasattr(x,'model_dump'):return x.model_dump(mode='json')
    if isinstance(x,Path):return str(x)
    raise TypeError(type(x).__name__)

def pack(x):return json.loads(json.dumps(x,default=plain))
def digest(x):return hashlib.sha256(json.dumps(pack(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(x,indent=2,default=plain)+'\n');tmp.replace(p)
def args_with(a,**kw):return SimpleNamespace(**(vars(a)|kw))
def hash_file(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

class Censored(RuntimeError):pass
class InvalidParent(RuntimeError):pass
class QualificationError(RuntimeError):pass

class Budgets:
    """Fresh completions only. Reused initial evidence/tapes do not consume these."""
    limits={'E1':192,'INITIAL_EDGES':16,'PUB':64,'MANDATORY':7680,'REPEATS':768}
    def __init__(self,path=None):self.path=path;self.used={k:0 for k in self.limits}
    def take(self,key):
        if self.used[key]>=self.limits[key] or sum(self.used.values())>=8720:raise Censored('Campaign request ceiling '+key)
        self.used[key]+=1
        if self.path:write(self.path,dict(limits=self.limits,used=self.used,total=sum(self.used.values()),ceiling=8720))

def checkpoint_hash(cp):return digest({k:v for k,v in cp.items() if k!='snapshot_hash'})
def authenticate_parent(p):
    if digest({k:v for k,v in p.items() if k!='asset_hash'})!=p['asset_hash']:raise InvalidParent('Bundled parent asset hash mismatch')
    cp=p['checkpoint']
    if checkpoint_hash(cp)!=cp['snapshot_hash']:raise InvalidParent('Original checkpoint hash mismatch')
    if digest(p['batch']['checkpoint'])!=digest(cp):raise InvalidParent('Batch/checkpoint mismatch')
    if pack(cp['messages'][-1].get('tool_calls'))!=pack(cp['pending_calls']):raise InvalidParent('Pending calls differ from actual final assistant message')
    return p
