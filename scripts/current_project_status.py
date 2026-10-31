"""Read-only status inspection. No model imports, Git writes or process control."""
from pathlib import Path
import argparse, json

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    current=json.loads((root/'CURRENT_EXPERIMENT.json').read_text())
    print('Current code:',current['directory'])
    print('GPU:',current['physical_gpu'],'; planned records:',current['planned_case_records'])
    print('Scientific status:',current['scientific_status'])
    base=root/'results/user_runs'
    runs=[args.run] if args.run else sorted(base.glob('reference_study_gpu2_*'),key=lambda p:p.stat().st_mtime,reverse=True)[:5]
    runs=[p for p in runs if p.is_dir()]
    if not runs:
        print('No current P0-P3 run directory is available here; no outcome inferred.')
    for run in runs:
        print('\nRUN',run)
        for path in [run/'status.json',run/'qwen/status.json',run/'gemma/status.json',run/'analysis/COMPLETENESS.json']:
            if path.is_file():
                try: print(path.relative_to(run),json.dumps(json.loads(path.read_text()))[:2200])
                except (OSError,ValueError): print(path.name,': incomplete/unreadable snapshot')
        for family in ['qwen','gemma']:
            files=list((run/family).glob('P*/**/result.json'))
            print(family,':',len(files),'saved P-stage result records; completion and mock flags remain in each record')
    print('\nHistorical panels: consult EXPERIMENT_HISTORY.json; retained Qwen records are not new inference.')

if __name__=='__main__':main()
