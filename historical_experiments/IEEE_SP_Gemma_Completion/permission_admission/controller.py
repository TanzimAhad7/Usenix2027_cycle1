"""Gemma-only completion; preserves verified Qwen readouts from the parent."""
from __future__ import annotations

import argparse
import fcntl
import importlib.metadata
import json
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import threading
import time
import traceback
from pathlib import Path

from .util import ROOT, activate, file_hash, read, write, verify_package
from .design import manifest
from .report import analyze
from .parent_evidence import default_parent, retain
from .device import GPU_INDEX, GPU_UUID, LOCK_NAME


class StopRequested(BaseException):
    pass


def package(out):
    paths = [p for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'SHA256SUMS']
    (out / 'SHA256SUMS').write_text(''.join(file_hash(p) + '  ' + str(p.relative_to(out)) + '\n' for p in paths))
    raw = Path(str(out) + '.tar.gz')
    temp = Path(str(raw) + '.partial')
    with tarfile.open(temp, 'w:gz', compresslevel=1) as archive:
        archive.add(out, arcname=out.name)
    temp.replace(raw)
    Path(str(raw) + '.sha256').write_text(file_hash(raw) + '  ' + raw.name + '\n')
    review = Path(str(out) + '.review.tar.gz')
    with tarfile.open(review, 'w:gz', compresslevel=1) as archive:
        for relative in ('status.json', 'FROZEN_MANIFEST.json', 'analysis', 'cpu_qualification/qualification.json',
                         'cpu_qualification/qualification.log', 'execution_environment.json'):
            p = out / relative
            if p.exists():
                archive.add(p, arcname=out.name + '/' + relative)
        for family in ('qwen', 'gemma'):
            for name in ('status.json', 'census.json', 'schedule_events.jsonl', 'fatal_error.json'):
                p = out / family / name
                if p.exists():
                    archive.add(p, arcname=out.name + '/' + family + '/' + name)
    return raw, review


