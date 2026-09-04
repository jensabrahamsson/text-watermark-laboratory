"""Lock the technical-report claims that Sol's 260903 review required."""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAPER = re.sub(r"\s+", " ", (ROOT / "paper" / "main.tex").read_text())
README = (ROOT / "paper" / "README.md").read_text()
BIB = (ROOT / "paper" / "references.bib").read_text()


def test_title_exposes_paired_reference_oracle() -> None:
    assert "Paired-Reference, Key-Free Indication" in PAPER
    assert "Public SynthID-Text Instance" in PAPER


def test_plain_english_ingress_precedes_the_abstract() -> None:
    lead = PAPER.split(r"\maketitle")[1].split(r"\begin{abstract}")[0]
    assert "In plain English" in lead
    assert "secret key" in lead
    assert "prompt groups" in lead
    assert "no keys" in lead
    assert "abstract below" in lead
    assert "76/100" not in lead
    assert "160" not in lead


def test_how_synthid_works_records_docstring_mismatch() -> None:
    text = (ROOT / "research" / "how-synthid-works.md").read_text()
    assert "lowest three bits" in text
    assert "(hash >> 30) % 2" in text
    assert "Do not edit" in text or "do not edit" in text.lower()


def test_installed_get_gvals_docstring_does_not_match_return() -> None:
    import inspect

    from synthid_text.logits_processing import SynthIDLogitsProcessor

    src = inspect.getsource(SynthIDLogitsProcessor.get_gvals)
    assert "lowest three bits" in src
    assert "num_apply_hash: int = 12" in src
    assert "(ngram_keys >> 30) % 2" in src
    assert "return (ngram_keys >> 30) % 2" in " ".join(src.split())
    intro = Path(ROOT / "paper" / "main.tex").read_text()
    intro = intro.split(r"\section{Introduction}")[1].split(r"\section{Related Work}")[0]
    assert "12 linear-congruential mixes" in intro or "12 LCG mixes" in intro


def test_intro_surfaces_get_gvals_docstring_mismatch() -> None:
    intro = PAPER.split(r"\section{Introduction}")[1].split(
        r"\section{Related Work}"
    )[0]
    assert "lowest three bits" in intro
    assert r"\gg 30" in intro or ">> 30" in intro
    assert "documentation bug" in intro
    assert "not a laboratory rewrite" in intro
    assert "12 linear-congruential mixes" in intro
    prelim = PAPER.split(r"\section{Preliminaries and Threat Model}")[1].split(
        r"\section{Method}"
    )[0]
    assert r"\gg 30" in prelim
    related = PAPER.split(r"\section{Related Work}")[1].split(
        r"\section{Preliminaries and Threat Model}"
    )[0]
    assert r"get\_gvals" in related


def test_hub_revisions_do_not_affect_committed_file_scores() -> None:
    assert "committed strings" in PAPER
    assert "does not affect the published scores" in PAPER
    limits = PAPER.split(r"\section{Limitations}")[1].split(
        r"\section{A Locked Next Experiment}"
    )[0]
    assert "committed strings" in limits
    assert "607a30d783dfa663caf39e06633721c8d4cfcd7e" in PAPER
    assert "bitwise re-generation" in PAPER
    assert "--hub-revision" in Path(ROOT / "paper" / "main.tex").read_text()
    howto = (ROOT / "HOW-TO.md").read_text()
    assert "--hub-revision" in howto
    assert "607a30d783dfa663caf39e06633721c8d4cfcd7e" in howto
    assert "--mixin kgw" in howto
    assert "PROTOCOL-next-kgw" in howto
    cache = Path.home() / ".cache/huggingface/hub/models--gpt2/refs/main"
    if cache.exists():
        assert cache.read_text().strip() == "607a30d783dfa663caf39e06633721c8d4cfcd7e"


def test_how_to_read_names_two_grain_hw12_and_occupancy() -> None:
    how = PAPER.split("How to read this report")[1].split(r"\section{Introduction}")[0]
    assert "fig:twograin" in how
    assert "fig:hw12" in how
    assert "tab:occ" in how
    assert r"get\_gvals" in how
    assert r"\textbf{36/36}" in how
    assert r"\textbf{47/96}" in how


def test_abstract_leads_with_group_then_full_isolated_matrix() -> None:
    assert r"\textbf{36/36}" in PAPER
    assert r"\textbf{99/100}" in PAPER
    assert r"\textbf{9/12}" in PAPER
    assert "25 true positives" in PAPER
    assert "22 true negatives" in PAPER
    assert r"\textbf{47/96}" in PAPER
    assert "48.96" in PAPER
    assert "0.590" in PAPER
    assert "leave-one-family-out" in PAPER


def test_margin_is_demoted_and_not_a_half_null() -> None:
    assert "does not establish above-chance performance under the margin" in PAPER
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "0.02" not in abs_
    assert "10/12" not in abs_
    assert "088" not in abs_
    assert "leftover" not in abs_


def test_claude_resample_20260903_is_dump_backed_and_not_in_abstract() -> None:
    import json

    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "35/40" not in abs_
    assert "37/40" not in abs_
    catalog = PAPER.split(r"\section{Additional transfer catalog}")[1]
    assert r"\textbf{35/40}" in catalog
    assert r"\textbf{37/40}" in catalog
    assert r"\textbf{29/40}" in catalog
    assert r"\textbf{33/40}" in catalog
    assert "style-shift order" in catalog
    assert "claude-sample-2026-08-21" in catalog
    assert "not an Anthropic detector" in catalog
    assert r"\textbf{25/48}" in catalog
    limits = PAPER.split(r"\section{Limitations}")[1].split(
        r"\section{A Locked Next Experiment}"
    )[0]
    assert r"\textbf{35/40}" in limits
    report = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-resample-work"
            / "report.json"
        ).read_text()
    )
    assert report["n_collected"] == 40
    by = {c["name"]: c for c in report["contrasts"]}
    assert by["premark-vs-new"]["last4_wins"] == 35
    assert by["premark-vs-new"]["last1_wins"] == 37
    assert by["previous-vs-new"]["last4_wins"] == 29
    assert by["premark-vs-new"]["used_keys"] is False
    k4 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-resample-work"
            / "blind-premark-vs-new-k4"
            / "results.json"
        ).read_text()
    )
    assert k4["used_keys"] is False
    assert k4["n_marked_wins"] == 35
    assert k4["n_marked_lr_positive"] == 32
    assert k4["n_prompt_wins_without_isolated_tp"] == 3


