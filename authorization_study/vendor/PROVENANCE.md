# Supplied third-party source

`AttriGuard.py` is copied unchanged from the user's A674 research artifact at:

`third_party/integrations/attriguard_zenodo_v1/usenix-artifacts/main/pipeline/AttriGuard.py`

SHA-256: `6d28e2208efbd521bf3f2e90c553e57b11c786e65564eababacb8cdf4f8050d8`.

The same bytes occur at `usenix-artifacts/main/pipeline/AttriGuard.py` inside the third-party ZIP bundled with that artifact. This source binding does not attest any other upstream version. The adaptive-attack copy is a different file and is not silently substituted.

Associated work: Yu He, Haozhe Zhu, Yiming Li, Shuo Shao, Hongwei Yao, Zhihao Liu and Zhan Qin, *AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via Causal Attribution of Tool Invocations*. Attribution and rights of the original source remain with its authors. No additional license for that source is inferred here.

Named interventions are generated at runtime with explicit diffs. AgentDojo is installed as a separate pinned dependency rather than replaced by copied stand-ins. The three core runtime hash comparisons are in the evidence directory.
