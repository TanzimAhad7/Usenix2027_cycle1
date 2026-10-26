"""Authored payment world and stock AgentDojo Inbox; no external effects."""
from __future__ import annotations
import copy
import datetime
import json
import time
from pathlib import Path
from types import SimpleNamespace
from agentdojo.default_suites.v1.tools import email_client
from agentdojo.functions_runtime import FunctionsRuntime, TaskEnvironment
from agentdojo.default_suites.v1.tools.email_client import Inbox, EmailContact, send_email, get_received_emails
from agentdojo.default_suites.v1.tools.types import Email, EmailStatus
from .common import pack

class Environment(TaskEnvironment): inbox: Inbox

class SimulatedClock:
    @staticmethod
    def now(tz=None):return datetime.datetime(2026,10,22,12,0,0,tzinfo=tz)

class World:
    def __init__(self,spec,directory,restore=None,gate=False):
        self.spec=copy.deepcopy(spec);self.directory=Path(directory);self.events=[];self.queue=[];self.active_id=None
        self.payments=[];self.keys={};self.pre_reads=0;self.post_reads=0;self.retries=0;self.read_counts=[]
        self.carrier_delivered=False;self.notice_created=False;self.carrier_records=[];self.gate=gate;self.fail_after_commit=False
        self.env=Environment(inbox=Inbox(account_email='researcher@example.com',initial_emails=[]))
        if restore:
            # Inbox's initialization validator rebuilds emails from initial_emails.
            # Round-tripping model_validate would silently erase live sent records.
            # Recreate typed fields without rerunning that initialization routine.
            raw=restore['env']['inbox']
            inbox=Inbox.model_construct(account_email=raw['account_email'],
                initial_emails=[Email.model_validate(e) for e in raw['initial_emails']],
                emails={k:Email.model_validate(e) for k,e in raw['emails'].items()},
                contact_list=[EmailContact.model_validate(e) for e in raw['contact_list']],
                trash={k:Email.model_validate(e) for k,e in raw['trash'].items()})
            self.env=Environment.model_construct(inbox=inbox);self.payments=copy.deepcopy(restore['payments'])
            self.keys=copy.deepcopy(restore['keys'])
            for k in ('pre_reads','post_reads','retries','carrier_delivered','notice_created','read_counts','carrier_records'):setattr(self,k,copy.deepcopy(restore[k]))
        elif spec['family']=='email' and not spec['late']: self.add_notice()
        self.event('world_initial',snapshot=self.snapshot(),gate=gate)

    def event(self,event,**fields):
        row=pack(dict(seq=len(self.events),epoch=time.time(),event=event,**fields));self.events.append(row)
        with (self.directory/'events.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush()

    def snapshot(self):
        return pack(dict(env=self.env,payments=self.payments,keys=self.keys,pre_reads=self.pre_reads,
            post_reads=self.post_reads,retries=self.retries,carrier_delivered=self.carrier_delivered,
            notice_created=self.notice_created,read_counts=self.read_counts,carrier_records=self.carrier_records))

    def count(self): return len(self.env.inbox.sent) if self.spec['family']=='email' else len(self.payments)

    def add_notice(self):
        if self.notice_created:return
        ident=str(max([int(x) for x in self.env.inbox.emails]+[100])+1)
        mail=Email(id_=ident,sender='notices@example.com',recipients=['researcher@example.com'],
            subject=self.spec['fact'],body=self.spec['notice_body'],status=EmailStatus.received,
            timestamp='2026-10-22T12:00:00')
        self.env.inbox.emails[ident]=mail;self.notice_created=True
        self.event('notice_available',notice_id=ident,after_committed_count=self.count())

    def pay(self,recipient,amount,key=''):
        if recipient!=self.spec['recipient']:raise ValueError('Unknown account_id; use get_iban result')
        if type(amount) is not int or amount<=0:raise ValueError('Positive integer required')
        identity=[recipient,amount]
        if key and key in self.keys:
            if self.keys[key]!=identity:raise ValueError('Conflicting registered key')
            self.retries+=1;self.event('idempotent_retry',occurrence_id=self.active_id,key=key)
            return dict(status='already_committed',effect_id=next(e['effect_id'] for e in self.payments if e['key']==key))
        # Explicit trusted-state control. This implementation is not the observer.
        if self.gate and (len(self.payments)>=self.spec['max_count'] or
            sum(e['amount'] for e in self.payments)+amount>self.spec['max_total'] or
            (self.spec['exact_amount'] is not None and amount!=self.spec['exact_amount'])):
            raise PermissionError('Application remaining permission denies a new effect')
        effect=dict(effect_id=f'payment-{len(self.payments)+1}',recipient=recipient,amount=amount,key=key,
                    occurrence_id=self.active_id)
        self.payments.append(effect)
        if key:self.keys[key]=identity
        return dict(status='committed',effect_id=effect['effect_id'])

    def make_runtime(self):
        world=self;runtime=FunctionsRuntime()
        if self.spec['family']=='email':
            runtime.register_function(send_email);runtime.register_function(get_received_emails)
        else:
            @runtime.register_function
            def get_iban(name:str)->str:
                """Read the beneficiary account and directory/status notice.

                :param name: Exact beneficiary person name.
                """
                if name!=world.spec['person']:raise ValueError('Unknown person')
                visible=not world.spec['late'] or world.count()>0
                return json.dumps(dict(person=name,account_id=world.spec['recipient'],
                    directory_note=world.spec['notice_body'] if visible else 'No follow-up notice is available yet.'))
            @runtime.register_function
            def pay(recipient:str,amount:int,key:str='')->dict:
                """Commit one simulated payment. Nonempty registered keys make identical retries effect-free.

                :param recipient: Exact account_id.
                :param amount: Positive integer units.
                :param key: Empty for an independent payment, otherwise a retry identity.
                """
                return world.pay(recipient,amount,key)
        original=runtime.run_function
        def traced(env,function,kwargs,raise_on_error=False):
            world.active_id=world.queue.pop(0) if world.queue else 'UNJOINED'
            before=world.snapshot();count_before=world.count()
            world.event('dispatch',occurrence_id=world.active_id,function=function,args=kwargs,before=before)
            is_read=function in ('get_received_emails','get_iban')
            if world.gate and function=='send_email' and (world.count()>=world.spec['max_count'] or
                 kwargs.get('recipients')!=[world.spec['recipient']] or kwargs.get('subject')!=world.spec['subject'] or
                 kwargs.get('body')!=world.spec['body'] or any(kwargs.get(k) for k in ('cc','bcc','attachments'))):
                result,error=None,'Application single-use permission denies this send'
            elif function=='send_email':
                # A declared fixed simulator clock removes timestamp drift across
                # counterfactual forks. Native send logic and IDs are unchanged.
                # This controller dispatches synchronously, never concurrently.
                saved_clock=email_client.datetime
                try:
                    email_client.datetime=SimpleNamespace(datetime=SimulatedClock)
                    result,error=original(env,function,kwargs,raise_on_error=raise_on_error)
                finally:email_client.datetime=saved_clock
            else: result,error=original(env,function,kwargs,raise_on_error=raise_on_error)
            after_count=world.count()
            if after_count>count_before:
                world.event('commit',occurrence_id=world.active_id,function=function,before_count=count_before,
                            after_count=after_count,state=world.snapshot())
                if world.spec['late'] and after_count==1 and world.spec['family']=='email':world.add_notice()
                if world.fail_after_commit:result,error=None,'Injected CPU diagnostic error after commit'
            if is_read and not error:
                world.read_counts.append(count_before)
                if count_before:world.post_reads+=1
                else:world.pre_reads+=1
                visible=not world.spec['late'] or count_before>0
                if visible:
                    world.carrier_delivered=True
                    world.carrier_records.append(pack(dict(occurrence_id=world.active_id,function=function,
                        args=kwargs,raw_result=result,after_committed_count=count_before)))
                    world.event('carrier_delivery',occurrence_id=world.active_id,hostile=world.spec['condition']=='hostile',
                                after_committed_count=count_before,notice=world.spec['notice_body'])
            world.event('runtime_result',occurrence_id=world.active_id,result=result,error=error,after=world.snapshot())
            return result,error
        runtime.run_function=traced
        return runtime

