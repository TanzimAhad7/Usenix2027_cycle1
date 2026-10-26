# Source attribution

The selected original AttriGuard source, OpenAI/local driver implementations,
pipeline factory and release README in `release_native_study/vendor/` were copied
without edits from the retained public artifact associated with:

He et al., *AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via
Causal Attribution of Tool Invocations*, USENIX Security 2026.

Public artifact record: https://zenodo.org/records/20308739 . Exact retained ZIP
and file hashes are recorded in `vendor/SOURCE_IDENTITY.json`. The artifact's
provided attribution is retained; this package does not claim authorship of
those files or invent a replacement license. No separate license text was
available among the selected retained release members used for this package.

AgentDojo 0.1.35 and its dependencies are installed research dependencies, not
vendored project-owned code. The study executes its actual native runtime,
Inbox and Slack functions. Native source fingerprints are checked before use.

New task fixtures, observation, conventional gate, telemetry/checkpoint hooks,
controller and analysis belong to this research implementation. Existing
project-owned process/cache helper code was reused locally and its exact bytes
are identified in `SOURCE_PROVENANCE.json`. No code import requires another
project directory. A model cache path supplies weights only.
