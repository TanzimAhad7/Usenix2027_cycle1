"""Public structured policy comparator; independent of the outcome observer.

This is ordinary application authorization, not a new defense. It has the same
declared structured contract and primitive ledger as the G ceiling. No model
decisions, observer labels, private gold outcomes, or future state are inputs.
"""
from collections import Counter
import copy

def public_policy(spec):
    return {k:copy.deepcopy(spec.get(k)) for k in ('family','recipient','recipients','subject','body',
        'max_count','max_total','exact_amount','recipient_wise','recipient_budget')}

def permit(policy,state,function,args):
    if function not in ('pay','send_email'):return True,'READ_ONLY'
    if function=='pay':
        amount=args.get('amount');key=args.get('key','');recipient=args.get('recipient')
        if recipient!=policy['recipient'] or type(amount) is not int or amount<=0:return False,'PARAMETERS'
        if key and key in state['keys']:
            return (state['keys'][key]==[recipient,amount],'REGISTERED_RETRY')
        if policy['exact_amount'] is not None and amount!=policy['exact_amount']:return False,'EXACT_AMOUNT'
        if len(state['payments'])>=policy['max_count']:return False,'COUNT'
        if sum(e['amount'] for e in state['payments'])+amount>policy['max_total']:return False,'TOTAL'
        return True,'WITHIN_PUBLIC_BUDGET'
    recipients=args.get('recipients',[])
    if not recipients or len(set(recipients))!=len(recipients):return False,'RECIPIENTS'
    allowed=policy.get('recipients') or [policy['recipient']]
    if any(r not in allowed for r in recipients):return False,'RECIPIENTS'
    if args.get('subject')!=policy['subject'] or args.get('body')!=policy['body'] or any(args.get(k) for k in ('cc','bcc','attachments')):
        return False,'MESSAGE_PARAMETERS'
    sent=[e for e in state['env']['inbox']['emails'].values() if e['sender']=='researcher@example.com' and e['status']=='sent']
    if policy.get('recipient_wise'):
        used=Counter(r for e in sent for r in e['recipients'])
        if any(used[r]>=policy['recipient_budget'][r] for r in recipients):return False,'RECIPIENT_BUDGET'
    elif len(sent)>=policy['max_count'] or recipients!=[policy['recipient']]:return False,'COUNT_OR_RECIPIENTS'
    return True,'WITHIN_PUBLIC_BUDGET'

def remaining(spec,state):
    if spec['family']=='payment':
        return dict(root_total=spec['max_total'],root_count=spec['max_count'],ledger=state['payments'],
            remaining_total=spec['max_total']-sum(e['amount'] for e in state['payments']),
            remaining_count=spec['max_count']-len(state['payments']),registered_keys=state['keys'])
    sent=[e for e in state['env']['inbox']['emails'].values() if e['sender']=='researcher@example.com' and e['status']=='sent']
    used=Counter(r for e in sent for r in e['recipients'])
    return dict(root_count=spec['max_count'],sent=sent,remaining_count=spec['max_count']-len(sent),
        remaining_recipient_uses={r:n-used[r] for r,n in spec.get('recipient_budget',{}).items()})
