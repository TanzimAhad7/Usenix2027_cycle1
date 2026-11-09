"""Authored discovery worlds; native AgentDojo tools and durable-state observer."""
import copy,datetime
from agentdojo.task_suite.load_suites import get_suite
from agentdojo.functions_runtime import FunctionsRuntime
from agentdojo.default_suites.v1.tools.email_client import Inbox
from agentdojo.default_suites.v1.tools.types import Email,EmailStatus
from agentdojo.default_suites.v1.tools.banking_client import BankAccount,Transaction
from .common import digest,matches,rank,write,violation_indices
from .checkpoint_state import restore_environment
from .effects import extract
SENSITIVE={'send_money','send_email'}
TOOLS={'banking':{'send_money','get_most_recent_transactions','get_scheduled_transactions','get_balance','get_iban'},'workspace':{'send_email','get_received_emails','get_sent_emails','search_emails','get_unread_emails'}}
class World:
    def __init__(self,spec,context,restore=None):
        self.spec=copy.deepcopy(spec);self.ctx=context;context.world=self
        self.suite=get_suite('v1',spec['suite']);self.env=self.suite.load_and_inject_default_environment({})
        self.notice_stage=0
        if restore is not None:
            self.env=restore_environment(type(self.env),restore['environment'],spec['suite']);self.notice_stage=restore['notice_stage']
        else:
            if spec['suite']=='banking':self.env.bank_account=BankAccount(balance=10000,iban='DE0000000000',transactions=[],scheduled_transactions=[])
            else:self.env.inbox=Inbox(account_email='operator@example.com',initial_emails=[])
            self.notice(1)
        self.runtime=self.make_runtime()
    def effects(self):return extract(self.env,self.spec['suite'])
    def snapshot(self):return dict(environment=self.env.model_dump(mode='json'),notice_stage=self.notice_stage)
    def notice(self,stage):
        body=self.spec['notices'][stage-1]
        if self.spec['suite']=='banking':
            b=self.env.bank_account;idx=max([t.id for t in b.transactions]+[0])+1
            b.transactions.append(Transaction(id=idx,sender='EXTERNAL-NOTICE',recipient=b.iban,amount=0,subject=body,date='2026-10-25',recurring=False))
        else:
            m=Email(id_=self.env.inbox._get_next_id(),sender='notices@example.com',recipients=[self.env.inbox.account_email],subject='Dispatch notice '+self.spec['id'],body=body,status=EmailStatus.received,read=False,timestamp=datetime.datetime(2026,10,25,9),attachments=[],cc=[],bcc=[])
            self.env.inbox.emails[m.id_]=m
        self.notice_stage=stage;self.ctx.event('environment_notification',stage=stage,body=body)
    def permitted(self,function,kwargs):
        if function not in SENSITIVE:return True
        # Mirror the native argument validation/coercion before judging physical effects.
        # Raw source signatures and model messages remain untouched.
        try:validated=self.runtime.functions[function].parameters.model_validate(kwargs).model_dump()
        except Exception:return False
        before=self.effects();slots=self.spec['choice_contract']['slots'];candidate=dict(function=function,args=validated)
        return rank(before+[candidate],slots)>rank(before,slots)
    def make_runtime(self):
        world=self
        class ObservedRuntime(FunctionsRuntime):
            def run_function(self,env,function,kwargs,raise_on_error=False):
                before=world.effects();ids={e['id'] for e in before};route=world.ctx.route_for(function,kwargs)
                world.ctx.event('dispatch',function=function,args=kwargs,route=route,proposal=world.ctx.proposal,before_state_sha256=digest(world.snapshot()))
                if world.ctx.setting['contract_gate'] and not world.permitted(function,kwargs):
                    error='PermissionError: R3 diagnostic current-state contract gate denied dispatch'
                    world.ctx.event('contract_gate_denial',function=function,args=kwargs,route=route)
                    if raise_on_error:raise PermissionError(error)
                    value=''
                else:value,error=super().run_function(env,function,kwargs,raise_on_error)
                new=[e for e in world.effects() if e['id'] not in ids]
                for e in new:world.ctx.event('commit',effect=e,route=route,proposal=world.ctx.proposal,actor_exposed=world.ctx.actor_exposed)
                if world.spec['shape']=='STAGED' and world.notice_stage==1 and any(matches(e,world.spec['stage_operations'][0]) for e in world.effects()):world.notice(2)
                world.ctx.event('tool_result',function=function,args=kwargs,value=value,error=error,route=route)
                effects=world.effects();write(world.ctx.out/'live_state_receipt.json',dict(world=world.snapshot(),effects=effects,violation_indices=violation_indices(effects,world.spec['choice_contract']['slots']),through_event_index=len(world.ctx.events)-1))
                return value,error
        return ObservedRuntime([f for f in self.suite.tools if f.name in TOOLS[self.spec['suite']]])
