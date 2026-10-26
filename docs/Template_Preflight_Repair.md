# Template preflight repair

The run `parallel_reference_gpu23_20261026T131613Z_976131_28637`
passed all 57 CPU qualification tests, then stopped before model inference while
writing its first Qwen template artifact. Transformers 5.20.2 returns a
`BatchEncoding` from tokenized `apply_chat_template` by default. Passing that
mapping object directly to `json.dumps` raised the reported `TypeError`.

The preflight now converts actual tokenizer outputs to JSON data explicitly.
It preserves the complete tokenization mapping, including masks, exposes the
single fixture's integer token IDs, and records the return type. Legacy list
returns and single-item batches are supported. Missing, malformed and multiple
conversation token results fail instead of being silently stringified.

Testing further fixtures against the exact Qwen tokenizer revision exposed a
second preflight error: direct Hugging Face rendering skipped the server's
OpenAI-content preprocessing. Qwen's unchanged template expects strings, while
wire messages can contain text-block arrays. The check now calls the installed
vLLM content-format resolver and message parser before rendering. It saves both
the original wire fixture and the resulting template conversation. Text-only
fixtures use a minimal configuration for that preprocessing path; no model
weights or media inputs are loaded. This configuration is not claimed to be
the complete live server ModelConfig. Required owned-server probes still test
actual request processing before scientific workflows.

The native template, model checkpoint, sampling parameters, scientific requests,
688 autonomous conditions and up to 60 conditional slots are unchanged. The
earlier live Inbox checkpoint restoration repair remains included.

Verification performed for this repair:

- Reproduced the exact BatchEncoding serialization failure using real
  Transformers 5.20.2, then verified successful JSON serialization with masks.
- Executed all four Qwen rendering/tokenization fixtures using the tokenizer
  from the pinned revision `9216db5781bf21249d130ec9da846c4624c16137`.
  These tests ran published vLLM 0.26.0 text parsing/content-format functions,
  with the unused media tracker replaced by a text-only stub. This is a
  targeted source-function test, not full installed-vLLM integration.
- Passed 25 host-independent operational tests, including serialization,
  malformed-token rejection and unmodified original-wire fixtures.
- Rechecked unchanged frozen scientific manifests, retained vendor hashes,
  syntax, package hashes and ZIP integrity.

Machine-readable scope, source hashes and fixture artifacts are in `validation/`.
The earlier native CPU qualification report remains: 56 passed, one build-host
PID-namespace skip; the user's subsequent run passed all 57. No GPU model run
was performed here. Full installed-vLLM preprocessing, Gemma parser integration
and GPU serving remain qualified on the user's machine before collection.

Template preflight failure output is now copied into the main run log as well
as its per-profile `process.log`, so any next error is visible directly.
