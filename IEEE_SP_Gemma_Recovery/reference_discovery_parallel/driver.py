"""Execute the actual retained release constructors and request serializers.

Logging wraps the client; it neither rewrites messages nor adds model options.
Actual HTTP bodies are saved separately from driver kwargs. Mocks use the same
SDK and driver with an httpx MockTransport; their data never count as inference.
"""
from __future__ import annotations
import contextlib,copy,importlib.util,inspect,os,sys,time
from .token_diagnostics import Diagnostics
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import openai
from openai import _base_client
httpx=getattr(_base_client,'httpx',None) or _base_client.httpx2
from openai.types.chat import ChatCompletion
from .common import PACKAGE,MODEL,MODEL_FAMILY,MAX_REQUESTS,MAX_SECONDS,wire,write,pack,digest,append,read,BudgetStop,ReplayMismatch

VENDOR=PACKAGE/'vendor'

def original_factory():
    # Original absolute imports resolve to these exact vendored members.
    sys.path.insert(0,str(VENDOR))
    import my_agent_pipeline
    if Path(my_agent_pipeline.__file__).resolve()!=VENDOR/'my_agent_pipeline.py':raise RuntimeError('Foreign author factory was already imported')
    return my_agent_pipeline

@contextlib.contextmanager
def local_profile_env():
    values=dict(OPENAI_API_KEY='EMPTY',OPENAI_BASE_URL='http://127.0.0.1:18080/v1',LOCAL_LLM_PORT='18080',ATTRIGUARD_BACKEND='openai',ATTRIGUARD_MODEL_ID=MODEL,ATTRIGUARD_JUDGE_MODEL_ID=MODEL,ATTRIGUARD_API_KEY='EMPTY')
    prior={k:os.environ.get(k) for k in values}
    proxy_keys=['HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy']
    proxies={k:os.environ.pop(k) for k in proxy_keys if k in os.environ}
    os.environ.update(values)
    try:yield
    finally:
        for k,v in prior.items():
            if v is None:os.environ.pop(k,None)
            else:os.environ[k]=v
        os.environ.update(proxies)

