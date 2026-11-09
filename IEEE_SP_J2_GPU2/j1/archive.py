"""Atomic ZIP snapshots after each stopped profile and final cleanup."""
import zipfile
from pathlib import Path
from reference_study.common import sha


def archive(out, stage=None):
    files = sorted(p for p in out.rglob('*') if p.is_file() and p.name != 'SHA256SUMS')
    (out / 'SHA256SUMS').write_text(''.join(sha(p) + '  ' + str(p.relative_to(out)) + '\n' for p in files))
    files.append(out / 'SHA256SUMS')
    stem = str(out) + (('.after_' + stage) if stage else '')
    target, review = Path(stem + '.zip'), Path(stem + '.review.zip')
    for destination, selected in [(target, files), (review, [p for p in files if
        str(p.relative_to(out)).startswith(('analysis/', 'preflight/', 'client_environments/')) or
        p.parent == out])]:
        temp = Path(str(destination) + '.partial')
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as z:
            for p in selected:
                z.write(p, str(Path(out.name) / p.relative_to(out)))
        temp.replace(destination)
        Path(str(destination) + '.sha256').write_text(sha(destination) + '  ' + destination.name + '\n')
    return target, review
