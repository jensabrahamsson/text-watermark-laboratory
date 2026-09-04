"""Lock exploratory holdouts that back the three proven width ideas."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DUMP = ROOT / "experiments" / "2026-09-04-lovande-holdouts"
README = DUMP / "README.md"
INDEX = DUMP / "index.json"
LOG = ROOT / "research" / "LOGBOOK.md"
RESEARCH = ROOT / "research" / "README.md"


def _holdout(*parts: str) -> dict:
    path = DUMP.joinpath(*parts)
    pay = json.loads(path.read_text())
    assert pay["used_keys"] is False
    assert pay["used_hash_iv"] is False
    assert pay["used_g_values"] is False
    return pay


def test_lovande_holdouts_are_json_only_and_key_free() -> None:
    assert README.is_file()
    assert INDEX.is_file()
    text = README.read_text()
    assert "25/48" in text
    assert "used_keys=false" in text
    assert "--skip-hashpool" in text
    assert "thesis/" in text
    assert "leftover-20" in text
    index = json.loads(INDEX.read_text())
    assert index["n_dumps"] >= 140
    assert all(d["used_keys"] is False for d in index["dumps"])
    assert "25/48" in index["note"]
    n_holdouts = 0
    for holdout in DUMP.rglob("holdout.json"):
        n_holdouts += 1
        pay = json.loads(holdout.read_text())
        assert pay["used_keys"] is False, holdout
        assert pay["used_hash_iv"] is False, holdout
        assert pay["used_g_values"] is False, holdout
    assert n_holdouts >= 200
    assert not list(DUMP.rglob("holdout.md"))
    log = LOG.read_text()
    assert "2026-09-04-lovande-holdouts" in log
    assert "cursor/lovande-holdouts-1051" in log
    assert "2026-09-04-lovande-holdouts" in RESEARCH.read_text()


def test_kirchenbauer_last2_hashpool_3264_still_ranks_the_body() -> None:
    gpt2 = _holdout(
        "probe-100x4-kgw-hashpool-k2-mid",
        "window-32-64",
        "hashpool",
        "holdout.json",
    )
    distil = _holdout(
        "probe-distil-100x4-kgw-hashpool-k2-mid",
        "window-32-64",
        "hashpool",
        "holdout.json",
    )
    assert gpt2["context_len"] == 2
    assert gpt2["n_prompts_marked_above"] == 100
    assert gpt2["n_marked_lr_positive"] == 333
    assert abs(gpt2["binary"]["auc"] - 0.898) < 0.001
    assert distil["n_prompts_marked_above"] == 97
    assert distil["n_marked_lr_positive"] == 253
    assert abs(distil["binary"]["auc"] - 0.796) < 0.001


def test_kirchenbauer_last2_hashtok2_3264_sits_with_hashtok() -> None:
    gpt2 = _holdout(
        "probe-100x4-kgw-hashtok2-k2-3264",
        "window-32-64",
        "hashtok2",
        "holdout.json",
    )
    distil = _holdout(
        "probe-distil-100x4-kgw-hashtok2-k2-3264",
        "window-32-64",
        "hashtok2",
        "holdout.json",
    )
    gpt2_tok = _holdout(
        "probe-100x4-kgw-hashtok-k2-mid",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    assert gpt2["n_prompts_marked_above"] == 98
    assert gpt2["n_marked_lr_positive"] == 326
    assert gpt2_tok["n_prompts_marked_above"] == 98
    assert gpt2_tok["n_marked_lr_positive"] == 322
    assert distil["n_prompts_marked_above"] == 98
    assert distil["n_marked_lr_positive"] == 257


def test_aaronson_qwen_last2_hashtok2_3264_recovers_isolated() -> None:
    hashtok2 = _holdout(
        "probe-qwen-100x4-aaronson-hashtok2-k2-3264",
        "window-32-64",
        "hashtok2",
        "holdout.json",
    )
    hashtok = _holdout(
        "probe-qwen-100x4-aaronson-hashtok-k2-mid",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    hits = _holdout(
        "probe-qwen-100x4-aaronson-hits-k2-mid",
        "window-32-64",
        "hits",
        "holdout.json",
    )
    hashpool = _holdout(
        "probe-qwen-100x4-aaronson-hashpool-k2-mid",
        "window-32-64",
        "hashpool",
        "holdout.json",
    )
    assert hashtok2["n_prompts_marked_above"] == 94
    assert hashtok2["n_marked_lr_positive"] == 320
    assert hashtok2["n_prompt_wins_without_isolated_tp"] == 14
    assert abs(hashtok2["binary"]["auc"] - 0.925) < 0.001
    assert hashtok["n_prompts_marked_above"] == 95
    assert hashtok["n_marked_lr_positive"] == 208
    assert hashtok["n_prompt_wins_without_isolated_tp"] == 43
    assert hits["n_marked_lr_positive"] == 356
    assert hashpool["n_prompts_marked_above"] == 99
    assert hashpool["n_marked_lr_positive"] == 240
    assert hashpool["n_prompt_wins_without_isolated_tp"] == 39
    assert hashtok2["n_marked_lr_positive"] < hits["n_marked_lr_positive"]
    assert hashtok2["n_marked_lr_positive"] > hashtok["n_marked_lr_positive"]


def test_aaronson_last2_hashtok2_3264_gpt2_distil_sit_with_hashtok() -> None:
    gpt2 = _holdout(
        "probe-100x4-aaronson-hashtok2-k2-3264",
        "window-32-64",
        "hashtok2",
        "holdout.json",
    )
    distil = _holdout(
        "probe-distil-100x4-aaronson-hashtok2-k2-3264",
        "window-32-64",
        "hashtok2",
        "holdout.json",
    )
    gpt2_tok = _holdout(
        "probe-100x4-aaronson-hashtok-k2-mid",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    distil_tok = _holdout(
        "probe-distil-100x4-aaronson-hashtok-k2-mid",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    assert gpt2["n_prompts_marked_above"] == 96
    assert gpt2["n_marked_lr_positive"] == 332
    assert gpt2_tok["n_prompts_marked_above"] == 96
    assert gpt2_tok["n_marked_lr_positive"] == 320
    assert distil["n_prompts_marked_above"] == 89
    assert distil["n_marked_lr_positive"] == 324
    assert distil_tok["n_prompts_marked_above"] == 90
    assert distil_tok["n_marked_lr_positive"] == 320


def test_public_synthid_last2_hash_3264_is_not_kgw_body() -> None:
    distil_pool = _holdout(
        "probe-distil-100x4-synthid-hashpool-k2-mid",
        "window-32-64",
        "hashpool",
        "holdout.json",
    )
    distil_tok = _holdout(
        "probe-distil-100x4-synthid-hashtok-k2-3264",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    gpt2_tok = _holdout(
        "probe-100x4-synthid-hashtok-k2-mid",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    kgw_tok = _holdout(
        "probe-100x4-kgw-hashtok-k2-mid",
        "window-32-64",
        "hashtok",
        "holdout.json",
    )
    assert distil_pool["n_prompts_marked_above"] == 75
    assert distil_pool["n_marked_lr_positive"] == 74
    assert distil_tok["n_prompts_marked_above"] == 71
    assert distil_tok["n_marked_lr_positive"] == 75
    assert gpt2_tok["n_prompts_marked_above"] == 82
    assert kgw_tok["n_prompts_marked_above"] == 98
    assert distil_pool["n_prompts_marked_above"] < kgw_tok["n_prompts_marked_above"]
