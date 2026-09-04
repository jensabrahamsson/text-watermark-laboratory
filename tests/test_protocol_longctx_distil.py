"""DistilGPT2 ngram_len=13 two-grain freeze, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx-distil.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_longctx_distil_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-d-ctrl" in text
    assert "H-long-d-group" in text
    assert "H-long-d-iso" in text
    assert "H-long-d-occ" in text
    assert "--ngram-len 13" in text
    assert "--model distilgpt2" in text
    assert "20260903" in text
    assert "2026-09-04-pair-distil-12x4-ngram13" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "2290a62682d06624634c1f46a6ad5be0f47f38aa" in text
    assert "detector_mean" in text
    assert "ngram_len=5" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-longctx.md" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-longctx-distil" in log
    assert "--model distilgpt2" in log
    assert "--ngram-len 13" in log
    assert "`bae6d81`" in log


def test_protocol_longctx_distil_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--model",
            "distilgpt2",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260903",
            "--ngram-len",
            "13",
            "--hub-revision",
            "2290a62682d06624634c1f46a6ad5be0f47f38aa",
            "--out-dir",
            "experiments/2026-09-04-pair-distil-12x4-ngram13",
        ]
    )
    assert args.model == "distilgpt2"
    assert args.ngram_len == 13
    assert args.seed == 20260903
    assert args.hub_revision == "2290a62682d06624634c1f46a6ad5be0f47f38aa"


PAIR = ROOT / "experiments" / "2026-09-04-pair-distil-12x4-ngram13"
PROBE = ROOT / "experiments" / "2026-09-04-probe-distil-12x4-ngram13-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-distil-12x4-ngram13"


def test_protocol_longctx_distil_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["ngram_len"] == 13
    assert pair["model_name"] == "distilgpt2"
    assert pair["seed"] == 20260903
    assert pair["hub_revision"] == "2290a62682d06624634c1f46a6ad5be0f47f38aa"
    assert len(pair["rows"]) == 12
    assert all(row["marked"]["mean"] > 0.55 for row in pair["rows"])
    assert all(row["unmarked_gen"]["mean"] <= 0.55 for row in pair["rows"])
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 9
    assert hard["n_prompts_marked_above"] == 6
    assert interp["n_marked_lr_positive"] == 21
    assert interp["n_unmarked_lr_nonpositive"] == 28
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 49
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 175
    assert occ["n_unseen"] == 11994
    ledger = " ".join((ROOT / "research" / "results-ledger.md").read_text().split())
    w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
    assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in ledger
    assert f"**{w0['n_seen']}** vs **{w0['n_unseen']}**" in ledger
    n_unmarked = sum(r["unmarked_gen"]["mean"] > 0.55 for r in pair["rows"])
    pair_readme = (PAIR / "README.md").read_text()
    assert f"Unmarked first-draw is **{n_unmarked}/12**" in pair_readme
    research = (ROOT / "research" / "README.md").read_text()
    row = next(
        ln
        for ln in research.splitlines()
        if "PROTOCOL-next-longctx-distil.md" in ln
        and "distil-100" not in ln
    )
    assert f"**{occ['n_seen']}** vs **{occ['n_unseen']}**" in row
    assert "H-long-d-ctrl **holds**" in text
    assert "H-long-d-group **holds**" in text
    assert "H-long-d-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **9/12**" in collapsed
    lo, hi = clopper_pearson(9, 12)
    assert lo <= 0.5 <= hi
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
