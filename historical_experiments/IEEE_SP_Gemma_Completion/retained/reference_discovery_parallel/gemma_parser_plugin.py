"""Non-streaming vLLM adapter; does not require Hermes tokens in Gemma vocabulary.

Uses documented tool-parser plugin API. Logs every original generated text.
Invalid tagged output raises a technical error rather than repairing arguments
or silently converting it into a successful no-tool response.
"""
import importlib,logging,json,sys,uuid
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from reference_discovery_parallel.strict_tags import parse

try:
    from vllm.tool_parsers.abstract_tool_parser import ToolParser,ToolParserManager
except ImportError:
    from vllm.entrypoints.openai.tool_parsers.abstract_tool_parser import ToolParser,ToolParserManager

def protocol_symbol(name):
    for module in ['vllm.entrypoints.generate.base.protocol','vllm.entrypoints.openai.engine.protocol','vllm.entrypoints.openai.protocol']:
        try:return getattr(importlib.import_module(module),name)
        except (ImportError,AttributeError):pass
    raise ImportError('Installed vLLM has no qualified protocol symbol '+name)

ToolCall=protocol_symbol('ToolCall');FunctionCall=protocol_symbol('FunctionCall')
ExtractedToolCallInformation=protocol_symbol('ExtractedToolCallInformation')

@ToolParserManager.register_module(['reference_gemma_strict_tags'])
class ReferenceGemmaParser(ToolParser):
    supports_required_and_named=False
    def adjust_request(self,request):
        if getattr(request,'stream',False):raise ValueError('This experimental profile is non-streaming only')
        return request
    def extract_tool_calls(self,model_output,request):
        logging.getLogger('vllm.reference_gemma_raw').warning('REFERENCE_GEMMA_RAW_OUTPUT %s',json.dumps(model_output,ensure_ascii=False))
        calls,content=parse(model_output)
        return ExtractedToolCallInformation(tools_called=bool(calls),
            tool_calls=[ToolCall(id='call_'+uuid.uuid4().hex[:24],type='function',function=FunctionCall(name=c['name'],arguments=json.dumps(c['arguments'],ensure_ascii=False))) for c in calls],content=content)
    def extract_tool_calls_streaming(self,*args,**kwargs):
        raise ValueError('Streaming is outside this frozen profile')
