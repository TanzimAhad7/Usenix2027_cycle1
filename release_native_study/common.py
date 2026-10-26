from __future__ import annotations
import dataclasses, enum, hashlib, json, os, time
import contextlib,functools,logging
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
GPU_UUID = 'GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
MODEL = 'qwen3-32b-release-native'
REVISION = '9216db5781bf21249d130ec9da846c4624c16137'
CACHE = '/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'
MAX_REQUESTS = 96
MAX_SECONDS = 1200
MAX_ITERS = 15

def pack(x):
    if hasattr(x, 'model_dump'): return pack(x.model_dump(mode='json'))
    if dataclasses.is_dataclass(x): return pack(dataclasses.asdict(x))
    if isinstance(x, enum.Enum): return x.value
    if isinstance(x, dict): return {str(k):pack(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [pack(v) for v in x]
    if isinstance(x, Path): return str(x)
    if hasattr(x, 'isoformat'): return x.isoformat()
    if x is None or isinstance(x,(str,int,float,bool)): return x
    if x.__class__.__name__ in ('NotGiven','Omit'): return '<NOT_GIVEN>'
    return repr(x)

def wire(x):
    """For certificates only. The original SDK receives unmodified kwargs."""
    return {k:pack(v) for k,v in x.items() if v.__class__.__name__ not in ('NotGiven','Omit')}

def digest(x): return hashlib.sha256(json.dumps(pack(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def file_hash(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_text(json.dumps(pack(x),indent=2,ensure_ascii=False)+'\n');q.replace(p)
def append(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f: f.write(json.dumps(pack(x),ensure_ascii=False)+'\n');f.flush()
def read(p): return json.loads(Path(p).read_text())

class StudyStop(BaseException): pass
class QualificationStop(StudyStop): pass
class BudgetStop(StudyStop): pass
class ReplayMismatch(StudyStop): pass
class FaultBeforeCommit(RuntimeError): pass

def native_messages(messages):
    from agentdojo.functions_runtime import FunctionCall
    rows=pack(messages)
    for m in rows:
        if m.get('tool_calls') is not None:m['tool_calls']=[FunctionCall(**c) for c in m['tool_calls']]
        if isinstance(m.get('tool_call'),dict):m['tool_call']=FunctionCall(**m['tool_call'])
    return rows

def seal(x):
    value=pack(x);value['snapshot_hash']=digest(value);return value
def unseal(x):
    value={k:v for k,v in x.items() if k!='snapshot_hash'}
    if digest(value)!=x['snapshot_hash']:raise ReplayMismatch('Checkpoint hash mismatch')
    return value

def capture_episode(fn):
    @functools.wraps(fn)
    def wrapped(self,*args,**kwargs):
        logger=logging.getLogger();old=logger.level;old_handlers=list(logger.handlers)
        handler=logging.FileHandler(self.directory/'native.log');logger.handlers=[handler];logger.setLevel(logging.INFO)
        try:
            with (self.directory/'diagnostic.log').open('a') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):return fn(self,*args,**kwargs)
        finally:logger.handlers=old_handlers;handler.close();logger.setLevel(old)
    return wrapped
