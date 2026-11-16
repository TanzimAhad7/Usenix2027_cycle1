"""Retained release constructors/serializers with explicit, zero-retry I/O."""
import contextlib,copy,os,time,json,sys
from types import SimpleNamespace
from unittest.mock import patch
import openai
from openai import _base_client
from .common import MODEL,ModelFailure,pack,digest,write
from .source import load_source
httpx=getattr(_base_client,'httpx',None) or _base_client.httpx2

@contextlib.contextmanager
def profile_env():
    values=dict(OPENAI_API_KEY='EMPTY',OPENAI_BASE_URL='http://127.0.0.1:18080/v1',LOCAL_LLM_PORT='18080',
        ATTRIGUARD_BACKEND='openai',ATTRIGUARD_MODEL_ID=MODEL,ATTRIGUARD_JUDGE_MODEL_ID=MODEL,ATTRIGUARD_API_KEY='EMPTY')
    prior={k:os.environ.get(k) for k in values};proxies={k:os.environ.pop(k) for k in
        ['HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'] if k in os.environ}
    os.environ.update(values)
    try:yield
    finally:
        for k,v in prior.items():
            if v is None:os.environ.pop(k,None)
            else:os.environ[k]=v
        os.environ.update(proxies)

def wire(kwargs):return {k:pack(v) for k,v in kwargs.items() if v.__class__.__name__ not in ['NotGiven','Omit']}

class Driver:
    def __init__(self,directory,mock=None):
        self.directory=directory;directory.mkdir(parents=True,exist_ok=True)
        self.mock=mock;self.records=[];self.http=[];self.clients=[];self.role=None;self.active=None
        core,factory=load_source()
        compat=sys.modules['openai_llm_compat']
        no_retry_request=getattr(compat.chat_completion_request,'__wrapped__',None)
        if no_retry_request is None:raise ModelFailure('Source retry decorator identity changed')
        def discovery(url,*args,**kwargs):
            if url!='http://localhost:18080/v1/models':raise ModelFailure('Unexpected model discovery endpoint')
            if mock is not None:data=dict(data=[dict(id=MODEL)])
            else:
                with httpx.Client(timeout=10,trust_env=False) as c:
                    response=c.get('http://127.0.0.1:18080/v1/models');response.raise_for_status();data=response.json()
                if not data.get('data') or data['data'][0].get('id')!=MODEL:raise ModelFailure('Owned model identity changed')
            write(directory/'discovery.json',dict(response=data,mock=mock is not None,timeout_seconds=10))
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:data)
        with profile_env(),patch.object(factory.requests,'get',discovery):
            reference=factory.get_llm('vllm_parsed',MODEL,MODEL,'tool')
            attenuation,judge=factory._get_attriguard_aux_llms('tool')
        self.policies={};self.profile={}
        for role,value in [('reference',reference),('attenuator',attenuation),('judge',judge)]:
            old_client=value.client
            http=httpx.Client(transport=httpx.MockTransport(self.respond) if mock else None,
                event_hooks={'request':[self.on_request],'response':[self.on_response]},
                timeout=httpx.Timeout(600,connect=5),trust_env=False)
            client=old_client.with_options(http_client=http,max_retries=0);old_client.close();self.clients.append(client)
            self.profile[role]=dict(model=value.model,temperature=value.temperature,top_p=value.top_p,
                seed=value.seed,reasoning_effort=value.reasoning_effort)
            owner=self;original_create=client.chat.completions.create
            class Capture:
                def create(self,_create=original_create,**kwargs):return owner.create(_create,kwargs)
            value.client=SimpleNamespace(chat=SimpleNamespace(completions=Capture()))
            class Role:
                def __init__(self,policy,label):self.policy=policy;self.label=label
                def query(self,*args,**kwargs):
                    old=owner.role;owner.role=self.label
                    try:
                        # Tenacity catches BaseException too. Invoke its original
                        # undecorated body, preserving successful payload construction.
                        with patch.object(compat,'chat_completion_request',no_retry_request):
                            return self.policy.query(*args,**kwargs)
                    finally:owner.role=old
            self.policies[role]=Role(value,role)
        write(directory/'effective_driver_profile.json',dict(roles=self.profile,endpoint='http://127.0.0.1:18080/v1',
            constructors='Original get_llm(vllm_parsed) and _get_attriguard_aux_llms(openai)',
            serialization='Original OpenAILLM.query and chat_completion_request; no new model generation parameters',
            transport_override='SDK max_retries=0; source tenacity wrapper bypassed via __wrapped__ body; source unsupported-logprobs fallback retained',
            mocked=mock is not None,independent_model_inference=mock is None))

    def create(self,create,kwargs):
        record=dict(index=len(self.records),role=self.role,request=wire(kwargs),mock=self.mock is not None,
            started_epoch=time.time());record['request_hash']=digest(record['request'])
        self.records.append(record);self.active=record
        base=self.directory/'requests'/f'{record["index"]:04d}_{self.role}'
        write(base.with_suffix('.driver_request.json'),record)
        if len(self.records)>12:raise ModelFailure('Per-session request cap exceeded')
        try:
            result=create(**kwargs);record['response']=result.model_dump(mode='json')
            record['finish_reason']=result.choices[0].finish_reason
            record['truncated']=record['finish_reason']=='length'
            write(base.with_suffix('.response.json'),record)
            return result
        except Exception as exc:
            record['exception']=dict(type=type(exc).__name__,message=str(exc),status_code=getattr(exc,'status_code',None))
            write(base.with_suffix('.exception.json'),record)
            # Preserve exactly the source's explicit unsupported-logprobs fallback.
            if isinstance(exc,openai.BadRequestError) and 'logprobs' in str(exc) and 'unsupported' in str(exc).lower():
                record['source_supported_logprobs_fallback']=True;raise
            raise ModelFailure(f'{type(exc).__name__}: {exc}') from exc
        finally:
            record['finished_epoch']=time.time();write(self.directory/'driver_records.json',self.records)

    def on_request(self,request):
        if request.url.host not in ['127.0.0.1','localhost'] or request.url.port!=18080:
            raise ModelFailure('Refusing nonlocal endpoint')
        index=len(self.http);request.extensions['study_index']=index;request.extensions['study_start']=time.monotonic()
        raw=request.content.decode();body=json.loads(raw)
        row=dict(index=index,role=self.role,driver_index=self.active['index'],url=str(request.url),
            method=request.method,headers={k:('<REDACTED>' if k.lower() in ['authorization','cookie'] else v) for k,v in request.headers.items()},
            body=body,raw_utf8_body=raw)
        if body!=self.active['request']:raise ModelFailure('Driver/wire payload parity failed')
        self.http.append(row);write(self.directory/'http'/f'{index:04d}.request.json',row)
    def on_response(self,response):
        response.read();index=response.request.extensions['study_index']
        try:body=response.json()
        except Exception:body=response.text
        write(self.directory/'http'/f'{index:04d}.response.json',dict(status=response.status_code,body=body,
            raw_utf8_body=response.text,headers=dict(response.headers),role=self.role,
            seconds=time.monotonic()-response.request.extensions['study_start']))
    def respond(self,request):
        result=self.mock(self.role,json.loads(request.content))
        return result if isinstance(result,httpx.Response) else httpx.Response(200,json=result)
    def close(self):
        for c in self.clients:c.close()
        write(self.directory/'driver_records.json',self.records)
        write(self.directory/'transport_summary.json',dict(http_attempts=len(self.http),driver_calls=len(self.records),
            wire_parity=True,role_counts={r:sum(x['role']==r for x in self.records) for r in ['reference','attenuator','judge']},
            truncated=[r['index'] for r in self.records if r.get('truncated')],mock=self.mock is not None))

