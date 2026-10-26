"""Execute every scheduled panel; scientific outcomes never suppress core slots."""
import copy,json,traceback,time
from pathlib import Path
from .util import write,read,ASSETS,digest,pack,args_with,Censored,InvalidParent
from .protocol import parent_key,live_item,load_parents
from .execution import make_session,calls,MockHTTP
from .graphs import canonical

def context_item(parent,slot):
    item=copy.deepcopy(parent['checkpoint']['item']);item.update(id=slot['slot_id'],panel=slot['panel'],seed=slot['seed'],origin=slot['origin'],defense='ON');item['settings']={};return item

def initial_cache(args,parent,key,directory,budget,client_factory=None,from_e1=None):
    """Original whole-set decisions stay original; singleton evidence is shared."""
    directory=Path(directory)
    if directory.exists():return read(directory/'initial_evidence.json')
    cp=parent['checkpoint'];proposed=calls(cp['pending_calls']);refs=calls(parent['batch']['reference'])
    decisions=parent['batch']['decisions']
    source=[]
    for c in proposed:
        matches=[d for d in decisions if d['actor_id']==c.id]
        if len(matches)!=1:raise InvalidParent('Initial source verdict not uniquely joined to actor occurrence')
        source.append(matches[0]['survived'])
    if from_e1 is not None:
        directory.mkdir(parents=True)
        data=dict(source_vector=source,default_vector=from_e1['default_vector'],matrix=from_e1['matrix'],
            provenance='Original archived source verdicts plus shared E1 canonical/set and singleton judgments',parent=key,source_parent_hash=cp['snapshot_hash'])
    elif '_A-P' in key:
        # Do not let a missing new singleton probe erase independently valid
        # original SOURCE or complete-lawful-release controls. Unknown edges
        # remain unknown; they cannot be used as negative verdicts.
        directory.mkdir(parents=True)
        ca=[canonical(c) for c in proposed];cr=[canonical(c) for c in refs]
        same=lambda x,y:x['function']==y['function'] and x['args']==y['args']
        default=[True if any(same(c,r) for r in cr) else None for c in ca]
        matrix=[[True if same(pack(c),pack(r)) else False if c.function!=r.function else None for r in refs] for c in proposed]
        data=dict(source_vector=source,default_vector=default,matrix=matrix,parent=key,source_parent_hash=cp['snapshot_hash'],
            provenance='E1 original encoding unavailable: original set verdicts retained; only exact canonical positives derived; all other singleton relations remain UNKNOWN',fresh_requests=0)
    else:
        item=copy.deepcopy(cp['item']);item.update(id='INITIAL_'+key,seed=20261019)
        s=make_session(args_with(args,max_requests=16),item,directory,legacy=parent['legacy'],parent=parent,
            config=dict(wire_example=parent['wire_example'],feedback='occurrence'),budget=budget,group='INITIAL_EDGES',client_factory=client_factory)
        unchanged=pack(proposed)==[canonical(c) for c in proposed] and pack(refs)==[canonical(c) for c in refs]
        errors=[]
        def attempt(c,rs,normalize=False):
            try:return s._judge(c,rs,normalize)
            except Exception as exc:errors.append(dict(actor=c.id,references=[r.id for r in rs],canonical=normalize,error=str(exc)));return None
        default=source[:] if unchanged else [attempt(c,refs,True) for c in proposed]
        matrix=[[attempt(c,[r]) for r in refs] for c in proposed]
        data=dict(source_vector=source,default_vector=default,matrix=matrix,source_parent_hash=cp['snapshot_hash'],parent=key,
            provenance='Original source verdicts; actual shared singleton queries; normalization queried only if argument representation changed',fresh_requests=s.client.fresh_count,query_errors=errors)
    if len(source)!=len(proposed) or len(data['matrix'])!=len(proposed):raise InvalidParent('Initial decision shape mismatch')
    write(directory/'initial_evidence.json',data);return data

