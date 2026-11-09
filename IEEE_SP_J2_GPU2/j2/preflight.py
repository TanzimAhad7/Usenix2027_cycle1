"""Serving-only CPU renderer; no research-environment dependency imports."""
import argparse
import sys
from pathlib import Path
from reference_study.common import ROOT

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--family',choices=('qwen','gemma'),required=True)
    p.add_argument('--cache',type=Path,required=True)
    p.add_argument('--prepared',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    sys.path.insert(0,str(ROOT/'retained'))
    from reference_discovery_parallel.base import serving
    from diagnostic.models import profiles
    profile=profiles()[a.family]
    snapshot,identity=serving.inspect_snapshot(a.cache/('models--'+profile['hub'].replace('/','--')),profile['hub'],profile['revision'])
    from .rendering import render
    render(snapshot,a.family,a.out,a.prepared)
