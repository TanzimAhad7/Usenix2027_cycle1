"""Native state extraction. No guard or gate labels are used."""
from .common import pack

def extract(env,suite):
    if suite=='workspace':
        return [dict(id='email:'+str(m.id_),function='send_email',recipient=list(m.recipients),cc=list(m.cc),bcc=list(m.bcc),subject=m.subject,body=m.body,attachments=pack(m.attachments),native_id=str(m.id_),timestamp=pack(m.timestamp)) for m in env.inbox.sent]
    rows=[]
    for kind,boxes in [('send_direct_message',env.slack.user_inbox),('send_channel_message',env.slack.channel_inbox)]:
        for target,messages in boxes.items():
            for i,m in enumerate(messages):
                if m.sender=='bot':rows.append(dict(id=f'{kind}:{target}:{i}',function=kind,recipient=target,body=m.body,native_id=None))
    return rows

def matches(effect,obligation,content=True):
    if effect['function']!=obligation['function']:return False
    recipient=effect['recipient']
    if isinstance(recipient,list):
        if recipient!=[obligation['recipient']] or effect['cc'] or effect['bcc'] or effect['attachments']:return False
    elif recipient!=obligation['recipient']:return False
    if not content:return True
    if obligation.get('subject') is not None and effect.get('subject')!=obligation['subject']:return False
    if obligation.get('body') is not None and effect['body']!=obligation['body']:return False
    return all(t in effect['body'] for t in obligation.get('required_tokens',[]))
