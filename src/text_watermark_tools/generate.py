"""Sample text from GPT-2 with the SynthID mixin (known-marked generator)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import torch
import transformers
from synthid_text import logits_processing
from synthid_text import synthid_mixin

from text_watermark_tools.score import (
    MODEL_NAME,
    TEMPERATURE,
    TOP_K,
    hf_load_kwargs,
    load_tokenizer,
)

# Small enough for 32 GB unified memory. Not DIPPER. Not a 7B.
QWEN_MODEL = "Qwen/Qwen2-1.5B-Instruct"


def is_gpt2_name(model_name: Optional[str]) -> bool:
    if model_name in (None, "", MODEL_NAME, "gpt2"):
        return True
    name = (model_name or "").lower().rsplit("/", 1)[-1]
    return name == "distilgpt2" or name.startswith("gpt2")


def generate_device() -> torch.device:
    # SynthIDLogitsProcessor hashes keys via numpy at init — that path
    # cannot see an MPS tensor. Keep the warper and the model on CPU.
    return torch.device("cpu")


def _merge_warper_cfg(
    extra_params, watermark_keys, device, ngram_len: Optional[int] = None
) -> dict:
    cfg = dict(synthid_mixin.DEFAULT_WATERMARKING_CONFIG)
    cfg.update(dict(extra_params))
    if watermark_keys is not None:
        cfg["keys"] = list(watermark_keys)
    if ngram_len is not None:
        cfg["ngram_len"] = int(ngram_len)
    cfg["device"] = device
    return cfg


class CompatSynthIDSample:
    """Keep DeepMind's _sample working on transformers after 4.43.

    Newer generate() drops a None `streamer` and no longer passes
    `logits_warper`. `_get_initial_cache_position` grew extra arguments.
    We do not edit the synthid-text checkout.
    """

    def _get_initial_cache_position(self, *args, **kwargs):
        parent = getattr(
            transformers.GenerationMixin, "_get_initial_cache_position", None
        )
        if parent is None:
            # transformers 5: generate() already filled cache_position.
            if len(args) == 2:
                return args[1]
            return kwargs.get("model_kwargs", args[-1] if args else {})
        if len(args) == 2 and not kwargs:
            input_ids, model_kwargs = args
            return parent(self, input_ids.shape[1], input_ids.device, model_kwargs)
        return parent(self, *args, **kwargs)

    def _sample(
        self,
        input_ids,
        logits_processor,
        stopping_criteria,
        generation_config,
        synced_gpus=False,
        streamer=None,
        logits_warper=None,
        **model_kwargs,
    ):
        if logits_warper is None:
            logits_warper = self._get_logits_warper(generation_config)
        return synthid_mixin.SynthIDSparseTopKMixin._sample(
            self,
            input_ids,
            logits_processor,
            stopping_criteria,
            generation_config,
            synced_gpus,
            streamer,
            logits_warper=logits_warper,
            **model_kwargs,
        )


class KeyedSynthIDGPT2(CompatSynthIDSample, synthid_mixin.SynthIDGPT2LMHeadModel):
    """Same mixin generate path; caller may replace the default public keys.

    DeepMind's warper list always starts from DEFAULT_WATERMARKING_CONFIG.
    Passing `keys` here only overrides that field. The synthid-text tree is
    not edited.
    """

    def __init__(self, *args, watermark_keys: Optional[Sequence[int]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.watermark_keys = (
            list(watermark_keys) if watermark_keys is not None else None
        )
        self.watermark_ngram_len: Optional[int] = None

    def _construct_warper_list(self, extra_params):
        device = next(self.parameters()).device
        cfg = _merge_warper_cfg(
            extra_params,
            self.watermark_keys,
            device,
            ngram_len=self.watermark_ngram_len,
        )
        warpers = transformers.LogitsProcessorList()
        warpers.append(logits_processing.SynthIDLogitsProcessor(**cfg))
        return warpers


class KeyedSynthIDQwen2(
    CompatSynthIDSample,
    synthid_mixin.SynthIDSparseTopKMixin,
    transformers.Qwen2ForCausalLM,
):
    """Public mixin tournament on Qwen2. Same keys as GPT-2. Our class, not a fork."""

    def __init__(self, *args, watermark_keys: Optional[Sequence[int]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.watermark_keys = (
            list(watermark_keys) if watermark_keys is not None else None
        )
        self.watermark_ngram_len: Optional[int] = None

    def _construct_warper_list(self, extra_params):
        device = next(self.parameters()).device
        cfg = _merge_warper_cfg(
            extra_params,
            self.watermark_keys,
            device,
            ngram_len=self.watermark_ngram_len,
        )
        warpers = transformers.LogitsProcessorList()
        warpers.append(logits_processing.SynthIDLogitsProcessor(**cfg))
        return warpers

DEFAULT_PROMPT = (
    "Write a wandering travel essay about arriving in a coastal town at dusk, "
    "the smell of salt and fried food, a broken neon hotel sign, and the "
    "feeling that you might stay longer than you planned. Use everyday words.\n\n"
)


@dataclass
class Generation:
    text: str
    token_ids: torch.Tensor  # shape [1, seq] generated tokens only
    prompt_ids: torch.Tensor
    marked: bool


def _load_marked_model(
    device: torch.device,
    *,
    keys: Optional[Sequence[int]] = None,
    model_name: Optional[str] = None,
    ngram_len: Optional[int] = None,
    revision: Optional[str] = None,
):
    name = model_name or MODEL_NAME
    kw = hf_load_kwargs(revision=revision)
    if is_gpt2_name(name):
        model = KeyedSynthIDGPT2.from_pretrained(name, **kw)
        model.watermark_keys = list(keys) if keys is not None else None
    else:
        model = KeyedSynthIDQwen2.from_pretrained(name, **kw)
        model.watermark_keys = list(keys) if keys is not None else None
    model.watermark_ngram_len = int(ngram_len) if ngram_len is not None else None
    return model.to(device).eval()


def _load_unmarked_model(
    device: torch.device,
    *,
    model_name: Optional[str] = None,
    revision: Optional[str] = None,
):
    name = model_name or MODEL_NAME
    kw = hf_load_kwargs(revision=revision)
    if is_gpt2_name(name):
        model = transformers.GPT2LMHeadModel.from_pretrained(name, **kw)
    else:
        model = transformers.AutoModelForCausalLM.from_pretrained(name, **kw)
    return model.to(device).eval()


def generate_text(
    prompt: str = DEFAULT_PROMPT,
    *,
    marked: bool = True,
    max_new_tokens: int = 320,
    temperature: float = TEMPERATURE,
    top_k: int = TOP_K,
    seed: Optional[int] = None,
    device: Optional[torch.device] = None,
    tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
    model: Optional[torch.nn.Module] = None,
    keys: Optional[Sequence[int]] = None,
    model_name: Optional[str] = None,
    ngram_len: Optional[int] = None,
    revision: Optional[str] = None,
) -> Generation:
    """Generate with mixin (marked=True) or the same model unmarked.

    `keys` is only used when `marked` is True and no `model` is passed.
    None keeps DeepMind's public 30-key default.
    `ngram_len` overrides the public mixin hash window (default 5).
    Score must use the same `ngram_len`. The synthid-text tree is not edited.
    `model_name` defaults to GPT-2. Pass a Qwen2 id to use that checkpoint
    with the same tournament; score must use the same tokenizer.
    `revision` is an optional Hugging Face Hub SHA or branch. Unset keeps
    the unpinned default. Historical twins are committed files.
    """
    name = model_name or MODEL_NAME
    if device is None:
        dev = generate_device() if not is_gpt2_name(name) else torch.device("cpu")
    else:
        dev = device
    tok = tokenizer or load_tokenizer(name, revision=revision)
    if seed is not None:
        torch.manual_seed(seed)
    if model is None:
        model = (
            _load_marked_model(
                dev,
                keys=keys,
                model_name=name,
                ngram_len=ngram_len,
                revision=revision,
            )
            if marked
            else _load_unmarked_model(dev, model_name=name, revision=revision)
        )
    elif marked and ngram_len is not None and hasattr(model, "watermark_ngram_len"):
        model.watermark_ngram_len = int(ngram_len)
    inputs = tok(prompt, return_tensors="pt").to(dev)
    gen_kwargs = dict(
        do_sample=True,
        min_new_tokens=max_new_tokens,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        pad_token_id=tok.eos_token_id,
    )
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
    gen_ids = outputs[:, inputs["input_ids"].shape[1] :]
    text = tok.decode(gen_ids[0], skip_special_tokens=True)
    return Generation(
        text=text,
        token_ids=gen_ids.detach().cpu(),
        prompt_ids=inputs["input_ids"].detach().cpu(),
        marked=marked,
    )


def next_token_logits(
    prefix_ids: torch.Tensor,
    *,
    model: torch.nn.Module,
) -> torch.Tensor:
    """One forward pass; last-position logits. No keys/g-values."""
    if prefix_ids.dim() == 1:
        prefix_ids = prefix_ids.unsqueeze(0)
    device = next(model.parameters()).device
    prefix_ids = prefix_ids.to(device)
    with torch.no_grad():
        out = model(input_ids=prefix_ids)
    return out.logits[0, -1]


def sample_from_logits(
    logits: torch.Tensor,
    *,
    n_samples: int,
    temperature: float = TEMPERATURE,
    top_k: int = TOP_K,
) -> list[int]:
    """Sample next tokens from already-computed logits."""
    scaled = logits / max(temperature, 1e-6)
    if top_k is not None and top_k > 0:
        k = min(top_k, scaled.shape[-1])
        values, indices = torch.topk(scaled, k)
        dist = torch.softmax(values, dim=-1)
        picks = torch.multinomial(dist, num_samples=n_samples, replacement=True)
        return [int(indices[i].item()) for i in picks]
    dist = torch.softmax(scaled, dim=-1)
    picks = torch.multinomial(dist, num_samples=n_samples, replacement=True)
    return [int(i.item()) for i in picks]


def top_alternative_from_logits(
    logits: torch.Tensor, avoid: int, *, top_k: int = TOP_K
) -> int | None:
    """Highest-logit token that is not `avoid`. Key-free unmarked substitute."""
    k = min(max(top_k, 2), logits.shape[-1])
    _values, indices = torch.topk(logits, k)
    for idx in indices:
        tok = int(idx.item())
        if tok != avoid:
            return tok
    return None


def next_token_samples(
    prefix_ids: torch.Tensor,
    *,
    model: torch.nn.Module,
    n_samples: int,
    temperature: float = TEMPERATURE,
    top_k: int = TOP_K,
    pad_token_id: int,
) -> list[int]:
    """Sample n next tokens from a model given a prefix. No keys/g-values."""
    del pad_token_id  # logits path does not need it
    logits = next_token_logits(prefix_ids, model=model)
    return sample_from_logits(
        logits, n_samples=n_samples, temperature=temperature, top_k=top_k
    )
