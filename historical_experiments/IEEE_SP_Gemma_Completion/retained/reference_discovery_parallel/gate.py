"""Privileged stateful complete mediation; independently coded from observer."""
import json
from collections import Counter

def key(function,args):
    a=dict(args)
    if function=='send_money' and 'amount' in a:a['amount']=float(a['amount'])
    if function=='send_email':
        for n in ('cc','bcc','attachments'):
            if not a.get(n):a.pop(n,None)
    return json.dumps([function,a],sort_keys=True,separators=(',',':'))

def permission(spec,effects,function,args):
    if function not in ('send_email','send_direct_message','send_channel_message','send_money'):return True,'read'
    limits=Counter(key(o['function'],o['args']) for o in spec['obligations'])
    spent=Counter(key(e['function'],e['args']) for e in effects)
    k=key(function,args)
    return (spent[k]<limits[k]),'remaining_machine_contract_capacity' if spent[k]<limits[k] else 'outside_or_consumed_contract'
