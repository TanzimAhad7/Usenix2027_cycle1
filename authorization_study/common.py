from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

PACKAGE = Path(__file__).resolve().parent
SEED = 20261019

def serial(value):
    if hasattr(value, 'model_dump'): return value.model_dump(mode='json')
    if isinstance(value, Path): return str(value)
    raise TypeError(type(value).__name__)

def pack(value): return json.loads(json.dumps(value, default=serial))
def digest(value): return hashlib.sha256(json.dumps(pack(value), sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, default=serial) + '\n'); tmp.replace(path)

def parse_json(raw):
    text = raw.strip()
    fence = re.fullmatch(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.S)
    if fence: text = fence[1].strip()
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result: raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(x): raise ValueError('Non-finite JSON value: ' + x)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant), bool(fence)

class BudgetExceeded(RuntimeError): pass
class UnidentifiedAllocation(RuntimeError): pass
class StopAtBatch(Exception): pass
class StopAtFeedback(Exception): pass
class WorkflowDeadline(BaseException): pass

def matching(edges, nrefs):
    """Lexicographically first maximum matching; unmatched sorts after refs.

    Obtain cardinality with augmenting paths, then fix candidates in order only
    when the optimum remains attainable. No exponential enumeration.
    """
    rows = [sorted(set(row)) for row in edges]
    if any(j < 0 or j >= nrefs for row in rows for j in row): raise ValueError('Bad edge')
    def size(indices, available):
        owners = {}
        def aug(i, seen):
            for j in rows[i]:
                if j not in available or j in seen: continue
                seen.add(j)
                if j not in owners or aug(owners[j], seen): owners[j] = i; return True
            return False
        return sum(aug(i, set()) for i in indices)
    available = set(range(nrefs)); target = size(range(len(rows)), available); result = {}
    for i in range(len(rows)):
        if target == 0: break
        for j in rows[i]:
            if j in available and 1 + size(range(i+1, len(rows)), available-{j}) == target:
                result[i] = j; available.remove(j); target -= 1; break
        else:
            if size(range(i+1, len(rows)), available) != target: raise AssertionError('Matching invariant')
    return result

