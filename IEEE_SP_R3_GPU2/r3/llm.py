"""Observe the official LocalLLM; preserve its prompts, parser and role decoding."""
import copy,json,time
import httpx
from .common import ALIAS,PORT,ROOT,ReplayMismatch,IncompleteResponse,pack,unpack,digest,append,write
class WireTransport(httpx.BaseTransport):
    def __init__(self,driver,role):self.driver=driver;self.role=role;self.inner=httpx.HTTPTransport(retries=0)
    def handle_request(self,request):
        if request.url.host not in ('127.0.0.1','localhost') or request.url.port!=PORT:
            raise RuntimeError('R3 permits only its owned local endpoint')
        rec=dict(index=len(self.driver.wires),role=self.role,method=request.method,path=request.url.path,request=json.loads(request.read()),started_epoch=time.time())
        try:
            response=self.inner.handle_request(request);body=response.read();rec['status']=response.status_code
            try:rec['response']=json.loads(body)
            except ValueError:rec['response_text']=body.decode(errors='replace')
            good=response.status_code==200 and bool(rec.get('response',{}).get('choices'))
            rec['complete']=good and all(c.get('finish_reason')=='stop' for c in rec.get('response',{}).get('choices',[]))
            headers=response.headers;response.close()
            return httpx.Response(rec['status'],headers=headers,content=body,request=request)
        except BaseException as exc:
            rec.update(complete=False,error=dict(type=type(exc).__name__,message=str(exc)));raise
        finally:
            rec['elapsed_seconds']=time.time()-rec['started_epoch'];self.driver.wires.append(rec);append(self.driver.ctx.out/'wire.jsonl',rec)
    def close(self):self.inner.close()
class Driver:
    def __init__(self,ctx,frozen=None):
        self.ctx=ctx;ctx.driver=self;self.records=[];self.wires=[];self.frozen=copy.deepcopy(frozen or[]);self.replay_index=0
        self.used=0 if ctx.resume is None else ctx.resume['model_queries_used'];self.clients=[];self.qualification_only=False
    def wrap(self,inner,role):
        old=inner.client
        client=old.with_options(max_retries=0,timeout=self.ctx.job['limits']['request_timeout_seconds'],http_client=httpx.Client(transport=WireTransport(self,role),trust_env=False))
        inner.client=client;old.close();self.clients.append(client)
        return RecordedLLM(inner,self,role)
    def close(self):
        for c in self.clients:c.close()
class RecordedLLM:
    def __init__(self,inner,driver,role):self.inner=inner;self.driver=driver;self.role=role
    def query(self,query,runtime,env,messages,extra_args):
        d=self.driver;c=d.ctx;role=c.invocation_role if self.role=='actor_reference' else self.role
        if d.used>=c.job['limits']['max_model_queries']:raise IncompleteResponse('Frozen model-query budget exhausted')
        request=pack(dict(client_parameters={k:getattr(self.inner,k) for k in ('model','temperature','top_p','reasoning_effort','tool_delimiter')},query=query,messages=messages,extra_args=extra_args,tools={n:f.parameters.model_json_schema() for n,f in sorted(runtime.functions.items())},environment=env.model_dump(mode='json') if hasattr(env,'model_dump') else None))
        key=digest(request);d.used+=1
        if d.replay_index<len(d.frozen):
            frozen=d.frozen[d.replay_index]
            if frozen['role']!=role or frozen['input_sha256']!=key:raise ReplayMismatch('Frozen reply input differs at '+str(d.replay_index))
            d.replay_index+=1;message=unpack(frozen['assistant']);response=(*[query,runtime,env],[*messages,message],unpack(frozen['returned_extra']))
            record=dict(index=len(d.records),role=role,input_sha256=key,input=request,assistant=pack(message),returned_extra=frozen['returned_extra'],acquisition='FROZEN_MATCHED_REPLY',parent_record_index=frozen['index'])
        else:
            before=len(d.wires);response=self.inner.query(query,runtime,env,messages,extra_args)
            added=d.wires[before:]
            if not added or any(not x.get('complete') for x in added):raise IncompleteResponse('Incomplete local model transport; official empty-output fallback is retained but not counted as a safe result')
            if len(response[3])!=len(messages)+1 or response[3][-1].get('role')!='assistant':raise IncompleteResponse('Unexpected official client output envelope')
            message=response[3][-1]
            record=dict(index=len(d.records),role=role,input_sha256=key,input=request,assistant=pack(message),returned_extra=pack(response[4]),acquisition='FRESH_MODEL',wire_indices=[r['index'] for r in added])
        text=json.dumps(pack(message.get('content')));record['function_tag_without_parsed_call']='<function' in text and not bool(message.get('tool_calls'))
        d.records.append(record);append(c.out/'model_queries.jsonl',record)
        if role=='actor' and 'BEGIN_UNTRUSTED_PROCEDURE' in json.dumps(request['messages']):c.actor_exposed=True
        c.event('model_reply',role=role,acquisition=record['acquisition'],input_sha256=key,model_queries_used=d.used)
        return response

def build_pipeline(ctx,frozen=None):
    import importlib,os,sys
    from .guard import module_for,observe_loop
    if str(ROOT/'vendor') not in sys.path:sys.path.insert(0,str(ROOT/'vendor'))
    for key in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'):os.environ.pop(key,None)
    os.environ.update(LOCAL_LLM_PORT=str(PORT),ATTRIGUARD_BACKEND='local',ATTRIGUARD_MODEL_ID=ALIAS,ATTRIGUARD_JUDGE_MODEL_ID=ALIAS,ATTRIGUARD_LOCAL_PORT=str(PORT),ATTRIGUARD_LOCAL_JUDGE_PORT=str(PORT),ATTRIGUARD_LEVEL='2',ATTRIGUARD_SURVIVAL='fuzzy',ATTRIGUARD_SKIP_EMPTY_AUDIT='1',ATTRIGUARD_DEBUG='0')
    api=importlib.import_module('my_agent_pipeline');module,generated,hooks=module_for(ctx);api.AttriGuardExecutionLoop=module.AttriGuardExecutionLoop
    config=api.PipelineConfig(llm='local',model_id=ALIAS,defense='attriguard',tool_delimiter='tool',system_message_name=None,system_message=None,tool_output_format=None,attack=None,suite_name=ctx.world.spec['suite'])
    pipeline=api.AgentPipeline.from_config(config);loop=pipeline.elements[-1];driver=Driver(ctx,frozen)
    roles={'actor_reference':pipeline.elements[-2],'attenuator':loop.attenuation_llm,'judge':loop.judge_llm}
    identity={name:dict(class_name=type(llm).__module__+'.'+type(llm).__name__,model=llm.model,temperature=llm.temperature,top_p=llm.top_p,reasoning_effort=llm.reasoning_effort,tool_delimiter=llm.tool_delimiter) for name,llm in roles.items()}
    actor=driver.wrap(roles['actor_reference'],'actor_reference');pipeline.elements[-2]=actor;loop.llm=actor
    loop.attenuation_llm=driver.wrap(roles['attenuator'],'attenuator');loop.judge_llm=driver.wrap(roles['judge'],'judge')
    loop.max_iters=ctx.job['limits']['max_iters'];observe_loop(loop,ctx)
    write(ctx.out/'construction.json',dict(configuration=pack(config),roles=identity,hooks=hooks,transport_retry_policy='ZERO_RETRIES',scope='Official generic local Qwen constructor and interface; same model for actor/reference/attenuation/judge. Not the paper principal GPT configuration or the Llama-target README example.'))
    (ctx.out/'instrumented_guard.py').write_text(generated)
    return pipeline,loop,driver
