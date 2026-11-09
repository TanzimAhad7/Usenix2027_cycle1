"""Synthetic arithmetic fixtures are discarded; never scientific observations."""
import sys,tempfile,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from e1.design import manifest
from e1.report import analyze
from reference_study.common import write,read
m=manifest()
with tempfile.TemporaryDirectory()as tmp:
 out=Path(tmp)
 for i in m['P1']:
  if i['setting']!='BANK'or i['candidate']!='B'or i['reference']not in ('A','NONE'):continue
  allow=True if i['criterion']=='FUZZY'else i['policy']=='C2'
  write(out/'qwen/P1'/i['id']/'result.json',dict(status='SYNTHETIC_UNIT_FIXTURE',qualified=True,mock=False,allowed=allow))
 analyze(out,m);g=read(out/'analysis/comparison_gaps.json')
 assert next(x for x in g if x['profile']=='qwen'and x['setting']=='BANK'and x['criterion']=='FUZZY')['mean_D_direct_minus_D_comparator']==1
 assert next(x for x in g if x['profile']=='qwen'and x['setting']=='BANK'and x['criterion']=='PERMISSION')['mean_D_direct_minus_D_comparator']==0
 assert all(x['mean_D_direct_minus_D_comparator']is None for x in g if x['profile']=='gemma')
 # A source logprob/text reversal must preempt the behavioral-context label.
 cell=next(i for i in m['P1']if i['setting']=='BANK'and i['policy']=='C1'and i['candidate']=='B'and i['reference']=='A'and i['criterion']=='FUZZY'and i['draw']==0)
 write(out/'qwen/P1'/cell['id']/'result.json',dict(status='SYNTHETIC_UNIT_FIXTURE',qualified=True,mock=False,allowed=True,strict_verdict=dict(parsed=dict(survive=False))))
 analyze(out,m)
 patterns=read(out/'analysis/descriptive_patterns.json')
 assert next(x for x in patterns if x['profile']=='qwen'and x['setting']=='BANK'and x['draw']==0)['descriptive_pattern']=='SOURCE_LOGPROB_ADJUDICATION_DISAGREEMENT_REVIEW'

print('PASS: synthetic policy-gap arithmetic and missing-profile handling; fixture rows discarded.')
