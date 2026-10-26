# Independent A674 audit evidence

Prepared 19 October 2026. This bundle accompanies `IEEE_SP_Deep_Analysis_and_Redesign.md` and `IEEE_SP_v6_Independent_Critique.md`.

## Contents

- `independent_audit.py`: standard-library-only executable audit.
- `audit_results.json`: independently reconstructed aggregates and bounded source-fixture observations.
- `artifact_inventory.csv`: every original ZIP member, bytes, SHA-256, line count, and Python definition locations.
- `code_content_groups.json`: Python/shell paths grouped by identical content.
- `source_manifest.json`: hashes and sizes of supplied sources and retrieved research PDFs.
- `reading_and_code_coverage.md`: fresh reading/code-inspection scope and unresolved evidence.
- `frozen_verification.log`: captured output of the supplied results-only verifier; its working-tree limitation is documented below.
- `raw_zip_integrity.json`: separate integrity result for the unchanged original archive.

The research PDFs, original A674 archive, private transcripts, model weights, API credentials, and v6's separately named newer code release are not included. Retain the original attached ZIP to rerun this audit.

## Reproduce

Use Python 3.10 or newer. No third-party installation, network, model/API, or GPU is needed:

```bash
python3 independent_audit.py \
  --artifact-zip '/absolute/path/influence-is-not-authority-artifact-A674(2).zip' \
  --output independent-audit-output
```

The script reads directly from the archive and writes to the selected output directory. It does not modify the archive or execute its shell setup/install scripts. It parses all distributed Python files and executes selected trusted audit subjects as described below. Run only on the supplied archive whose hash is recorded in `source_manifest.json`.

## Interpretation

The original archive passes its 5,787-entry manifest. The inventory includes `SHA256SUMS.txt` itself, hence 5,788 total payload members. Python parsing establishes syntactic readability, not dependency compatibility or correctness. Duplicate groups identify identical file contents, not independent experiments.

Source contrasts are reconstructed from `condition_scores.jsonl` and N3 `SCIENCE_SCORES.jsonl`. N3 uses its own nuisance-replication baseline; the script does not silently substitute an earlier A14 snapshot. Live counts come from `studies/08_live_end_to_end/frozen_results/scientific_v1/RUN_ROWS.jsonl`. Historical PAEF and utility labels are counted as distributed; this does not certify their authorization semantics.

The oracle probes execute the supplied `implementation_evidence/paef_oracle.py`. They show URL normalization and negation-sensitive examples, not the number of historical records affected. The two-payment example uses a one-target contract: failure under that contract is not itself an oracle defect. It illustrates why legal multiplicity must be specified rather than assumed.

The source-executed guard fixtures parse the supplied `AttriGuard.py`, retain its definitions/constants, replace unavailable imports with declared minimal stand-ins, and use deterministic model responses. A fake non-idempotent runtime records committed simulated payments. These fixtures establish bounded behavior of supplied source control flow: occurrence-insensitive matching/receipt mapping, malformed fuzzy-response handling, and stale route reasons. They do not establish autonomous reachability, deployment prevalence, full-runtime exploitability, or behavior of another source revision. The complete fixture setup is in the script.

The supplied results verifier reported 56 PASS / 0 FAIL. Its later tree-integrity step found an extra temporary file in the extracted working directory, absent from the original ZIP. That invocation therefore did not complete its later source-coverage stage. The independent direct-ZIP check passes; do not interpret the working-tree stop as archive corruption or the 56 checks as a fresh model replication.

The independent audit was rerun into a second output directory and its machine-readable results and inventories compared for equality. This checks deterministic audit reproducibility, not research-model replication.
