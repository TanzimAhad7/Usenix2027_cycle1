"""Derived owned-server/cache helpers; original lineage in SOURCE_PROVENANCE.json."""
import csv,hashlib,io,json,os,signal,socket,subprocess,time,urllib.request
from pathlib import Path
GPU=3
PORT=18080

def write(path,value):
    path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,indent=2,default=str)+'\n');tmp.replace(path)


def command(argv,timeout=30):
    r=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
    if r.returncode: raise RuntimeError(f'{argv[0]} failed ({r.returncode}): {r.stderr}')
    return r.stdout


def hash_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def inspect_snapshot(directory,model,revision):
    if not revision or '/' in revision or revision in ('.','..'):
        raise RuntimeError('Invalid cached model revision')
    snap=directory/'snapshots'/revision
    if not snap.is_dir(): raise RuntimeError(f'Cached snapshot missing: {snap}')
    required=['config.json','tokenizer_config.json','tokenizer.json']
    for name in required:
        if not (snap/name).is_file(): raise RuntimeError(f'Incomplete cache: {snap/name}')
    indices=list(snap.glob('*.safetensors.index.json'))
    shards=set()
    for index in indices: shards.update(json.loads(index.read_text())['weight_map'].values())
    if not shards: shards={p.name for p in snap.glob('*.safetensors')}
    if not shards: raise RuntimeError(f'No cached safetensors weights for {model}')
    for name in shards:
        p=snap/name
        if not p.is_file() or p.stat().st_size==0: raise RuntimeError(f'Missing/empty weight shard: {p}')
    files=[]
    for p in sorted(snap.rglob('*')):
        if p.is_file():
            entry=dict(name=str(p.relative_to(snap)),bytes=p.stat().st_size,symlink=os.readlink(p) if p.is_symlink() else None)
            if p.stat().st_size<20_000_000: entry['sha256']=hash_file(p)
            files.append(entry)
    tc=json.loads((snap/'tokenizer_config.json').read_text())
    template=tc.get('chat_template')
    tj=snap/'chat_template.json'
    if tj.is_file(): template=json.loads(tj.read_text()).get('chat_template',template)
    tf=snap/'chat_template.jinja'
    if tf.is_file(): template=tf.read_text()
    if template is None: raise RuntimeError(f'No cached chat template for {model}')
    if isinstance(template,dict):template=template.get('default')
    if not isinstance(template,str):raise RuntimeError(f'A single default text template is required for {model}')
    serialized=template
    return snap,dict(hub_model=model,revision=revision,snapshot=str(snap),files=files,
                     weight_hash_policy='Cache blob names and shard presence/size; large weights not reread for digest',
                     chat_template=template,chat_template_sha256=hashlib.sha256(serialized.encode()).hexdigest())


def gpu_table():
    return list(csv.reader(io.StringIO(command(['nvidia-smi','--query-gpu=index,uuid,memory.used,memory.total','--format=csv,noheader,nounits']))))


def gpu_applications():
    return list(csv.reader(io.StringIO(command(['nvidia-smi','--query-compute-apps=pid,gpu_uuid,used_gpu_memory','--format=csv,noheader,nounits']))))


def ensure_free(uuid):
    occupied=[r for r in gpu_applications() if len(r)>1 and r[1].strip()==uuid]
    if occupied: raise RuntimeError('GPU 3 has existing compute processes; none were stopped: '+str(occupied))


def ensure_port_free():
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try: s.bind(('127.0.0.1',PORT))
        except OSError as e: raise RuntimeError(f'Port {PORT} occupied; existing service is not used or stopped') from e


def read_json_url(url):
    with urllib.request.urlopen(url,timeout=5) as r: return json.load(r)


def descendant_pids(parent):
    pairs={int(p):int(pp) for p,pp in (line.split() for line in command(['ps','-eo','pid=,ppid=']).splitlines() if len(line.split())==2)}
    found={parent}
    while True:
        updated=found|{p for p,pp in pairs.items() if pp in found}
        if updated==found:return found
        found=updated


def proc_start(pid):
    try:
        fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        return None if fields[0]=='Z' else fields[19]
    except (FileNotFoundError,IndexError): return None


def stop_owned(server,owned,record):
    if server is None:return
    # Capture child identity before parent exits. Never use a global pkill.
    try:
        for pid in descendant_pids(server.pid): owned.setdefault(pid,proc_start(pid))
    except Exception: pass
    for sig,wait in [(signal.SIGTERM,40),(signal.SIGKILL,15)]:
        # A process-group ID can be reused after the root exits. Authenticate
        # the root identity before group signaling; individually tracked child
        # identities remain safe to signal after a parent exit.
        if owned.get(server.pid) is not None and proc_start(server.pid)==owned[server.pid]:
            try: os.killpg(server.pid,sig)
            except ProcessLookupError: pass
        for pid,start in owned.items():
            if start is not None and proc_start(pid)==start:
                try: os.kill(pid,sig)
                except ProcessLookupError: pass
        end=time.time()+wait
        while time.time()<end:
            server.poll()
            if not any(start is not None and proc_start(pid)==start for pid,start in owned.items()):break
            time.sleep(.5)
    try: server.wait(timeout=5)
    except subprocess.TimeoutExpired: pass
    remaining=[pid for pid,start in owned.items() if start is not None and proc_start(pid)==start]
    write(record,dict(server_pid=server.pid,returncode=server.poll(),remaining_owned_pids=remaining))
    if remaining:raise RuntimeError('Owned server processes did not stop: '+str(remaining))


def telemetry(out,stop):
    while not stop.is_set():
        try:
            rows=command(['nvidia-smi','--query-gpu=index,uuid,timestamp,utilization.gpu,memory.used,memory.total,power.draw','--format=csv,noheader,nounits'])
            with (out/'gpu_telemetry.csv').open('a') as f:
                for row in csv.reader(io.StringIO(rows)):
                    if row and row[0].strip()==str(GPU):f.write(','.join(row)+'\n');f.flush()
        except Exception as e:
            with (out/'telemetry_errors.log').open('a') as f:f.write(str(e)+'\n')
        stop.wait(10)

