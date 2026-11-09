"""Apply a verified operational patch; preserve source backups and all results."""
import datetime,fcntl,hashlib,json,os,re,shutil,sys,uuid
from pathlib import Path
BASE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def safe(rel):
 p=Path(rel)
 if p.is_absolute()or not p.parts or any(x in ('..','.')for x in p.parts):raise RuntimeError('Unsafe patch path')
 return p

def verify(root,manifest):
 for rel,h in manifest['files'].items():
  p=root/safe(rel)
  if not p.is_file()or sha(p)!=h:raise RuntimeError('Source drift; patch refused before changes: '+rel)

def main(target):
 target=Path(target).resolve();info=json.loads((BASE/'PATCH.json').read_text());locks=[]
 if not(target/'RUN_E1.sh').is_file():raise RuntimeError('Target must be the existing IEEE_SP_E1_GPU3 directory')
 (target/'logs').mkdir(exist_ok=True)
 try:
  for name in ('bootstrap.lock','gpu3_sequence.lock'):
   f=(target/'logs'/name).open('a');locks.append(f)
   try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:raise RuntimeError('This E1 package is active; no files changed. Let it finish before patching.')
  new_manifest=json.loads((BASE/'payload/PACKAGE_MANIFEST.json').read_text())
  current=sha(target/'PACKAGE_MANIFEST.json')
  if current==info['new_manifest_sha256']:
   verify(target,new_manifest);print('Already patched; source verified. Existing results preserved.');return
  if current!=info['expected_parent_manifest_sha256']:raise RuntimeError('Unexpected package revision; no files changed')
  verify(target,json.loads((target/'PACKAGE_MANIFEST.json').read_text()))
  for rel,h in info['payload'].items():
   src=BASE/'payload'/safe(rel);dst=target/safe(rel)
   if sha(src)!=h:raise RuntimeError('Corrupt patch payload: '+rel)
   if dst.is_symlink()or any(x.is_symlink()for x in dst.parents if x!=target and target in x.parents):raise RuntimeError('Refusing symlink destination: '+rel)
  stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8]
  backup=target/'patch_backups'/('preflight_'+stamp);backup.mkdir(parents=True)
  original={};replaced=[]
  for rel in info['payload']:
   dst=target/rel;original[rel]=sha(dst)if dst.is_file()else None
   if dst.exists():
    b=backup/'original'/rel;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,b)
  (backup/'patch_record.json').write_text(json.dumps(dict(patch=info,original_files=original,results_preserved=True),indent=2)+'\n')
  try:
   # Publish the new source manifest last; locks cover the entire transaction.
   order=sorted(info['payload'],key=lambda x:x=='PACKAGE_MANIFEST.json')
   for rel in order:
    dst=target/rel;dst.parent.mkdir(parents=True,exist_ok=True);tmp=backup/'staged'/rel;tmp.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(BASE/'payload'/rel,tmp);os.replace(tmp,dst);replaced.append(rel)
   verify(target,new_manifest)
  except BaseException:
   for rel in reversed(replaced):
    dst=target/rel;b=backup/'original'/rel
    if original[rel]is None:dst.unlink(missing_ok=True)
    else:shutil.copy2(b,dst)
   raise
  print('APPLIED: research request preparation + isolated serving rendering.')
  print('BACKUP:',backup)
  print('Previous results, logs, environments, GPU placement and experiment design preserved.')
  # Surface the actual preceding error, which was omitted from the original main log.
  latest=target/'logs/LATEST_E1'
  if latest.exists():
   run=latest.read_text().strip()
   if re.fullmatch('[A-Za-z0-9_-]+',run):
    for family in ('qwen','gemma'):
     for name in ('error.json','rendering.log'):
      p=target/'results/user_runs'/run/'preflight'/family/name
      if p.is_file():print('PREVIOUS PREFLIGHT',family,name,'\n'+'\n'.join(p.read_text(errors='replace').splitlines()[-12:]))
 finally:
  for f in reversed(locks):f.close()
if __name__=='__main__':
 try:main(sys.argv[1])
 except BaseException as e:print('PATCH STOPPED:',str(e),file=sys.stderr);raise SystemExit(1)
