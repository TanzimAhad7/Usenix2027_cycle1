"""Unchanged helpers from archived p0b3_live_common.py.
Source SHA-256: cb6a33c392b8d6d4e89794f86d1c309e6eceebc3aec1a83c77692af3cfc4ad53
"""
import json
from typing import Sequence


def get_text(content) -> str:
    if content is None:
        return ''
    if isinstance(content,str):
        return content
    parts=[]
    for x in content:
        parts.append(str(x.get('content','') or '') if isinstance(x,dict) else str(x))
    return '\n'.join(parts)


def action_string(call) -> str:
    args=dict(call.args or {})
    return f"{call.function}({json.dumps(args,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)})"


def is_privileged(function_name: str,proto: dict) -> bool:
    rule=proto['config']['detector']['privileged_rule']; name=str(function_name)
    if name in set(rule['explicit']):
        return True
    if name.startswith(('get_','search_','list_')):
        return False
    return any(name.startswith(p) for p in rule['side_effect_prefixes'])


def context_serializer(messages: Sequence[dict],*,ablate_user=False,ablate_tool_message_index=None) -> str:
    """Prospectively frozen live representation of C_t.

    Uses AgentDojo history before proposed Y. First user message is U; every role=tool message is one S.
    C\\U deletes the first user message. C\\S deletes exactly the selected tool-result message.
    No matched replacement or truncation is used.
    """
    out=[]; user_deleted=False
    for idx,m in enumerate(messages):
        role=m.get('role','?')
        if role=='user' and ablate_user and not user_deleted:
            user_deleted=True; continue
        if role=='tool' and ablate_tool_message_index is not None and idx==ablate_tool_message_index:
            continue
        txt=get_text(m.get('content'))
        if role=='system':
            out += ['<SYSTEM>',txt,'</SYSTEM>']
        elif role=='user':
            out += ['<USER>',txt,'</USER>']
        elif role=='assistant':
            out += ['<ASSISTANT>',txt]
            for tc in (m.get('tool_calls') or []):
                out.append('<TOOL_CALL>'+action_string(tc)+'</TOOL_CALL>')
            out.append('</ASSISTANT>')
        elif role=='tool':
            tc=m.get('tool_call'); name=getattr(tc,'function','tool') if tc is not None else 'tool'
            out += [f'<TOOL_RESULT name="{name}">',str(m.get('error')) if m.get('error') else txt,'</TOOL_RESULT>']
        else:
            out += [f'<{str(role).upper()}>',txt,f'</{str(role).upper()}>']
    out.append('<ASSISTANT_ACTION>')
    return '\n'.join(out)+'\n'
