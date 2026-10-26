"""Offline engineering responses; never scientific model evidence."""
import json
from ..common import write

class FixtureClient:
    scripted=True
    restart_full=False
    def __init__(self,session):self.session=session;self.count=0;self.models=[];self.usage=[];self.actor_count=0
    def request(self,payload,role):
        self.count+=1;s=self.session;spec=s.spec;calls=[];text=''
        def pay(n,key=''):return dict(name='pay',arguments=dict(recipient=spec['recipient'],amount=n,key=key))
        def send(recipients=None):return dict(name='send_email',arguments=dict(recipients=recipients or [spec['recipient']],subject=spec['subject'],body=spec['body']))
        if role=='attenuator':text=payload['messages'][-1]['content']
        elif role=='judge':text=json.dumps(dict(survive=True,reason='CPU_FIXTURE_SEMANTIC_ACCEPTANCE'))
        elif role=='reference':
            pending=(s.current or {}).get('pending_calls',[])
            if spec.get('split') and not s.world.payments:calls=[pay(spec['max_total'])]
            else:calls=[dict(name=c['function'],arguments=c['args']) for c in pending[:1]]
        else:
            self.actor_count+=1
            if self.actor_count==1 and not spec.get('late'):
                calls=[dict(name='get_received_emails',arguments={})] if spec['family']=='email' else [dict(name='get_iban',arguments={'name':'Alice'})]
            elif spec['family']=='email':
                sent=list(s.world.env.inbox.sent)
                if spec.get('late') and self.actor_count==2:calls=[dict(name='get_received_emails',arguments={})]
                elif spec.get('recipient_wise'):
                    used={r for e in sent for r in e.recipients};calls=[send([r]) for r in spec['recipients'] if r not in used]
                elif len(sent)<spec['required_count']:calls=[send()]*(spec['required_count']-len(sent))
                elif spec['condition']=='hostile' and self.actor_count<=3:calls=[send()]
                text='Committed identifiers: '+', '.join(str(e.id_) for e in sent)
            else:
                total=sum(e['amount'] for e in s.world.payments)
                if spec.get('registered_key') and not s.world.retries:calls=[pay(spec['amount'],spec['registered_key'])]
                elif total<spec.get('target_total',spec['max_total']):
                    if spec.get('split') and not s.world.payments and s.item['panel']=='A':calls=[pay(n) for n in spec['split']]
                    else:calls=[pay(spec['max_total'] if self.restart_full and spec.get('split') else min(spec['amount'],spec['max_total']-total))]
                text='Committed identifiers: '+', '.join(e['effect_id'] for e in s.world.payments)
        if role in ('actor','reference'):
            if s.item['transport']=='native':raw=dict(role='assistant',content=text,tool_calls=[dict(id=f'{role}-{s.id_offset+self.count}-{i}',type='function',function=dict(name=c['name'],arguments=json.dumps(c['arguments']))) for i,c in enumerate(calls)])
            else:raw=dict(role='assistant',content=json.dumps(dict(content=text,tool_calls=calls)))
        else:raw=dict(role='assistant',content=text)
        data=dict(model=s.args.model,usage={},choices=[dict(message=raw,finish_reason='stop')])
        p=s.directory/f'http_{self.count:03d}_{role}';write(p.with_suffix('.request.json'),payload);write(p.with_suffix('.response.json'),data)
        write(p.with_suffix('.scripted.json'),dict(evidence_class='CPU_ENGINEERING_FIXTURE',model_generations=0))
        self.models.append(s.args.model);self.usage.append({});return raw
