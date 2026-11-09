"""Build compact, GitHub-sized evidence extracts from raw run outputs (read-only).

The raw bridge episodes (~490 MB) and final-experiment ledgers (E1R.jsonl 673 MB) are too large
for the light GitHub mirror. This script writes per-episode / per-record CSV tables that contain
every field used by the unified authority's Part I Appendix C (C.3, C.4, §4.5), plus a manifest
with SHA-256 digests of every source file, so the extracts can be checked against the local raw
archives (hashes in Part II §11).

Run from IEEE_SP_2027/:  python3 v3_reanalysis_scripts/extract_artifacts.py
"""
import csv, glob, hashlib, json, os, sys

OUT = 'artifact_extracts'
E13 = 'IEEE_SP_END_TO_END_LARGE_GPU23/runs/20261108T002314Z_133843_16274'
E14 = 'IEEE_SP_QWEN_FORMAT_REPAIR/runs/20261108T034212Z_uvckj4cb'
E15 = 'IEEE_SP_FINAL_EXPERIMENT_GPU3_SHARED_PREFILL/runs/20261108T232225Z_3654860_31695'
WITNESSES = ['banking.3.0.live.1000']   # full episodes copied for every arm (Part I §4.1 witness)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def forms(v):
    if isinstance(v, float):
        return {repr(v), str(int(v)) if v == int(v) else repr(v)}
    if isinstance(v, list):
        return {str(x) for x in v}
    return {str(v)}


def bridge(profile, episode_dir, plan):
    bases = {b['id']: b for b in plan['bases']}
    files = sorted(glob.glob(os.path.join(episode_dir, '*.json')))
    rows, digests = [], []
    for f in files:
        digests.append(os.path.basename(f) + ' ' + sha(f))
        y = json.load(open(f))
        c, arm = y['cell'], y['arm']
        b = bases[c['base']]
        events = y['events']
        commits = [cm for e in events for cm in ((e.get('result') or {}).get('commits') or [])]
        sans = [s for e in events for s in (e.get('sanitizers') or [])]
        san_text = ' '.join(s['result']['text'] for s in sans)
        proposal = next((e['proposal'] for e in events
                         if (e.get('proposal') or {}).get('function') == b['action']), None)
        dispatched = next((e.get('dispatched') for e in events
                           if (e.get('dispatched') or {}).get('function') == b['action']), None)
        rows.append(dict(
            profile=profile, episode=c['id'], base=c['base'], family=b['family'], action=b['action'],
            identifier_field=b['identifier'], parameter_field=b['parameter'], layout=b['layout'], arm=arm,
            flex=c['flex'], attack=c['attack'], source=c['source'], linked=c['linked'], copy=c['copy'],
            terminal=y.get('terminal'), n_events=len(events),
            flagged=int(any(e.get('flags') for e in events)), sanitized=int(bool(sans)),
            identifier_retained='' if not sans else int(any(t in san_text for t in forms(b['good'][b['identifier']]))),
            parameter_retained='' if not sans else int(any(t in san_text for t in forms(b['good'][b['parameter']]))),
            denied=int(any((e.get('result') or {}).get('denied') for e in events)),
            commit_classes='|'.join(cm['class'] for cm in commits),
            first_commit_args=json.dumps(commits[0]['args'], sort_keys=True) if commits else '',
            first_proposal_args=json.dumps(proposal['args'], sort_keys=True) if proposal else '',
            first_dispatched_args=json.dumps(dispatched['args'], sort_keys=True) if dispatched else '',
            good_args=json.dumps(b['good'], sort_keys=True), alt_args=json.dumps(b['alt'], sort_keys=True),
        ))
    return rows, digests


def primary(scores):
    sp = [s for s in scores['spans'] if s.get('primary')]
    return sp[0] if sp else None


def e1r(path):
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            c = r['cell']
            row = dict(record=c['id'], base=r['base'], cluster=r['cluster'], family=r['family'], seed=r['seed'],
                       status=r['status'], exposed=r['exposed'], trusted=c['trusted'], duplicate=c['duplicate'],
                       layout=c['layout'], echo=c['echo'], edit=c['edit'], force=c['force'])
            for tag, key in (('lawful', 'scores'), ('forbidden', 'alternate_scores')):
                sp = primary(r[key]) if r.get(key) else None
                if sp:
                    row.update({f'{tag}_scalar': sp['scalar'], f'{tag}_delta_user': sp['delta_user'],
                                f'{tag}_delta_tool': sp['delta_tool'],
                                **{f'{tag}_part_{k}': v for k, v in sp['parts'].items()},
                                **{f'{tag}_patched_{k}': v for k, v in sp['patched'].items()}})
            for arm, a in r['arms'].items():
                row[f'arm_{arm}_status'] = a.get('status')
                row[f'arm_{arm}_outcome'] = a.get('outcome')
            rows.append(row)
    return rows


def e2l(path):
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            c = r['cell']
            row = dict(record=c['id'], base=r['base'], cluster=r['cluster'], family=r['family'], seed=r['seed'],
                       status=r['status'], exposed=r['exposed'], trusted=c['trusted'], duplicate=c['duplicate'],
                       layout=c['layout'], echo=c['echo'], edit=c['edit'], force=c['force'])
            for arm, a in r['arms'].items():
                row[f'arm_{arm}_status'] = a.get('status')
                row[f'arm_{arm}_outcome'] = a.get('outcome')
            rows.append(row)
    return rows


def write(name, rows):
    path = os.path.join(OUT, name)
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    return dict(path=path, rows=len(rows), bytes=os.path.getsize(path), sha256=sha(path))


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'witness_episodes'), exist_ok=True)
    plan_path = os.path.join(E13, 'bridge_plan.json')
    plan = json.load(open(plan_path))
    manifest = dict(script='v3_reanalysis_scripts/extract_artifacts.py',
                    note='Derived, read-only extracts. Raw sources stay local; see Part II §11 for archive hashes.',
                    sources={}, outputs=[])
    manifest['sources'][plan_path] = sha(plan_path)
    for profile, d, out in (('gemma', E13 + '/model_gemma/bridge/episodes', 'bridge_E13_gemma_episodes.csv'),
                            ('qwen_e13_censored', E13 + '/model_qwen/bridge/episodes', 'bridge_E13_qwen_censored_episodes.csv'),
                            ('qwen_e14_repaired', E14 + '/full_live/episodes', 'bridge_E14_qwen_episodes.csv')):
        rows, digests = bridge(profile, d, plan)
        dig = os.path.join(OUT, out.replace('.csv', '.source_SHA256SUMS'))
        open(dig, 'w').write('\n'.join(digests) + '\n')
        manifest['sources'][d] = dict(files=len(digests), sha256_of_listing=sha(dig))
        manifest['outputs'].append(write(out, rows))
        for w in WITNESSES:
            for f in glob.glob(os.path.join(d, w + '.*.json')):
                dst = os.path.join(OUT, 'witness_episodes', profile + '__' + os.path.basename(f))
                open(dst, 'wb').write(open(f, 'rb').read())
    for name, fn, src in (('final_E1R_qwen_records.csv', e1r, E15 + '/qwen/E1R.jsonl'),
                          ('final_E2L_qwen_records.csv', e2l, E15 + '/qwen/E2L.jsonl')):
        manifest['sources'][src] = sha(src)
        manifest['outputs'].append(write(name, fn(src)))
    json.dump(manifest, open(os.path.join(OUT, 'EXTRACT_MANIFEST.json'), 'w'), indent=2)
    print(json.dumps(manifest['outputs'], indent=1))


if __name__ == '__main__':
    sys.exit(main())
