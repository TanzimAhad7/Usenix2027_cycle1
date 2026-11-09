"""Secondary envelope diagnostic; never normalizes an operative source reply."""
import json,re

def inspect(raw,finish_reason='stop'):
 result=dict(interpretable=False,boolean=None,envelope=None,bare_json=False)
 def fail(reason):return dict(result,reason=reason)
 if not isinstance(raw,str)or finish_reason!='stop':return fail('missing_or_incomplete')
 text=raw.strip();envelope=[]
 if text.startswith('<think>'):
  if text.count('<think>')!=1 or text.count('</think>')!=1:return fail('ambiguous_think')
  text=text.split('</think>',1)[1].strip();envelope.append('think')
 elif '<think>'in text or '</think>'in text:return fail('unexpected_think')
 if text.startswith('```'):
  match=re.fullmatch(r'```(?:json)?[ \t]*\n(.*?)\n```',text,re.S)
  if not match:return fail('malformed_fence')
  text=match.group(1).strip();envelope.append('fence')
 def unique(pairs):
  obj={}
  for key,value in pairs:
   if key in obj:raise ValueError('Duplicate JSON key')
   obj[key]=value
  return obj
 try:data=json.loads(text,object_pairs_hook=unique)
 except (ValueError,TypeError):return fail('not_one_json_object')
 if not isinstance(data,dict)or type(data.get('survive'))is not bool:return fail('not_typed_boolean')
 return dict(result,interpretable=True,boolean=data['survive'],parsed=data,envelope='+'.join(envelope)or'bare',bare_json=not envelope,reason='typed_terminal_boolean')
