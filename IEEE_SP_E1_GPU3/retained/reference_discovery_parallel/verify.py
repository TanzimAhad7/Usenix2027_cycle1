import argparse,hashlib,tarfile
from pathlib import Path
from .common import file_hash,read
from .integrity import verify_package

def verify_archive(path):
    with tarfile.open(path,'r:gz') as t:
        files={m.name:m for m in t.getmembers() if m.isfile()}
        sums=[name for name in files if name.count('/')==1 and name.endswith('/SHA256SUMS')]
        if len(sums)!=1:raise RuntimeError('Expected one checksum manifest')
        root=sums[0].rsplit('/',1)[0];count=0
        for line in t.extractfile(files[sums[0]]).read().decode().splitlines():
            expected,relative=line.split('  ',1);name=root+'/'+relative
            if name not in files:raise RuntimeError('Missing archive file: '+relative)
            h=hashlib.sha256()
            stream=t.extractfile(files[name])
            for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
            if h.hexdigest()!=expected:raise RuntimeError('Checksum mismatch: '+relative)
            count+=1
    return count

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive',nargs='?',type=Path);a=p.parse_args()
    if a.archive:print('Verified archive files:',verify_archive(a.archive))
    else:verify_package(Path.cwd());print('Package hashes and frozen schedule: PASS')
