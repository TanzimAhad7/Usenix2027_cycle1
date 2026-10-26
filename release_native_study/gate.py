"""Conventional privileged complete mediation. Not a novel learned guard.

The independent observer does not import this module.
"""
from collections import Counter

def permission(spec,current_effects,function,args):
    if function not in ('send_email','send_direct_message','send_channel_message'):return True,'read'
    permitted=spec['obligations']
    destination=args.get('recipients') if function=='send_email' else args.get('recipient',args.get('channel'))
    used=Counter((e['function'],tuple(e['recipient']) if isinstance(e['recipient'],list) else e['recipient'],e.get('subject'),e['body']) for e in current_effects)
    for item in permitted:
        expected=[item['recipient']] if function=='send_email' else item['recipient']
        if item['function']!=function or destination!=expected:continue
        if function=='send_email' and any(args.get(k) for k in ['cc','bcc','attachments']):continue
        if item.get('subject') is not None and args.get('subject')!=item['subject']:continue
        if item.get('body') is not None and args.get('body')!=item['body']:continue
        # S2 content tokens are goal requirements, not permission constraints.
        consumed=sum(v for k,v in used.items() if k[0]==function and k[1]==(tuple(expected) if isinstance(expected,list) else expected) and (item.get('subject') is None or k[2]==item['subject']) and (item.get('body') is None or k[3]==item['body']))
        if consumed==0:return True,'available_explicit_obligation'
    return False,'outside_or_consumed_explicit_contract'
