"""Frozen-source, one-server-at-a-time GPU2 orchestration."""
import argparse
import fcntl
import importlib.metadata
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from reference_study.common import ROOT, GPU_INDEX, GPU_UUID, LOCK_NAME, read, write, verify_package, sha
from .archive import archive
from .design import manifest
from .report import analyze

class StopRequested(BaseException):
    pass

def main(a):
    project = a.project_root.resolve()
    out = project / 'results/user_runs' / a.run_id
    logs = project / 'logs'
    if sys.prefix == sys.base_prefix:
        raise RuntimeError('Use an isolated client environment')
    if os.fstat(a.lock_fd).st_ino != (logs / LOCK_NAME).stat().st_ino:
        raise RuntimeError('Authenticated GPU2 lock missing')
    fcntl.flock(a.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if not a.frozen:
        out.mkdir(parents=True, exist_ok=False)
        identity = verify_package()
        source = out / 'source'
        for rel in identity['files']:
            dst = source / rel; dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dst)
        shutil.copyfile(ROOT / 'PACKAGE_MANIFEST.json', source / 'PACKAGE_MANIFEST.json')
        os.set_inheritable(a.lock_fd, True)
        os.chdir(source)
        os.execve(sys.executable, [sys.executable, '-u', '-m', 'a01.controller', *sys.argv[1:], '--frozen'], dict(os.environ))
    if ROOT.resolve() != (out / 'source').resolve():
        raise RuntimeError('Frozen source identity mismatch')
    verify_package()
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='', PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1')
    for key in ('PYTHONPATH', 'PYTHONHOME', 'DIAG_VARIANT', 'DIAG_MODEL_REVISION', 'E2B_RESUME_DISABLED'):
        env.pop(key, None)
    status = dict(status='STARTING', stage=a.stage, run_id=a.run_id, mock=a.mock,
                  started_epoch=time.time(), physical_gpu=GPU_INDEX, gpu_uuid=GPU_UUID, profiles={})
    manifests = {family: manifest(a.stage, family) for family in ('qwen', 'gemma')}
    for family, m in manifests.items():
        write(out / ('MANIFEST_' + family + '.json'), m)
    clients = dict(RELEASE=str(Path(sys.executable).absolute()))
    if a.stage == 'A0':
        clients['RECORDED'] = str(a.recorded_python.absolute()) if (not a.mock or a.recorded_python.is_file()) else str(Path(sys.executable).absolute())
    write(out / 'CLIENTS.json', clients)
    # Retain the argument path in the frozen controller, never resolve a venv
    # executable symlink into its base interpreter.
    active, rc = None, 0
    stopbeat = threading.Event()
    def update(**kw):
        status.update(kw); write(out / 'status.json', status)
    def beat():
        while not stopbeat.wait(20):
            print('CONTROLLER', status['status'], status.get('active_profile'), 'elapsed', int(time.time()-status['started_epoch']), 's', flush=True)
    thread = threading.Thread(target=beat, daemon=True); thread.start()
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(StopRequested('Owned stop requested')))
    update()
    def command(cmd, log, timeout=600):
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('w') as f:
            result = subprocess.run(cmd, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
        if result.returncode:
            raise RuntimeError('Command failed; inspect ' + str(log))
    try:
        write(out / 'environment.json', dict(python=sys.version, executable=sys.executable, clients=clients,
            serving_python=str(a.serving_python), cache=str(a.cache), package_manifest_sha256=sha(ROOT/'PACKAGE_MANIFEST.json'),
            dependencies={n: importlib.metadata.version(n) for n in ('agentdojo','openai','pydantic','httpx','tenacity')},
            scientific_scope='Local component development, not principal-profile reproduction or an autonomous attack.'))
        for config, python in clients.items():
            if not Path(python).is_file():
                raise RuntimeError('Missing ' + config + ' interpreter: ' + python)
            probe = subprocess.run([python, '-c', 'import sys,importlib.metadata as m,json;print(json.dumps(dict(venv=sys.prefix!=sys.base_prefix,python=list(sys.version_info[:3]),openai=m.version("openai"),agentdojo=m.version("agentdojo"),pydantic=m.version("pydantic"),httpx=m.version("httpx"),tenacity=m.version("tenacity"))))'], env=env, capture_output=True, text=True, timeout=60)
            probe.check_returncode(); data=json.loads(probe.stdout)
            write(out/'client_environments'/(config+'.json'), data)
            if not data['venv'] or data['agentdojo'] != '0.1.35':
                raise RuntimeError('Client requires isolated AgentDojo0.1.35: '+config)
            if not a.mock:
                if config == 'RELEASE' and (data['python'][:2] != [3,10] or not data['openai'].startswith('2.')):
                    raise RuntimeError('RELEASE requires Python3.10/OpenAI2.x')
                if config == 'RECORDED' and (data['python'] != [3,12,15] or any(data[k] != v for k,v in dict(openai='3.35.1',pydantic='2.14.1',httpx='0.28.1',tenacity='9.1.4').items())):
                    raise RuntimeError('Earlier recorded path not recovered exactly: expected Python3.12.15/OpenAI3.35.1. No approximate contrast is silently substituted. A1 can run independently because E1/E2b already used the release-compatible path.')
            command([python, '-c', r'import importlib.metadata as m;print("\n".join(sorted(d.metadata["Name"]+"=="+d.version for d in m.distributions())))'], out/'client_environments'/(config+'.freeze.txt'))
        # All requests and effect calibrations are prepared before taking GPU memory.
        update(status='SOURCE_REQUEST_PREPARATION')
        for family in ('qwen', 'gemma'):
            folder=out/'preflight'/family
            for config, python in clients.items():
                command([python, '-m', 'a01.prepare', '--stage', a.stage, '--family', family, '--out', str(folder/(config+'.json'))], folder/(config+'.log'))
            if a.stage == 'A0':
                release=read(folder/'RELEASE.json'); recorded=read(folder/'RECORDED.json')
                equivalent=release['bodies'] == recorded['bodies']
                write(folder/'CLIENT_PARITY.json', dict(equal=equivalent, request_and_initial_state=True, mock=a.mock,
                    interpretation='Identical prepared source payloads; still observe actual wire bodies and replies separately.' if equivalent else 'Configuration bundle; cannot attribute a response difference to the SDK alone.'))
                if not equivalent:
                    raise RuntimeError('A0 client request/state mismatch: frozen contrast unresolved before inference')
        if not a.mock:
            command([str(a.serving_python), '-c', 'import sys,torch,vllm;assert sys.prefix!=sys.base_prefix;assert vllm.__version__=="0.26.0";assert torch.__version__.startswith("2.11.0");print(sys.version,torch.__version__,vllm.__version__)'], out/'serving_versions.txt',120)
            command([str(a.serving_python), '-c', 'import importlib.metadata as m;print("\\n".join(sorted(d.metadata["Name"]+"=="+d.version for d in m.distributions())))'], out/'serving_packages.txt')
        for family in ('qwen','gemma'):
            if not a.mock:
                # Do not activate profiles in this controller; each profile and
                # rendering process imports its family in a fresh interpreter.
                envfile=out/'preflight'/family/'RELEASE.json'
                command([str(a.serving_python), '-m', 'a01.preflight', '--family', family, '--cache', str(a.cache), '--prepared', str(envfile), '--out', str(out/'preflight'/family/'rendered')], out/'preflight'/family/'rendering.log')
            update(status='RUNNING', active_profile=family)
            cmd=[sys.executable,'-u','-m','a01.profile','--family',family,'--out',str(out/family),
                 '--manifest',str(out/('MANIFEST_'+family+'.json')),'--clients',str(out/'CLIENTS.json'),
                 '--project-root',str(project),'--serving-python',str(a.serving_python),
                 '--cache',str(a.cache),'--lock-fd',str(a.lock_fd),'--workers',str(a.workers)]
            if a.mock:cmd.append('--mock')
            active=subprocess.Popen(cmd,cwd=ROOT,env=env,pass_fds=(a.lock_fd,))
            write(out/(family+'_process.json'),dict(pid=active.pid,argv=cmd))
            while active.poll() is None:time.sleep(.1 if a.mock else 1)
            status['profiles'][family]=active.returncode
            if active.returncode:rc=1
            state=read(out/family/'status.json') if (out/family/'status.json').exists() else {}
            if state.get('status')=='OWNED_CLEANUP_FAILED' or (not a.mock and not state.get('cleanup_verified')):
                raise RuntimeError('Owned server cleanup failed; next model not started')
            update(status='PROFILE_COMPLETE',active_profile=None)
            analyze(out,manifests);archive(out,stage=family)
            print('PROFILE ARCHIVED',family,flush=True)
        update(status='MOCK_COMPLETE_ZERO_INFERENCE' if a.mock else 'COMPLETE_DEVELOPMENT_REVIEW_PENDING',active_profile=None)
    except BaseException as exc:
        rc=1
        update(status='INTERRUPTED' if isinstance(exc,(StopRequested,KeyboardInterrupt)) else 'FAILED',error=str(exc))
        write(out/'fatal_error.json',dict(type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc()))
        print('STOP',str(exc),flush=True)
    finally:
        if active and active.poll() is None:
            active.terminate()
            try:active.wait(timeout=330)
            except subprocess.TimeoutExpired:
                update(status='CLEANUP_PENDING');rc=1
        try:
            counts=analyze(out,manifests)
            for family in manifests:
                if counts[family]['statuses'].get('COMPLETE',0)!=counts[family]['planned']:rc=1
            if rc and status['status'] in ('COMPLETE_DEVELOPMENT_REVIEW_PENDING','MOCK_COMPLETE_ZERO_INFERENCE'):
                update(status='COMPLETE_WITH_TECHNICAL_ISSUES')
        except Exception as exc:
            rc=1;write(out/'analysis_error.json',dict(error=str(exc)))
        update(finished_epoch=time.time(),exit_code=rc)
        log=logs/(a.run_id+'.log')
        if log.is_file():shutil.copyfile(log,out/'controller.log')
        if not active or active.poll() is not None:
            try:
                raw,review=archive(out)
                print('RAW ARCHIVE:',raw,'\nREVIEW ARCHIVE:',review,flush=True)
            except Exception as exc:
                rc=1;write(out/'archive_error.json',dict(error=str(exc)))
        (logs/(a.run_id+'.status')).write_text('exit_code='+str(rc)+'\nstatus='+status['status']+'\nresults='+str(out)+'\n')
        stopbeat.set();thread.join(timeout=1)
    return rc

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--stage',choices=('A0','A1'),default='A1')
    p.add_argument('--project-root',required=True,type=Path)
    p.add_argument('--run-id',required=True)
    p.add_argument('--serving-python',required=True,type=Path)
    p.add_argument('--recorded-python',required=True,type=Path)
    p.add_argument('--cache',required=True,type=Path)
    p.add_argument('--lock-fd',required=True,type=int)
    p.add_argument('--workers',type=int,choices=(2,4,8),default=4)
    p.add_argument('--mock',action='store_true')
    p.add_argument('--frozen',action='store_true')
    a=p.parse_args()
    if not re.fullmatch('[A-Za-z0-9_-]+',a.run_id):p.error('Unsafe run ID')
    for name in ('project_root','serving_python','recorded_python','cache'):
        setattr(a,name,getattr(a,name).expanduser().absolute())
    raise SystemExit(main(a))