def fixed_condition(args,slot,parent,directory,budget,client_factory=None):
    item=context_item(parent,slot)
    s=make_session(args_with(args,max_requests=8),item,directory,legacy=parent['legacy'],parent=parent,
        config=dict(wire_example=parent['wire_example']),budget=budget,group='E1',client_factory=client_factory)
    a=pack(parent['checkpoint']['pending_calls']);r=pack(parent['batch']['reference']);encoding=slot['encoding']
    def toggle(rows):
        for c in rows:
            if c['function']=='pay':
                if c['args'].get('key')=='':c['args'].pop('key',None)
                elif 'key' not in c['args']:c['args']['key']=''
                else:raise InvalidParent('Nonempty registered key is not a default-spelling treatment')
    if encoding in ('TOGGLE_ACTOR_DEFAULT','TOGGLE_BOTH_DEFAULTS'):toggle(a)
    if encoding in ('TOGGLE_REFERENCE_DEFAULT','TOGGLE_BOTH_DEFAULTS'):toggle(r)
    ac,rc=calls(a),calls(r)
    source=[s._judge(c,rc) for c in ac];default=[s._judge(c,rc,True) for c in ac]
    matrix=[[s._judge(c,[ref]) for ref in rc] for c in ac]
    from .graphs import choose
    pair0,cert0=choose(matrix,len(rc),'PAIR_M0');pair1,cert1=choose(matrix,len(rc),'PAIR_M1')
    result=dict(slot=slot,kind='FIXED_DECISION_NOT_WORKFLOW',actor=a,reference=r,source_vector=source,default_vector=default,
        matrix=matrix,pair_M0=pair0,pair_M1=pair1,certificates=[cert0,cert1],fresh_requests=s.client.fresh_count,
        archived_source_decisions=parent['batch']['decisions'],scientific_evidence=not getattr(s.client,'scripted',False))
    write(Path(directory)/'fixed_result.json',result);return result

def historical_matrix(parent,family):
    data=read(ASSETS/'historical_L3'/family/'batch_000_result.json')
    refs=data['reference'];proposed=parent['checkpoint']['pending_calls']
    if len(refs)!=1 or len(proposed)!=2:raise InvalidParent('E3 requires its authenticated single-reference/two-call exposure')
    rows=[]
    for c in proposed:
        ds=[d for d in data['decisions'] if d['actor_id']==c['id']]
        if len(ds)!=1 or len(ds[0]['reference_ids'])!=1:raise InvalidParent('Historical singleton evidence not identified')
        rows.append([ds[0]['survived']])
    if rows!=[[True],[True]]:raise InvalidParent('Historical gate does not select intended 4-unit first prefix')
    if [c['args']['amount'] for c in proposed]!=[4,6]:raise InvalidParent('Historical legal batch not actual 4+6')
    return dict(source_vector=[True,True],default_vector=[True,True],matrix=rows,provenance='Authenticated archived one-reference singleton decisions')

def continuation(args,slot,parent,initial,directory,budget,client_factory=None,repeat_policy=None):
    panel=slot['panel'];policy=repeat_policy or slot['policy'];config=dict(initial_policy=policy,future_policy='SOURCE_M0',feedback='occurrence',continuous=True,wire_example=parent['wire_example'])
    if panel=='E3':
        service=policy=='PRE_DISPATCH_SERVICE_FAILURE'
        config.update(initial_policy='RELEASE_LAWFUL_BATCH' if service else 'PAIR_M1',service_failure=service,interruption_feedback=slot['feedback'],expected_initial_prefix=4)
        initial=historical_matrix(parent,slot['model_family'])
    if panel=='E2-G':config['trusted_ledger']=True
    if panel=='E2-R':config['sample_temperature']=slot['actor_reference_temperature']
    s=make_session(args,context_item(parent,slot),directory,legacy=parent['legacy'],config=config,parent=parent,initial=initial,budget=budget,
        group='REPEATS' if panel=='E2-R' else 'MANDATORY',client_factory=client_factory)
    result=s.run()
    if panel=='E3' and s.batch_records:
        first=s.batch_records[0]['world_after'];total=sum(p['amount'] for p in first['payments'])
        if total!=4 or len(first['payments'])!=1:
            result['comparison_validity']='INVALID_INITIAL_COMMITTED_PREFIX';result['error']=result.get('error') or {'type':'InvalidInitialPrefix','message':str(first)}
        else:result['comparison_validity']='EXPECTED_FOUR_UNIT_PREFIX_REACHED'
    result.update(scheduled_slot=slot['slot_id'],evidence_unit='CONDITIONAL_FRESH_CONTINUATION',parent_checkpoint_hash=parent['checkpoint']['snapshot_hash'])
    write(Path(directory)/'result.json',result);return result