def test_claude_resample_20260904_is_dump_backed_and_not_in_abstract() -> None:
    import json

    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "19/40" not in abs_
    assert "20/40" not in abs_
    assert "36/40" not in abs_
    assert "37/40" not in abs_
    catalog = PAPER.split(r"\section{Additional transfer catalog}")[1]
    assert "claude-sample-2026-09-04" in catalog
    assert r"\textbf{36/40}" in catalog
    assert r"\textbf{19/40}" in catalog
    assert r"\textbf{20/40}" in catalog
    assert "watermark-window order" in catalog
    limits = PAPER.split(r"\section{Limitations}")[1].split(
        r"\section{A Locked Next Experiment}"
    )[0]
    assert "2026-09-04" in limits
    assert r"\textbf{37/40}" in limits
    assert r"\textbf{19/40}" in limits
    report = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-resample-work"
            / "report.json"
        ).read_text()
    )
    assert report["n_collected"] == 40
    by = {c["name"]: c for c in report["contrasts"]}
    assert by["premark-vs-new"]["last4_wins"] == 37
    assert by["premark-vs-new"]["last1_wins"] == 36
    assert by["previous-vs-new"]["last4_wins"] == 19
    assert by["previous-vs-new"]["last1_wins"] == 20
    assert by["premark-vs-new"]["used_keys"] is False
    k4 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-resample-work"
            / "blind-premark-vs-new-k4"
            / "results.json"
        ).read_text()
    )
    assert k4["used_keys"] is False
    assert k4["n_marked_wins"] == 37
    assert k4["n_marked_lr_positive"] == 32
    assert k4["n_prompt_wins_without_isolated_tp"] == 5
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "experiments/claude-sample-2026-09-04" in log
    assert "**40** long texts" in log
    assert "37/40" in log


def test_isolated_primary_is_confusion_matrix_not_sensitivity_alone() -> None:
    assert "TP 25, FN 23, TN 22, FP 26" in PAPER
    assert "Balanced accuracy" in PAPER
    assert "does not test whether threshold zero is calibrated" in PAPER
    assert "25/51" in PAPER
    assert "0.703" in PAPER
    assert "Declared operating criteria" in PAPER


def test_lock_a_is_loo_not_frozen_fitted_detector() -> None:
    assert "not a frozen fitted detector" in PAPER
    assert "leave-one-family-out on the 100 new families" in PAPER
    assert "native" in PAPER.lower()


def test_witten_bell_and_rankpath_are_specified() -> None:
    assert "Witten--Bell" in PAPER
    assert "ranks 11--40" in PAPER
    assert "ranks 2--3" in PAPER
    assert r"\tau=0" in PAPER
    assert r"\Hw" in PAPER or "H_{\\mathrm{w}}" in PAPER
    math = PAPER.split(r"\section{Why a Fixed Key Can Leave a Trace}")[1].split(
        r"\section{Results}"
    )[0]
    assert "has not been generated" not in math
    assert "is untested" not in math
    assert "PROTOCOL-next-aaronson" in PAPER
    assert "747f3cd" in PAPER
    assert "PROTOCOL-next-kgw" in PAPER
    assert "PROTOCOL-next-kgw-distil" in PAPER
    assert "PROTOCOL-next-kgw-qwen" in PAPER
    assert "PROTOCOL-next-kgw-qwen-100" in PAPER
    assert "PROTOCOL-next-kgw-qwen-100-windows" in PAPER
    assert "e270546" in PAPER
    assert "PROTOCOL-next-longctx-distil" in PAPER
    assert "bae6d81" in PAPER
    assert "PROTOCOL-next-longctx-distil-100" in PAPER
    assert "d891622" in PAPER
    assert "PROTOCOL-next-longctx-qwen" in PAPER
    assert "d7303a2" in PAPER
    assert "PROTOCOL-next-aaronson-distil" in PAPER
    assert "9bdf12a" in PAPER
    assert "PROTOCOL-next-aaronson-distil-100" in PAPER
    assert "bf05759" in PAPER
    assert "PROTOCOL-next-aaronson-qwen" in PAPER
    assert "1171d5c" in PAPER
    assert "PROTOCOL-next-aaronson-qwen-100" in PAPER
    assert "a761a7d" in PAPER
    assert "PROTOCOL-next-longctx-qwen-100" in PAPER
    assert "636765c" in PAPER
    assert "PROTOCOL-next-longctx-windows" in PAPER
    assert "8283d1f" in PAPER
    assert "--mixin kgw" in PAPER
    assert "20260904" in PAPER
    assert "8371406" in PAPER
    assert "8f09aa6" in PAPER
    assert "1582a09" in PAPER
    assert "text-watermark-laboratory/tree/1582a09" in PAPER
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "kgw" not in abs_
    assert "Kirchenbauer" not in abs_
    assert "85/96" not in abs_
    next_sec = PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]
    assert r"\textbf{12/12}" in next_sec
    assert "85/96" in next_sec
    assert "114 seen" in next_sec or "114 seen versus" in next_sec
    assert "747/800" in next_sec
    assert "4557" in next_sec
    assert r"\textbf{100/100}" in next_sec
    assert "distilgpt2" in next_sec
    assert "130 seen" in next_sec or "130 seen versus" in next_sec
    assert r"\textbf{11/12}" in next_sec
    assert "68/96" in next_sec
    assert r"\textbf{8/12}" in next_sec
    assert "pair-distil-100x4-kgw" in next_sec
    assert "4fad227" in next_sec
    assert "683/800" in next_sec
    assert r"\textbf{82/100}" in next_sec
    assert "16170" in next_sec
    assert "20260905" in next_sec
    assert "56/96" in next_sec
    assert "573" in next_sec
    assert "608/800" in next_sec
    assert "25167" in next_sec
    assert "pair-distil-12x4-ngram13" in next_sec
    assert "49/96" in next_sec
    assert "bae6d81" in next_sec
    assert "PROTOCOL-next-longctx-distil-100" in next_sec
    assert "d891622" in next_sec
    assert "557/800" in next_sec
    assert "pair-distil-100x4-ngram13" in next_sec
    assert "b46a5d5debed1485" in PAPER
    assert "22d8c29006252a26" in PAPER
    assert "331dbab436097872" in PAPER
    assert "PROTOCOL-next-longctx-qwen" in next_sec
    assert "d7303a2" in next_sec
    assert "41/96" in next_sec
    assert "pair-qwen-12x4-ngram13" in next_sec
    assert "PROTOCOL-next-aaronson-distil" in next_sec
    assert "9bdf12a" in next_sec
    assert "48/96" in next_sec
    assert "pair-distil-12x4-aaronson" in next_sec
    assert "PROTOCOL-next-aaronson-distil-100" in next_sec
    assert "bf05759" in next_sec
    assert "601/800" in next_sec
    assert "pair-distil-100x4-aaronson" in next_sec
    assert "a043578f9795a7be" in PAPER
    assert "89d3b8c7f8d5d0e0" in PAPER
    assert "06b4d85a772626d4" in PAPER
    assert "PROTOCOL-next-aaronson-qwen" in next_sec
    assert "1171d5c" in next_sec
    assert "60/96" in next_sec
    assert "pair-qwen-12x4-aaronson" in next_sec
    assert "PROTOCOL-next-aaronson-qwen-100" in next_sec
    assert "a761a7d" in next_sec
    assert "616/800" in next_sec
    assert "pair-qwen-100x4-aaronson" in next_sec
    assert "PROTOCOL-next-longctx-qwen-100" in next_sec
    assert "636765c" in next_sec
    assert "pair-qwen-100x4-ngram13" in next_sec
    assert "474/800" in next_sec
    assert "has not been generated" not in next_sec
    assert "PROTOCOL-next-kgw-qwen-100" in next_sec
    assert "ed9fb20" in next_sec
    assert "pair-qwen-100x4-kgw" in next_sec
    assert "before generation" in next_sec
    assert r"\textbf{96/100}" in next_sec
    assert "620/800" in next_sec
    assert r"\textbf{63/100}" in next_sec
    assert "4858" in next_sec
    assert "96740" in next_sec
    assert "PROTOCOL-next-kgw-qwen-100-windows" in next_sec
    assert "e270546" in next_sec
    assert "before those LRs" in next_sec
    assert "PROTOCOL-isolated-rankpath-lm" in next_sec
    assert "d8e6f7f" in next_sec
    assert "PROTOCOL-isolated-rankpath-m12" in next_sec
    assert "32/48" in next_sec
    assert "31/48" in next_sec
    assert "H-rplm-d **holds**" not in next_sec
    assert "tab:kgwq100" in next_sec
    assert "15485863" in next_sec
    assert "ba1cf1846d7df0a0591d6c00649f57e798519da8" in next_sec
    assert "lefthash" in next_sec
    assert "used_keys=false" in next_sec or "used\\_keys=false" in next_sec
    assert "Isolated-file detection remains unfinished" in next_sec
    assert "PROTOCOL-next-longctx-windows" in next_sec
    assert "8283d1f" in next_sec
    assert "50/100" in next_sec
    assert "93/100" in next_sec
    assert "has not been dumped" not in next_sec
    assert "12ea3ef1c34f037b" in PAPER
    assert "ac41821f88adba14" in PAPER
    assert "419a2088b2ba8e6e" in PAPER
    assert "ab8f1a9f340960c5" in PAPER
    assert "c36caf9745da2ce3" in PAPER
    assert "cc5ad2fcf035fdca" in PAPER
    assert "905c76810744421d" in PAPER
    assert "617663de48b81879" in PAPER
    assert "d7867f4c81b21ca2" in PAPER
    assert "8dc1d84856d1df5d" in PAPER
    assert "e8ac790aebdb8919" in PAPER
    assert "e0ccc7de1f47a79c" in PAPER
    assert "ca4c793eaaf77c18" in PAPER
    assert "d051137c566c5629" in PAPER
    assert "1d0ae9837b3cd4e0" in PAPER
    assert "4fb67051fb89839b" in PAPER
    assert "9bb1cf87dc11328e" in PAPER
    assert "d3932e3b1346789b" in PAPER
    assert "3535" in PAPER
    assert "8750" in PAPER
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "68/96" not in abs_
    assert "pair-distil-100x4-kgw" not in abs_
    assert "683/800" not in abs_
    assert "16170" not in abs_
    assert "56/96" not in abs_
    assert "573" not in abs_
    assert "608/800" not in abs_
    assert "3535" not in abs_
    assert "8750" not in abs_
    assert "98064" not in abs_
    assert "92842" not in abs_
    assert "85493" not in abs_
    assert "61305" not in abs_
    assert "1092" not in abs_
    assert "2036" not in abs_
    assert "1470" not in abs_
    assert "2048" not in abs_
    assert "3/100" not in abs_
    assert "ca4c793eaaf77c18" not in abs_
    assert "25167" not in abs_
    assert "49/96" not in abs_
    assert "41/96" not in abs_
    assert "pair-distil-12x4-aaronson" not in abs_
    assert "60/96" not in abs_
    assert "pair-qwen-12x4-aaronson" not in abs_
    assert "557/800" not in abs_
    assert "pair-distil-100x4-ngram13" not in abs_
    assert "601/800" not in abs_
    assert "pair-distil-100x4-aaronson" not in abs_
    assert "pair-qwen-100x4-aaronson" not in abs_
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "747/800" not in abs_
    assert "4557" not in abs_
    assert "pair-qwen-100x4-kgw" not in abs_
    assert "ed9fb20" not in abs_
    assert "620/800" not in abs_
    assert "4858" not in abs_
    assert "d8e6f7f" not in abs_
    assert "tab:kgwq100" not in abs_
    assert "context_width" in next_sec or "context\\_width" in next_sec


