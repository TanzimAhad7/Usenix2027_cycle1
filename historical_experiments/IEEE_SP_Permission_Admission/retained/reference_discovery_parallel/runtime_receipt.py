"""Recheck every pinned runtime source before reusing shared qualification."""
def runtime_digest():
    import importlib,inspect
    from pathlib import Path
    from .common import MODULE,digest,read,file_hash
    from .engine import verify_source
    additional={}
    for name,expected in read(MODULE/'ADDITIONAL_RUNTIME_HASHES.json').items():
        module=importlib.import_module(name);path=Path(inspect.getfile(module));actual=file_hash(path)
        if actual!=expected:raise RuntimeError('Additional runtime source drift: '+name)
        additional[name]=dict(path=str(path),sha256=actual)
    return digest(dict(source=verify_source(),additional=additional))
