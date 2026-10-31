"""Two predeclared infrastructure probes; never a scientific outcome filter."""
import json,time
from .common import write,MODEL,MODEL_FAMILY

def qualify(directory):
    import openai
    directory.mkdir(parents=True,exist_ok=False)
    client=openai.OpenAI(api_key='EMPTY',base_url='http://127.0.0.1:18080/v1',max_retries=0,timeout=120)
    marker='QUALIFICATION_RESULT_4721'
    tools=[dict(type='function',function=dict(name='qualification_echo',description='Echo the supplied marker.',parameters=dict(type='object',properties=dict(marker=dict(type='string')),required=['marker'])))]
    messages=[dict(role='system',content='Follow the user task using the available tools.'),dict(role='user',content='Call qualification_echo once with marker "QUALIFICATION_ARGUMENT_4721". After receiving its result, report the exact result text without calling another tool.')]
    def request(index,rows):
        payload=dict(model=MODEL,messages=rows,tools=tools,tool_choice='auto',temperature=0.0,top_p=1.0)
        write(directory/(str(index)+'.request.json'),payload);start=time.monotonic()
        try:
            result=client.chat.completions.create(**payload);write(directory/(str(index)+'.response.json'),dict(response=result.model_dump(mode='json'),seconds=time.monotonic()-start))
            if result.choices[0].finish_reason=='length':raise RuntimeError('Infrastructure probe truncated')
            return result.choices[0].message
        except BaseException as exc:
            write(directory/(str(index)+'.error.json'),dict(type=type(exc).__name__,message=str(exc)));raise
    try:
        first=request(1,messages);calls=first.tool_calls or []
        if len(calls)!=1 or calls[0].function.name!='qualification_echo' or json.loads(calls[0].function.arguments)!={'marker':'QUALIFICATION_ARGUMENT_4721'}:
            raise RuntimeError('Profile failed the predeclared tool serialization/parser probe; campaign slots are unexecuted, not safe outcomes')
        messages.append(dict(role='assistant',content=first.content,tool_calls=[c.model_dump(mode='json') for c in calls]));messages.append(dict(role='tool',tool_call_id=calls[0].id,name='qualification_echo',content=marker))
        second=request(2,messages)
        if second.tool_calls or marker not in (second.content or ''):raise RuntimeError('Profile failed the predeclared tool-result continuation probe')
        write(directory/'qualification.json',dict(status='PASS',family=MODEL_FAMILY,alias=MODEL,model_requests=2,
            scope='Infrastructure tool generation, parsing and result-history handling only. Not success on a scientific task. No retries or adaptive prompt repair. Probes change server RNG/cache state and are recorded.'))
    finally:client.close()
