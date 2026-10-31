"""vLLM 0.26 nonstreaming adapter; logs original text and exact syntax path."""
import importlib
import json
import logging
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from permission_admission.gemma_syntax import parse_with_receipt

try:
    from vllm.tool_parsers.abstract_tool_parser import ToolParser, ToolParserManager
except ImportError:
    from vllm.entrypoints.openai.tool_parsers.abstract_tool_parser import ToolParser, ToolParserManager


def symbol(name):
    for module in ['vllm.entrypoints.generate.base.protocol', 'vllm.entrypoints.openai.engine.protocol', 'vllm.entrypoints.openai.protocol']:
        try:
            return getattr(importlib.import_module(module), name)
        except (ImportError, AttributeError):
            pass
    raise ImportError('Installed vLLM has no qualified symbol ' + name)


ToolCall = symbol('ToolCall')
FunctionCall = symbol('FunctionCall')
ExtractedToolCallInformation = symbol('ExtractedToolCallInformation')


@ToolParserManager.register_module(['permission_gemma_strict_json_xml_v1'])
class PermissionGemmaParser(ToolParser):
    supports_required_and_named = False

    def adjust_request(self, request):
        if getattr(request, 'stream', False):
            raise ValueError('This declared profile is nonstreaming only')
        return request

    def extract_tool_calls(self, model_output, request):
        logger = logging.getLogger('vllm.permission_gemma_raw')
        logger.warning('PERMISSION_GEMMA_RAW_OUTPUT %s', json.dumps(model_output, ensure_ascii=False))
        calls, content, formats = parse_with_receipt(model_output)
        logger.warning('PERMISSION_GEMMA_SYNTAX %s', json.dumps({'formats': formats, 'calls': calls}, ensure_ascii=False))
        return ExtractedToolCallInformation(tools_called=bool(calls),
            tool_calls=[ToolCall(id='call_' + uuid.uuid4().hex[:24], type='function',
                function=FunctionCall(name=call['name'], arguments=json.dumps(call['arguments'], ensure_ascii=False))) for call in calls],
            content=content if calls else model_output)

    def extract_tool_calls_streaming(self, *args, **kwargs):
        raise ValueError('Streaming is outside this declared profile')

