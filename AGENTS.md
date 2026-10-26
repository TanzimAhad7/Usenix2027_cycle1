# IEEE S&P whole-plan project instructions

This repository supports the entire standalone v6.2 research program and a new IEEE S&P paper. The sole active authority is `docs/RESEARCH_PLAN.md`. Rejected prior work is the inherited scientific/implementation basis, not a rebuttal framework. Do not substitute the immediate R/B diagnostic for the whole plan.

The selected inherited tree is local under `research_basis/`; selection, exclusions, original hashes, every plan section, reviewer obligations and remaining work are documented. Preserve its original bytes. New implementation and scientific corrections belong in separately named code/analysis trees with actual tests and provenance. No research command may depend on an external old project, archive or venv.

- Only physical GPU 2 or 3 is authorized for model computation. Select explicitly and verify actual server worker placement. Never fall back to GPU 0/1.
- Use current root `LAUNCH.sh` for setup and research: nohup, unique log/PID/status, project `.venv`. System Python may bootstrap the venv only. Do not install globally.
- Inherited entrypoints/GPU defaults are historical source. Do not run them as current commands. The root figure worker uses only CPU stage 12 with local frozen parents; other old fresh GPU wrappers need the documented repairs and qualification.
- Distinguish inventory integrity, frozen reanalysis, historical display reproduction, forced components, fresh inference, independent semantic review and confirmation. Do not upgrade one into another.
- Keep all outcomes, raw IDs, failures, nulls, unknowns, source/rendering/configuration changes and exclusions. Preserve historical labels; corrected claims need their own primitive records. Reruns are not independent task structures.
- Read relevant papers fully when studying them, including methods, figures, tables, limitations, appendices and artifacts; record exact inspection coverage. Copied PDFs and targeted inspections are not full readings.
- Select one important new claim from evidence and nearest-work differences. No deadline-based scientific decisions or benchmark-only novelty. Human review, actual model qualification and new experiments are work, not artifacts that can be declared done by generating a template.
