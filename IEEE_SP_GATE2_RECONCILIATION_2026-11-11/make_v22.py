"""Derive analyze_v22.py from the frozen V2.1 analyze.py (read-only) by the single preregistered V2.2 rule
(IEEE_SP_GATE2_ANALYSIS_AMENDMENT_V2.2_2026-11-11.md) plus output redirection. Every replacement must match once."""
import sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
t = src.read_text()
edits = [
 ('ANALYSIS_VERSION = "V2.1"', 'ANALYSIS_VERSION = "V2.2"'),
 ('''            if same(got, good):
                continue
            for value in flat_values(got):''',
  '''            if same(got, good):
                continue
            if key not in TEXT_FIELDS and got in ([], "") and good not in ([], "", None):  # V2.2 empty_value
                material = True
                row["substitutions"].append({"field": key, "value": got, "source": "empty_value"})
                continue
            for value in flat_values(got):'''),
 ('def analyze(run):', 'def analyze(run, out):'),
 ('(run / "analysis.json").write_text', '(out / "analysis_v2.2.json").write_text'),
 ('with (run / "episodes.csv").open("w", newline="") as f:', 'with (out / "episodes_v2.2.csv").open("w", newline="") as f:'),
 ('    report(run, result, plan)\n    return result', '    report(out, result, plan)\n    return result'),
  ('(run / "report.txt").write_text', '(run / "report_v2.2.txt").write_text'),
]
for a, b in edits:
    if t.count(a) != 1:
        raise SystemExit(f"edit target not found exactly once: {a[:60]!r}")
    t = t.replace(a, b)
dst.write_text(t)
