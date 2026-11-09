import importlib.util,json,unittest,hashlib
from pathlib import Path
from reference_discovery_parallel.strict_tags import parse
ROOT=Path(__file__).resolve().parents[1]
JSON='<tool_call>{"name":"qualification_echo","arguments":{"marker":"ARG"}}</tool_call>'
XML='<tool_call><name>qualification_echo</name><arguments>{"marker":"ARG"}</arguments></tool_call>'

class Recovery(unittest.TestCase):
    def test_actual_failure(self):
        text=(ROOT/'recovery_provenance/actual_failed_output.txt').read_text().strip()
        self.assertEqual(parse(text),([dict(name='qualification_echo',arguments=dict(marker='QUALIFICATION_ARGUMENT_4721'))],None))
        spec=importlib.util.spec_from_file_location('old',ROOT/'recovery_provenance/strict_tags_original.py')
        old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        with self.assertRaises(ValueError):old.parse(text)
    def test_json_unchanged(self):self.assertEqual(parse(JSON),parse(XML))
    def test_mixed_calls(self):
        calls,content=parse('before\n'+JSON+'\n'+XML+'\nafter')
        self.assertEqual(len(calls),2);self.assertEqual(content,'before\n\n\nafter')
    def test_no_tools(self):self.assertEqual(parse('Final report.'),([], 'Final report.'))
    def test_values_preserved(self):
        args={'a':[1,None,True,{'unicode':'é','tag':'<name>literal</name>'}],'b':0.25}
        s='<tool_call><name>tool_name</name><arguments>'+json.dumps(args)+'</arguments></tool_call>'
        self.assertEqual(parse(s)[0],[dict(name='tool_name',arguments=args)])
    def test_invalid(self):
        bad=['<tool_call>','</tool_call>','<tool_call>'+XML+'</tool_call>',
             '<tool_call><name>x</name><arguments>{}</arguments><extra/></tool_call>',
             '<tool_call><arguments>{}</arguments><name>x</name></tool_call>',
             '<tool_call><name>x</name><name>y</name><arguments>{}</arguments></tool_call>',
             '<tool_call><name></name><arguments>{}</arguments></tool_call>',
             '<tool_call><name a="b">x</name><arguments>{}</arguments></tool_call>',
             '<tool_call><name>x</name><arguments>[]</arguments></tool_call>',
             '<tool_call><name>x</name><arguments>"{}"</arguments></tool_call>',
             '<tool_call><name>x</name><arguments>{"a":1,"a":2}</arguments></tool_call>',
             '<tool_call><name>x</name><arguments>{"a":NaN}</arguments></tool_call>',
             '<tool_call>{"name":"x","name":"y","arguments":{}}</tool_call>',
             '<tool_call>{"name":"x","arguments":{},"extra":1}</tool_call>',
             '<tool_call>{"name":"x","arguments":{"nested":{"a":1,"a":2}}}</tool_call>',
             '<tool_call>{"name":"x","arguments":{},}</tool_call>']
        for s in bad:
            with self.subTest(s=s),self.assertRaises(ValueError):parse(s)
    def test_schedule_integrity(self):
        from reference_discovery_parallel.integrity import verify_package
        verify_package(ROOT)
    def test_template_unchanged(self):
        old=json.loads((ROOT/'recovery_provenance/ORIGINAL_PACKAGE_MANIFEST.json').read_text())
        name='reference_discovery_parallel/templates/gemma3_tools_adapted.jinja'
        self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),old['files'][name])

if __name__=='__main__':unittest.main()
