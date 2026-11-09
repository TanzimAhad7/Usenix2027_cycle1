"""Preserve setup/lock failure even before the research environment exists."""
import json,sys,tarfile,time
from pathlib import Path
root=Path(sys.argv[1]);run=sys.argv[2];code=int(sys.argv[3]);out=root/'results/user_runs'/run;out.mkdir(parents=True,exist_ok=True)
log=root/'logs'/(run+'.log')
if log.exists():(out/'bootstrap.log').write_bytes(log.read_bytes())
status=dict(status='BOOTSTRAP_FAILED',exit_code=code,run_id=run,finished_epoch=time.time(),model_inference=0,note='No scientific result inferred from setup or lock failure; inspect log. No foreign process stopped.')
(out/'status.json').write_text(json.dumps(status,indent=2)+'\n')
with tarfile.open(str(out)+'.tar.gz','w:gz')as t:t.add(out,arcname=run)
(root/'logs'/(run+'.status')).write_text('exit_code='+str(code)+'\nstatus=BOOTSTRAP_FAILED\nresults='+str(out)+'\n')