def main(args):
    if sys.prefix == sys.base_prefix:
        raise RuntimeError('Research must run inside a virtual environment')
    if sys.version_info < (3, 11):
        raise RuntimeError('Python 3.11+ required; Python 3.12 tested')
    project = args.project_root.resolve()
    out = project / 'results/user_runs' / args.run_id
    out.mkdir(parents=True, exist_ok=False)
    logs = project / 'logs'
    logs.mkdir(exist_ok=True)
    lock = (logs / LOCK_NAME).open('a')
    active_profile = None
    status = dict(status='STARTING', run_id=args.run_id, started_epoch=time.time(),
                  mode='CPU_ONLY' if args.cpu_only else 'MOCK_ZERO_INFERENCE' if args.mock else 'MODEL_EXPERIMENT',
                  profiles={}, project='USENIX-based IEEE S&P; ICLR project excluded',
                  acquisition_profile='gemma',qwen_inference_enabled=False,
                  physical_gpu=GPU_INDEX,gpu_uuid=GPU_UUID)
    frozen = manifest()
    write(out / 'FROZEN_MANIFEST.json', frozen)
    acquired = False
    heartbeat_stop = threading.Event()
    archived = None
    review = None
    rc = 0

    def update(**values):
        status.update(values)
        write(out / 'status.json', status)

    def heartbeat():
        while not heartbeat_stop.wait(20):
            print(f'CONTROLLER status={status["status"]} profile={status.get("active_profile")} '
                  f'elapsed={int(time.time()-status["started_epoch"])}s results={out}', flush=True)

    def stop_child():
        if active_profile is not None and active_profile.poll() is None:
            active_profile.terminate()
            try:
                active_profile.wait(timeout=110)
            except subprocess.TimeoutExpired:
                # Profile holds separate server ownership records. Do not use
                # pkill or signal an unauthenticated process group.
                from reference_discovery_parallel.base import serving
                folder = out / status['active_profile'] / 'serving'
                identities = read(folder / 'owned_identities.json') if (folder / 'owned_identities.json').is_file() else {}
                for pid, started in identities.items():
                    if started is not None and serving.proc_start(int(pid)) == started:
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                        except ProcessLookupError:
                            pass
                active_profile.kill()
                active_profile.wait()
                raise RuntimeError('Profile cleanup timed out; inspect retained owned identities before any next launch')

    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(StopRequested('SIGTERM')))
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except BlockingIOError:
            update(status='BLOCKED_CONCURRENT_SEQUENCE')
            raise RuntimeError('Another campaign owns logs/gpu2_sequence.lock. No model was started or stopped.')
        verify_package()
        source = out / 'source'
        source.mkdir()
        for relative in read(ROOT / 'PACKAGE_MANIFEST.json')['files']:
            dest = source / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dest)
        shutil.copyfile(ROOT / 'PACKAGE_MANIFEST.json', source / 'PACKAGE_MANIFEST.json')
        update(status='VERIFYING_RETAINED_QWEN')
        parent_path=args.parent if args.parent else default_parent(project)
        parent_receipt=retain(parent_path,out,frozen)
        print('RETAINED QWEN:',parent_receipt['retained_qwen_records'],'verified records; zero Qwen inference in this run.',flush=True)
        write(out / 'execution_environment.json', dict(python=sys.version, executable=sys.executable,
              prefix=sys.prefix, research_cuda_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),
              dependencies={name: importlib.metadata.version(name) for name in ('agentdojo', 'openai', 'pydantic', 'httpx', 'tenacity')},
              package_manifest_sha256=file_hash(ROOT / 'PACKAGE_MANIFEST.json'),
              scientific_redraws=0, workers=args.workers,
              deadline_hours=args.max_hours, physical_gpu=GPU_INDEX, gpu_uuid=GPU_UUID,
              cuda_visibility_policy='Only owned Gemma server sees physical GPU 2 by UUID; research workers have no CUDA devices'))
        freeze = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True, timeout=30)
        (out / 'research_packages.txt').write_text(freeze.stdout + freeze.stderr)
        activate('qwen')
        update(status='CPU_QUALIFICATION')
        from .qualification import qualify
        q = qualify(out / 'cpu_qualification')
        print(f'CPU QUALIFICATION: {q["status"]}; {q["tests_run"]} tests; zero inference', flush=True)
        if q['status'] != 'PASS':
            raise RuntimeError('CPU qualification failed; no model will be started')
        if args.cpu_only:
            update(status='CPU_QUALIFICATION_COMPLETE_ZERO_INFERENCE')
        else:
            # Preserve the venv's executable path: resolving its symlink would
            # invoke the base interpreter without .venv-serving packages.
            serving_python = Path(os.path.abspath(args.serving_python))
            cache = args.cache
            from .completion_models import PROFILES
            from reference_discovery_parallel.base import serving
            if not args.mock:
                update(status='PREFLIGHT_GEMMA')
                if not serving_python.is_file():
                    raise RuntimeError('Missing existing .venv-serving/bin/python; no environment is replaced')
                version_command = [str(serving_python), '-c',
                    'import sys,torch,vllm,json; print(json.dumps(dict(python=sys.version,torch=torch.__version__,vllm=vllm.__version__,venv=sys.prefix!=sys.base_prefix)))']
                version_process = subprocess.run(version_command, capture_output=True, text=True, timeout=90,
                                                   env={**os.environ, 'CUDA_VISIBLE_DEVICES': ''})
                (out / 'serving_version_process.log').write_text(version_process.stdout + version_process.stderr)
                version_process.check_returncode()
                versions = json.loads(version_process.stdout.strip().splitlines()[-1])
                write(out / 'serving_versions.json', versions)
                if not versions['venv'] or versions['vllm'] != '0.26.0' or not versions['torch'].startswith('2.11.0'):
                    raise RuntimeError('Serving profile requires vLLM 0.26.0 / torch 2.11.0 in a venv; no install/change attempted')
                env = os.environ.copy()
                env.update(CUDA_VISIBLE_DEVICES='', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                           PATH=str(serving_python.parent) + os.pathsep + env.get('PATH', ''),
                           PYTHONPATH=str(source)+os.pathsep+str(source / 'retained'))
                env.pop('PYTHONHOME', None)
                for family, p in PROFILES.items():
                    snap, identity = serving.inspect_snapshot(Path(cache) / ('models--' + p['hub'].replace('/', '--')), p['hub'], p['revision'])
                    folder = out / 'template_qualification' / family
                    folder.mkdir(parents=True)
                    write(folder / 'snapshot_identity.json', identity)
                    with (folder / 'process.log').open('w') as stream:
                        process = subprocess.run([str(serving_python), '-m', 'permission_admission.completion_models',
                            '--snapshot', str(snap), '--out', str(folder)],
                            cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=600)
                    if process.returncode != 0 or read(folder / 'qualification.json')['status'] != 'PASS':
                        raise RuntimeError('Cached template/parser qualification failed: ' + family)
            deadline = None if args.max_hours is None else time.time() + args.max_hours * 3600
            for family in ('gemma',):
                if deadline is not None and time.time() >= deadline:
                    raise StopRequested('Optional collection deadline reached before ' + family)
                update(status='RUNNING_PROFILE', active_profile=family)
                cmd = [sys.executable, '-u', '-m', 'permission_admission.profile', '--family', family,
                       '--out', str(out / family), '--manifest', str(out / 'FROZEN_MANIFEST.json'),
                       '--project-root', str(project), '--serving-python', str(serving_python),
                       '--cache', cache, '--lock-fd', str(lock.fileno()), '--workers', str(args.workers)]
                if args.mock:
                    cmd.append('--mock')
                if deadline is not None:
                    cmd += ['--deadline', str(deadline)]
                env = os.environ.copy()
                env.pop('PYTHONPATH', None)
                env.update(CUDA_VISIBLE_DEVICES='', REFERENCE_DISCOVERY_MODEL_FAMILY=family)
                active_profile = subprocess.Popen(cmd, cwd=source, env=env, pass_fds=(lock.fileno(),))
                while active_profile.poll() is None:
                    time.sleep(.3 if args.mock else 2)
                code = active_profile.returncode
                status['profiles'][family] = code
                update()
                if code:
                    rc = 1
                    print(f'{family} ended with technical issues; evidence retained. No failed scientific cell is redrawn.', flush=True)
                if (out / family / 'status.json').is_file() and read(out / family / 'status.json')['status'] == 'OWNED_CLEANUP_FAILED':
                    raise RuntimeError('Owned cleanup failed; refusing to start another server')
            update(status='COMPLETE_WITH_TECHNICAL_ISSUES' if rc else
                   'MOCK_COMPLETE_ZERO_INFERENCE' if args.mock else 'COMPLETE_REVIEW_PENDING', active_profile=None)
    except BaseException as exc:
        rc = 2 if status['status'] == 'BLOCKED_CONCURRENT_SEQUENCE' else 1
        if status['status'] != 'BLOCKED_CONCURRENT_SEQUENCE':
            update(status='INTERRUPTED' if isinstance(exc, (StopRequested, KeyboardInterrupt)) else 'FAILED')
        write(out / 'fatal_error.json', {'type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()})
        print('STOP:', str(exc), flush=True)
    finally:
        try:
            stop_child()
        except BaseException as exc:
            rc = 1
            update(status='OWNED_CLEANUP_FAILED', cleanup_error=str(exc))
        try:
            summary = analyze(out, frozen)
            write(out / 'analysis/COMPLETENESS.json', summary)
            from .judge_format import audit as audit_judge_format
            audit_judge_format(out, frozen)
            from .completion_models import PROFILE
            planned_ids=[('E1',i['id']) for i in frozen['E1']]+[('E2',i['id']) for i in frozen['E2']]+[('E3',i['id']) for b in frozen['E3_blocks'] for i in b]
            new_results=[read(out/'gemma'/panel/ident/'result.json') for panel,ident in planned_ids if (out/'gemma'/panel/ident/'result.json').is_file()]
            new_summary=dict(planned=len(planned_ids),recorded=len(new_results),qualified=sum(bool(r['qualified']) for r in new_results),
                current_acquisition='Gemma only',profile=PROFILE,retained_qwen_records=544 if (out/'qwen/RETAINED_EVIDENCE.json').is_file() else 0,
                new_qwen_inference=0,old_qwen_qualification_flags_preserved=True,
                interpretation='Combined outputs include historical Qwen readouts and the amended Gemma interface. '
                    'Completion exit status depends on new Gemma collection, not old Qwen strict-format flags.')
            new_summary['source_paths_or_workflows_complete'] = sum(
                bool(r.get('source_path_complete')) if r.get('panel') in ('E1','E2') else bool(r.get('qualified'))
                for r in new_results)
            new_summary['qualification_profile'] = 'INTERFACE_GATE_BARE_OR_SINGLE_FENCED_JSON_V3_SOURCE_UNMODIFIED'
            new_summary['strict_format_only_unqualified'] = sum(
                r.get('panel') in ('E1','E2') and bool(r.get('source_path_complete')) and not r.get('qualified')
                for r in new_results)
            write(out/'analysis/NEW_GEMMA_COMPLETENESS.json',new_summary)
            write(out/'analysis/ACQUISITION_PROVENANCE.json',dict(new_profile='gemma',
                amended_interface=PROFILE['interface'],new_qwen_inference=0,
                retained_qwen_run='permission_admission_20261027T205610Z_3429255_17219',
                original_qualification_flags_preserved=True,
                warning='The 1088-row combined panel includes 544 retained Qwen readouts and up to 544 new Gemma results. '
                        'It is not 1088 newly executed cases. Qwen whole-response JSON flags remain unchanged.'))
            findings=out/'analysis/FINDINGS.md'
            if findings.is_file():
                findings.write_text('# Acquisition provenance\n\nThis run acquires Gemma only under the declared strict JSON/XML interface amendment. '
                    'Qwen readouts are retained from the completed parent; zero Qwen inference is performed. '
                    'Read NEW_GEMMA_COMPLETENESS.json separately from combined totals. Original Qwen qualification flags remain unchanged.\n\n'+findings.read_text())
            if status['status'] in ('COMPLETE_REVIEW_PENDING', 'MOCK_COMPLETE_ZERO_INFERENCE') and new_summary['recorded'] != new_summary['planned']:
                rc = 1
                update(status='COMPLETE_WITH_MISSING_RECORDS')
            elif status['status'] in ('COMPLETE_REVIEW_PENDING', 'MOCK_COMPLETE_ZERO_INFERENCE') and new_summary['qualified'] != new_summary['planned']:
                rc = 1
                if new_summary['source_paths_or_workflows_complete'] == new_summary['planned']:
                    update(status='COMPLETE_WITH_STRICT_FORMAT_WARNINGS')
                    print('All new Gemma cases collected; original strict JSON flags include failures. '
                          'Raw source decisions are preserved. Read FORMAT_AND_COLLECTION_AUDIT.json; '
                          'do not equate collection completion with strict semantic qualification.', flush=True)
                else:
                    update(status='COMPLETE_WITH_TECHNICAL_ISSUES')
        except Exception as exc:
            rc = 1
            write(out / 'analysis_failure.json', {'error': str(exc), 'traceback': traceback.format_exc()})
        update(finished_epoch=time.time(), exit_code=rc)
        log = logs / (args.run_id + '.log')
        if log.is_file():
            shutil.copyfile(log, out / 'controller.log')
        try:
            print('PACKAGING new Gemma raw evidence and linked Qwen readouts; GPU collection has ended.', flush=True)
            archived, review = package(out)
            print('COMPLETE RAW ARCHIVE:', archived, flush=True)
            print('COMPACT REVIEW:', review, flush=True)
        except Exception as exc:
            rc = 1
            update(status='ARCHIVE_FAILED_RAW_DIRECTORY_PRESERVED', archive_error=str(exc))
        (logs / (args.run_id + '.status')).write_text(f'exit_code={rc}\nstatus={status["status"]}\nresults={out}\narchive={archived}\nreview={review}\n')
        heartbeat_stop.set()
        thread.join(timeout=1)
        if acquired:
            fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()
    return rc


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--project-root', required=True, type=Path)
    p.add_argument('--run-id', required=True)
    p.add_argument('--serving-python', required=True, type=Path)
    p.add_argument('--cache', default='/home/tahad/ACM_SAC_2027/repairbench_gpu23_ready/.hf_cache')
    p.add_argument('--parent',type=Path,help='Audited original result directory or full raw tar.gz; auto-detected by default')
    p.add_argument('--workers', type=int, choices=[1, 2], default=2)
    p.add_argument('--max-hours', type=float)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--cpu-only', action='store_true')
    mode.add_argument('--mock', action='store_true')
    args = p.parse_args()
    if args.max_hours is not None and args.max_hours <= 0:
        p.error('--max-hours must be positive')
    if not __import__('re').fullmatch(r'[A-Za-z0-9_-]+', args.run_id):
        p.error('Unsafe run ID')
    raise SystemExit(main(args))

