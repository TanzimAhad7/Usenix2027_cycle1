import copy
from .common import pack,unpack,write,digest,matches,source_sig,CHECKER_SHA,ALIAS
from .design import SETTINGS
class Context:
    def __init__(self,job,out,resume=None):
        self.job=job;self.out=out;self.setting=SETTINGS[job['setting']];self.events=[];self.driver=None;self.world=None
        self.proposal=0;self.routes={};self.default_route='INITIAL';self.invocation_role='actor';self.checkpoint=None;self.pending=None
        self.actor_exposed=bool(resume and resume['actor_exposed']);self.resume=resume
    def event(self,kind,**kwargs):
        from .common import append
        row=dict(event_index=len(self.events),kind=kind,**pack(kwargs));self.events.append(row);append(self.out/'events.jsonl',row)
    def route_for(self,function,args):return self.routes.get(source_sig(dict(function=function,args=args)),self.default_route)
    def hook(self,kind,state):
        loop=state['self']
        if kind=='proposal':
            self.proposal=state['_']+1;self.routes={};self.invocation_role='actor'
            self.default_route='SOURCE_SKIP_EMPTY' if state['skip_next_audit'] else 'SOURCE_NO_EXTERNAL_OBSERVATION' if not state['has_tool_observation'] else 'SOURCE_REVIEWED'
            monitor={k:pack(state[k]) for k in ('messages','extra_args','shadow_history','shadow_index','has_tool_observation','skip_next_audit','last_attenuated_external')}
            monitor.update(iteration=state['_'],loop_state={k:getattr(loop,k) for k in ('_last_judge_reason','_last_attenuated_external','_last_defense_input')})
            self.pending=dict(schema='R3_CONTINUATION_CHECKPOINT_V1',parent=self.job['id'],world=pack(self.world.snapshot()),monitor=monitor,actor_exposed=self.actor_exposed,model_queries_used=self.driver.used,model_record_start=len(self.driver.records),prefix_effect_count=len(self.world.effects()),job_fixture_sha256=digest(self.world.spec))
            self.event('proposal',proposal=self.proposal,calls=state['orig_calls'],route=self.default_route,pre_state_sha256=digest(self.world.snapshot()))
        elif kind=='reference_start':self.invocation_role='reference'
        elif kind=='reference_end':self.invocation_role='actor'
        elif kind=='reference_ready':self.event('reference',proposal=self.proposal,calls=state['shadow_calls'])
        elif kind=='admission':
            self.event('admission',proposal=self.proposal,allowed=state['executed_calls'],blocked=state['blocked_calls'],references=state['shadow_calls'],routes=[dict(call=pack(c),route=self.route_for(c.function,c.args)) for c in state['orig_calls']])
            target=self.world.spec['attack_targets']['PARAMETER']
            eligible=any(matches(c,target) for c in state['blocked_calls'])
            if self.job['kind']=='FULL' and self.job['setting']=='A' and eligible and self.checkpoint is None:
                cp=copy.deepcopy(self.pending);cp['frozen_model_replies']=copy.deepcopy(self.driver.records[cp.pop('model_record_start'):]);cp['prefix_qualified']=True;cp['source_checker_sha256']=CHECKER_SHA;cp['model_alias']=ALIAS;cp['limits']=copy.deepcopy(self.job['limits'])
                cp['checkpoint_digest']=digest(cp);self.checkpoint=cp;write(self.out/'checkpoint.json',cp)
                self.event('checkpoint_selected',proposal=self.proposal,checkpoint_digest=cp['checkpoint_digest'],selection='FIRST_SOURCE_DENIAL_OF_PREDECLARED_PARAMETER_TARGET',conditioned_on_future_outcome=False)
