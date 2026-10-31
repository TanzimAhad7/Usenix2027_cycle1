"""Restore captured live state, without replaying Inbox initialization.

The pinned Inbox's after-validator rebuilds ``emails`` from ``initial_emails``.
That is appropriate for creating a task, but erases later sends and notices
when loading a live checkpoint. Validate each persisted Inbox field separately
and construct that one container without invoking its initialization validators.
All other environment fields retain their normal native validation. The entire
serialized environment must match exactly afterwards; discrepancies fail closed.
Native tools, source guard, contract and checkpoint hashes are unchanged.
"""
import copy
from pydantic import TypeAdapter
from .common import digest,ReplayMismatch


def restore_environment(environment_type, snapshot, suite):
    saved=copy.deepcopy(snapshot)
    env=environment_type.model_validate(copy.deepcopy(saved))
    if suite=='workspace':
        inbox_type=type(env.inbox)
        raw=saved['inbox']
        values={}
        for name,field in inbox_type.model_fields.items():
            if name not in raw:
                raise ReplayMismatch('Live inbox checkpoint field missing: '+name)
            values[name]=TypeAdapter(field.rebuild_annotation()).validate_python(copy.deepcopy(raw[name]))
        for box in ('emails','trash'):
            if any(str(key)!=str(email.id_) for key,email in values[box].items()):
                raise ReplayMismatch('Live inbox checkpoint has an inconsistent email ID')
        env.inbox=inbox_type.model_construct(_fields_set=set(values),**values)
    if digest(env.model_dump(mode='json'))!=digest(saved):
        raise ReplayMismatch('Native environment restoration changes captured live state')
    return env