def test_kgw_qwen_100_freeze_table_has_no_invented_scores() -> None:
    tex = Path(ROOT / "paper" / "main.tex").read_text()
    before, after = tex.split(r"\label{tab:kgwq100}", 1)
    caption = before.rsplit(r"\begin{table}", 1)[1]
    body = after.split(r"\end{table}", 1)[0]
    table = caption + body
    assert "ed9fb20" in table
    assert "mixin=kgw" in table
    assert "15485863" in table
    assert "20260904" in table
    assert "results.json" in table
    assert r"\textbf{25/48}" in table
    assert "100/100" not in table
    assert "76/100" not in table
    assert "/800" not in table
    assert "H-kgw-q100-ctrl **holds**" not in table


def test_paper_opened_kgw_counts_match_dumps() -> None:
    next_sec = PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]
    gpt2_12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-12x4-kgw-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    gpt2_100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-100x4-kgw-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    distil_12_hard = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-distil-12x4-kgw-hard-last4"
            / "hard"
            / "holdout.json"
        ).read_text()
    )
    distil_100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-distil-100x4-kgw-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    distil_100_hard = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-distil-100x4-kgw-hard-last4"
            / "hard"
            / "holdout.json"
        ).read_text()
    )
    qwen_12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-qwen-12x4-kgw-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    qwen_12_hard = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-qwen-12x4-kgw-hard-last4"
            / "hard"
            / "holdout.json"
        ).read_text()
    )
    occ12 = json.loads(
        (ROOT / "experiments" / "2026-09-03-atoms-12x4-kgw" / "atoms.json").read_text()
    )
    occ100 = json.loads(
        (ROOT / "experiments" / "2026-09-03-atoms-100x4-kgw" / "atoms.json").read_text()
    )
    occ_d12 = json.loads(
        (
            ROOT / "experiments" / "2026-09-03-atoms-distil-12x4-kgw" / "atoms.json"
        ).read_text()
    )
    occ_d100 = json.loads(
        (
            ROOT / "experiments" / "2026-09-03-atoms-distil-100x4-kgw" / "atoms.json"
        ).read_text()
    )
    occ_q12 = json.loads(
        (
            ROOT / "experiments" / "2026-09-03-atoms-qwen-12x4-kgw" / "atoms.json"
        ).read_text()
    )
    assert gpt2_12["used_keys"] is False
    assert gpt2_100["used_keys"] is False
    ba12 = gpt2_12["n_marked_lr_positive"] + gpt2_12["n_unmarked_lr_nonpositive"]
    ba100 = gpt2_100["n_marked_lr_positive"] + gpt2_100["n_unmarked_lr_nonpositive"]
    ba_q = qwen_12["n_marked_lr_positive"] + qwen_12["n_unmarked_lr_nonpositive"]
    ba_d100 = distil_100["n_marked_lr_positive"] + distil_100["n_unmarked_lr_nonpositive"]
    assert f"{gpt2_12['n_prompts_marked_above']}/12" in next_sec
    assert f"{ba12}/96" in next_sec
    assert f"{gpt2_100['n_prompts_marked_above']}/100" in next_sec
    assert f"{ba100}/800" in next_sec
    assert str(occ12["n_seen"]) in next_sec
    assert str(occ100["n_seen"]) in next_sec
    assert f"{distil_12_hard['n_prompts_marked_above']}/12" in next_sec
    assert str(occ_d12["n_seen"]) in next_sec
    assert f"{distil_100['n_prompts_marked_above']}/100" in next_sec
    assert f"{ba_d100}/800" in next_sec
    assert f"{distil_100_hard['n_prompts_marked_above']}/100" in next_sec
    assert str(occ_d100["n_seen"]) in next_sec
    assert f"{ba_q}/96" in next_sec
    assert f"{qwen_12_hard['n_prompts_marked_above']}/12" in next_sec
    assert str(occ_q12["n_seen"]) in next_sec
    assert str(occ12["n_unseen"]) in next_sec
    assert str(occ100["n_unseen"]) in next_sec
    assert str(occ_d12["n_unseen"]) in next_sec
    assert str(occ_d100["n_unseen"]) in next_sec
    assert str(occ_q12["n_unseen"]) in next_sec
    ba_d12_hard = (
        distil_12_hard["n_marked_lr_positive"]
        + distil_12_hard["n_unmarked_lr_nonpositive"]
    )
    ba_q_hard = (
        qwen_12_hard["n_marked_lr_positive"]
        + qwen_12_hard["n_unmarked_lr_nonpositive"]
    )
    ba_d100_hard = (
        distil_100_hard["n_marked_lr_positive"]
        + distil_100_hard["n_unmarked_lr_nonpositive"]
    )
    assert f"{ba_d12_hard}/96" in next_sec
    assert f"{ba_q_hard}/96" in next_sec
    assert f"{ba_d100_hard}/800" in next_sec
    assert "ed9fb20" in next_sec
    assert "pair-qwen-100x4-kgw" in next_sec
    assert "before generation" in next_sec
    qwen_100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-probe-qwen-100x4-kgw-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    qwen_100_hard = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-probe-qwen-100x4-kgw-hard-last4"
            / "hard"
            / "holdout.json"
        ).read_text()
    )
    occ_q100 = json.loads(
        (
            ROOT / "experiments" / "2026-09-04-atoms-qwen-100x4-kgw" / "atoms.json"
        ).read_text()
    )
    ba_q100 = qwen_100["n_marked_lr_positive"] + qwen_100["n_unmarked_lr_nonpositive"]
    assert qwen_100["used_keys"] is False
    assert f"{qwen_100['n_prompts_marked_above']}/100" in next_sec
    assert f"{ba_q100}/800" in next_sec
    assert f"{qwen_100_hard['n_prompts_marked_above']}/100" in next_sec
    assert str(occ_q100["n_seen"]) in next_sec
    assert str(occ_q100["n_unseen"]) in next_sec


