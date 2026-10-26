#!/usr/bin/env python3
"""Read saved per-model progress without changing experiment state."""
import argparse
import json
from collections import Counter
from pathlib import Path


def load(path, problems):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        problems.append(f'{path.name}: {type(exc).__name__}')
        return None


def describe(run):
    problems = []
    parent = load(run / 'status.json', problems) or {}
    profiles = {}
    for family in ('qwen', 'gemma'):
        local = run / 'models' / family
        state = load(local / 'status.json', problems) or {}
        census = load(local / 'census.json', problems) or {}
        results = []
        for path in sorted((local / 'workflows').glob('*/result.json')):
            value = load(path, problems)
            if isinstance(value, dict):
                results.append(value)
        workflow_counts = dict(Counter(census.get('workflows', {}).values()))
        terminal = sum(n for key, n in workflow_counts.items() if key not in ('SCHEDULED', 'RUNNING'))
        profiles[family] = {
            'status': state.get('status', 'NO_CHILD_STATUS_SUPPLIED'),
            'active_cases': state.get('active_cases', state.get('active')),
            'workflow_census': workflow_counts,
            'terminal_census_entries': terminal,
            'saved_result_files': len(results),
            'producer_qualified_results': sum(row.get('qualified') is True for row in results),
            'saved_outcome_labels': dict(Counter(row.get('outcome', 'MISSING_LABEL') for row in results)),
            'conditional_census': dict(Counter(census.get('forks', {}).values())),
            'terminal_census_minus_saved_results': terminal - len(results),
        }
    return {
        'run_id': run.name,
        'parent_status': parent.get('status', 'NO_PARENT_STATUS_SUPPLIED'),
        'parent_active_model': parent.get('active_model'),
        'profiles': profiles,
        'read_problems': problems,
        'scope': 'Saved file contents at read time, potentially non-atomic. Producer labels are not independently audited effects. Parent census refreshes at model boundaries. Missing results are not safe results. This reader performs no inference or mutation.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, help='Explicit run directory; otherwise newest named parallel campaign')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.run is None:
        runs = sorted(p for p in (root / 'results/user_runs').glob('parallel_reference_gpu23_*') if p.is_dir())
        if not runs:
            parser.exit(1, 'No saved parallel-reference run directory found. A lightweight clone may not contain runs.\n')
        target = runs[-1]
    else:
        target = args.run.resolve()
        if not target.is_dir():
            parser.error('Run directory does not exist')
    print(json.dumps(describe(target), indent=2))


if __name__ == '__main__':
    main()
