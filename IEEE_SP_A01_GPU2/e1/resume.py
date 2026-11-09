"""Resume only unrecorded blocks; preserve failed terminal rows without redraws."""
import shutil
from pathlib import Path
from reference_study.common import ROOT,read,write,sha

def validate(parent,mock):
 parent=Path(parent).resolve();status=read(parent/'status.json')
 if sha(parent/'source/PACKAGE_MANIFEST.json')!=sha(ROOT/'PACKAGE_MANIFEST.json'):raise RuntimeError('Resume code/fixture manifest differs; use a new amended cohort instead')
 for rel,h in read(parent/'source/PACKAGE_MANIFEST.json')['files'].items():
  if not(parent/'source'/rel).is_file()or sha(parent/'source'/rel)!=h:raise RuntimeError('Parent frozen source was modified: '+rel)
 expected='MOCK_ZERO_INFERENCE'if mock else'LIVE_CONDITIONAL_DIAGNOSTIC'
 if status['mode']!=expected:raise RuntimeError('Cannot mix mock/CPU/live cohorts during resume')
 if status['status']in('STARTING','RUNNING','PROFILE_COMPLETE','PREFLIGHT','CPU_QUALIFICATION','CLEANUP_PENDING'):raise RuntimeError('Parent is active or cleanup unresolved; do not resume it')
 for p in parent.glob('*_process.json'):
  row=read(p);pid=row.get('pid')
  if pid and Path(f'/proc/{pid}/cmdline').exists():
   cmd=Path(f'/proc/{pid}/cmdline').read_bytes()
   if b'e1.profile'in cmd:raise RuntimeError('Parent profile may still be active')
 return parent

def retain(parent,target,family,manifest):
 kept=[];base=Path(parent)/family/'P1'
 for item in manifest['P1']:
  src=base/item['id'];r=src/'result.json'
  if not src.exists():continue
  # Any terminal row, including INTERRUPTED/TECHNICAL_ERROR, stays as recorded.
  dest=target/family/'P1'/item['id'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(src,dest)
  if not r.is_file():
   write(dest/'result.json',dict(id=item['id'],status='RETAINED_INCOMPLETE_ATTEMPT',qualified=False,mock=read(Path(parent)/'status.json')['mode']=='MOCK_ZERO_INFERENCE',scientific_negative=False,error='Partial attempted cell retained; no redraw.'))
  files=[dict(path=str(p.relative_to(src)),sha256=sha(p))for p in src.rglob('*')if p.is_file()]
  for x in files:
   if sha(dest/x['path'])!=x['sha256']:raise RuntimeError('Retained block byte mismatch')
  kept.append(dict(id=item['id'],result_sha256=sha(dest/'result.json'),parent=str(src),files=files,new_model_inference=False))
 write(target/family/'retained_parent_blocks.json',dict(parent=str(parent),blocks=kept,failed_terminal_rows_preserved=True,scientific_redraws=0))
 return len(kept)
