"""Existing pinned local profiles; eight independent blocks keep server supplied."""
from diagnostic.models import profiles,live,rendering
from diagnostic.models import command as original

def command(python,snapshot,family):
 argv=original(python,snapshot,family)
 argv[argv.index('--max-num-seqs')+1]='8'
 return argv

if __name__=='__main__':
 import argparse
 from pathlib import Path
 from reference_study.common import activate
 p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();activate(a.family);rendering(a.snapshot,a.family,a.out)
