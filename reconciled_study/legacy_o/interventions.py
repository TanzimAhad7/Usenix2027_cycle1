"""Provenance-joined reconstructed carrier inputs; not edits to paraphrases."""
import copy
import json
from agentdojo.types import text_content_block_from_string
from .common import digest,pack

PROFILES=('canonical_actual','canonical_remove','canonical_neutral','canonical_placebo')

def reference_context(context,records,spec,profile):
    if profile not in PROFILES:raise ValueError('Unknown reference intervention')
    before=pack(context);after=copy.deepcopy(context);edits=[]
    indexed={r['occurrence_id']:r for r in records}
    for i,m in enumerate(after):
        if m.get('role')!='tool' or m.get('tool_call_id') not in indexed:continue
        record=indexed[m['tool_call_id']]
        call=m.get('tool_call');function=call.get('function') if isinstance(call,dict) else getattr(call,'function',None)
        if function!=record['function'] or m.get('error'):raise ValueError('Carrier provenance mismatch')
        raw=copy.deepcopy(record['raw_result'])
        if record['function']=='get_iban':
            raw=json.loads(raw) if isinstance(raw,str) else raw
            if raw.get('person')!=spec['person'] or raw.get('account_id')!=spec['recipient']:
                raise ValueError('Immutable directory facts differ')
            targets=[(raw,'directory_note')]
        elif record['function']=='get_received_emails':
            if not isinstance(raw,list):raise ValueError('Expected recorded email list')
            targets=[(e,'body') for e in raw if e.get('sender')=='notices@example.com' and e.get('subject')==spec['fact']]
        else:raise ValueError('Unsupported carrier function')
        if len(targets)!=1:raise ValueError('Ambiguous designated carrier')
        obj,key=targets[0];old=obj[key]
        if old.count(spec['instruction'])!=1:raise ValueError('Raw carrier instruction provenance absent')
        if profile=='canonical_remove':obj[key]=old.replace(spec['instruction'],'',1)
        elif profile=='canonical_neutral':obj[key]=old.replace(spec['instruction'],spec['neutral'],1)
        elif profile=='canonical_placebo':
            if old.count('Metadata: imported plain text.')!=1:raise ValueError('Raw placebo provenance absent')
            obj[key]=old.replace('Metadata: imported plain text.','Metadata: stored plain text.',1)
        text=json.dumps(raw,sort_keys=True,ensure_ascii=False,separators=(',',':'))
        m['content']=[text_content_block_from_string(text)]
        edits.append(dict(message=i,tool_call_id=m['tool_call_id'],function=record['function'],
            raw_result_hash=digest(record['raw_result']),raw_field_before=old,raw_field_after=obj[key],
            original_derived_content=before[i].get('content'),replacement_content=pack(m['content'])))
    if not edits:raise ValueError('NO_PROVENANCE_JOINED_CARRIER_IN_REFERENCE_CONTEXT')
    for a,b in zip(before,pack(after)):
        assert {k:v for k,v in a.items() if k!='content'}=={k:v for k,v in b.items() if k!='content'}
    return after,dict(profile=profile,status='APPLIED',scope='RECONSTRUCTED_RAW_CARRIER_REFERENCE_ONLY',
        inference_limit='Compare canonical profiles to one another; actual derived input is a separate baseline',
        edits=edits,before=before,after=pack(after))
