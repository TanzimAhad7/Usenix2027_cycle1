# Development evidence record

All local research attempts are retained. The final code should be used for new reruns.

| Directory | Status | Interpretation |
| --- | --- | --- |
| `component_run` | 90 executions; 55/55 checks passed | Initial control-flow matrix, before adding the skipped-branch error chain and explicit scripted fuzzy judge. Development evidence only. |
| `component_run_with_controls` | 98 executions; 58/61 checks passed | Exposed a harness defect: the list-valued lookup schedule was shared and consumed across arms. This invalidated comparisons involving that new scenario. |
| `qualified_component_run` | 98 executions; 61/61 checks passed | The lookup schedule was deep-copied per episode. A regression test now checks schedule independence. |
| `final_component_run` | 98 executions; 61/61 checks passed | Canonical packaged run, with harness hash, runtime hashes, and the final metadata logic. |

The failure was corrected in the harness, not hidden or reclassified as a model failure. No model or external API call was involved in these component runs. Earlier runs do not carry a complete archived harness snapshot and must not be used as independent reproducibility evidence; their transcripts are retained to document development. The final run records the exact delivered `diagnostic.py` hash.

The final unit suite contains 15 test methods, including native runtime error semantics, effect-oracle edge cases, all-scenario passive instrumentation parity, and local HTTP transport. The HTTP test uses a scripted localhost fixture server, not a model. The Qwen and Gemma endpoint checks each returned connection refused in this workspace. No autonomous model research episode was run.
