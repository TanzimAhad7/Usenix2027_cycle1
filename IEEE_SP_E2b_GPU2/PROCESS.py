"""PID/start-time matching; signal only this launcher, never search-and-kill."""
import argparse,json,os,signal,time
from pathlib import Path

def start(pid):
 try:
  fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
  return None if fields[0]=='Z' else fields[19]
 except (FileNotFoundError,IndexError):return None

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=('record','stop'));p.add_argument('value');p.add_argument('path',nargs='?');a=p.parse_args()
 if a.action=='record':
  pid=int(a.value);identity=start(pid)
  if identity is None:raise SystemExit('Launcher already exited or /proc identity is unavailable. Inspect its log; no running PID was published.')
  Path(a.path).write_text(json.dumps(dict(pid=pid,start=identity))+'\n')
 else:
  x=json.loads(Path(a.value).read_text());pid=x['pid']
  if not x.get('start')or start(pid)!=x['start']:raise SystemExit('Recorded process is no longer running; nothing signaled.')
  # During setup the launcher is a shell, so include only authenticated descendants.
  identities={pid:x['start']};changed=True
  while changed:
   changed=False
   for f in Path('/proc').glob('[0-9]*/stat'):
    try:
     fields=f.read_text().rsplit(')',1)[1].split();child=int(f.parent.name)
     if int(fields[1])in identities and child not in identities:identities[child]=fields[19];changed=True
    except (FileNotFoundError,ProcessLookupError,ValueError):pass
  # Source controller handles owned server cleanup. Signal controller/profile first;
  # do not kill the frozen controller's GPU children independently.
  controllers=[]
  for child,s in identities.items():
   try:
    cmd=Path(f'/proc/{child}/cmdline').read_bytes().replace(b'\0',b' ')
    if b'e2b.controller' in cmd and start(child)==s:controllers.append(child)
   except FileNotFoundError:pass
  targets=controllers or list(reversed(identities))
  for child in targets:
   if start(child)==identities[child]:os.kill(child,signal.SIGTERM)
  print('Stop requested for owned E2b controller; cleanup and partial evidence archiving will follow.')
