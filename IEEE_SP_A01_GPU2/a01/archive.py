"""Stable raw snapshot and compact review archive after each stopped profile."""
import tarfile
from pathlib import Path
from reference_study.common import sha

def archive(out, stage=None):
    files=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    (out/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(out))+'\n' for p in files))
    stem=str(out)+(('.after_'+stage) if stage else '')
    target=Path(stem+'.tar.gz');temp=Path(str(target)+'.partial')
    with tarfile.open(temp,'w:gz',compresslevel=1) as f:f.add(out,arcname=out.name)
    temp.replace(target)
    Path(str(target)+'.sha256').write_text(sha(target)+'  '+target.name+'\n')
    review=Path(stem+'.review.tar.gz')
    with tarfile.open(review,'w:gz',compresslevel=1) as f:
        for rel in ('status.json','MANIFEST_qwen.json','MANIFEST_gemma.json','CLIENTS.json','analysis','preflight','environment.json','client_environments','fatal_error.json','serving_versions.txt'):
            p=out/rel
            if p.exists():f.add(p,arcname=out.name+'/'+rel)
    return target,review
