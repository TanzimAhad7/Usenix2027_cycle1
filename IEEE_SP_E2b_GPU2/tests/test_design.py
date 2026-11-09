import unittest
from collections import Counter
from e2b.design import manifest,logical_conditions,inputs,expected,key_for,pair
from e2b.terminal import inspect
class Tests(unittest.TestCase):
 def test_aliases(self):
  m=manifest();self.assertEqual(len(m['P1']),168);self.assertEqual(sum(len(j['aliases'])for j in m['P1']),192)
  self.assertEqual(Counter(j['criterion']for j in m['P1']),dict(SOURCE=45,ATTENTION=45,ARGUMENT_EQUALITY=45,DIRECT=33))
  for j in m['P1']:
   for a in j['aliases']:self.assertEqual(key_for(a),j['input_key']);self.assertEqual(expected(a),expected(j))
 def test_policy(self):
  for axis in ('amount','recipient'):
   a,b=pair(axis,'forward');c,d=pair(axis,'reverse');self.assertEqual((a,b),(d,c));self.assertEqual(sum(a['args'][k]!=b['args'][k]for k in a['args']),1)
  for item in logical_conditions():
   q,c,r,allowed=inputs(item);self.assertEqual(c in allowed,expected(item))
   if r:self.assertIn(r[0],allowed)
 def test_terminal(self):
  self.assertTrue(inspect('<think>x</think>\n```json\n{"survive":false}\n```')['interpretable'])
  for t in ['{"survive":"true"}','{"survive":true,"survive":false}','prefix {"survive":true}','{"survive":true} trailing']:self.assertFalse(inspect(t)['interpretable'])
  self.assertFalse(inspect('{"survive":true}','length')['interpretable'])
if __name__=='__main__':unittest.main()
