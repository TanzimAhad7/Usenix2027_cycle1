import tempfile,unittest
from pathlib import Path
from reference_study.common import read,write
from e2b.design import manifest
from e2b.report import analyze

class ReportTests(unittest.TestCase):
 def test_partial_commit_and_unknowns(self):
  m=manifest();item=next(x for x in m['P1']if(x['axis'],x['direction'],x['policy'],x['candidate'],x['criterion'],x['draw'])==('amount','forward','STRICT','EDIT','SOURCE',0))
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);cell=p/'qwen/P1'/item['id']
   write(cell/'operative_decision.json',dict(allowed=True,prepared_request_verified=True,mock=False))
   write(cell/'native/JUDGE_RELEASE/after_and_effects.json',dict(assessment=dict(committed_count=1,violation=True),effects=[dict(amount=19)]))
   counts=analyze(p,m)
   self.assertEqual(counts['qwen']['scientific_observed'],1)
   self.assertEqual(counts['qwen']['recorded'],0)
   row=next(x for x in read(p/'analysis/cell_metrics.json')if(x['profile'],x['axis'],x['direction'],x['criterion'])==('qwen','amount','forward','SOURCE'))
   self.assertEqual(row['F']['unknown'],2);self.assertEqual(row['F']['bounds'],[1/3,1]);self.assertEqual(row['F']['native_violations'],1)
 def test_mock_is_not_science(self):
  m=manifest();item=m['P1'][0]
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);cell=p/'qwen/P1'/item['id']
   write(cell/'operative_decision.json',dict(allowed=False,prepared_request_verified=True,mock=True))
   write(cell/'result.json',dict(mock=True,primary_observed=True,status='COMPLETE'))
   counts=analyze(p,m)
   self.assertEqual(counts['qwen']['scientific_observed'],0);self.assertEqual(counts['qwen']['mock_acquisitions'],1)

if __name__=='__main__':unittest.main()
