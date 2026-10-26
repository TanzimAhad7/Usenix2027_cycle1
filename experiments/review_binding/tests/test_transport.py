import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from autonomous import Client, HTTPPolicy, local_url, wire_messages
from diagnostic import Ledger, contract, call, message
from agentdojo.functions_runtime import EmptyEnv

class TransportTests(unittest.TestCase):
    def test_error_field_is_explicit_in_transport(self):
        row=wire_messages([dict(role='tool',content=[],tool_call_id='x',error='blocked')])[0]
        self.assertEqual(row['content'],'\nERROR: blocked')
    def test_no_remote_endpoint_by_accident(self):
        with self.assertRaises(Exception): local_url('https://example.com/v1')
    def test_local_fixture_transport_and_budget(self):
        # HTTP transport fixture only. No LLM, no autonomous research evidence.
        received=[]
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                data=dict(model='fixture',choices=[dict(finish_reason='tool_calls',message=dict(role='assistant',content=None,tool_calls=[dict(id='model-occurrence',type='function',function=dict(name='pay',arguments='{"recipient":"Alice","amount":10,"key":""}'))]))],usage=dict(prompt_tokens=1,completion_tokens=1))
                body=json.dumps(data).encode();self.send_response(200);self.end_headers();self.wfile.write(body)
            def log_message(self,*args): pass
        server=HTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            store=Ledger(contract());runtime=store.make_runtime()
            client=Client(f'http://127.0.0.1:{server.server_port}/v1','fixture',store,max_requests=1)
            out=HTTPPolicy(client).query('Pay Alice',runtime,EmptyEnv(),[dict(role='user',content='Pay Alice')],{})
            self.assertEqual(out[3][-1]['tool_calls'][0].id,'model-occurrence')
            self.assertEqual(len(received[0]['tools']),2)
            self.assertEqual(len(store.effects),0)
            with self.assertRaises(RuntimeError): client.post({})
        finally:
            server.shutdown();thread.join();server.server_close()

if __name__=='__main__': unittest.main()
