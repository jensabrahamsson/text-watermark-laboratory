"""Longer-context two-grain replication, frozen before generation."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
PAIR = ROOT / "experiments" / "2026-09-03-pair-12x4-ngram13"
PROBE = ROOT / "experiments" / "2026-09-03-probe-12x4-ngram13-hard-last4"
PAIR100 = ROOT / "experiments" / "2026-09-03-pair-100x4-ngram13"
PROBE100 = ROOT / "experiments" / "2026-09-03-probe-100x4-ngram13-hard-last4"
ATOMS13 = ROOT / "experiments" / "2026-09-03-atoms-12x4-ngram13"
ATOMSPUB = ROOT / "experiments" / "2026-09-03-atoms-12x4-public-loo"
ATOMS100 = ROOT / "experiments" / "2026-09-03-atoms-100x4-ngram13"
ATOMS100PUB = ROOT / "experiments" / "2026-09-03-atoms-100x4-public-loo"


def test_protocol_longctx_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-ctrl" in text
    assert "H-long-group" in text
    assert "H-long-hard" in text
    assert "H-long-iso" in text
    assert "H-long-occ" in text
    assert "--ngram-len 13" in text
    assert "ngram_len` | **13**" in text or "`ngram_len` | **13**" in text
    assert "20260903" in text
    assert "2026-08-17-grok-prompts" in text
    assert "2026-09-03-pair-12x4-ngram13" in text
    assert "2026-09-03-probe-12x4-ngram13-hard-last4" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--skip-hashpool" in text
    assert "--n-samples 4" in text
    assert "leave-one-family-out" in text
    assert "confusion matrix" in text
    assert "thesis/" in text
    assert "synthid-text" in text
    assert "Do **not** look at key-free LRs" in text or "Do not look at key-free LRs" in text
    assert PROMPTS.is_dir()
    n_prompts = len(list(PROMPTS.glob("*.txt")))
    assert n_prompts == 12
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "PROTOCOL-next-longctx" in log
    assert "ngram_len=13" in log or "`ngram_len=13`" in log
    assert "`b70986d`" in log


def test_protocol_longctx_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260903",
            "--ngram-len",
            "13",
            "--out-dir",
            "experiments/2026-09-03-pair-12x4-ngram13",
        ]
    )
    assert args.ngram_len == 13
    assert args.n_samples == 4
    assert args.seed == 20260903


def test_protocol_longctx_official_control_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    probe = json.loads((PROBE / "results.json").read_text())
    assert pair["ngram_len"] == 13
    assert pair["seed"] == 20260903
    assert pair["max_new_tokens"] == 128
    assert len(pair["rows"]) == 12
    for row in pair["rows"]:
        assert row["marked"]["mean"] > 0.55
        assert abs(row["unmarked_gen"]["mean"] - 0.5) < 0.08
        assert row["marked"]["n_tokens"] == 128
    assert probe["used_keys"] is False
    assert probe["include_first"] is False
    hard = holdout_from_json(PROBE / "hard" / "holdout.json")
    interp = holdout_from_json(PROBE / "interpolate" / "holdout.json")
    assert hard.used_keys is False
    assert interp.used_keys is False
    assert hard.n_prompts_marked_above == 6
    assert interp.n_prompts_marked_above == 6
    hard_raw = json.loads((PROBE / "hard" / "holdout.json").read_text())
    interp_raw = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    assert hard_raw["n_marked_lr_positive"] == 22
    assert hard_raw["n_unmarked_lr_nonpositive"] == 30
    assert interp_raw["n_marked_lr_positive"] == 20
    assert interp_raw["n_unmarked_lr_nonpositive"] == 31
    assert interp_raw["prompt_sign_p"] > 0.2
    assert hard_raw["prompt_sign_p"] > 0.2
    assert abs(hard_raw["binary"]["auc"] - 0.544) < 0.001
    lo, hi = clopper_pearson(6, 12)
    assert lo <= 0.5 <= hi
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
    assert "H-long-ctrl **holds**" in text
    assert "H-long-group **holds**" in text
    assert "H-long-hard **holds**" in text
    assert "H-long-iso **holds**" in text
    assert "H-long-occ **holds**" in text
    assert "--leave-one-out" in text
    assert "2026-09-03-atoms-12x4-ngram13" in text
    assert "2026-09-03-atoms-12x4-public-loo" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    collapsed = " ".join(text.split())
    assert "Do not sell **6/12**" in collapsed
    assert not (PROBE / "tables-counts").exists()
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`b70986d`" in log


def test_ngram13_official_scores_all_48_marked_files() -> None:
    """Matching ngram_len=13 official_score_text on committed twins."""
    from text_watermark_tools.score import (
        load_tokenizer,
        official_processor,
        official_score_text,
    )

    tok = load_tokenizer("gpt2")
    proc = official_processor(ngram_len=13)
    marked = [p for p in PAIR.glob("*-marked*.txt") if "unmarked" not in p.name]
    unmarked = list(PAIR.glob("*-unmarked-gen*.txt"))
    assert len(marked) == 48
    assert len(unmarked) == 48
    n_hi = 0
    for path in marked:
        if official_score_text(path.read_text(), tokenizer=tok, processor=proc).mean > 0.55:
            n_hi += 1
    n_u_hi = 0
    u_max = -1.0
    for path in unmarked:
        mean = official_score_text(path.read_text(), tokenizer=tok, processor=proc).mean
        u_max = max(u_max, mean)
        if mean > 0.55:
            n_u_hi += 1
    assert n_hi == 48
    assert n_u_hi == 0
    assert u_max < 0.55
    text = PROTOCOL.read_text()
    assert "**48/48**" in text


def test_protocol_longctx_phase_b_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR100 / "results.json").read_text())
    probe = json.loads((PROBE100 / "results.json").read_text())
    assert pair["ngram_len"] == 13
    assert pair["seed"] == 20260903
    assert len(pair["rows"]) == 100
    assert all(row["marked"]["mean"] > 0.55 for row in pair["rows"])
    assert all(row["unmarked_gen"]["mean"] < 0.55 for row in pair["rows"])
    assert probe["used_keys"] is False
    interp = holdout_from_json(PROBE100 / "interpolate" / "holdout.json")
    hard = holdout_from_json(PROBE100 / "hard" / "holdout.json")
    assert interp.n_prompts_marked_above == 76
    assert hard.n_prompts_marked_above == 66
    interp_raw = json.loads((PROBE100 / "interpolate" / "holdout.json").read_text())
    assert interp_raw["n_marked_lr_positive"] == 267
    assert interp_raw["n_unmarked_lr_nonpositive"] == 222
    assert interp_raw["prompt_sign_p"] < 0.001
    assert "prompt_sign_p" in PROTOCOL.read_text()
    lo, hi = clopper_pearson(76, 100)
    assert lo > 0.5
    assert "H-long-B-ctrl **holds**" in text
    assert "H-long-B-group **holds**" in text
    assert "Do **not** sell **76/100**" in text or "Do not sell **76/100**" in " ".join(
        text.split()
    )
    assert "facc538" in text
    exp = (ROOT / "experiments" / "README.md").read_text()
    assert "2026-09-03-probe-100x4-ngram13-hard-last4" in exp
    assert "76/100" in exp
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "Phase B start" in log
    assert not (PROBE100 / "tables-counts").exists()


def test_ngram13_pair_readmes_note_unpinned_hub() -> None:
    for dump in (PAIR, PAIR100):
        readme = (dump / "README.md").read_text()
        assert "Hub revision was not recorded" in readme
        assert "committed strings" in readme
        data = json.loads((dump / "results.json").read_text())
        assert "hub_revision" not in data
        assert data["ngram_len"] == 13


def test_ngram13_phase_b_official_all_400_marked_files() -> None:
    from text_watermark_tools.score import (
        load_tokenizer,
        official_processor,
        official_score_text,
    )

    tok = load_tokenizer("gpt2")
    proc = official_processor(ngram_len=13)
    marked = [p for p in PAIR100.glob("*-marked*.txt") if "unmarked" not in p.name]
    unmarked = list(PAIR100.glob("*-unmarked-gen*.txt"))
    assert len(marked) == 400
    assert len(unmarked) == 400
    n_hi = sum(
        official_score_text(p.read_text(), tokenizer=tok, processor=proc).mean > 0.55
        for p in marked
    )
    n_u = sum(
        official_score_text(p.read_text(), tokenizer=tok, processor=proc).mean > 0.55
        for p in unmarked
    )
    assert n_hi == 400
    assert n_u == 0
    assert "**400/400**" in PROTOCOL.read_text()


def test_protocol_longctx_occupancy_from_dumps() -> None:
    hw = json.loads((ATOMS13 / "atoms.json").read_text())
    pub = json.loads((ATOMSPUB / "atoms.json").read_text())
    hold = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    assert hw["used_keys"] is False
    assert pub["used_keys"] is False
    assert hw["mode"] == "leave-one-family-out"
    assert pub["mode"] == "leave-one-family-out"
    assert hw["n_rows"] == 96
    assert hw["n_seen"] == 160
    assert hw["n_unseen"] == 12026
    assert pub["n_seen"] == 269
    assert pub["n_unseen"] == 11912
    assert hw["n_marked_lr_positive"] == 20
    assert hw["n_seen"] < pub["n_seen"]
    assert all(
        hw["windows"][i]["n_seen"] < pub["windows"][i]["n_seen"] for i in range(5)
    )
    assert [w["n_seen"] for w in hw["windows"]] == [71, 10, 17, 16, 46]
    assert [w["n_seen"] for w in pub["windows"]] == [84, 32, 33, 26, 94]

    def _hold_key(row: dict) -> tuple:
        side = "unmarked" if "unmarked" in row["file"] else "marked"
        return row["stem"], row["sample"], side

    hold_lrs = {_hold_key(r): r["lr"] for r in hold["files"]}
    atom_lrs = {
        (r["stem"], r["sample"], r["side"]): r["lr"] for r in hw["files"]
    }
    assert hold_lrs.keys() == atom_lrs.keys()
    for key, lr in atom_lrs.items():
        assert abs(hold_lrs[key] - lr) < 1e-9
    text = PROTOCOL.read_text()
    assert "H-long-occ **holds**" in text
    assert "**160**" in text
    assert "**269**" in text
    assert "**12026**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **160**" in collapsed
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`df5487d`" in log
    assert not (PROBE / "tables-counts").exists()


def test_protocol_longctx_occupancy_100_from_dumps() -> None:
    hw = json.loads((ATOMS100 / "atoms.json").read_text())
    pub = json.loads((ATOMS100PUB / "atoms.json").read_text())
    hold = json.loads((PROBE100 / "interpolate" / "holdout.json").read_text())
    lock_a = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-probe-100x4-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    assert hw["used_keys"] is False
    assert pub["used_keys"] is False
    assert hw["mode"] == "leave-one-family-out"
    assert hw["n_rows"] == 800
    assert hw["n_seen"] == 5878
    assert hw["n_unseen"] == 95624
    assert pub["n_seen"] == 10158
    assert pub["n_unseen"] == 91353
    assert hw["n_marked_lr_positive"] == 267
    assert pub["n_marked_lr_positive"] == 352
    assert hw["n_seen"] < pub["n_seen"]
    assert all(
        hw["windows"][i]["n_seen"] < pub["windows"][i]["n_seen"] for i in range(5)
    )
    assert [w["n_seen"] for w in hw["windows"]] == [1287, 840, 544, 1099, 2108]
    assert [w["n_seen"] for w in pub["windows"]] == [1633, 2086, 1239, 1899, 3301]

    def _hold_key(row: dict) -> tuple:
        side = "unmarked" if "unmarked" in row["file"] else "marked"
        return row["stem"], row["sample"], side

    hold_lrs = {_hold_key(r): r["lr"] for r in hold["files"]}
    atom_lrs = {
        (r["stem"], r["sample"], r["side"]): r["lr"] for r in hw["files"]
    }
    assert hold_lrs.keys() == atom_lrs.keys()
    for key, lr in atom_lrs.items():
        assert abs(hold_lrs[key] - lr) < 1e-9
    pub_lrs = {
        (r["stem"], r["sample"], r["side"]): r["lr"] for r in pub["files"]
    }
    lock_lrs = {_hold_key(r): r["lr"] for r in lock_a["files"]}
    assert pub_lrs.keys() == lock_lrs.keys()
    for key, lr in pub_lrs.items():
        assert abs(lock_lrs[key] - lr) < 1e-9
    text = PROTOCOL.read_text()
    assert "**5878**" in text
    assert "**10158**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **5878**" in collapsed
    assert not (PROBE100 / "tables-counts").exists()
