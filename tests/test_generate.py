"""Mixin generate at temp 1.0 scores above chance on the official scorer."""

from text_watermark_tools.generate import _merge_warper_cfg, generate_text, is_gpt2_name
from text_watermark_tools.score import (
    control_keys,
    load_tokenizer,
    official_score_token_ids,
)

PROMPT = "The harbour lights flickered over wet cobblestones. "


def test_merge_warper_cfg_caller_keys_win() -> None:
    import torch

    dummy = [1, 2, 3]
    cfg = _merge_warper_cfg({"temperature": 1.0, "top_k": 40}, dummy, torch.device("cpu"))
    assert cfg["keys"] == dummy
    assert cfg["temperature"] == 1.0
    assert cfg["device"].type == "cpu"


def test_merge_warper_cfg_ngram_len_overrides_extra_params() -> None:
    import torch

    cfg = _merge_warper_cfg(
        {"ngram_len": 5, "temperature": 1.0, "top_k": 40},
        [1, 2, 3],
        torch.device("cpu"),
        ngram_len=13,
    )
    assert cfg["ngram_len"] == 13
    assert cfg["keys"] == [1, 2, 3]


def test_hf_load_kwargs_omits_unset_revision() -> None:
    from text_watermark_tools.score import hf_load_kwargs

    assert hf_load_kwargs() == {}
    assert hf_load_kwargs(revision=None) == {}
    assert hf_load_kwargs(revision="607a30d783dfa663caf39e06633721c8d4cfcd7e") == {
        "revision": "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    }


def test_load_tokenizer_forwards_hub_revision(monkeypatch) -> None:
    from types import SimpleNamespace

    seen: dict = {}

    def fake_from_pretrained(name, **kwargs):
        seen["name"] = name
        seen["kwargs"] = kwargs
        tok = SimpleNamespace(pad_token=None, eos_token="eos")
        return tok

    monkeypatch.setattr(
        "transformers.AutoTokenizer.from_pretrained", fake_from_pretrained
    )
    from text_watermark_tools.score import load_tokenizer

    tok = load_tokenizer("gpt2", revision="abc123")
    assert seen["name"] == "gpt2"
    assert seen["kwargs"]["revision"] == "abc123"
    assert tok.pad_token == "eos"


def test_cli_pair_accepts_hub_revision() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/prompts",
            "--hub-revision",
            "607a30d783dfa663caf39e06633721c8d4cfcd7e",
        ]
    )
    assert args.hub_revision == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert args.ngram_len == 5


def test_gpt2_family_names_use_the_gpt2_mixin() -> None:
    assert is_gpt2_name(None) is True
    assert is_gpt2_name("gpt2") is True
    assert is_gpt2_name("distilgpt2") is True
    assert is_gpt2_name("gpt2-medium") is True
    assert is_gpt2_name("openai-community/gpt2") is True
    assert is_gpt2_name("Qwen/Qwen2-1.5B-Instruct") is False


def test_mixin_generate_scores_above_chance() -> None:
    gen = generate_text(
        PROMPT,
        marked=True,
        max_new_tokens=64,
        seed=2,
    )
    score = official_score_token_ids(gen.token_ids, tokenizer=load_tokenizer())
    assert gen.marked is True
    assert score.n_tokens == 64
    assert score.n_unmasked_ngrams >= 50
    assert score.mean > 0.5
    assert score.weighted_mean > 0.5


def test_ngram_len_13_generate_scores_with_matching_processor() -> None:
    """Longer mixin history is a different instance; matching ngram_len must light up."""
    tok = load_tokenizer()
    gen = generate_text(
        PROMPT,
        marked=True,
        max_new_tokens=32,
        seed=2,
        ngram_len=13,
    )
    matching = official_score_token_ids(
        gen.token_ids, tokenizer=tok, ngram_len=13
    )
    public = official_score_token_ids(gen.token_ids, tokenizer=tok, ngram_len=5)
    assert gen.token_ids.shape[-1] == 32
    assert matching.n_unmasked_ngrams >= 10
    assert matching.mean > 0.5
    assert matching.mean > public.mean


def test_control_key_generate_is_chance_on_public_high_on_match() -> None:
    """Caller-supplied keys: public detector_mean is chance; matching keys light up."""
    tok = load_tokenizer()
    keys = control_keys()
    gen = generate_text(
        PROMPT,
        marked=True,
        max_new_tokens=80,
        seed=3,
        keys=keys,
    )
    public = official_score_token_ids(gen.token_ids, tokenizer=tok)
    matching = official_score_token_ids(gen.token_ids, tokenizer=tok, keys=keys)
    assert gen.token_ids.shape[-1] == 80
    assert public.n_unmasked_ngrams >= 60
    assert abs(public.mean - 0.5) < 0.08
    assert matching.mean > 0.5
    assert matching.mean > public.mean