def test_paper_opened_100_family_counts_match_dumps() -> None:
    next_sec = PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]

    def ba(path: Path) -> tuple[int, int]:
        interp = json.loads((path / "interpolate" / "holdout.json").read_text())
        assert interp["used_keys"] is False
        wins = interp["n_prompts_marked_above"]
        balanced = (
            interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"]
        )
        return wins, balanced

    qwen_aar = ba(
        ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-aaronson-hard-last4"
    )
    qwen_hw12 = ba(
        ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-ngram13-hard-last4"
    )
    distil_hw12 = ba(
        ROOT / "experiments" / "2026-09-04-probe-distil-100x4-ngram13-hard-last4"
    )
    distil_aar = ba(
        ROOT / "experiments" / "2026-09-04-probe-distil-100x4-aaronson-hard-last4"
    )
    assert f"{qwen_aar[0]}/100" in next_sec
    assert f"{qwen_aar[1]}/800" in next_sec
    assert f"{qwen_hw12[0]}/100" in next_sec
    assert f"{qwen_hw12[1]}/800" in next_sec
    assert f"{distil_hw12[0]}/100" in next_sec
    assert f"{distil_hw12[1]}/800" in next_sec
    assert f"{distil_aar[0]}/100" in next_sec
    assert f"{distil_aar[1]}/800" in next_sec
    distil_hw12_pair = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-distil-100x4-ngram13"
            / "results.json"
        ).read_text()
    )
    n_unmarked = sum(
        row["unmarked_gen"]["mean"] > 0.55 for row in distil_hw12_pair["rows"]
    )
    assert f"${n_unmarked}/100$ above $0.55$" in next_sec
    qwen_hw12_pair = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-qwen-100x4-ngram13"
            / "results.json"
        ).read_text()
    )
    qwen_aar_pair = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-qwen-100x4-aaronson"
            / "results.json"
        ).read_text()
    )
    n_qhw = sum(
        row["unmarked_gen"]["mean"] > 0.55 for row in qwen_hw12_pair["rows"]
    )
    n_qaar = sum(
        row["unmarked_gen"]["z_score"] > 3.0 for row in qwen_aar_pair["rows"]
    )
    assert f"${n_qhw}/100$ above $0.55$" in next_sec
    assert f"${n_qaar}/100$ above $3.0$" in next_sec
    for rel in (
        "experiments/2026-09-04-atoms-qwen-100x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-qwen-100x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-100x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-100x4-aaronson/atoms.json",
    ):
        occ = json.loads((ROOT / rel).read_text())
        assert occ["used_keys"] is False
        assert f"{occ['n_seen']} seen versus {occ['n_unseen']} unseen" in next_sec
        w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
        assert f"{w0['n_seen']} versus {w0['n_unseen']}" in next_sec
    assert "pair-qwen-100x4-kgw" in next_sec
    assert "ed9fb20" in next_sec
    assert "before generation" in next_sec


