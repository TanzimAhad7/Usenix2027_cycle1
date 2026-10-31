"""Gemma interface syntax only. No authorization judgments or output repair."""
import json,re

def unique_object(pairs):
    obj={}
    for key,value in pairs:
        if key in obj:raise ValueError('Duplicate JSON field: '+key)
        obj[key]=value
    return obj

def invalid_constant(value):raise ValueError('Non-JSON numeric constant: '+value)

def parse(text):
    opening='<tool_call>';closing='</tool_call>'
    if opening not in text and closing not in text:return [],text
    matches=list(re.finditer(r'<tool_call>(.*?)</tool_call>',text,re.S))
    if not matches or len(matches)!=text.count(opening) or len(matches)!=text.count(closing):raise ValueError('Unbalanced or nested tool-call tags')
    calls=[]
    for match in matches:
        value=json.loads(match.group(1),object_pairs_hook=unique_object,parse_constant=invalid_constant)
        if not isinstance(value,dict) or set(value)!={'name','arguments'} or not isinstance(value['name'],str) or not value['name'] or not isinstance(value['arguments'],dict):raise ValueError('Tool call must contain exactly string name and object arguments')
        calls.append(value)
    content=re.sub(r'<tool_call>.*?</tool_call>','',text,flags=re.S).strip()
    return calls,content or None
