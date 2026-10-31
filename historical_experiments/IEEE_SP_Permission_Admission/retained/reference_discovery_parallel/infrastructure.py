"""Separate transport outages from scientific negatives and model errors."""
from .common import read

def transport_outage(directory):
    candidates=[directory/'driver_records.json',directory/'model_io/driver_records.json']
    for path in candidates:
        if not path.is_file():continue
        for row in read(path):
            error=row.get('exception') or {}
            status=error.get('status_code')
            message=str(error.get('message','')).lower()
            if status in [502,503,504]:return error
            if status==500 and any(token in message for token in ['enginecore','enginedead','engine is dead','worker died']):return error
            if error.get('type') in ['APIConnectionError','APITimeoutError','ConnectError','ReadError','ReadTimeout','RemoteProtocolError']:return error
    return None

def reserve_restart(previous,limit=2):
    if previous>=limit:raise RuntimeError('Owned-server infrastructure restart budget exhausted; preserving remaining unexecuted slots')
    return previous+1
