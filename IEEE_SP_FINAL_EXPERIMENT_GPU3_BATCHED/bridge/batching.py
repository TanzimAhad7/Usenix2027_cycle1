"""Deterministic cooperative scheduling and bounded model batches."""
from collections import Counter, OrderedDict, defaultdict
from time import monotonic

from bridge.plan import compact
from design import digest
from score import BATCH, padded_logprobs, score_batch_limit

DEFAULT_LANES = 48
MAX_LANES = 48
GENERATION_TOKEN_BUDGET = 49152
REPLAY_CACHE_ENTRIES = 32768
FIXED_SCORE_WINDOW = 512


def bounded_inference(requests, infer, stats):
    """Yield actual batches and retry only CUDA allocation failures."""
    import torch

    try:
        output = infer(requests)
    except torch.cuda.OutOfMemoryError:
        if len(requests) == 1:
            raise
    else:
        yield requests, output
        return
    stats["oom_splits"] += 1
    torch.cuda.empty_cache()
    mid = len(requests) // 2
    yield from bounded_inference(requests[:mid], infer, stats)
    yield from bounded_inference(requests[mid:], infer, stats)


def generation_request(tokenizer, label, chat, purpose, limit, seed=None):
    encoded = tokenizer.apply_chat_template(
        chat, tokenize=True, add_generation_prompt=True, return_dict=True,
        **({"enable_thinking": False} if label == "qwen" else {}))
    pids = encoded["input_ids"]
    if not pids or len(pids) + limit > 8192:
        raise RuntimeError("Generation exceeds frozen 8192-token limit or has an empty prompt")
    return {"id": digest(["generate", pids, limit, purpose, seed]), "kind": purpose, "messages": chat, "pids": pids, "limit": limit, "seed": seed}


class BlockEngine:
    """Cache exact model requests across every policy arm of one condition."""
    def __init__(self, backend, condition):
        self.tokenizer, self.label = backend.tokenizer, backend.label
        self.condition = condition
        self.results = {}
        self.score_prompts = {}
        self.generation_inputs = {}

    def score_actions(self, prefixes, continuations):
        requests = {}
        for prompt in prefixes:
            if prompt not in self.score_prompts:
                self.score_prompts[prompt] = self.tokenizer.encode(prompt, add_special_tokens=True)
        orders = []
        for cids in continuations:
            order = []
            for prompt in prefixes:
                pids = self.score_prompts[prompt]
                if not pids or len(pids) + len(cids) > 8192:
                    raise RuntimeError("Score input exceeds frozen 8192-token limit")
                key = digest(["score", pids, cids])
                order.append(key)
                if key not in self.results:
                    requests[key] = {"id": key, "kind": "score", "pids": pids, "cids": cids,
                                     "prompt": prompt, "condition": self.condition}
            orders.append(order)
        if requests:
            self.results.update((yield tuple(requests.values())))
        return [(order, [self.results[key] for key in order]) for order in orders]

    def generate(self, chat, purpose, seed=None):
        limit = 256 if purpose == "actor" else 384
        rendered = purpose, seed, compact(chat)
        if rendered not in self.generation_inputs:
            self.generation_inputs[rendered] = generation_request(self.tokenizer, self.label, chat, purpose, limit, seed)
        request = self.generation_inputs[rendered]
        key = request["id"]
        if key not in self.results:
            self.results.update((yield (request | {"condition": self.condition},)))
        return self.results[key]


