"""Mixin generate at temp 1.0 scores above chance on the official scorer."""

from text_watermark_tools.generate import _merge_warper_cfg, generate_text
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
