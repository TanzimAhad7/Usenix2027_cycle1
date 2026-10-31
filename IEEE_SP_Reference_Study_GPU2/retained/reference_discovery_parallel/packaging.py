"""One final lossless raw archive; compact review. Optional duplicate raw shards."""
import hashlib,io,json,tarfile,time
from pathlib import Path
from .common import file_hash,write

def raw_files(out):return [p for p in sorted(out.rglob('*')) if p.is_file() and '__pycache__' not in p.relative_to(out).parts]

def review_selected(relative):
    case=any(x in ('workflows','forks') for x in relative.parts)
    return not case or relative.name in ('item.json','result.json','events.jsonl','final_reporting.json','effective_driver_profile.json','error.json','recovery_selection_error.json','initial_decision_replay.json','common_feedback.json')

def package(out,raw_parts=False):
    start=time.monotonic();files=[p for p in raw_files(out) if p!=out/'SHA256SUMS']
    sums=out/'SHA256SUMS';sums.write_text(''.join(file_hash(p)+'  '+str(p.relative_to(out))+'\n' for p in files))
    target=Path(str(out)+'.tar.gz');partial=Path(str(target)+'.partial')
    print('PACKAGING one complete lossless raw archive (gzip level 1). GPU collection has ended.',flush=True)
    with tarfile.open(partial,'w:gz',compresslevel=1) as tar:
        for p in files+[sums]:tar.add(p,arcname=out.name+'/'+str(p.relative_to(out)),recursive=False)
    partial.replace(target);Path(str(target)+'.sha256').write_text(file_hash(target)+'  '+target.name+'\n')
    selected=[p for p in files if review_selected(p.relative_to(out))]
    scope=json.dumps(dict(kind='ALL_CASE_REVIEW_NOT_COMPLETE_MODEL_IO',profiles=['qwen','gemma'],all_available_results_and_events=True,
        excluded='Full per-case model/wire histories, snapshots and counterfactuals; all are in the complete raw archive.',
        full_evidence=str(target),raw_parts='Optional convenience only: python -m reference_discovery_parallel.uploads --create RAW_DIRECTORY'),indent=2).encode()
    review=Path(str(out)+'.review.tar.gz')
    def add(t,name,data):
        member=tarfile.TarInfo(out.name+'/'+name);member.size=len(data);member.mode=0o644;t.addfile(member,io.BytesIO(data))
    manifest=''.join(file_hash(p)+'  '+str(p.relative_to(out))+'\n' for p in selected)
    manifest+=file_hash(sums)+'  RAW_SHA256SUMS\n'+hashlib.sha256(scope).hexdigest()+'  REVIEW_SCOPE.json\n'
    with tarfile.open(review,'w:gz',compresslevel=1) as tar:
        for p in selected:tar.add(p,arcname=out.name+'/'+str(p.relative_to(out)),recursive=False)
        add(tar,'RAW_SHA256SUMS',sums.read_bytes());add(tar,'REVIEW_SCOPE.json',scope);add(tar,'SHA256SUMS',manifest.encode())
    outputs=dict(archive=str(target),archive_sha256=file_hash(target),review_bundle=str(review),review_sha256=file_hash(review),raw_parts=None,
        packaging_seconds=time.monotonic()-start,raw_files=len(files)+1,raw_evidence_losslessly_preserved=True)
    if raw_parts:
        from .uploads import make_uploads
        outputs['raw_parts']=make_uploads(out)['raw_parts']
    write(Path(str(out)+'.packaging.json'),outputs);return outputs
