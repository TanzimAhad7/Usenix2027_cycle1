"""S0 V2 sanitizer prompts and message arrangements (no model calls here).

Wordings
  archived   - the Gate 2 sanitizer text, read verbatim from the frozen Gate 2 package
               (IEEE_SP_GATE2_VALUE_SELECTION/data/historical_guard.json: detector.sanitizer_system_prompt +
               "\n\n" + detector.sanitizer_user_template, exactly as bridge/live.py:194-198 joins them).
  published  - CausalArmor Appendix D.1 (arXiv:2602.07918v1, pp. 24-25) as one block, frozen in
               prompts/D1_published_block.txt. Amendment A2 (12 Nov 2026) transcribed it from the PDF's monospace
               box: same words as the archived text, typographic U+2019 quotes, literal ** and * markers, the
               paper's line breaks (first paragraph broken after "examine," and "malicious"; no blank line before
               "The **original user request**") and its double spaces after "sanitizer.", "was:", "tool:",
               "request." and "text.". Published-wording configurations refuse to run until
               prompts/D1_confirmation.json confirms that file's sha256.

Y_t conditioning (ablation)
  The displayed D.1 template has no Y_t slot; Algorithms 1-2 condition on (U, Y_t). The +Y variant inserts, after
  the user-request line, the line used by the causal-armor 0.1.2 package:
      "The agent proposed this action:  **{proposed_action}**"

Message arrangements
  user            - the whole filled block as one user turn (the Gate 2 rendering; continuity only).
  system+closing  - the filled block in the system role, and a user turn containing the block's own final
                    instruction sentence verbatim. Needed because a system-only message is not universally
                    renderable: the Gemma-3 chat template silently DROPS a system-only message (verified on CPU,
                    12 Nov 2026: it renders '<bos><start_of_turn>model\\n'), and the Gemini API needs a user turn.
                    Each model's own template/provider then handles the system role natively (Qwen3: a system turn;
                    Gemma-3: folded into the first user turn by its template; Gemini via OpenRouter: system
                    instruction). The paper does not specify the API message arrangement; this is documented as an
                    unresolved implementation choice, not a reproduction of the complete defense.
"""
import json
import re
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE2 = HERE.parent / "IEEE_SP_GATE2_VALUE_SELECTION"
GUARD = GATE2 / "data" / "historical_guard.json"
PUBLISHED_FILE = HERE / "prompts" / "D1_published_block.txt"
CONFIRMATION_FILE = HERE / "prompts" / "D1_confirmation.json"
Y_LINE = "The agent proposed this action:  **{proposed_action}**\n"
REQUEST_LINE = re.compile(r"^.*was:\s+['’]\{user_request\}['’]\n", re.MULTILINE)


def archived_block():
    d = json.loads(GUARD.read_text())["detector"]
    return d["sanitizer_system_prompt"] + "\n\n" + d["sanitizer_user_template"]


def published_from_archived(block):
    """Superseded by amendment A2 (kept for provenance): quote substitution only, without the paper's layout."""
    return block.replace("'", "’")


def published_block():
    return PUBLISHED_FILE.read_text(encoding="utf-8")


def closing_sentence(block):
    """The block's final instruction sentence, verbatim (used as the user turn of system+closing)."""
    start = block.rindex("Return")
    return block[start:].strip()


def with_y(block):
    """Insert the package's proposed-action line after the user-request line (either quote style or spacing)."""
    hits = list(REQUEST_LINE.finditer(block))
    if len(hits) != 1:
        raise ValueError("User-request line not found exactly once")
    return block[:hits[0].end()] + Y_LINE + block[hits[0].end():]


def fill(block, user_request, tool_name, untrusted_content, proposed_action=None):
    # str.replace, not str.format: the content may contain braces.
    out = block.replace("{user_request}", user_request).replace("{tool_name}", tool_name)
    if proposed_action is not None:
        out = out.replace("{proposed_action}", proposed_action)
    if "{untrusted_content}" not in out:
        raise ValueError("Template lacks {untrusted_content}")
    return out.replace("{untrusted_content}", untrusted_content)


def gate2_fill(block, user_request, tool_name, untrusted_content):
    """Exactly Gate 2's str.format filling (continuity configuration only)."""
    d = json.loads(GUARD.read_text())["detector"]
    return d["sanitizer_system_prompt"] + "\n\n" + d["sanitizer_user_template"].format(
        user_request=user_request, tool_name=tool_name, untrusted_content=untrusted_content)


def messages(wording, arrangement, y, user_request, tool_name, untrusted_content, proposed_action=None):
    if wording == "archived":
        block = archived_block()
    elif wording == "published":
        require_confirmation()
        block = published_block()
    else:
        raise ValueError(wording)
    if y:
        block = with_y(block)
    if wording == "archived" and not y and arrangement == "user":
        filled = gate2_fill(block, user_request, tool_name, untrusted_content)
    else:
        filled = fill(block, user_request, tool_name, untrusted_content, proposed_action if y else None)
    if arrangement == "user":
        return [{"role": "user", "content": filled}]
    if arrangement == "system+closing":
        return [{"role": "system", "content": filled}, {"role": "user", "content": closing_sentence(block)}]
    raise ValueError(arrangement)


def file_sha(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def require_confirmation():
    if not CONFIRMATION_FILE.exists():
        raise SystemExit(f"Published-wording configuration blocked: create {CONFIRMATION_FILE} confirming "
                         f"sha256 {file_sha(PUBLISHED_FILE)} of {PUBLISHED_FILE} (see PROTOCOL.md section 3)")
    c = json.loads(CONFIRMATION_FILE.read_text())
    if not c.get("confirmed") or c.get("sha256") != file_sha(PUBLISHED_FILE):
        raise SystemExit("D1 confirmation does not match the frozen published block")


def write_published_block():
    """One-time generation of the frozen published block (refuses to overwrite)."""
    PUBLISHED_FILE.parent.mkdir(exist_ok=True)
    if PUBLISHED_FILE.exists():
        raise SystemExit(f"{PUBLISHED_FILE} exists (frozen)")
    PUBLISHED_FILE.write_text(published_from_archived(archived_block()), encoding="utf-8")
    return file_sha(PUBLISHED_FILE)


if __name__ == "__main__":
    print(write_published_block())
