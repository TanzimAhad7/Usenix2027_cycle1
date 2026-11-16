"""Inherited boundary-aware completion tokenization."""
def action_tokenization(tokenizer, text, spans):
    enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    roles, strict = [], []
    for start, stop in enc["offset_mapping"]:
        hits = [name for name, (a, b) in spans.items() if max(a, start) < min(b, stop)]
        role = hits[0] if len(hits) == 1 else "other"
        roles.append(role)
        strict.append(role if role in spans and spans[role][0] <= start < stop <= spans[role][1] else "other")
    if spans and any(role not in roles for role in spans):
        raise ValueError("A scored value has no attributable token")
    if len(roles) != len(enc["input_ids"]) or not roles:
        raise ValueError("Invalid completion offset mapping")
    return {"completion": text, "cids": enc["input_ids"], "roles": roles, "strict_roles": strict,
            "offsets": [list(pair) for pair in enc["offset_mapping"]]}