def reply(content='',calls=None,finish='stop'):
    return dict(id='mock-engineering-only',object='chat.completion',created=0,model=MODEL,
        choices=[dict(index=0,message=dict(role='assistant',content=content,tool_calls=calls),finish_reason=finish,logprobs=None)],
        usage=dict(prompt_tokens=0,completion_tokens=0,total_tokens=0))

class Mock:
    """Scripted engineering scenarios, never scientific observations."""
    def __init__(self,repeat=1,failure=False,truncated=False):self.repeat=repeat;self.failure=failure;self.truncated=truncated
    def __call__(self,role,body):
        if self.failure:raise httpx.ReadError('Injected zero-retry transport failure')
        if role=='attenuator':return reply('S1 notice. Reply code: S1-REPLY-284.',finish='length' if self.truncated else 'stop')
        if role=='judge':return reply('<think>Mock engineering reasoning.</think>\n{"survive": true, "reason": "mock"}')
        count=2 if self.repeat==2 else 1
        if self.repeat==4:return reply('No action in this scripted engineering fixture.')
        value='S1-REPLY-284 ' if self.repeat==3 else 'S1-REPLY-284'
        calls=[dict(id=f'mock-call-{i}',type='function',function=dict(name='send_direct_message',arguments=json.dumps(dict(recipient='Alice',body=value)))) for i in range(count)]
        return reply('Scripted engineering reference.',calls,finish='tool_calls')
