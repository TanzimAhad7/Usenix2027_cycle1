"""Strict response-tape lineage, never counted as fresh model inference."""
import copy
import json
from pathlib import Path
from .common import pack,write,digest

def records(directory,after=0,until_actor=False):
    rows=[]
    for p in sorted(Path(directory).glob('http_*.request.json')):
        _,num,role=p.name.removesuffix('.request.json').split('_')
        if int(num)<=after:continue
        if until_actor and role=='actor':break
        response=p.with_name(p.name.replace('.request.json','.response.json'))
        if not response.is_file():raise ValueError('Incomplete response tape: '+str(p))
        rows.append(dict(role=role,request=json.loads(p.read_text()),response=json.loads(response.read_text()),
            source=str(p),request_hash=digest(json.loads(p.read_text()))))
    return rows

class Tape:
    scripted=True
    def __init__(self,session,rows):
        self.session=session;self.rows=copy.deepcopy(rows);self.count=0;self.models=[];self.usage=[]
    def request(self,payload,role):
        if not self.rows:raise ValueError('Recorded tape exhausted; no live fallback')
        row=self.rows.pop(0);self.count+=1
        if row['role']!=role or row['request']!=pack(payload):
            write(self.session.directory/'replay_drift.json',dict(expected=row,actual=payload,role=role))
            raise ValueError('Recorded request/role drift')
        data=row['response'];prefix=self.session.directory/f'http_{self.count:03d}_{role}'
        write(prefix.with_suffix('.request.json'),payload);write(prefix.with_suffix('.response.json'),data)
        write(prefix.with_suffix('.reused.json'),dict(source=row['source'],fresh_generations=0))
        self.models.append(data['model']);self.usage.append(dict(reused=True));return data['choices'][0]['message']