class BatchEngine:
    def __init__(self, model, tokenizer, device, out, label, lanes, score_mode="single"):
        self.model, self.tokenizer, self.device, self.label = model, tokenizer, device, label
        self.lanes = lanes
        self.score_mode = score_mode
        self.score_pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
        self.stats = Counter()
        self.replay = OrderedDict()
        self.stream = (out / "requests.jsonl").open("a", encoding="utf-8")
        self.reuse_stream = (out / "request_reuse.jsonl").open("a", encoding="utf-8")

    def close(self):
        self.stream.close()
        self.reuse_stream.close()

    def generate_group(self, requests):
        import torch

        limit = requests[0]["limit"]
        if any(r["limit"] != limit for r in requests):
            raise ValueError("Generation batch requires matching decode limits")
        width = max(len(r["pids"]) for r in requests)
        pad = self.tokenizer.pad_token_id
        if pad is None:
            pad = self.tokenizer.eos_token_id
        if pad is None:
            raise ValueError("Tokenizer has no pad or EOS token")
        padding = [width - len(r["pids"]) for r in requests]
        ids = torch.tensor([[pad] * n + r["pids"] for n, r in zip(padding, requests, strict=True)],
                           device=self.device)
        mask = torch.tensor([[0] * n + [1] * (width - n) for n in padding], device=self.device)
        # Independent per-request generators keep stochastic decoding paired
        # across arms and independent of lane order. A common seed shares draws.
        generators = [None if r["seed"] is None else
                      torch.Generator(device=self.device).manual_seed(r["seed"]) for r in requests]
        seeded = [(index, generator) for index, generator in enumerate(generators) if generator is not None]
        seeded_rows = torch.tensor([index for index, _ in seeded], dtype=torch.long, device=self.device)

        def paired_draw(_input_ids, logits):
            values, tokens = logits.index_select(0, seeded_rows).float().topk(32, dim=-1)
            probabilities = torch.softmax(values / 0.35, dim=-1)
            choices = torch.stack([torch.multinomial(row, 1, generator=generator)
                                   for row, (_, generator) in zip(probabilities, seeded, strict=True)])
            winners = tokens.gather(1, choices).squeeze(1)
            logits.index_fill_(0, seeded_rows, float("-inf"))
            logits[seeded_rows, winners] = 0.0
            return logits

        with torch.inference_mode():
            output = self.model.generate(input_ids=ids, attention_mask=mask, do_sample=False,
                                         logits_processor=[paired_draw] if seeded else None,
                                         max_new_tokens=limit, use_cache=True, pad_token_id=pad)
        eos = self.model.generation_config.eos_token_id
        stop = set(eos if isinstance(eos, (list, tuple)) else [eos])
        results = []
        for req, suffix in zip(requests, output[:, width:].tolist(), strict=True):
            # A short row is padded after its first EOS while other rows continue.
            end = next((i + 1 for i, token in enumerate(suffix) if token in stop), len(suffix))
            generated = suffix[:end]
            results.append({"id": req["id"], "text": self.tokenizer.decode(generated, skip_special_tokens=True),
                            "limit_reached": end == limit, "generated": generated})
        return results

    def qualify_generation(self):
        requests = [generation_request(self.tokenizer, self.label, [{"role": "user", "content": prompt}],
                                       "technical_probe", 12, seed) for seed in (None, 319031) for prompt in (
            "Return one integer.", "This is a technical probe. Return a short JSON object containing one integer.")]
        serial = [self.generate_group([req])[0] for req in requests]
        batched = self.generate_group(requests) if self.lanes > 1 else serial
        return {"input_lengths": [len(r["pids"]) for r in requests],
                "serial": serial, "batched": batched, "exact_match": serial == batched}

    def resolve(self, requests):
        scores, generations, answers = [], defaultdict(list), {}
        for key, req in requests.items():
            cached = self.replay.get(key)
            if cached is not None:
                value, kind, batch_index = cached
                self.replay.move_to_end(key)
                self.stats[kind + "_cache_hits"] += 1
                answers[key] = value
                self.reuse_stream.write(compact({
                    "id": key, "conditions": req["conditions"], "kind": req["kind"],
                    "source_batch_index": batch_index,
                }) + "\n")
            elif req["kind"] == "score":
                scores.append(req)
            else:
                generations[req["limit"]].append(req)
        self.reuse_stream.flush()

        def evaluate(rows, infer, kind):
            started = monotonic()
            for batch, outputs in bounded_inference(rows, infer, self.stats):
                self.stats[kind + "_batches"] += 1
                self.stats[kind + "_requests"] += len(batch)
                self.stats[kind + "_max_batch"] = max(self.stats[kind + "_max_batch"], len(batch))
                for req, value in zip(batch, outputs, strict=True):
                    if kind == "generation":
                        raw = {"generated": value["generated"], "text": value["text"],
                               "limit_reached": value["limit_reached"]}
                        answers[req["id"]] = {k: v for k, v in value.items() if k != "generated"}
                    else:
                        raw = {"logprobs": value}
                        answers[req["id"]] = value
                    key = req["id"]
                    batch_index = self.stats[kind + "_batches"]
                    row = {**req, **raw, "batch_index": batch_index, "batch_size": len(batch)}
                    self.stream.write(compact(row) + "\n")
                    self.replay[key] = (answers[key], kind, batch_index)
                    if len(self.replay) > REPLAY_CACHE_ENTRIES:
                        self.replay.popitem(last=False)
                self.stream.flush()
            self.stats[kind + "_wall_seconds"] += monotonic() - started

        scores.sort(key=lambda req: len(req["pids"]) + len(req["cids"]), reverse=True)
        offset = 0
        while offset < len(scores):
            width = len(scores[offset]["pids"]) + len(scores[offset]["cids"])
            size, tail = 1, len(scores[offset]["cids"])
            if self.score_mode == "batch":
                for req in scores[offset + 1:offset + BATCH]:
                    next_tail = max(tail, len(req["cids"]))
                    if size + 1 > score_batch_limit(width - next_tail, next_tail):
                        break
                    size += 1
                    tail = next_tail
            infer = lambda rows: padded_logprobs(self.model, rows, self.device, self.score_pad)
            evaluate(scores[offset:offset + size], infer, "score")
            offset += size
        for limit, rows in generations.items():
            rows.sort(key=lambda req: len(req["pids"]), reverse=True)
            offset = 0
            while offset < len(rows):
                padded = len(rows[offset]["pids"]) + limit
                size = min(self.lanes, max(1, GENERATION_TOKEN_BUDGET // padded))
                evaluate(rows[offset:offset+size], self.generate_group, "generation")
                offset += size
        return answers


def schedule(cells, make_job, resolve, lanes):
    """Advance fixed lane slots to their next model request, then batch a round."""
    cells = iter(cells)
    active = {}
    exhausted = False
    while active or not exhausted:
        for lane in range(lanes):
            if lane in active or exhausted:
                continue
            cell = next(cells, None)
            if cell is None:
                exhausted = True
                break
            job = make_job(cell, lane)
            try:
                active[lane] = job, next(job)
            except StopIteration as done:
                yield done.value
        if not active:
            continue
        requests = {}
        for lane in sorted(active):
            for req in active[lane][1]:
                key = req["id"]
                if key not in requests:
                    requests[key] = {k: v for k, v in req.items() if k != "condition"} | {"conditions": []}
                requests[key]["conditions"].append(req["condition"])
        replies = resolve(requests)
        for lane in sorted(active):
            job, pending = active[lane]
            try:
                active[lane] = job, job.send({req["id"]: replies[req["id"]] for req in pending})
            except StopIteration as done:
                del active[lane]
                yield done.value
