#!/usr/bin/env python3
"""Validate declared v6.2 pilot/conditional factorial schedules; NOT an execution claim."""
import pathlib,json,math,sys
root=pathlib.Path(__file__).resolve().parents[1]
expected={'D24':24,'H24':24,'S128':128,'A64':64,'H64':64}
errors=[]
for name,n in expected.items():
 p=root/'protocols/proposed'/f'{name}.json'
 try:
  a=json.loads(p.read_text()); got=math.prod(a['factors'].values())
  if got!=n or a['expected_scheduled_episodes']!=n or a['id']!=name:errors.append(f'{name}: wrong schedule')
  if a['evidence_kind']!='PROPOSED_OR_REPORTED_NOT_EXECUTED':errors.append(f'{name}: changed evidence status')
  print(f'{name}: {n} scheduled episodes; status {a["evidence_kind"]}')
 except Exception as e:errors.append(f'{name}: {e}')
if errors:
 print('\n'.join(errors),file=sys.stderr);sys.exit(1)
print('PROTOCOL_DECLARATIONS_PASS (No model experiment was run.)')
