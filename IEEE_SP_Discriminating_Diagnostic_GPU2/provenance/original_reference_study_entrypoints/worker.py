"""Persistent isolated worker: fresh state/clients per case, fixed model per process."""
from __future__ import annotations
import argparse,contextlib,json,signal,sys,time,traceback
from pathlib import Path
from .common import activate,read,write

def run_job(item,directory,family,mock=False):
    from permission_admission.runtime import configure
    configure(family)
    from . import mechanisms
    directory=Path(directory);started=time.monotonic();old=None
    log=directory.parent/'_diagnostic_logs'/(item['id']+'.log');log.parent.mkdir(parents=True,exist_ok=True)
    try:
        if hasattr(signal,'SIGALRM'):
            old=signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('1200-second technical case watchdog')));signal.alarm(1200)
        with log.open('a')as stream,contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
            if item['panel']!='P3':directory.mkdir(parents=True,exist_ok=False)
            result=getattr(mechanisms,item['panel'].lower())(item,directory,family,mock)
    except BaseException as e:
        directory.mkdir(parents=True,exist_ok=True)
        result=dict(status='INTERRUPTED'if isinstance(e,KeyboardInterrupt)else'TECHNICAL_ERROR',qualified=False,
            scientific_negative=False,error=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
    finally:
        if old is not None:signal.alarm(0);signal.signal(signal.SIGALRM,old)
    path=directory/('driver_records.json'if item['panel']=='P3'else'model_io/driver_records.json')
    records=read(path)if path.is_file()else[]
    from .mechanisms import diagnostic
    result.update(id=item['id'],panel=item['panel'],profile=family,mock=mock,attempted=True,
        evaluation_mode='MOCK_ENGINEERING_ZERO_INFERENCE'if mock else'MODEL_EXPERIMENT',
        elapsed_seconds=time.monotonic()-started,
        role_counts={r:sum(x['role']==r for x in records)for r in('actor','attenuator','reference','judge')},
        judge_diagnostics=[dict(record_index=r['index'],**diagnostic(r))for r in records if r['role']=='judge'],
        token_usage={k:sum(((r.get('response')or{}).get('usage')or{}).get(k,0)or 0 for r in records)for k in('prompt_tokens','completion_tokens','total_tokens')},
        model_generation_records=len(records),independent_human_semantic_review='PENDING',
        source_profile_scope='Byte-preserved source logic with declared local auxiliaries/interfaces; not principal published-profile reproduction.')
    if records:
        bad=[r['index']for r in records if r.get('truncated')or(r.get('exception')and not r.get('source_supported_logprobs_fallback'))]
        result['incomplete_model_records']=bad
        if bad:result['qualified']=False
        result['strict_judge_format_pass']=all(d['whole_response_json_boolean']for d in result['judge_diagnostics'])
    else:result['strict_judge_format_pass']=None
    write(directory/'item.json',item);write(directory/'result.json',result)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--family',choices=('qwen','gemma'),required=True);p.add_argument('--mock',action='store_true');a=p.parse_args()
    activate(a.family)
    signal.signal(signal.SIGTERM,lambda *_:(_ for _ in()).throw(KeyboardInterrupt('Owned controller requested stop')))
    for line in sys.stdin:
        request=json.loads(line)
        r=run_job(request['item'],request['out'],a.family,a.mock)
        print(json.dumps(dict(id=r['id'],status=r['status'],qualified=r['qualified'])),flush=True)
if __name__=='__main__':main()
