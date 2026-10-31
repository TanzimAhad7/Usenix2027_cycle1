"""Run unedited source; trace pauses occur immediately before side effects."""
import ast,copy,importlib,importlib.metadata,inspect,sys
from pathlib import Path
from .common import PACKAGE,Invalid,Pause,pack,digest,file_hash,native_messages,write

def load_source():
    directory=PACKAGE/'vendor'
    if str(directory) not in sys.path:sys.path.insert(0,str(directory))
    for name in ['AttriGuard','openai_llm_compat','local_llm_compat','my_agent_pipeline']:
        module=importlib.import_module(name)
        if Path(module.__file__).resolve()!=directory/(name+'.py'):raise Invalid('INVALID_PROFILE: foreign module '+name)
    return sys.modules['AttriGuard'],sys.modules['my_agent_pipeline']

def verify_source():
    if importlib.metadata.version('agentdojo')!='0.1.35':raise Invalid('INVALID_PROFILE: agentdojo==0.1.35 required')
    from .common import read
    identity=read(PACKAGE/'vendor/SOURCE_IDENTITY.json')
    for name,expected in identity['files'].items():
        if file_hash(PACKAGE/'vendor'/name)!=expected:raise Invalid('INVALID_PROFILE: release source drift '+name)
    runtime={}
    for name,expected in read(PACKAGE/'RUNTIME_HASHES.json').items():
        m=importlib.import_module(name);p=Path(inspect.getfile(m));actual=file_hash(p)
        runtime[name]=dict(path=str(p),sha256=actual)
        if actual!=expected:raise Invalid('INVALID_PROFILE: native runtime drift '+name)
    return dict(release=identity,runtime=runtime,agentdojo=importlib.metadata.version('agentdojo'))

def input_record(query,runtime,env,messages,extra_args):
    return pack(dict(query=query,messages=messages,extra_args=extra_args,
        schema=[dict(name=f.name,description=f.description,parameters=f.parameters.model_json_schema()) for f in runtime.functions.values()],
        environment=env))

class RecordPolicy:
    def __init__(self,policy,directory,label):self.policy=policy;self.directory=directory;self.label=label;self.records=[]
    def query(self,query,runtime,env,messages,extra_args):
        before=input_record(query,runtime,env,messages,extra_args)
        result=self.policy.query(query,runtime,env,messages,extra_args)
        row=dict(input=before,input_hash=digest(before),messages=pack(result[3]),extra_args=pack(result[4]))
        self.records.append(row);write(self.directory/(self.label+'_policy_records.json'),self.records)
        return result

class ReplayPolicy:
    def __init__(self,records,label):self.records=copy.deepcopy(records);self.label=label;self.cursor=0;self.checks=[]
    def query(self,query,runtime,env,messages,extra_args):
        if self.cursor>=len(self.records):raise Invalid('INVALID_PROFILE: unrecorded '+self.label+' query; no fresh fallback')
        row=self.records[self.cursor];self.cursor+=1
        actual=input_record(query,runtime,env,messages,extra_args)
        self.checks.append(dict(label=self.label,input_hash=digest(actual),recorded_input_hash=row['input_hash'],equal=actual==row['input']))
        if actual!=row['input']:raise Invalid('INVALID_INTERVENTION: shared '+self.label+' input changed')
        return query,runtime,env,native_messages(row['messages']),copy.deepcopy(row['extra_args'])
    def complete(self):
        if self.cursor!=len(self.records):raise Invalid('INVALID_PROFILE: unused '+self.label+' evidence')

def source_pause(loop,query,world,messages,phase):
    """No source rewrite. Stop at a verified unique query-line boundary."""
    core,_=load_source();path=Path(core.__file__)
    anchor='            shadow_sigs = {_call_signature(c) for c in shadow_calls}' if phase=='reference' else '            executed_results = _execute_calls('
    lines=path.read_text().splitlines();matches=[i for i,s in enumerate(lines,1) if s==anchor]
    if len(matches)!=1:raise Invalid('INVALID_PROFILE: source trace anchor drift')
    target=matches[0];previous=sys.gettrace()
    def trace(frame,event,arg):
        if frame.f_code is not core.AttriGuardExecutionLoop.query.__code__:return None
        if event=='line' and frame.f_code.co_filename==str(path) and frame.f_code.co_name=='query' and frame.f_lineno==target:
            f=frame.f_locals
            data=dict(phase=phase,shadow_context=pack(f['shadow_context']),reference=pack(f['shadow_calls']),
                pending=pack(f['orig_calls']),has_tool_observation=f['has_tool_observation'],
                trace_line=target,source_sha256=file_hash(path),shadow_history=pack(f['shadow_history']))
            if phase=='admission':data.update(released=pack(f['executed_calls']),blocked=pack(f['blocked_calls']),reasons=pack(f['call_reasons']))
            raise Pause(data)
        return trace
    sys.settrace(trace)
    try:
        loop.query(query,world.runtime,world.env,native_messages(messages),{})
    except Pause as stop:return stop.data
    finally:sys.settrace(previous)
    raise Invalid('INVALID_ORIGIN: source did not reach reviewed '+phase+' boundary')

def make_loop(reference,attenuator,judge,mode):
    core,_=load_source()
    loop=core.AttriGuardExecutionLoop(reference,attenuation_llm=attenuator,judge_llm=judge,
        attenuation_level=2,survival_mode='fuzzy',max_iters=1,debug=True)
    transforms=[]
    original=loop._attenuate_observation
    def transformation(text,runtime,env):
        result=original(text,runtime,env) if mode=='ATTENUATE' else text
        transforms.append(dict(mode=mode,input=text,output=result,input_hash=digest(text),output_hash=digest(result)))
        return result
    loop._attenuate_observation=transformation
    return loop,transforms

def occurrence_spy(loop,reference,candidates,driver):
    core,_=load_source();original=loop._fuzzy_survive;rows=[]
    def survive(call,refs,query,runtime,env):
        index=len(rows)
        if index>=len(candidates) or pack(call)!=pack(candidates[index]):raise Invalid('INVALID_PROFILE: occurrence order drift')
        exact=[i for i,r in enumerate(refs) if core._call_signature(call)==core._call_signature(r)]
        same=[i for i,r in enumerate(refs) if r.function==call.function]
        start=len(driver.records)
        answer=original(call,refs,query,runtime,env)
        requests=driver.records[start:]
        route='EXACT' if exact else 'ABSENT_FUNCTION' if not same else 'FUZZY'
        rows.append(dict(occurrence=index,call=pack(call),route=route,exact_reference_indices=exact,
            same_function_indices=same,survived=bool(answer),judge_request_indices=[r['index'] for r in requests],
            source_reason=loop._last_judge_reason,source_reason_can_be_stale=bool(exact),
            judge_invoked=bool(requests)))
        return answer
    loop._fuzzy_survive=survive
    return rows
