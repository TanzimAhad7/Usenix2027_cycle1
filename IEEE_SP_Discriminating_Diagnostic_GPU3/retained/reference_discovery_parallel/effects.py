"""Extract committed effects from native state, without admission verdicts."""
from .common import pack

def extract(env,suite):
    if suite=='workspace':
        return [dict(id='email:'+str(m.id_),function='send_email',args=dict(recipients=list(m.recipients),subject=m.subject,body=m.body,cc=list(m.cc),bcc=list(m.bcc),attachments=pack(m.attachments))) for m in env.inbox.sent]
    if suite=='banking':
        return [dict(id='bank:'+str(t.id),function='send_money',args=dict(recipient=t.recipient,amount=t.amount,subject=t.subject,date=t.date),native=pack(t)) for t in env.bank_account.transactions if t.sender==env.bank_account.iban]
    return [dict(id=f'{function}:{target}:{i}',function=function,args={key:target,'body':m.body})
            for function,key,boxes in [('send_direct_message','recipient',env.slack.user_inbox),('send_channel_message','channel',env.slack.channel_inbox)]
            for target,rows in boxes.items() for i,m in enumerate(rows) if m.sender=='bot']

def normalized(op):
    args=dict(op['args'])
    if op['function']=='send_money' and 'amount' in args:
        try:args['amount']=float(args['amount'])
        except (ValueError,TypeError):pass
    if op['function']=='send_email':
        for k in ['cc','bcc','attachments']:
            if not args.get(k):args.pop(k,None)
    return dict(function=op['function'],args=args)

def matches(effect,obligation):return normalized(effect)==normalized(obligation)
