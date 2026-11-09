"""CPU rendering of actual official-client wire fixtures, no model weights."""
import argparse
import hashlib
from collections.abc import Mapping
from numbers import Integral
from pathlib import Path
from .common import read, write


def tokenization_artifact(value):
    """Preserve native tokenizer output and expose one validated ID sequence.

    Transformers may return BatchEncoding/dict instead of list[int]. Reading
    mapping keys as token IDs is a container error, not invalid tokenization.
    This normalization changes no tokenizer arguments or model request.
    """
    def plain(item):
        if isinstance(item, Mapping):
            if any(not isinstance(k, str) for k in item):
                raise RuntimeError('Invalid tokenization mapping key')
            return {k: plain(v) for k, v in item.items()}
        if isinstance(item, (list, tuple)):
            return [plain(v) for v in item]
        if hasattr(item, 'tolist'):
            return plain(item.tolist())
        if isinstance(item, bool) or item is None or isinstance(item, (str, float)):
            return item
        if isinstance(item, Integral):
            return int(item)
        raise RuntimeError('Unsupported tokenization value: ' + type(item).__name__)

    data = plain(value)
    if isinstance(data, dict):
        if 'input_ids' not in data:
            raise RuntimeError('Tokenizer output mapping has no input_ids')
        ids = data['input_ids']
    else:
        ids = data
    if isinstance(ids, list) and ids and isinstance(ids[0], list):
        if len(ids) != 1:
            raise RuntimeError('Expected one tokenized conversation, not a batch')
        ids = ids[0]
    if not isinstance(ids, list) or not ids or any(type(v) is not int or v < 0 for v in ids):
        raise RuntimeError('Invalid native token IDs: expected a nonempty integer sequence')
    return dict(token_ids=ids, tokenization=data,
                tokenization_return_type=type(value).__module__ + '.' + type(value).__qualname__)


def render(snapshot, prepared, out):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    template = tok.chat_template
    if not isinstance(template, str):
        raise RuntimeError('An unambiguous native text chat template is required')
    requests = read(prepared)
    records = []
    for i, r in enumerate(requests):
        msgs = r['request']['messages']
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        native = tok.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True)
        artifact = tokenization_artifact(native)
        if any(m['content'].strip() and m['content'].strip() not in text for m in msgs):
            raise RuntimeError('Native template changed/dropped source request content')
        records.append(dict(index=i, role=r['role'], rendered=text, request=r['request'], **artifact))
    write(out / 'rendered_requests.json', records)
    (out / 'native_chat_template.jinja').write_text(template)
    write(out / 'qualification.json', dict(status='PASS', new_model_inference=0,
          requests=len(records), native_template_sha256=hashlib.sha256(template.encode()).hexdigest(),
          scope='Actual released LocalLLM text requests rendered/tokenized by cached tokenizer; live owned server remains a separate qualification',
          tokenization_container_fix='PRESERVE_NATIVE_OUTPUT_VALIDATE_INPUT_IDS'))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--prepared', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    render(a.snapshot, a.prepared, a.out)
