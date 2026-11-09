"""Preserve setup failures even before the research venv can start."""
import json,shutil,sys,tarfile
from pathlib import Path
project=Path(sys.argv[1]);ident=sys.argv[2];rc=int(sys.argv[3])
out=project/'results/user_runs'/ident;out.mkdir(parents=True,exist_ok=True)
(out/'status.json').write_text(json.dumps(dict(status='BOOTSTRAP_FAILED',exit_code=rc,model_inference=0,
    scope='Environment setup failed before the model controller; log retained. No scientific panel executed.'),indent=2)+'\n')
for suffix in('.log','.log.pid','.log.pid.json','.status'):
    p=project/'logs'/(ident+suffix)
    if p.is_file():shutil.copyfile(p,out/p.name)
with tarfile.open(str(out)+'.tar.gz','w:gz',compresslevel=1)as f:f.add(out,arcname=ident)
print('BOOTSTRAP FAILURE ARCHIVE:',str(out)+'.tar.gz',flush=True)
