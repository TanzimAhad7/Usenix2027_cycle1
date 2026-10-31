"""Scripted engineering responses only; never counted as research evidence."""
import json,re
from .effects import matches
from .protocol import malicious_operation
from .base.transport import reply,httpx

def call(op,index):return dict(id=f'mock-{index}',type='function',function=dict(name=op['function'],arguments=json.dumps(op['args'])))

def model(role,body,session):
    s=session.spec;effects=session.world.effects();events=session.world.events;n=len(session.driver.records)
    if role=='judge':return reply('{"survive": false, "reason": "mock"}')
    if role=='attenuator':
        raw=body['messages'][-1]['content']
        if isinstance(raw,list):raw='\n'.join(x.get('text','') for x in raw)
        return reply(re.sub(r'BEGIN_UNTRUSTED_PROCEDURE.*?END_UNTRUSTED_PROCEDURE','NEUTRALIZED_ENGINEERING_DATA',raw,flags=re.S))
    observed=[e for e in events if e['kind']=='carrier_tool_return']
    if session.world.carrier_created and not any(session.world.notice_stage in e.get('stages',[1]) for e in observed):return reply(calls=[call(s['read_call'],n)],finish='tool_calls')
    remaining=list(s['obligations'])
    for e in effects:
        i=next((i for i,o in enumerate(remaining) if matches(e,o)),None)
        if i is not None:remaining.pop(i)
    if remaining:
        # For the final batch, deliberately construct exact duplicate proposals
        # in hostile mocks, but only one reference occurrence. This validates
        # measurement and the declared capacity comparator, not model behavior.
        op=remaining[0];count=sum(matches(o,op) for o in remaining)
        if role=='reference':count=1
        elif s['carrier_condition'] in ['HOSTILE','COUNT'] and session.world.carrier_created:count+=1
        if role=='actor' and s['carrier_condition'] in ['RECIPIENT','PARAMETER'] and session.world.carrier_created:
            # Exactly one attempted substitution; recover after a block or
            # after the substitution commits. Scripted engineering, not an LLM.
            wrong=malicious_operation(op,s['family'],s['carrier_condition'])
            attempted=any(e['kind']=='proposal' and any(c['function']==wrong['function'] and c['args']==wrong['args'] for c in e['calls']) for e in events)
            if not attempted:op=wrong
        return reply(calls=[call(op,n*10+i) for i in range(count)],finish='tool_calls')
    return reply('Completed. '+s['report_code'])

def failure(role,body,session):raise httpx.ReadError('Injected zero-retry workflow failure')
