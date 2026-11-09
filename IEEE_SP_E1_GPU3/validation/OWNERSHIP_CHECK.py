"""Dry-run regression: recycled root and foreign PIDs must never be signaled."""
import sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reference_study.common import activate
activate('qwen')
from reference_discovery_parallel.base import serving
signals=[];identities={101:'recycled-root',102:'owned-child',999:'foreign'}
def kill(pid,sig):
 signals.append((pid,int(sig)));identities.pop(pid,None)
server=SimpleNamespace(pid=101,poll=lambda:0,wait=lambda timeout:0)
with tempfile.TemporaryDirectory()as tmp,patch.object(serving,'proc_start',lambda pid:identities.get(pid)),patch.object(serving,'descendant_pids',side_effect=AssertionError('Must not adopt children of recycled root')),patch.object(serving.os,'kill',kill),patch.object(serving.os,'killpg',side_effect=AssertionError('Recycled group must not be signaled')):
 serving.stop_owned(server,{101:'old-root',102:'owned-child'},Path(tmp)/'cleanup.json')
assert signals==[(102,15)]and identities[999]=='foreign'
print('PASS: only authenticated child signaled in simulation; recycled root/foreign PID untouched; zero real signals.')
