"""Gemma interface syntax only. No authorization judgments or output repair."""
import json,re

def unique_object(pairs):
    obj={}
    for key,value in pairs:
        if key in obj:raise ValueError('Duplicate JSON field: '+key)
        obj[key]=value
    return obj

def invalid_constant(value):raise ValueError('Non-JSON numeric constant: '+value)

def envelope(body):
    """Two declared envelopes; no guessed tool names or argument repair."""
    body=body.strip()
    if body.startswith('<'):
        m=re.fullmatch(r'<name>([^<>&\s]+)</name>\s*<arguments>(.*)</arguments>',body,re.S)
        if not m:raise ValueError('Invalid XML tool-call envelope')
        return {'name':m.group(1),'arguments':json.loads(m.group(2),object_pairs_hook=unique_object,parse_constant=invalid_constant)}
    return json.loads(body,object_pairs_hook=unique_object,parse_constant=invalid_constant)

def parse(text):
    opening='<tool_call>';closing='</tool_call>'
    if opening not in text and closing not in text:return [],text
    matches=list(re.finditer(r'<tool_call>(.*?)</tool_call>',text,re.S))
    if not matches or len(matches)!=text.count(opening) or len(matches)!=text.count(closing):raise ValueError('Unbalanced or nested tool-call tags')
    calls=[]
    for match in matches:
        value=envelope(match.group(1))
        if not isinstance(value,dict) or set(value)!={'name','arguments'} or not isinstance(value['name'],str) or not value['name'] or not isinstance(value['arguments'],dict):raise ValueError('Tool call must contain exactly string name and object arguments')
        calls.append(value)
    content=re.sub(r'<tool_call>.*?</tool_call>','',text,flags=re.S).strip()
    return calls,content or None
