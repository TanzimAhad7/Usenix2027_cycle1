"""Read-only verdict diagnostics. Never fed back to the guard or transport."""
import collections
import json
import re

from .gemma_syntax import DECODER, finite
from .util import read, write


def inspect(raw, finish_reason='stop'):
    result = dict(raw=raw, finish_reason=finish_reason, interpretable=False,
                  envelope='UNSUPPORTED', parsed=None, reported_survive=None,
                  whole_response_json_boolean=False, source_fallback_prediction=None)
    if not isinstance(raw, str):
        return result
    # Mirror the preserved source's initial JSON/boolean eligibility separately
    # from the stricter diagnostic decoder (which also rejects duplicate keys).
    try:
        original = json.loads(raw)
        result['whole_response_json_boolean'] = isinstance(original, dict) and type(original.get('survive')) is bool
    except (ValueError, TypeError):
        pass
    if not result['whole_response_json_boolean']:
        result['source_fallback_prediction'] = 'true' in raw.lower()
    text = raw.strip()
    envelope = 'WHOLE_RESPONSE_JSON'
    if text.startswith('```'):
        match = re.fullmatch(r'```(?:json)?[ \t]*\r?\n(.*?)\r?\n```', text, re.S)
        if not match:
            return result
        text = match.group(1).strip()
        envelope = 'SINGLE_JSON_CODE_FENCE'
    try:
        value, end = DECODER.raw_decode(text)
        if text[end:].strip() or not isinstance(value, dict) or type(value.get('survive')) is not bool:
            return result
        finite(value)
    except (ValueError, TypeError):
        return result
    result.update(envelope=envelope, parsed=value, reported_survive=value['survive'],
                  interpretable=finish_reason == 'stop')
    return result


def record_diagnostic(record):
    response = record.get('response') or {}
    choices = response.get('choices') or []
    if len(choices) != 1:
        return inspect(None, None)
    choice = choices[0]
    return inspect((choice.get('message') or {}).get('content'), choice.get('finish_reason'))


def require_probe(record):
    """Syntax/capability gate only; either semantic verdict is permitted."""
    result = record_diagnostic(record)
    if not result['interpretable']:
        raise RuntimeError('Judge probe is incomplete or lacks one explicit JSON boolean verdict')
    return result


def annotate(result, records):
    # Deliberately never change qualified, source_decisions, allowed, outcomes,
    # messages, responses, prompts, qualification flags or authorization state.
    diagnostics = [dict(record_index=r.get('index'), **record_diagnostic(r))
                   for r in records if r.get('role') == 'judge' and not r.get('source_supported_logprobs_fallback')]
    result['judge_format_diagnostics'] = diagnostics
    result['judge_format_diagnostic_scope'] = 'Read-only; raw source execution and original strict qualification unchanged'
    return result


def audit(out, manifest):
    """Additional readouts; original strict reports and parent flags untouched."""
    diagnostics, pairs, collection = [], [], {}
    for family in manifest['profiles']:
        e1 = {}
        panels = [('E1', manifest['E1']), ('E2', manifest['E2']),
                  ('E3', [i for b in manifest['E3_blocks'] for i in b])]
        for panel, planned in panels:
            acquired, complete, strict = 0, 0, 0
            for item in planned:
                path = out / family / panel / item['id'] / 'result.json'
                if not path.is_file():
                    continue
                r = read(path)
                acquired += 1
                strict += bool(r.get('qualified'))
                path_complete = bool(r.get('source_path_complete')) if panel != 'E3' else bool(r.get('qualified'))
                complete += path_complete
                for d in r.get('judge_format_diagnostics', []):
                    diagnostics.append(dict(profile=family, panel=panel, id=item['id'], **d))
                if panel == 'E1':
                    e1[item['id']] = r
            collection[family + '_' + panel] = dict(planned=len(planned), recorded=acquired,
                source_path_or_workflow_complete=complete, original_qualified=strict,
                qualification_definition='E1/E2 original whole-response-JSON criterion; E3 original workflow criterion. Not pooled.')
        for item in manifest['E1']:
            ident = item['id']
            if item['permission'] != 'FORBID':
                continue
            other = ident.replace('_FORBID_', '_ALLOW_')
            if ident not in e1 or other not in e1:
                continue
            no, yes = e1[ident], e1[other]
            raw_ready = bool(no.get('source_path_complete') and yes.get('source_path_complete'))
            nd, yd = no.get('judge_format_diagnostics', []), yes.get('judge_format_diagnostics', [])
            reported_ready = (raw_ready and len(nd) == len(yd) == 1 and nd[0]['interpretable'] and yd[0]['interpretable'])
            pairs.append(dict(profile=family, forbidden_id=ident, allowed_id=other,
                both_original_qualified=bool(no.get('qualified') and yes.get('qualified')),
                both_source_paths_complete=raw_ready,
                raw_source_permission_response=int(yes['allowed']) - int(no['allowed']) if raw_ready else None,
                both_reported_verdicts_interpretable=reported_ready,
                reported_permission_response_diagnostic=(int(yd[0]['reported_survive']) - int(nd[0]['reported_survive'])) if reported_ready else None))
    report = dict(panels=collection, new_diagnostic_envelopes=dict(collections.Counter(d['envelope'] for d in diagnostics)),
        scope='Supplemental source-behavior and reported-verdict diagnostics; not a requalification of old Qwen, '
              'not a replacement for original strict-qualified contrasts or an executed strict-parser patch. '
              'Complete E1/E2 paths may exercise source substring fallback. Read its predictions separately from explicit verdicts.')
    write(out / 'analysis/FORMAT_AND_COLLECTION_AUDIT.json', report)
    write(out / 'analysis/JUDGE_FORMAT_DIAGNOSTICS.json', diagnostics)
    write(out / 'analysis/RAW_SOURCE_AND_REPORTED_PERMISSION_CONTRASTS.json', pairs)
    return report