def test_paper_opened_12loo_mixin_counts_match_dumps() -> None:
    next_sec = PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]

    def ba(path: Path) -> tuple[int, int, int]:
        interp = json.loads((path / "interpolate" / "holdout.json").read_text())
        hard = json.loads((path / "hard" / "holdout.json").read_text())
        assert interp["used_keys"] is False
        wins = interp["n_prompts_marked_above"]
        hard_wins = hard["n_prompts_marked_above"]
        balanced = (
            interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"]
        )
        return wins, hard_wins, balanced

    distil_hw12 = ba(
        ROOT / "experiments" / "2026-09-04-probe-distil-12x4-ngram13-hard-last4"
    )
    qwen_hw12 = ba(
        ROOT / "experiments" / "2026-09-04-probe-qwen-12x4-ngram13-hard-last4"
    )
    distil_aar = ba(
        ROOT / "experiments" / "2026-09-04-probe-distil-12x4-aaronson-hard-last4"
    )
    qwen_aar = ba(
        ROOT / "experiments" / "2026-09-04-probe-qwen-12x4-aaronson-hard-last4"
    )
    assert f"{distil_hw12[0]}/12" in next_sec
    assert f"{distil_hw12[2]}/96" in next_sec
    assert f"{distil_hw12[1]}/12" in next_sec
    assert f"{qwen_hw12[0]}/12" in next_sec
    assert f"{qwen_hw12[2]}/96" in next_sec
    assert f"{distil_aar[0]}/12" in next_sec
    assert f"{distil_aar[2]}/96" in next_sec or f"{distil_aar[2]}/48" in next_sec
    marked = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-probe-distil-12x4-aaronson-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )["n_marked_lr_positive"]
    assert f"{marked}/48" in next_sec
    assert f"{qwen_aar[0]}/12" in next_sec
    assert f"{qwen_aar[2]}/96" in next_sec
    for rel in (
        "experiments/2026-09-04-atoms-distil-12x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-qwen-12x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-12x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-qwen-12x4-aaronson/atoms.json",
    ):
        occ = json.loads((ROOT / rel).read_text())
        assert occ["used_keys"] is False
        assert f"{occ['n_seen']} seen versus {occ['n_unseen']} unseen" in next_sec
        w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
        assert f"{w0['n_seen']} versus {w0['n_unseen']}" in next_sec
    distil_hw12_12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-distil-12x4-ngram13"
            / "results.json"
        ).read_text()
    )
    qwen_hw12_12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-qwen-12x4-ngram13"
            / "results.json"
        ).read_text()
    )
    n_d12 = sum(
        row["unmarked_gen"]["mean"] > 0.55 for row in distil_hw12_12["rows"]
    )
    n_q12 = sum(
        row["unmarked_gen"]["mean"] > 0.55 for row in qwen_hw12_12["rows"]
    )
    assert f"${n_d12}/12$ above $0.55$" in next_sec
    assert f"${n_q12}/12$ above $0.55$" in next_sec
    assert "ed9fb20" in next_sec
    assert "before generation" in next_sec
    qwen_aar12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-qwen-12x4-aaronson"
            / "results.json"
        ).read_text()
    )
    n_qaar12 = sum(
        row["unmarked_gen"]["z_score"] > 3.0 for row in qwen_aar12["rows"]
    )
    assert f"${n_qaar12}/12$ above $3.0$" in next_sec
    distil_aar12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-distil-12x4-aaronson"
            / "results.json"
        ).read_text()
    )
    distil_aar100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-distil-100x4-aaronson"
            / "results.json"
        ).read_text()
    )
    n12 = sum(row["unmarked_gen"]["z_score"] > 3.0 for row in distil_aar12["rows"])
    n100 = sum(
        row["unmarked_gen"]["z_score"] > 3.0 for row in distil_aar100["rows"]
    )
    assert f"${n12}/12$ above $3.0$" in next_sec
    assert f"${n100}/100$ above $3.0$" in next_sec


def test_maskabs_table_is_dump_backed() -> None:
    tex = Path(ROOT / "paper" / "main.tex").read_text()
    assert r"\label{tab:maskabs}" in tex
    assert "58094d769726dc18" in tex
    assert "headline-windows-absolute" in tex
    body = tex.split(r"\label{tab:maskabs}")[1].split(r"\end{table}")[0]
    assert r"$5/12$" in body
    assert r"$9/12$" in body
    assert r"$4/12$" in body
    assert r"$3/12$" in body
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "58094d769726dc18" not in abs_
    assert "tab:maskabs" not in abs_


def test_nested_youden_is_post_hoc() -> None:
    assert "not second-level nested cross-validation" in PAPER
    assert "stay out of detector-performance comparisons" in PAPER
    assert "would remove $p$ before" in PAPER


def test_no_lab_slang_in_report_body() -> None:
    body = PAPER.split(r"\begin{document}")[1]
    for banned in (
        "honest miss",
        "sold as",
        "uniquely cursed",
        "this notebook",
        "official lamp",
        "already-opened",
        "post-open",
        "remains unopened",
    ):
        assert banned not in body
    body_main = body.split(r"\appendix")[0]
    assert "Grok-length" not in body_main


def test_readme_matches_revised_title() -> None:
    assert "Paired-Reference, Key-Free Indication" in README
    assert "47/96" in README
    assert "Not a valid $1/2$ null test" in README
    assert "25/51" in README
    assert "b70986d" in README
    assert "ngram_len=13" in README
    assert "8283d1f" in README
    assert "50/100" in README
    assert "93/100" in README
    assert "a761a7d" in README
    assert "616/800" in README
    assert "636765c" in README
    assert "474/800" in README
    assert "PROTOCOL-next-kgw" in README
    assert "--mixin kgw" in README
    assert "12/12" in README
    assert "85/96" in README
    assert "747/800" in README
    assert "PROTOCOL-next-kgw-qwen-100" in README
    assert "ed9fb20" in README
    assert "96/100" in README
    assert "620/800" in README
    assert "PROTOCOL-isolated-rankpath-lm" in README
    assert "d8e6f7f" in README
    assert "8f09aa6" in README
    assert "1582a09" in README
    assert "27 A4" in README
    assert "2a544de" in README
    assert "tectonic" in README.lower() or "pdflatex" in README.lower()
    assert "607a30d783dfa663caf39e06633721c8d4cfcd7e" in README
    assert "lowest three bits" in README
    qhw = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-atoms-qwen-100x4-ngram13"
            / "atoms.json"
        ).read_text()
    )
    qaar = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-atoms-qwen-100x4-aaronson"
            / "atoms.json"
        ).read_text()
    )
    assert qhw["used_keys"] is False
    assert qaar["used_keys"] is False
    readme_flat = re.sub(r"\s+", " ", README)
    assert f"**{qhw['n_seen']}** seen versus **{qhw['n_unseen']}** unseen" in readme_flat
    assert f"**{qaar['n_seen']}** seen versus **{qaar['n_unseen']}** unseen" in readme_flat
    w_hw = next(w for w in qhw["windows"] if w["start"] == 0 and w["end"] == 4)
    w_aar = next(w for w in qaar["windows"] if w["start"] == 0 and w["end"] == 4)
    assert f"**{w_hw['n_seen']}** versus **{w_hw['n_unseen']}**" in readme_flat
    assert f"**{w_aar['n_seen']}** versus **{w_aar['n_unseen']}**" in readme_flat


