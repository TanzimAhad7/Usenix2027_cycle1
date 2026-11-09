from __future__ import annotations
import hashlib,json,os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GPU_INDEX=2
GPU_UUID='GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932'
LOCK_NAME='gpu2_sequence.lock'

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb')as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.'+str(os.getpid())+'.tmp');tmp.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n');tmp.replace(p)
def append(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a')as f:f.write(json.dumps(x,ensure_ascii=False)+'\n');f.flush()
def activate(family):
    from permission_admission.util import activate as original
    return original(family)
def verify_package():
    m=read(ROOT/'PACKAGE_MANIFEST.json')
    for name,h in m['files'].items():
        p=ROOT/name
        if not p.is_file()or sha(p)!=h:raise RuntimeError('Package drift: '+name)
    return m
