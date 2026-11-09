import argparse,json,os,signal
from pathlib import Path
from .common import read
from .serving_base import proc_start,verify_pid_namespace
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stop',action='store_true');a=p.parse_args();latest=a.root/'logs/latest.json'
    if not latest.is_file():raise SystemExit('No R3 launch recorded.')
    meta=read(latest);out=Path(meta['results'])
    if a.stop:
        verify_pid_namespace();pid=meta['pid'];birth=meta['start']
        if not isinstance(pid,int) or pid<=1 or birth is None or proc_start(pid)!=birth:raise SystemExit('Recorded controller is no longer active. No process was signaled.')
        cmd=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
        if b'r3.controller' not in cmd or meta['run_id'].encode() not in cmd:raise SystemExit('Controller command identity differs. No process was signaled.')
        os.kill(pid,signal.SIGTERM);raise SystemExit('Stop requested for the authenticated R3 controller; it will clean up its own workers/server and archive partial results.')
    print('Run:',meta['run_id'])
    if (out/'status.json').is_file():
        s=read(out/'status.json');print(json.dumps({k:s.get(k) for k in ('status','completed','full_planned','conditional_slots','active','elapsed_seconds','exit_code','owned_cleanup_verified')},indent=2))
    else:print('Controller initialization; inspect log below.')
    print('Log:',meta['log']);print('Results:',out)
    for suffix in ('.zip','.review.zip'):
        f=out.parent/(out.name+suffix)
        if f.is_file():print('Archive:',f)
    log=Path(meta['log'])
    if log.is_file():print('\n'.join(log.read_text(errors='replace').splitlines()[-15:]))
