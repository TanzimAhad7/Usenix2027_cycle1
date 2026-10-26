"""Keep import/argument failures visible even before the controller loads."""
import json,re,runpy,sys,tarfile,traceback
from pathlib import Path

def main():
    args=sys.argv[1:];root=Path(args[args.index('--root')+1]).resolve();run_id=args[args.index('--run-id')+1]
    if not re.fullmatch(r'[A-Za-z0-9_-]+',run_id):raise ValueError('Invalid run ID')
    try:runpy.run_module('release_native_study.sequence',run_name='__main__')
    except BaseException as exc:
        status=root/'logs'/(run_id+'.status')
        if not status.exists():
            out=root/'results/user_runs'/run_id;out.mkdir(parents=True,exist_ok=True)
            rc=exc.code if isinstance(exc,SystemExit) and isinstance(exc.code,int) else 1
            status.write_text(f'exit_code={rc}\nstatus=BOOTSTRAP_FAILED\nresults={out}\n')
            (out/'bootstrap_failure.json').write_text(json.dumps(dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),model_server_started=False),indent=2)+'\n')
            target=Path(str(out)+'.tar.gz')
            with tarfile.open(target,'w:gz') as tar:tar.add(out,arcname=out.name)
            print('BOOTSTRAP FAILED; inspect launcher log. UPLOAD ARCHIVE:',target,flush=True)
        raise

if __name__=='__main__':main()
