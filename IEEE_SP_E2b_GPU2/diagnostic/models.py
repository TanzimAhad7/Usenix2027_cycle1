"""Owned local profiles. Optional Gemma12 is an explicitly adapted sensitivity."""
from __future__ import annotations
import argparse,json,os
from pathlib import Path
from reference_study.common import ROOT,activate,read,write
from reference_study.models import command as retained_command,live,rendering as retained_rendering

def profiles():
    from reference_discovery_parallel.models import PROFILES
    from permission_admission.completion_models import PROFILE
    values=dict(qwen=dict(PROFILES['qwen']),gemma=dict(PROFILE))
    if os.environ.get('DIAG_VARIANT')=='gemma12_sensitivity':
        revision=os.environ.get('DIAG_MODEL_REVISION')
        if not revision:raise RuntimeError('Gemma12 cached revision must be resolved before server launch')
        values['gemma'].update(hub='google/gemma-3-12b-it',revision=revision,alias='gemma3-12b-it-diagnostic-tag-adapted',
            interface='Recorded explicit tag interface on Gemma12; not published principal profile replication')
    return values

def command(python,snapshot,family):
    argv=retained_command(python,snapshot,family)
    argv[argv.index('--served-model-name')+1]=profiles()[family]['alias']
    return argv

def rendering(snapshot,family,out):
    retained_rendering(snapshot,family,out)
    p=Path(out)/'qualification.json';data=read(p);data['actual_diagnostic_profile']=profiles()[family]
    data['profile_scope']='Recorded interface reused and explicitly bound to selected cached model. No principal published-profile reproduction claim.';write(p,data)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--snapshot',type=Path,required=True);ap.add_argument('--family',required=True,choices=('qwen','gemma'));ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();activate(a.family);rendering(a.snapshot,a.family,a.out)
