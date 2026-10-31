from __future__ import annotations
import contextlib, dataclasses, enum, hashlib, json, signal
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
GPU_UUID = 'GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
MODEL = 'qwen3-32b-release-native'
REVISION = '9216db5781bf21249d130ec9da846c4624c16137'
CACHE = '/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache'

def pack(x):
    if hasattr(x, 'model_dump'): return pack(x.model_dump(mode='json'))
    if dataclasses.is_dataclass(x): return pack(dataclasses.asdict(x))
    if isinstance(x, enum.Enum): return x.value
    if isinstance(x, dict): return {str(k):pack(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)): return [pack(v) for v in x]
    if isinstance(x, Path): return str(x)
    if hasattr(x, 'isoformat'): return x.isoformat()
    if x is None or isinstance(x,(str,int,float,bool)): return x
    if x.__class__.__name__ in ('NotGiven','Omit'): return '<NOT_GIVEN>'
    return repr(x)

def digest(x): return hashlib.sha256(json.dumps(pack(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def file_hash(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_text(json.dumps(pack(x),indent=2,ensure_ascii=False)+'\n');q.replace(p)
def read(p): return json.loads(Path(p).read_text())
def append(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:f.write(json.dumps(pack(x),ensure_ascii=False)+'\n');f.flush()
def native_messages(rows):
    from agentdojo.functions_runtime import FunctionCall
    rows=pack(rows)
    for m in rows:
        if m.get('tool_calls') is not None:m['tool_calls']=[FunctionCall(**c) for c in m['tool_calls']]
        if isinstance(m.get('tool_call'),dict):m['tool_call']=FunctionCall(**m['tool_call'])
    return rows
class Invalid(RuntimeError): pass
class Pause(BaseException):
    def __init__(self,data):self.data=data
class ModelFailure(BaseException): pass
class Deadline(BaseException): pass
@contextlib.contextmanager
def deadline(seconds):
    def expired(*_):raise Deadline(f'Phase deadline {seconds}s')
    old=signal.signal(signal.SIGALRM,expired);signal.alarm(seconds)
    try:yield
    finally:signal.alarm(0);signal.signal(signal.SIGALRM,old)
