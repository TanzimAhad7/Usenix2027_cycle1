"""Tokenizer container regressions; no models, weights or GPU required."""
import importlib.util
import json
import tempfile
import unittest
from collections import UserDict
from pathlib import Path
from unittest.mock import patch
from r3.render import tokenization_artifact, render

class ArrayLike:
    def __init__(self, data): self.data = data
    def tolist(self): return self.data

class Tests(unittest.TestCase):
    def test_flat_list_and_tuple(self):
        for value in ([0, 7, 42], (0, 7, 42)):
            self.assertEqual(tokenization_artifact(value)['token_ids'], [0, 7, 42])
    def test_batch_encoding_style_mapping(self):
        value = UserDict(input_ids=[1, 2], attention_mask=[1, 1])
        result = tokenization_artifact(value)
        self.assertEqual(result['token_ids'], [1, 2])
        self.assertEqual(result['tokenization'], dict(value))
    def test_single_batch_preserves_native_container(self):
        native = {'input_ids': [[1, 2]], 'attention_mask': [[1, 1]]}
        result = tokenization_artifact(native)
        self.assertEqual(result['token_ids'], [1, 2])
        self.assertEqual(result['tokenization'], native)
    def test_tensor_style_output_without_truth_value_test(self):
        result = tokenization_artifact({'input_ids': ArrayLike([[1, 2]])})
        self.assertEqual(result['token_ids'], [1, 2])
    def test_invalid_and_multiple_sequences_rejected(self):
        for value in ([], {}, {'attention_mask': [1]}, [True], [1.0], [-1], ['1'], [[1], [2]], {'input_ids': [1, [2]]}):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                tokenization_artifact(value)
    @unittest.skipUnless(importlib.util.find_spec('transformers'), 'Serving-side integration requires transformers')
    def test_real_fast_tokenizer_render_and_ids(self):
        from tokenizers import Tokenizer, models, pre_tokenizers
        from transformers import PreTrainedTokenizerFast
        backend = Tokenizer(models.WordLevel({'[UNK]': 0, 'user': 1, 'hello': 2, 'assistant': 3, ':': 4}, unk_token='[UNK]'))
        backend.pre_tokenizer = pre_tokenizers.Whitespace()
        tok = PreTrainedTokenizerFast(tokenizer_object=backend, unk_token='[UNK]')
        tok.chat_template = "{% for m in messages %}{{ m['role'] }}: {{ m['content'] }}\n{% endfor %}{% if add_generation_prompt %}assistant: {% endif %}"
        msgs = [{'role': 'user', 'content': 'hello'}]
        native = tok.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True)
        expected = tok.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True, return_dict=False)
        self.assertEqual(tokenization_artifact(native)['token_ids'], expected)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); prepared = root / 'requests.json'; out = root / 'out'; out.mkdir()
            prepared.write_text(json.dumps([{'role': 'actor', 'request': {'messages': msgs}}]))
            with patch('transformers.AutoTokenizer.from_pretrained', return_value=tok): render(root, prepared, out)
            records = json.loads((out / 'rendered_requests.json').read_text())
            self.assertEqual(records[0]['token_ids'], expected)
            self.assertEqual(json.loads((out / 'qualification.json').read_text())['status'], 'PASS')
    @unittest.skipUnless(importlib.util.find_spec('transformers'), 'Serving-side integration requires transformers')
    def test_real_batch_encoding_and_arrays(self):
        import numpy as np
        from transformers import BatchEncoding
        native = BatchEncoding({'input_ids': np.array([[0, 2, 3]]), 'attention_mask': np.ones((1, 3), dtype=int)})
        result = tokenization_artifact(native)
        self.assertEqual(result['token_ids'], [0, 2, 3])
        self.assertEqual(result['tokenization']['attention_mask'], [[1, 1, 1]])

if __name__ == '__main__': unittest.main()
