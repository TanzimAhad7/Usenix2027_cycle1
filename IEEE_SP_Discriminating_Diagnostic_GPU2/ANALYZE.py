from pathlib import Path
import argparse
from diagnostic.report import analyze
from reference_study.common import read
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args()
print(analyze(a.run,read(a.run/'FROZEN_MANIFEST.json')))
