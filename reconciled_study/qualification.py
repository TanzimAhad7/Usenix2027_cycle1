"""CPU/tape qualification, separate from fresh autonomous experiments."""
import copy,json
from pathlib import Path
from .util import read,write,pack,digest,checkpoint_hash
from .protocol import load_parents
from .execution import make_session

class QualificationTape:
    scripted=True
    def __init__(self,session,parent,block_next=False):
        self.session=session;self.parent=parent;self.rows=[r for r in parent['qualification_tape'] if r['role']=='judge'];self.count=0;self.fresh_count=0;self.models=[];self.usage=[];self.block_next=block_next;self.diffs=[]
    def reused(self,label,value):self.count+=1;self.session.world.event('qualification_fixed_initial_reference',label=label,evidence=value,fresh_generations=0)
    def request(self,payload,role):
        self.count+=1;self.models.append(payload['model']);self.usage.append({'reused':True})
        if role=='judge':
            if not self.rows:raise ValueError('Qualification judge tape exhausted; no model fallback')
            row=self.rows.pop(0);equal=payload==row['request'];self.diffs.append(dict(role=role,exact_request_equal=equal,expected=row['request'],actual=payload))
            raw=row['response']['choices'][0]['message']
            self.session.world.event('qualification_authenticated_response',role=role,source=row['source'],request_equal=equal,response=raw)
            return raw
        if role=='actor' and self.block_next:
            c=copy.deepcopy(self.parent['checkpoint']['pending_calls'][0]);c['id']='qualification-next-call'
            if self.session.item['transport']=='json':raw=dict(content=json.dumps(dict(content='',tool_calls=[dict(name=c['function'],arguments=c['args'])])))
            else:raw=dict(content=None,tool_calls=[dict(id=c['id'],type='function',function=dict(name=c['function'],arguments=json.dumps(c['args'])))])
            self.session.world.event('qualification_controlled_actor',role=role,response=raw,scientific=False,reason='Fixed next proposal probes routing; not autonomous model behavior')
            return raw
        raise ValueError('Unexpected qualification role: '+role)

def derive(parent,kind):
    p=copy.deepcopy(parent);cp=p['checkpoint']
    if kind=='EXACT_MATCH':
        pending=copy.deepcopy(p['batch']['reference'])
        for i,c in enumerate(pending):c['id']=f'qualification-actor-{i}'
        cp['pending_calls']=pending;cp['messages'][-1]['tool_calls']=copy.deepcopy(pending)
    if kind=='BLOCK_NEXT_REVIEW':
        cp['pending_calls']=copy.deepcopy(cp['pending_calls'][:1]);cp['messages'][-1]['tool_calls']=copy.deepcopy(cp['pending_calls'])
        p['batch']['reference']=[]
    cp['snapshot_hash']=checkpoint_hash(cp);p['batch']['checkpoint']=copy.deepcopy(cp)
    p['asset_hash']=digest({k:v for k,v in p.items() if k!='asset_hash'});return p

def qualify_profiles(args,out):
    parents=load_parents();out=Path(out);rows=[]
    for family in ('qwen','gemma'):
        for kind in ('EXACT_MATCH','DEFAULT_FUZZY_PATH','BLOCK_NEXT_REVIEW','LAWFUL_MULTI_OPERATION'):
            key=(f'{family}_R17_POLICY_M0_T0_Va0_Vr0_G0' if kind=='LAWFUL_MULTI_OPERATION' else f'{family}_R10_POLICY_M0_T0_Va0_Vr0_G0')
            if family=='qwen':key='qwen_A-P17_arm0' if kind=='LAWFUL_MULTI_OPERATION' else 'qwen_A-P10_arm0'
            p=derive(parents[key],kind);item=copy.deepcopy(p['checkpoint']['item']);item['id']=f'PUB_{family}_{kind}'
            local=copy.copy(args);local.model='qwen3-32b' if family=='qwen' else 'gemma3-27b-it'
            pair=[]
            for profile in ('PUB_CLOSEST','ADAPTED_STUDY'):
                config=dict(policy='SOURCE_M0',feedback='original' if profile=='PUB_CLOSEST' else 'occurrence',continuous=profile!='PUB_CLOSEST',
                    wire_example=p['wire_example'],stop_after_batch=kind!='BLOCK_NEXT_REVIEW',qualification_stop_next=kind=='BLOCK_NEXT_REVIEW',published_logprobs=profile=='PUB_CLOSEST')
                factory=lambda s,p=p,k=kind:QualificationTape(s,p,k=='BLOCK_NEXT_REVIEW')
                s=make_session(local,item,out/item['id']/profile,legacy=p['legacy'],parent=p,config=config,client_factory=factory,pub_closest=profile=='PUB_CLOSEST')
                result=s.run();proposals=[e for e in s.world.events if e['event']=='proposal']
                pair.append(dict(profile=profile,error=result['error'],snapshot=result['snapshot'],next_review_skip=proposals[-1]['skip_next_audit'] if len(proposals)>1 else None,
                    requests=s.client.count,fresh_requests=0,tape_request_checks=s.client.diffs,source_diff=str(s.directory/'source_changes.diff')))
            if any(x['error'] for x in pair):status='UNSUPPORTED_OR_INCOMPLETE'
            elif pair[0]['snapshot']!=pair[1]['snapshot'] or pair[0]['next_review_skip']!=pair[1]['next_review_skip']:
                status='DOCUMENTED_PROFILE_DIFFERENCE'
            elif any(not d['exact_request_equal'] for x in pair for d in x['tape_request_checks']):status='DOCUMENTED_PROFILE_DIFFERENCE'
            else:status='PARITY_ON_QUALIFIED_FIXTURE'
            row=dict(fixture_id=item['id'],status=status,profiles=pair,origin_parent=key,
                construction='Authenticated original state and judge responses; exact and block-next are declared controlled candidate/reference modifications. Block-next actor is a fixed routing probe, not model inference.',
                limits='CPU conditional path qualification only. Published cross-model deployment and generation distribution remain unreplicated.',fresh_model_requests=0)
            rows.append(row)
    write(out/'PROFILE_QUALIFICATION.json',dict(fixtures=rows,fresh_requests=0,status='RECORDED_PROFILE_SCOPE_LIMITS',published_generation_profile_reproduced=False))
    return rows