def test_experiments_readme_mixin_opening_occupancy_from_atoms() -> None:
    readme = (ROOT / "experiments" / "README.md").read_text()
    howto = re.sub(r"\s+", " ", (ROOT / "HOW-TO.md").read_text())
    dumps = (
        "experiments/2026-09-04-atoms-distil-12x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-100x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-qwen-12x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-qwen-100x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-12x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-distil-100x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-qwen-12x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-qwen-100x4-aaronson/atoms.json",
    )
    for rel in dumps:
        occ = json.loads((ROOT / rel).read_text())
        assert occ["used_keys"] is False
        w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
        stem = rel.split("/")[1]
        row = next(ln for ln in readme.splitlines() if stem in ln)
        assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in row
        assert f"opening **{w0['n_seen']}** vs **{w0['n_unseen']}**" in row
        if "100x4" in stem:
            assert (
                f"**{occ['n_seen']}** seen versus **{occ['n_unseen']}** unseen"
                in howto
            )
            assert f"**{w0['n_seen']}** versus **{w0['n_unseen']}**" in howto
    assert "Do not invent those scores" in howto
    assert "ed9fb20" in howto


def test_keys_withheld_by_design() -> None:
    assert "withheld by design" in PAPER


def test_prompt_matched_not_seed_paired() -> None:
    assert "prompt-matched" in PAPER
    assert "not seed-paired" in PAPER


def test_method_citations_present() -> None:
    assert "neyman1933most" in PAPER
    assert "fawcett2006roc" in PAPER
    assert "witten1991zero" in PAPER
    assert "lidstone1920note" in PAPER
    assert "ernst2004permutation" in PAPER
    assert "@article{neyman1933most" in BIB
    assert "@article{fawcett2006roc" in BIB
    assert "@article{youden1950index" in BIB


def test_h3_uses_paired_mcnemar() -> None:
    assert "McNemar" in PAPER
    assert "B-only" in PAPER or "only on B" in PAPER
    assert "0.00044" in PAPER


def test_pdf_metadata_and_monochrome_links() -> None:
    assert "pdftitle" in PAPER
    assert "pdfauthor" in PAPER
    assert "pdflang" in PAPER
    assert "linkcolor=black" in PAPER


def test_wang_cost_contrast_is_quoted_not_shared_benchmark() -> None:
    import json

    tables = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-transfer-100x4-to-12x4-hard-last4"
            / "tables-counts"
            / "tables.json"
        ).read_text()
    )
    n_marked = len(tables["marked"]["counts"])
    n_unmarked = len(tables["unmarked"]["counts"])
    assert tables["used_keys"] is False
    assert tables["n_train_prompts"] == 100
    assert str(n_marked) in PAPER
    assert str(n_unmarked) in PAPER
    assert "Qwen2.5-3B" in PAPER
    assert "0 neural parameters" in PAPER
    assert "2$\\times$A100" in PAPER or r"2$\times$A100" in PAPER
    assert "shared-benchmark TPR" in PAPER
    assert n_marked == 108454
    assert n_unmarked == 116491