class Driver:
    def __init__(self,session,mock=None,replay=None):
        self.session=session;self.directory=session.directory;self.mock=mock;self.role='actor';self.records=[];self.http_count=0
        self.diagnostics=Diagnostics(self.tokenize);self.token_http=None
        self.start=time.monotonic();self.replay=list(replay or []);self.replay_cursor=0;self.clients=[];self.active_record=None
        factory=original_factory()
        compat=sys.modules['openai_llm_compat']
        no_retry=getattr(compat.chat_completion_request,'__wrapped__',None)
        if no_retry is None:raise BudgetStop('Retry wrapper identity changed')
        def models_get(url,*args,**kwargs):
            if url!='http://localhost:18080/v1/models':raise RuntimeError('Unexpected discovery endpoint')
            if mock is not None:data=dict(data=[dict(id=MODEL)])
            else:
                with httpx.Client(timeout=10,trust_env=False) as c:
                    r=c.get('http://127.0.0.1:18080/v1/models');r.raise_for_status();data=r.json()
                if not data.get('data') or data['data'][0].get('id')!=MODEL:raise BudgetStop('Owned model identity changed')
            write(self.directory/'discovery.json',dict(response=data,mock=mock is not None,timeout_seconds=10))
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:data)
        with local_profile_env(), patch.object(factory.requests,'get',models_get):
            actor=factory.get_llm('vllm_parsed',MODEL,MODEL,'tool')
            attenuation,judge=factory._get_attriguard_aux_llms('tool')
        self.policies={}
        for role,llm in [('actor',actor),('attenuator',attenuation),('judge',judge)]:
            transport=httpx.MockTransport(self.respond_mock) if mock is not None else None
            http=httpx.Client(transport=transport,event_hooks={'request':[self.on_request],'response':[self.on_response]},timeout=httpx.Timeout(600,connect=5),trust_env=False)
            old_client=llm.client
            client=old_client.with_options(http_client=http,max_retries=0);old_client.close()
            self.clients.append(client)
            original_create=client.chat.completions.create
            owner=self
            class Capture:
                def create(self,_create=original_create,**kwargs):return owner.create(_create,kwargs)
            # The same original OpenAILLM.query performs its normal conversion.
            llm.client=SimpleNamespace(chat=SimpleNamespace(completions=Capture()))
            class RolePolicy:
                def __init__(self,value,label):self.value=value;self.label=label
                def query(self,*args,**kwargs):
                    old=owner.role
                    caller=inspect.currentframe().f_back
                    reference=(caller.f_code.co_filename==owner.session.core.__file__ and caller.f_lineno==owner.session.shadow_query_line)
                    owner.role=('reference' if reference else 'actor') if self.label=='actor' else self.label
                    if owner.role=='actor':owner.session.messages=copy.deepcopy(kwargs.get('messages',args[3] if len(args)>3 else []))
                    try:
                        with patch.object(compat,'chat_completion_request',no_retry):
                            result=self.value.query(*args,**kwargs)
                        if owner.role=='actor':owner.session.messages=result[3]
                        return result
                    finally:owner.role=old
            self.policies[role]=RolePolicy(llm,role)
        write(self.directory/'effective_driver_profile.json',dict(factory='my_agent_pipeline.get_llm(vllm_parsed) + _get_attriguard_aux_llms(backend=openai)',actor=dict(model=MODEL,temperature=actor.temperature,top_p=actor.top_p,seed=actor.seed),auxiliary=dict(model=MODEL,temperature=judge.temperature,top_p=judge.top_p),endpoint='http://127.0.0.1:18080/v1',network='Local owned server only',request_changes='No model option changes; SDK max_retries=0, original source tenacity body called without decorator; unsupported-logprobs fallback retained',server_output_cap=8192,scope='Source-supported driver; model/interface profile recorded separately. No pure model-effect or published principal-configuration claim',model_family=MODEL_FAMILY,diagnostic_tokenization='One background CPU endpoint worker; exact payloads retained, drained before session close; no concurrent model generations'))

    def create(self,create,kwargs):
        encoded=wire(kwargs);index=len(self.records)
        row=dict(index=index,role=self.role,request=encoded,request_hash=digest(encoded),mock=self.mock is not None,reused=False)
        self.records.append(row);self.active_record=row
        base=self.directory/'requests'/f'{index:04d}_{self.role}'
        write(base.with_suffix('.driver_request.json'),row)
        self.session.model_view(self.role,encoded)
        if self.replay_cursor<len(self.replay):
            expected=self.replay[self.replay_cursor]
            if expected['role']!=self.role or expected['request']!=encoded:
                write(self.directory/'REPLAY_MISMATCH.json',dict(expected=expected,actual=row))
                raise ReplayMismatch('Cached response requested under changed driver input/role')
            self.replay_cursor+=1;row['reused']=True
            if 'exception' in expected:
                error=expected['exception'];row['exception']=copy.deepcopy(error);write(base.with_suffix('.reused_exception.json'),row)
                cls=getattr(openai,error['type'],None)
                if cls is None or not isinstance(cls,type) or not issubclass(cls,openai.APIStatusError) or error.get('status_code') is None:raise ReplayMismatch('Original exception cannot be faithfully reconstructed; no live fallback')
                response=httpx.Response(error['status_code'],request=httpx.Request('POST',error['url']),json=error.get('body'))
                raise cls(error['message'],response=response,body=error.get('body'))
            row['response']=copy.deepcopy(expected['response'])
            write(base.with_suffix('.reused_response.json'),row)
            return ChatCompletion.model_validate(row['response'])
        if self.session.restore and self.session.first_decision:
            raise ReplayMismatch('Unrecorded generation before replayed source decision; no live fallback')
        if time.monotonic()-self.start>MAX_SECONDS:raise BudgetStop('Workflow wall-clock limit')
        try:
            result=create(**kwargs);row['response']=result.model_dump(mode='json');row['truncated']=result.choices[0].finish_reason=='length';write(base.with_suffix('.response.json'),row)
            if self.role=='actor':self.session.final_text=result.choices[0].message.content or ''
            return result
        except Exception as exc:
            response=getattr(exc,'response',None)
            row['exception']=dict(type=type(exc).__name__,message=str(exc),status_code=getattr(exc,'status_code',None),body=pack(getattr(exc,'body',None)),url=str(response.request.url) if response is not None else None);write(base.with_suffix('.exception.json'),row)
            if isinstance(exc,openai.BadRequestError) and 'logprobs' in str(exc) and 'unsupported' in str(exc).lower():raise
            raise BudgetStop(f'Zero-retry transport failure: {type(exc).__name__}: {exc}') from exc

    def on_request(self,request):
        if request.url.host not in ('127.0.0.1','localhost') or request.url.port!=18080:raise RuntimeError('Refusing nonlocal or unowned model endpoint')
        if self.http_count>=MAX_REQUESTS:raise BudgetStop('Generation HTTP-attempt cap; SDK/source retries count')
        self.http_count+=1;request.extensions['study_started']=time.monotonic();request.extensions['study_index']=self.http_count
        try:body=__import__('json').loads(request.content)
        except Exception:body=request.content.decode(errors='replace')
        request.extensions['study_body']=body
        if body!=self.active_record['request']:raise BudgetStop('Driver/wire payload mismatch')
        write(self.directory/'http'/f'{self.http_count:04d}.request.json',dict(role=self.role,method=request.method,url=str(request.url),headers={k:('<REDACTED>' if k.lower() in ['authorization','cookie'] else v) for k,v in request.headers.items()},body=body,raw_utf8_body=request.content.decode(errors='replace'),driver_index=self.active_record['index'] if self.active_record else None))

    def on_response(self,response):
        response.read();i=response.request.extensions['study_index']
        try:body=response.json()
        except Exception:body=response.text
        write(self.directory/'http'/f'{i:04d}.response.json',dict(status=response.status_code,headers=dict(response.headers),body=body,seconds=time.monotonic()-response.request.extensions['study_started'],role=self.role))
        self.session.world.event('generation_transport_response',role=self.role,http_index=i,status=response.status_code,carrier_marker_in_request='BEGIN_UNTRUSTED_PROCEDURE' in __import__('json').dumps(response.request.extensions['study_body']),mock=self.mock is not None)
        if self.mock is None:
            self.diagnostics.submit(i,response.request.extensions['study_body'])

    def tokenize(self,index,body):
        payload={k:v for k,v in body.items() if k in ('model','messages','tools','tool_choice')}
        payload.update(add_generation_prompt=True,return_token_strs=True)
        try:
            if self.token_http is None:self.token_http=httpx.Client(trust_env=False,timeout=15)
            r=self.token_http.post('http://127.0.0.1:18080/tokenize',json=payload)
            try:data=r.json()
            except Exception:data=r.text
            write(self.directory/'tokenization'/f'{index:04d}.json',dict(status=r.status_code,request=payload,response=data,scope='Asynchronous diagnostic tokenize endpoint, not independent attestation of tokens consumed by generation'))
        except Exception as exc:write(self.directory/'tokenization'/f'{index:04d}.json',dict(status='UNAVAILABLE',error=str(exc),request=payload))

    def respond_mock(self,request):
        answer=self.mock(self.role,__import__('json').loads(request.content),self.session)
        return answer if isinstance(answer,httpx.Response) else httpx.Response(200,json=answer)

    def close(self):
        try:self.diagnostics.close()
        finally:
            try:
                if self.token_http is not None:self.token_http.close()
                for client in self.clients:client.close()
            finally:write(self.directory/'driver_records.json',self.records)