def live_transport_probes(args,family,out,budget,client_factory=None):
    """Bounded fixed-candidate probes, not extra autonomous workflows.

    Compare published logprob-request behavior with the archived adaptation
    while holding the authenticated reference fixed. Routing has CPU fixtures.
    """
    import traceback
    from .execution import calls
    parents=load_parents();out=Path(out);rows=[]
    for kind in ('EXACT_MATCH','DEFAULT_FUZZY_PATH','BLOCK_NEXT_REVIEW','LAWFUL_MULTI_OPERATION'):
        key=f'{family}_R17_POLICY_M0_T0_Va0_Vr0_G0' if kind=='LAWFUL_MULTI_OPERATION' else f'{family}_R10_POLICY_M0_T0_Va0_Vr0_G0'
        if family=='qwen':key='qwen_A-P17_arm0' if kind=='LAWFUL_MULTI_OPERATION' else 'qwen_A-P10_arm0'
        parent=derive(parents[key],kind);item=copy.deepcopy(parent['checkpoint']['item']);item['id']='LIVE_PUB_'+family+'_'+kind
        pair=[]
        for profile in ('PUB_CLOSEST','ADAPTED_STUDY'):
            directory=out/kind/profile
            try:
                config=dict(policy='SOURCE_M0',feedback='original' if profile=='PUB_CLOSEST' else 'occurrence',continuous=profile!='PUB_CLOSEST',wire_example=parent['wire_example'],published_logprobs=profile=='PUB_CLOSEST')
                s=make_session(args,item,directory,legacy=parent['legacy'],parent=parent,config=config,pub_closest=profile=='PUB_CLOSEST',budget=budget,group='PUB',client_factory=client_factory)
                vector=[s._judge(c,calls(parent['batch']['reference'])) for c in calls(parent['checkpoint']['pending_calls'])]
                row=dict(profile=profile,vector=vector,fresh_requests=s.client.fresh_count,status='FIXED_PATH_PROBE_RECORDED',
                    logprobs_requested_by_profile=profile=='PUB_CLOSEST',source_parent_hash=parents[key]['checkpoint']['snapshot_hash'],scientific_evidence=not getattr(s.client,'scripted',False))
            except Exception as exc:
                row=dict(profile=profile,status='UNSUPPORTED_OR_INCOMPLETE',error=str(exc),traceback=traceback.format_exc())
            write(directory/'probe_result.json',row);pair.append(row)
        rows.append(dict(fixture=kind,profiles=pair,scope='Fixed candidate/source-input comparison; archived common reference, no dispatch or regenerated actor. CPU qualification separately checks next-review routing.'))
    write(out/'LIVE_PROFILE_PROBES.json',dict(fixtures=rows,profile='Same pinned local model in all roles; published cross-model example not reproduced',
        fresh_requests=sum(p.get('fresh_requests',0) for r in rows for p in r['profiles']),
        limits='Source file identity plus bounded interface/path qualification. Not a complete published benchmark or model-distribution reproduction.'))
    return rows