def test_next_experiment_lock_is_ngram13_before_generation() -> None:
    assert r"\mathtt{ngram\_len}=13" in PAPER
    assert "b70986d" in PAPER
    assert "facc538" in PAPER
    assert "df5487d" in PAPER
    assert "--leave-one-out" in PAPER
    assert "4d29c92147e6da9d" in PAPER
    assert "ee0fcb86e6aceafc" in PAPER
    assert "PROTOCOL-next-longctx" in PAPER
    assert "seed 20260903" in PAPER
    assert "different corpus" in PAPER
    import json

    hard = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-12x4-ngram13-hard-last4"
            / "hard"
            / "holdout.json"
        ).read_text()
    )
    interp = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-12x4-ngram13-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    assert hard["used_keys"] is False
    pair12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-pair-12x4-ngram13"
            / "results.json"
        ).read_text()
    )
    assert pair12["ngram_len"] == 13
    assert pair12["seed"] == 20260903
    assert len(pair12["rows"]) == 12
    assert all(row["marked"]["mean"] > 0.55 for row in pair12["rows"])
    assert hard["n_prompts_marked_above"] == 6
    assert interp["n_prompts_marked_above"] == 6
    assert abs(hard["binary"]["auc"] - 0.544) < 0.001
    assert abs(interp["binary"]["auc"] - 0.541) < 0.001
    assert abs(hard["binary"]["mean_diff"] - 0.009) < 0.001
    assert abs(interp["binary"]["mean_diff"] - 0.021) < 0.001
    assert "0.009" in PAPER
    assert "0.021" in PAPER
    assert "0.544" in PAPER
    assert "0.541" in PAPER
    assert r"\textbf{6/12}" in PAPER
    assert "52/96" in PAPER
    intro = PAPER.split(r"\section{Introduction}")[1].split(r"\section{Related Work}")[0]
    assert r"\textbf{76/100}" in intro
    assert "tab:occ" in intro
    assert r"\textbf{76/100}" in PAPER
    assert r"\textbf{66/100}" in PAPER
    assert "not Distil/Qwen Phase" in PAPER
    assert "Phase~A" not in PAPER and "Phase A" not in PAPER
    assert r"Original 12, $\Hw=12$" in PAPER or "Original 12" in PAPER
    assert "One hundred families" in PAPER
    assert "Interpretation" in PAPER.split(r"\section{A Locked Next Experiment}")[1]
    interp_para = PAPER.split(r"\paragraph{Interpretation.}")[1].split(r"\section{Conclusion}")[0]
    assert "tab:occ" in interp_para
    assert "mostly backoff" in interp_para
    assert "mostly exact copies" in interp_para
    assert "Observed counts follow" in PAPER
    assert "489/800" in PAPER
    assert "436/800" in PAPER
    assert r"\textbf{400/400}" in PAPER
    pair100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-pair-100x4-ngram13"
            / "results.json"
        ).read_text()
    )
    assert pair100["ngram_len"] == 13
    assert len(pair100["rows"]) == 100
    assert all(row["marked"]["mean"] > 0.55 for row in pair100["rows"])
    assert r"\textbf{100/100}" in PAPER.split(r"\section{A Locked Next Experiment}")[1]
    assert "clustered permutation" in PAPER
    assert "0.247" in PAPER
    assert "0.0005" in PAPER
    assert abs(interp["prompt_sign_p"] - 0.247) < 0.01
    b100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-100x4-ngram13-hard-last4"
            / "interpolate"
            / "holdout.json"
        ).read_text()
    )
    hard100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-probe-100x4-ngram13-hard-last4"
            / "hard"
            / "holdout.json"
        ).read_text()
    )
    assert b100["used_keys"] is False
    assert b100["n_prompts_marked_above"] == 76
    assert abs(b100["binary"]["auc"] - 0.666) < 0.001
    assert abs(hard100["binary"]["auc"] - 0.579) < 0.001
    assert "0.666" in PAPER
    assert "0.579" in PAPER
    assert hard100["n_prompts_marked_above"] == 66
    assert (
        hard100["n_marked_lr_positive"] + hard100["n_unmarked_lr_nonpositive"]
        == 436
    )
    assert (
        b100["n_marked_lr_positive"] + b100["n_unmarked_lr_nonpositive"]
        == 489
    )
    assert abs(b100["binary"]["mean_diff"] - 0.156) < 0.001
    assert abs(b100["prompt_sign_p"] - 0.0005) < 0.0001
    assert "0.156" in PAPER
    assert r"\label{fig:hw12}" in Path(ROOT / "paper" / "main.tex").read_text()
    from collections import defaultdict
    from math import floor
    from statistics import median as _median

    by = defaultdict(lambda: {"m": [], "u": []})
    for row in b100["files"]:
        side = "u" if "unmarked" in row["file"] else "m"
        by[row["stem"]][side].append(row["lr"])
    counts = [0] * 11
    dps = []
    for v in by.values():
        dp = sum(v["m"]) / len(v["m"]) - sum(v["u"]) / len(v["u"])
        dps.append(dp)
        b = int(floor((dp + 0.4) / 0.1))
        b = max(0, min(10, b))
        counts[b] += 1
    assert abs(_median(dps) - 0.164) < 0.001
    assert min(dps) > -0.387 and min(dps) < -0.385
    assert max(dps) > 0.601 and max(dps) < 0.603
    assert "0.164" in PAPER
    assert "0.174" not in PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]
    assert sum(counts) == 100
    expected = ",".join(f"{i}/{c}" for i, c in enumerate(counts))
    assert expected == "0/1,1/2,2/8,3/13,4/17,5/15,6/20,7/13,8/5,9/5,10/1"
    assert expected in Path(ROOT / "paper" / "main.tex").read_text()
    assert "all 48 marked files" in PAPER
    next_raw = PAPER.split(r"\section{A Locked Next Experiment}")[1]
    assert "ferry-queue" in next_raw
    from collections import defaultdict as _dd
    from statistics import mean as _mean

    def _wins(hold: dict) -> set[str]:
        g = _dd(lambda: {"m": [], "u": []})
        for row in hold["files"]:
            side = "u" if "unmarked" in row["file"] else "m"
            g[row["stem"]][side].append(row["lr"])
        return {s for s, v in g.items() if _mean(v["m"]) > _mean(v["u"])}

    hard_wins = _wins(hard)
    interp_wins = _wins(interp)
    assert hard_wins == {
        "04-market",
        "06-station",
        "07-rain",
        "08-letter",
        "09-workshop",
        "12-ferry-queue",
    }
    assert interp_wins == {
        "03-library",
        "04-market",
        "06-station",
        "08-letter",
        "09-workshop",
        "12-ferry-queue",
    }
    assert len(hard_wins & interp_wins) == 5
    for name in ("market", "station", "rain", "letter", "workshop", "library"):
        assert name in next_raw
    occ = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-atoms-12x4-ngram13"
            / "atoms.json"
        ).read_text()
    )
    occ_pub = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-atoms-12x4-public-loo"
            / "atoms.json"
        ).read_text()
    )
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 160
    assert occ_pub["n_seen"] == 269
    assert occ["windows"][0]["n_seen"] == 71
    assert occ_pub["windows"][0]["n_seen"] == 84
    next_sec = PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]
    leftover = PAPER.split("Leftover versus covered isolated true positives")[1].split(
        "Ablations and Mechanistic Perturbation"
    )[0]
    assert "not a leftover union" in leftover
    assert "160 exact next-token events versus 269" in next_sec
    assert "20/48" in next_sec
    tex = Path(ROOT / "paper" / "main.tex").read_text()
    assert r"\label{tab:occ}" in tex
    assert "Original 12, full file & 160 & 269 & 12026 & 11912" in tex
    assert r"Original 12, $[0{:}4)$ & 71 & 84 & 217 & 204" in tex
    assert "100 families, full file & 5878 & 10158 & 95624 & 91353" in tex
    assert r"100 families, $[0{:}4)$ & 1287 & 1633 & 1113 & 767" in tex
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "160" not in abs_
    assert "269" not in abs_
    occ100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-atoms-100x4-ngram13"
            / "atoms.json"
        ).read_text()
    )
    occ100_pub = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-03-atoms-100x4-public-loo"
            / "atoms.json"
        ).read_text()
    )
    assert occ100["used_keys"] is False
    assert occ100["n_seen"] == 5878
    assert occ100_pub["n_seen"] == 10158
    assert occ100["windows"][0]["n_seen"] == 1287
    assert occ100_pub["windows"][0]["n_seen"] == 1633
    assert "5878 versus 10158" in next_sec
    assert "5878" not in abs_
    assert "10158" not in abs_
    concl = PAPER.split(r"\section{Conclusion}")[1].split(r"\appendix")[0]
    assert "tab:occ" in concl
    assert "tab:split" in concl
    assert r"\textbf{6/12}" in concl
    assert r"\textbf{25/48}" in concl
    assert r"\textbf{76/100}" in concl
    assert r"\textbf{47/96}" in concl
    assert r"\textbf{36/36}" in PAPER.split(r"\begin{abstract}")[1]
    assert hard["n_marked_lr_positive"] == 22
    assert hard["n_unmarked_lr_nonpositive"] == 30
    assert hard["n_marked_lr_positive"] + hard["n_unmarked_lr_nonpositive"] == 52
    abs_ = PAPER.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    assert "ngram_len=13" not in abs_
    assert "108454" not in abs_
    assert r"\textbf{6/12}" not in abs_
    assert r"\textbf{76/100}" not in abs_
    assert "489/800" not in abs_