def autonomous(args,slot,directory,budget,client_factory=None):
    item,record=live_item(slot);pol=slot['policy'];config=dict(feedback='occurrence',continuous=True)
    if slot['panel']=='E4b':
        config.update(feedback='original' if pol=='SOURCE_M0_ORIGINAL' else 'occurrence',continuous=False)
        pol='SOURCE_M0' if pol.startswith('SOURCE_M0_') else pol.removesuffix('_OCCURRENCE')
    config.update(policy=pol,wire_example=record['first_payload'])
    # Source-M0 archival email preserves the original allocation path itself.
    closest=slot['panel']=='E4b' and pol in ('SOURCE_M0','OFF')
    s=make_session(args,item,directory,legacy=record['legacy'],config=config,pub_closest=closest,budget=budget,client_factory=client_factory)
    result=s.run();result.update(scheduled_slot=slot['slot_id'],evidence_unit='AUTONOMOUS_TASK_ROOT',archived_profile_source=record['source'])
    events=s.world.events
    first=next((e['effective_payload'] for e in events if e['event']=='model_request_context' and e['role']=='actor'),None)
    expected=record['first_payload']
    same=expected is not None and first==expected
    write(Path(directory)/'profile_certificate.json',dict(status='EXACT_FIRST_REQUEST_FIELDS' if same else 'PROSPECTIVE_AUTHORED_PROFILE' if expected is None else 'PROFILE_VARIATION',
        expected_first_payload=expected,actual_first_payload=first,root_hash=digest(item['spec']['root_request']),schema_and_system_hash=digest(first) if first else None,
        source_world=record['legacy'],continuous=config['continuous'],feedback=config['feedback'],original_allocation_path=closest,
        limits='Initial payload parity only. Complete later traces and route deltas remain recorded; not a full published-configuration reproduction.'))
    write(Path(directory)/'result.json',result);return result

def select_repeat(parent_results):
    priority=read(ASSETS/'REPEAT_SELECTION_RULE.json')['contrast_priority']
    for left,right in priority:
        a=parent_results.get(left);b=parent_results.get(right)
        if a is None or b is None:continue
        va=a.get('initial_admission');vb=b.get('initial_admission')
        if va and vb and va['selected_indices']!=vb['selected_indices']:
            return dict(status='TRIGGERED',left=left,right=right,basis='IDENTIFIED_INITIAL_RELEASE_VECTORS_ONLY',vectors=[va['selected_indices'],vb['selected_indices']])
    return dict(status='NOT_TRIGGERED',basis='NO_QUALIFYING_INITIAL_ADMISSION_CONTRAST')

def execute_family(args,family,out,frozen,budget,progress,client_factory=None):
    parents=load_parents();base=Path(out)/family;cache={};fixed={};e2={};failures={}
    ordering={'E1':0,'E2':1,'E2-G':2,'E2-R':3,'E3':4,'E4a-OFF':5,'E4a':6,'E4b':7,'E5':8}
    slots=sorted([s for s in frozen['slots'] if s['model_family']==family],key=lambda s:ordering[s['panel']])
    def get_initial(key):
        if key in cache:
            if isinstance(cache[key],Exception):raise InvalidParent(str(cache[key]))
            return cache[key]
        try:cache[key]=initial_cache(args,parents[key],key,base/'shared_initial'/key,budget,client_factory,fixed.get(key))
        except Exception as e:cache[key]=e;raise
        return cache[key]
    for slot in slots:
        ident=slot['slot_id'];target=base/'slots'/ident;panel=slot['panel'];progress(ident,'RUNNING');start=time.time()
        try:
            if panel=='E1':
                key=parent_key(slot);result=fixed_condition(args,slot,parents[key],target,budget,client_factory)
                if slot['encoding']=='ORIGINAL':fixed[key]=result
            elif panel in ('E2','E2-G','E3','E2-R'):
                key=parent_key(slot)
                repeat_policy=None
                if panel=='E2-R':
                    if key in failures:selection={'status':'INVALID_PARENT','reason':failures[key]}
                    elif len(e2.get(key,{}))!=5 or any(r.get('initial_admission') is None for r in e2.get(key,{}).values()):selection={'status':'INVALID_PARENT','reason':'Incomplete identified initial-admission evidence across E2 arms'}
                    else:selection=select_repeat(e2.get(key,{}))
                    write(base/'repeat_selection'/f'{key}.json',selection)
                    if selection['status']!='TRIGGERED':
                        write(target/'slot_status.json',dict(status=selection['status'],slot=slot,selection=selection));progress(ident,selection['status']);continue
                    repeat_policy=selection['left' if slot['policy'].endswith('LEFT') else 'right']
                result=continuation(args,slot,parents[key],get_initial(key),target,budget,client_factory,repeat_policy)
                if panel=='E2':e2.setdefault(key,{})[slot['policy']]=result
            else:result=autonomous(args,slot,target,budget,client_factory)
            status='CENSORED' if result.get('lifecycle_disposition')=='CENSORED' else 'RECORDED_WITH_ERROR' if result.get('error') else 'RECORDED'
            write(target/'slot_status.json',dict(status=status,slot=slot,elapsed_seconds=time.time()-start));progress(ident,status)
        except Exception as exc:
            status='INVALID_PARENT' if isinstance(exc,InvalidParent) else 'CENSORED' if isinstance(exc,Censored) else 'TECHNICAL_FAILURE'
            write(target/'slot_status.json',dict(status=status,slot=slot,error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc())))
            if panel in ('E1','E2') and isinstance(exc,InvalidParent):failures[parent_key(slot)]=str(exc)
            progress(ident,status)
    from .analysis import certify_e3
    certify_e3(base,frozen)
