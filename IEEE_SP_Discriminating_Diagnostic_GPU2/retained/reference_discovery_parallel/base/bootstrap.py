"""Capture dependency/import failures before the controller loads."""
import json,re,runpy,sys,tarfile,traceback
from pathlib import Path
def main():
    args=sys.argv[1:];root=Path(args[args.index('--root')+1]).resolve();ident=args[args.index('--run-id')+1]
    if not re.fullmatch(r'[A-Za-z0-9_-]+',ident):raise ValueError('Invalid run ID')
    try:runpy.run_module('s1_reference_study.sequence',run_name='__main__')
    except BaseException as exc:
        status=root/'logs'/(ident+'.status')
        if not status.exists():
            out=root/'results/user_runs'/ident;out.mkdir(parents=True,exist_ok=True)
            (out/'bootstrap_failure.json').write_text(json.dumps(dict(error=str(exc),type=type(exc).__name__,traceback=traceback.format_exc(),server_started=False),indent=2)+'\n')
            status.write_text(f'exit_code=1\nstatus=BOOTSTRAP_FAILED\nresults={out}\n')
            target=Path(str(out)+'.tar.gz')
            with tarfile.open(target,'w:gz') as t:t.add(out,arcname=out.name)
            print('BOOTSTRAP FAILED. UPLOAD ARCHIVE:',target,flush=True)
        raise
if __name__=='__main__':main()
