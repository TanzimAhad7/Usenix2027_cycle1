"""Privileged diagnostic gate, independently implemented by state enumeration.

It enforces authored choice/capacity only, not every prose workflow constraint.
This gate is used on clones, never as an extra autonomous campaign policy.
"""
from __future__ import annotations

import json

SENSITIVE = {'send_money', 'send_email', 'send_direct_message', 'send_channel_message'}


def key(op):
    args = dict(op['args'])
    if op['function'] == 'send_money':
        args['amount'] = float(args['amount'])
    if op['function'] == 'send_email':
        for field in ('cc', 'bcc', 'attachments'):
            if args.get(field) is None or args.get(field) == []:
                args.pop(field, None)
    return json.dumps([op['function'], args], sort_keys=True)


def permission(spec, effects, function, args):
    if function not in SENSITIVE:
        return True, 'read'
    slots = spec.get('choice_contract', {}).get('slots')
    if slots is None:
        slots = [{'alternatives': [op]} for op in spec['obligations']]
    available = [{key(op) for op in slot['alternatives']} for slot in slots]
    states = {frozenset()}
    for op in [*effects, {'function': function, 'args': args}]:
        wanted = key(op)
        states = {used | {i} for used in states for i, choices in enumerate(available)
                  if i not in used and wanted in choices}
        if not states:
            return False, 'outside_or_consumed_choice_contract'
    return True, 'unused_choice_slot'

