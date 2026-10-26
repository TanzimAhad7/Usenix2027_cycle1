"""Actual singleton relations; no inference of pairwise edges from set verdicts."""
from .legacy_a.common import matching

def certificate(positive,unknown,nrefs):
    rows=[sorted(set(r)) for r in positive]
    up=[set(r) for r in rows]
    for i,j in unknown:up[i].add(j)
    lower=matching(rows,nrefs);upper=matching([sorted(x) for x in up],nrefs)
    full=len(lower)==len(rows)
    identified=full or lower==upper
    return dict(status='IDENTIFIED' if identified else 'UNKNOWN_UNIDENTIFIED_ALLOCATION',
        known_edges=rows,unknown_edges=list(unknown),lower_cardinality=len(lower),upper_cardinality=len(upper),
        full_actor_cover=full,assignment=lower if identified else None,
        witness_assignment=lower,explanation='Known full actor cover certifies every admission despite unknown cross-edges' if full else 'Matching bounds and deterministic assignment compared')

def choose(matrix,nrefs,policy):
    known=[[j for j,v in enumerate(row) if v is True] for row in matrix]
    unknown=[(i,j) for i,row in enumerate(matrix) for j,v in enumerate(row) if v is None]
    cert=certificate(known,unknown,nrefs)
    if policy=='PAIR_M0':
        if any(not row and any(v is None for v in matrix[i]) for i,row in enumerate(known)):
            return None,cert
        return [i for i,r in enumerate(known) if r],cert
    if policy!='PAIR_M1':raise ValueError(policy)
    return (sorted(cert['assignment']) if cert['status']=='IDENTIFIED' else None),cert

def canonical(call):
    from .util import pack
    c=pack(call)
    if c['function']=='pay' and 'key' not in c['args']:c['args']['key']=''
    return c
