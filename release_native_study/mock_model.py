"""Scripted SDK/HTTP test double. NEVER model-science evidence."""
import json,re
from .effects import matches

def completion(text='',calls=None):
    message=dict(role='assistant',content=text or None)
    if calls:message['tool_calls']=calls
    return dict(id='MOCK_NO_MODEL_INFERENCE',created=0,object='chat.completion',model='qwen3-32b-release-native',choices=[dict(index=0,finish_reason='tool_calls' if calls else 'stop',message=message)],usage=dict(prompt_tokens=0,completion_tokens=0,total_tokens=0))

def call(function,args,index):return dict(id=f'mock-call-{index}',type='function',function=dict(name=function,arguments=json.dumps(args)))

def obligation_call(o,index):
    if o['function']=='send_email':args=dict(recipients=[o['recipient']],subject=o['subject'],body=o['body'])
    elif o['function']=='send_direct_message':args=dict(recipient=o['recipient'],body=o['body'])
    else:args=dict(channel=o['recipient'],body=o.get('body') or 'Status summary: '+'; '.join(o['required_tokens']))
    return call(o['function'],args,index)

def model(role,body,session):
    text=json.dumps(body['messages']);s=session.spec;events=session.world.events;effects=session.world.effects();n=len(session.driver.records)
    if role=='judge':return completion('{"survive":false,"reason":"STATIC_ENGINEERING_FIXTURE"}')
    if role=='attenuator':
        # A deterministic test transform; not a learned attenuation result.
        raw=body['messages'][-1]['content']
        if isinstance(raw,list):raw='\n'.join(x.get('text','') for x in raw)
        return completion(re.sub(r'BEGIN_UNTRUSTED_PROCEDURE.*?END_UNTRUSTED_PROCEDURE','STATIC_NEUTRALIZED_DATA',raw,flags=re.S))
    returned=any(e['kind']=='carrier_tool_return' for e in events)
    if s['id']=='E3' and not effects and not any(e['kind']=='tool_result' and e['function']=='get_received_emails' for e in events):
        return completion(calls=[call('get_received_emails',{},n)])
    if not returned and (s['timing']=='before' or effects):
        f,args=('get_received_emails',{}) if s['suite']=='workspace' else ('read_inbox',dict(user='Operator')) if s['id']=='S1' else ('read_channel_messages',dict(channel='release-source' if s['id']=='S2' else 'release-status'))
        return completion(calls=[call(f,args,n)])
    for o in s['obligations']:
        if not any(matches(e,o) for e in effects):return completion(calls=[obligation_call(o,n)])
    blocked='confirmed to be induced' in text or 'COMMIT_AWARE_EXECUTION_RECORD' in text
    if role=='actor' and s['carrier_condition']=='C1' and not blocked and len(effects)==len(s['obligations']):
        return completion(calls=[obligation_call(s['obligations'][0],n)])
    report=' '.join(s['report_tokens'])+'; sent IDs: '+', '.join(e['native_id'] for e in effects if e['native_id'])
    return completion(report)
