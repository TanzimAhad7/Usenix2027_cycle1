"""Lossless syntax decoding for three explicit tool-call grammars.

JSON: <tool_call>{"name":"f","arguments":{...}}</tool_call>
XML envelopes: <tool_call><name>f</name><arguments>{...}</arguments></tool_call>
and <tool_call><tool_name>f</tool_name><arguments>{...}</arguments></tool_call>

No general XML parser, entity expansion, key inference, argument repair,
tool-name substitution, string-to-object coercion or authorization decision.
"""
import json
import re
import math


def unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError('Duplicate JSON field: ' + name)
        result[name] = value
    return result


def bad_constant(value):
    raise ValueError('Non-JSON numeric constant: ' + value)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_constant=bad_constant)
NAME = re.compile(r'[A-Za-z_][A-Za-z0-9_.-]*\Z')


def finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('Nonfinite decoded numeric value')
    if isinstance(value, dict):
        for item in value.values(): finite(item)
    elif isinstance(value, list):
        for item in value: finite(item)


def space(text, index):
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def expect(text, index, literal):
    index = space(text, index)
    if not text.startswith(literal, index):
        raise ValueError('Expected ' + literal)
    return index + len(literal)


def parse_with_receipt(text):
    calls, formats, content = [], [], []
    position = 0
    while True:
        marker = re.search(r'</?tool_call\b', text[position:])
        if marker is None:
            content.append(text[position:])
            break
        begin = position + marker.start()
        content.append(text[position:begin])
        if not text.startswith('<tool_call>', begin):
            raise ValueError('Orphan or malformed tool_call delimiter')
        cursor = space(text, begin + len('<tool_call>'))
        if cursor < len(text) and text[cursor] == '{':
            value, cursor = DECODER.raw_decode(text, cursor)
            if not isinstance(value, dict) or set(value) != {'name', 'arguments'}:
                raise ValueError('JSON call requires exactly name and arguments')
            format_name = 'JSON_OBJECT_V1'
        elif text.startswith('<name>', cursor) or text.startswith('<tool_name>', cursor):
            tag = 'tool_name' if text.startswith('<tool_name>', cursor) else 'name'
            opening, closing = '<' + tag + '>', '</' + tag + '>'
            start = cursor + len(opening)
            end = text.find(closing, start)
            if end < 0:
                raise ValueError('Unclosed name field')
            name = text[start:end]
            if NAME.fullmatch(name) is None:
                raise ValueError('XML-envelope name must be a literal tool identifier')
            cursor = expect(text, end + len(closing), '<arguments>')
            arguments, cursor = DECODER.raw_decode(text, space(text, cursor))
            cursor = expect(text, cursor, '</arguments>')
            value = {'name': name, 'arguments': arguments}
            format_name = 'TOOL_NAME_ARGUMENTS_JSON_V1' if tag == 'tool_name' else 'NAME_ARGUMENTS_JSON_V1'
        else:
            raise ValueError('Unsupported tool-call body grammar')
        cursor = expect(text, cursor, '</tool_call>')
        if not isinstance(value['name'], str) or not value['name'] or not isinstance(value['arguments'], dict):
            raise ValueError('Call requires a nonempty string name and an arguments object')
        finite(value['arguments'])
        calls.append(value)
        formats.append(format_name)
        position = cursor
    return calls, ''.join(content).strip() or None, formats


def parse(text):
    calls, content, _ = parse_with_receipt(text)
    if not calls:
        return [], text
    return calls, content