def test_appendix_sha_prefixes_match_committed_dumps() -> None:
    import hashlib

    mapping = {
        "experiments/2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json": "e4f758305b631761",
        "experiments/2026-09-01-probe-100x4-hard-last4/interpolate/holdout.json": "de0f0c5738729e87",
        "experiments/2026-09-01-probe-100x4-opening-poshits/poshits/holdout.json": "aca0f852266c6b41",
        "experiments/2026-09-01-probe-distil-100x4-opening-poshits/poshits/holdout.json": "37834c2f0e45856c",
        "experiments/2026-09-01-probe-qwen-100x4-opening-poshits/poshits/holdout.json": "5b7e3c00264561f8",
        "experiments/2026-09-03-probe-12x4-headline-windows-absolute/results.json": "58094d769726dc18",
        "experiments/2026-09-03-pair-12x4-ngram13/results.json": "61153a82dab1eaea",
        "experiments/2026-09-03-probe-12x4-ngram13-hard-last4/hard/holdout.json": "fcff60687ac27348",
        "experiments/2026-09-03-pair-100x4-ngram13/results.json": "761b5d2ea676fa5d",
        "experiments/2026-09-03-probe-100x4-ngram13-hard-last4/interpolate/holdout.json": "e17cda239aa36e43",
        "experiments/2026-09-03-atoms-12x4-ngram13/atoms.json": "4d29c92147e6da9d",
        "experiments/2026-09-03-atoms-12x4-public-loo/atoms.json": "1247287a6369e93d",
        "experiments/2026-09-03-atoms-100x4-ngram13/atoms.json": "ee0fcb86e6aceafc",
        "experiments/2026-09-03-atoms-100x4-public-loo/atoms.json": "6d6d516ec296aae1",
        "experiments/2026-09-03-pair-12x4-kgw/results.json": "c4360e0c259b1f77",
        "experiments/2026-09-03-probe-12x4-kgw-hard-last4/interpolate/holdout.json": "67b8ed6bb2b96bcd",
        "experiments/2026-09-03-atoms-12x4-kgw/atoms.json": "cbde7405e481bfad",
        "experiments/2026-09-03-pair-100x4-kgw/results.json": "d96793694eaa2ab1",
        "experiments/2026-09-03-probe-100x4-kgw-hard-last4/interpolate/holdout.json": "dce85a6796def442",
        "experiments/2026-09-03-atoms-100x4-kgw/atoms.json": "e59753393fdc1d3e",
        "experiments/2026-09-03-resample-work/report.json": "e7a1a62a10585d1d",
        "experiments/2026-09-03-resample-work/blind-premark-vs-new-k4/results.json": "31894db2db724064",
        "experiments/2026-09-03-resample-work/blind-previous-vs-new-k4/results.json": "f852be4c7fd1dcf1",
        "experiments/2026-09-03-pair-distil-12x4-kgw/results.json": "f17ba689c14ecf21",
        "experiments/2026-09-03-probe-distil-12x4-kgw-hard-last4/interpolate/holdout.json": "845af54db1aeb37f",
        "experiments/2026-09-03-atoms-distil-12x4-kgw/atoms.json": "52c8fe2505a567c0",
        "experiments/2026-09-03-pair-qwen-12x4-kgw/results.json": "1e7e7a85888e2746",
        "experiments/2026-09-03-probe-qwen-12x4-kgw-hard-last4/interpolate/holdout.json": "68b96241a91e8a9c",
        "experiments/2026-09-03-atoms-qwen-12x4-kgw/atoms.json": "df93d69c13d85869",
        "experiments/2026-09-04-pair-distil-12x4-ngram13/results.json": "8dc1d84856d1df5d",
        "experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4/interpolate/holdout.json": "e8ac790aebdb8919",
        "experiments/2026-09-04-atoms-distil-12x4-ngram13/atoms.json": "e0ccc7de1f47a79c",
        "experiments/2026-09-04-pair-qwen-12x4-ngram13/results.json": "905c76810744421d",
        "experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4/interpolate/holdout.json": "617663de48b81879",
        "experiments/2026-09-04-atoms-qwen-12x4-ngram13/atoms.json": "d7867f4c81b21ca2",
        "experiments/2026-09-04-pair-distil-12x4-aaronson/results.json": "ab8f1a9f340960c5",
        "experiments/2026-09-04-probe-distil-12x4-aaronson-hard-last4/interpolate/holdout.json": "c36caf9745da2ce3",
        "experiments/2026-09-04-atoms-distil-12x4-aaronson/atoms.json": "cc5ad2fcf035fdca",
        "experiments/2026-09-04-pair-qwen-12x4-aaronson/results.json": "12ea3ef1c34f037b",
        "experiments/2026-09-04-probe-qwen-12x4-aaronson-hard-last4/interpolate/holdout.json": "ac41821f88adba14",
        "experiments/2026-09-04-atoms-qwen-12x4-aaronson/atoms.json": "419a2088b2ba8e6e",
        "experiments/2026-09-04-pair-distil-100x4-ngram13/results.json": "b46a5d5debed1485",
        "experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4/interpolate/holdout.json": "22d8c29006252a26",
        "experiments/2026-09-04-atoms-distil-100x4-ngram13/atoms.json": "331dbab436097872",
        "experiments/2026-09-04-pair-distil-100x4-aaronson/results.json": "a043578f9795a7be",
        "experiments/2026-09-04-probe-distil-100x4-aaronson-hard-last4/interpolate/holdout.json": "89d3b8c7f8d5d0e0",
        "experiments/2026-09-04-atoms-distil-100x4-aaronson/atoms.json": "06b4d85a772626d4",
        "experiments/2026-09-04-pair-qwen-100x4-ngram13/results.json": "ca4c793eaaf77c18",
        "experiments/2026-09-04-probe-qwen-100x4-ngram13-hard-last4/interpolate/holdout.json": "d051137c566c5629",
        "experiments/2026-09-04-atoms-qwen-100x4-ngram13/atoms.json": "1d0ae9837b3cd4e0",
        "experiments/2026-09-04-pair-qwen-100x4-aaronson/results.json": "4fb67051fb89839b",
        "experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4/interpolate/holdout.json": "9bb1cf87dc11328e",
        "experiments/2026-09-04-atoms-qwen-100x4-aaronson/atoms.json": "d3932e3b1346789b",
        "experiments/2026-09-04-resample-work/report.json": "c54c5beb6da07adb",
        "experiments/2026-09-04-resample-work/blind-premark-vs-new-k4/results.json": "4a8f0fba8cbda791",
        "experiments/2026-09-04-resample-work/blind-previous-vs-new-k4/results.json": "b31a564d60ade346",
    }
    tex = (ROOT / "paper" / "main.tex").read_text()
    for rel, prefix in mapping.items():
        digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:16]
        assert digest == prefix, f"{rel}: {digest} != {prefix}"
        assert prefix in tex, f"appendix missing {prefix} for {rel}"
    assert "PROTOCOL-next-kgw" in tex
    assert "2026-09-03-pair-12x4-kgw" in tex
    assert "ed9fb20" in tex
    assert "pair-qwen-100x4-kgw" in tex
    assert "d8e6f7f" in tex
    assert "PROTOCOL-isolated-rankpath-lm" in tex
    appendix = tex.split(r"\appendix")[1]
    assert "d8e6f7f" in appendix
    assert "rankpath-distil-lm" in appendix
    assert "rankpath-medium-lm" in appendix
    assert "Do not invent those scores" in appendix
    occ_qhw = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-atoms-qwen-100x4-ngram13"
            / "atoms.json"
        ).read_text()
    )
    occ_qaar = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-atoms-qwen-100x4-aaronson"
            / "atoms.json"
        ).read_text()
    )
    assert occ_qhw["used_keys"] is False
    assert occ_qaar["used_keys"] is False
    assert f"{occ_qhw['n_seen']} seen versus {occ_qhw['n_unseen']} unseen" in tex
    assert f"{occ_qaar['n_seen']} seen versus {occ_qaar['n_unseen']} unseen" in tex
    appendix = tex.split(r"\appendix")[1]
    assert "Do not invent interpolate counts" in appendix
    assert r"\textbf{25/48}" in appendix
