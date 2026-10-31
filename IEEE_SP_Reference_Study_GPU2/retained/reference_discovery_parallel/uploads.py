"""A compact all-case review bundle and independently valid raw tar shards."""
import argparse,hashlib,io,json,shutil,tarfile
from pathlib import Path
from .common import file_hash,read,write

def raw_files(out):
    return [p for p in sorted(out.rglob('*')) if p.is_file() and '__pycache__' not in p.relative_to(out).parts]

def add_bytes(t,name,data):
    info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;t.addfile(info,io.BytesIO(data))

def make_uploads(out,part_budget=256*1024*1024):
    files=raw_files(out);folder=out.parent/(out.name+'.upload_parts');folder.mkdir(exist_ok=False)
    sums=out/'SHA256SUMS';shutil.copy2(sums,folder/'RAW_SHA256SUMS')
    groups=[];group=[];size=0
    for p in files:
        estimate=((p.stat().st_size+511)//512)*512+4096
        if estimate>part_budget:
            if group:groups.append(group);group=[];size=0
            groups.append([p]);continue
        if group and size+estimate>part_budget:groups.append(group);group=[];size=0
        group.append(p);size+=estimate
    if group:groups.append(group)
    index=dict(schema='RAW_UPLOAD_SHARDS_1',root=out.name,raw_manifest='RAW_SHA256SUMS',raw_manifest_sha256=file_hash(sums),raw_files=len(files),target_uncompressed_budget=part_budget,oversized_single_files=[str(p.relative_to(out)) for p in files if p.stat().st_size+4096>part_budget],parts=[])
    for number,group in enumerate(groups,1):
        target=folder/f'raw_{number:03d}.tar.gz';temporary=Path(str(target)+'.partial')
        with tarfile.open(temporary,'w:gz',compresslevel=3) as t:
            for p in group:t.add(p,arcname=out.name+'/'+str(p.relative_to(out)),recursive=False)
        temporary.replace(target)
        index['parts'].append(dict(file=target.name,sha256=file_hash(target),bytes=target.stat().st_size,files=len(group)))
        print(f'UPLOAD PACKAGING: raw part {number}/{len(groups)} saved ({target.stat().st_size} bytes)',flush=True)
    write(folder/'INDEX.json',index)
    selected=[]
    for p in files:
        rel=p.relative_to(out)
        if p==sums:continue
        if not any(x in ['workflows','forks'] for x in rel.parts) or p.name in ['item.json','result.json','events.jsonl','final_reporting.json','effective_driver_profile.json','error.json']:
            selected.append(p)
    review=out.parent/(out.name+'.review.tar.gz');scope=json.dumps(dict(
        kind='ALL_CASE_REVIEW_NOT_COMPLETE_MODEL_IO',all_available_case_results_included=True,
        includes='Complete census and all available result/event ledgers, conditions, source, analysis, conditional experiment evidence and metadata',
        excluded='Autonomous and conditional full wire/model histories, native snapshots and local counterfactual files; preserved without selection in the raw parts and full archive',
        required_for_full_audit='All raw parts with INDEX.json and RAW_SHA256SUMS, or the complete full archive'),indent=2).encode()
    manifest=''.join(file_hash(p)+'  '+str(p.relative_to(out))+'\n' for p in selected)
    manifest+=file_hash(sums)+'  RAW_SHA256SUMS\n'+hashlib.sha256(scope).hexdigest()+'  REVIEW_SCOPE.json\n'
    with tarfile.open(review,'w:gz',compresslevel=3) as t:
        for p in selected:t.add(p,arcname=out.name+'/'+str(p.relative_to(out)),recursive=False)
        add_bytes(t,out.name+'/RAW_SHA256SUMS',sums.read_bytes());add_bytes(t,out.name+'/REVIEW_SCOPE.json',scope)
        add_bytes(t,out.name+'/SHA256SUMS',manifest.encode())
    result=dict(review_bundle=str(review),review_sha256=file_hash(review),raw_parts=str(folder),index=str(folder/'INDEX.json'),parts=len(groups))
    write(folder/'UPLOAD_INSTRUCTIONS.json',result)
    print('UPLOAD REVIEW BUNDLE:',review,flush=True);print('UPLOAD COMPLETE RAW PARTS:',folder,flush=True)
    return result

def verify_parts(index_path):
    index=read(index_path);folder=index_path.parent;sums=folder/index['raw_manifest']
    if file_hash(sums)!=index['raw_manifest_sha256']:raise RuntimeError('Raw checksum manifest changed')
    expected={line.split('  ',1)[1]:line.split('  ',1)[0] for line in sums.read_text().splitlines()}
    expected['SHA256SUMS']=file_hash(sums);seen={}
    for part in index['parts']:
        path=folder/part['file']
        if file_hash(path)!=part['sha256']:raise RuntimeError('Shard checksum mismatch: '+part['file'])
        with tarfile.open(path,'r|gz') as t:
            for member in t:
                if not member.isfile():continue
                prefix=index['root']+'/'
                if not member.name.startswith(prefix):raise RuntimeError('Unexpected raw shard root')
                name=member.name[len(prefix):]
                if name in seen:raise RuntimeError('Duplicate raw file: '+name)
                stream=t.extractfile(member);h=hashlib.sha256()
                for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
                seen[name]=h.hexdigest()
    if seen!=expected:raise RuntimeError('Raw shards are incomplete or contain altered files')
    return dict(status='PASS',raw_files_verified=len(seen),parts=len(index['parts']))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('index',type=Path);p.add_argument('--create',action='store_true');a=p.parse_args();print(json.dumps(make_uploads(a.index) if a.create else verify_parts(a.index),indent=2))
