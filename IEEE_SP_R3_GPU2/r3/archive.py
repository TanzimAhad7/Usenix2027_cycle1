"""Archive each member's bytes once so live logs and hashes remain consistent."""
import hashlib,os,zipfile
from copy import copy
from pathlib import Path
REVIEW_NAMES={'result.json','job.json','events.jsonl','construction.json','parent_link.json','checkpoint.json','initial_world.json','final_world.json','partial_world.json','live_state_receipt.json','qualification.json','receipt.json','PACKAGE_MANIFEST.json','SOURCE_PROVENANCE.json'}
def review_member(rel):
    if rel.parts[0]=='source':return False
    if len(rel.parts)>1 and rel.name not in REVIEW_NAMES and rel.parts[0]!='serving':return False
    return not (rel.name.endswith('.log') or rel.name in ('wire.jsonl','model_queries.jsonl','rendered_requests.json'))
def archive(out,label=None):
    paths=[out.parent/(out.name+('.'+label if label else '')+('.review' if review else '')+'.zip') for review in [False,True]]
    temps=[p.with_name(p.name+'.tmp') for p in paths];manifests=[[],[]]
    with zipfile.ZipFile(temps[0],'w',zipfile.ZIP_DEFLATED,compresslevel=3) as raw,zipfile.ZipFile(temps[1],'w',zipfile.ZIP_DEFLATED,compresslevel=3) as review:
        for p in sorted(out.rglob('*')):
            if not p.is_file() or p.name=='SHA256SUMS' or '__pycache__' in p.parts:continue
            rel=p.relative_to(out);data=p.read_bytes();line=hashlib.sha256(data).hexdigest()+'  '+str(rel)+'\n'
            info=zipfile.ZipInfo.from_file(p,arcname=out.name+'/'+str(rel));info.compress_type=zipfile.ZIP_DEFLATED
            raw.writestr(copy(info),data);manifests[0].append(line)
            if review_member(rel):review.writestr(copy(info),data);manifests[1].append(line)
        for z,lines in [(raw,manifests[0]),(review,manifests[1])]:z.writestr(out.name+'/SHA256SUMS',''.join(lines))
    (out/'SHA256SUMS').write_text(''.join(manifests[0]))
    for tmp,target in zip(temps,paths):
        with zipfile.ZipFile(tmp) as z:
            if z.testzip():raise RuntimeError('Archive CRC verification failed')
        os.replace(tmp,target)
    return paths
