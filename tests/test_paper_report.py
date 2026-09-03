"""Lock the technical-report claims that Sol's 260903 review required."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPER = re.sub(r"\s+", " ", (ROOT / "paper" / "main.tex").read_text())
README = (ROOT / "paper" / "README.md").read_text()
BIB = (ROOT / "paper" / "references.bib").read_text()


def test_title_exposes_paired_reference_oracle() -> None:
    assert "Paired-Reference, Key-Free Indication" in PAPER
    assert "Public SynthID-Text Instance" in PAPER


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


def test_readme_matches_revised_title() -> None:
    assert "Paired-Reference, Key-Free Indication" in README
    assert "47/96" in README
    assert "Not a valid $1/2$ null test" in README
    assert "25/51" in README
    assert "b70986d" in README
    assert "ngram_len=13" in README
    assert "19 A4" in README
    assert "pdflatex" in README.lower() or "pdflatex" in README


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
    assert "0.544" in PAPER
    assert "0.541" in PAPER
    assert r"\textbf{6/12}" in PAPER
    assert "52/96" in PAPER
    intro = PAPER.split(r"\section{Introduction}")[1].split(r"\section{Related Work}")[0]
    assert r"\textbf{76/100}" in intro
    assert r"\textbf{76/100}" in PAPER
    assert r"\textbf{66/100}" in PAPER
    assert "not Distil/Qwen Phase" in PAPER
    assert r"Original 12, $\Hw=12$" in PAPER or "Original 12" in PAPER
    assert "One hundred families" in PAPER
    assert "Interpretation" in PAPER.split(r"\section{A Locked Next Experiment}")[1]
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

    by = defaultdict(lambda: {"m": [], "u": []})
    for row in b100["files"]:
        side = "u" if "unmarked" in row["file"] else "m"
        by[row["stem"]][side].append(row["lr"])
    counts = [0] * 11
    for v in by.values():
        dp = sum(v["m"]) / len(v["m"]) - sum(v["u"]) / len(v["u"])
        b = int(floor((dp + 0.4) / 0.1))
        b = max(0, min(10, b))
        counts[b] += 1
    assert sum(counts) == 100
    expected = ",".join(f"{i}/{c}" for i, c in enumerate(counts))
    assert expected == "0/1,1/2,2/8,3/13,4/17,5/15,6/20,7/13,8/5,9/5,10/1"
    assert expected in Path(ROOT / "paper" / "main.tex").read_text()
    assert "all 48 marked files" in PAPER
    assert "ferry-queue" in PAPER.split(r"\section{A Locked Next Experiment}")[1]
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
    next_sec = PAPER.split(r"\section{A Locked Next Experiment}")[1].split(
        r"\section{Conclusion}"
    )[0]
    assert "160 exact" in next_sec
    assert "269 versus 11912" in next_sec
    assert "20/48" in next_sec
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
    assert "5878 exact" in next_sec
    assert "10158 versus 91353" in next_sec
    assert "5878" not in abs_
    assert "10158" not in abs_
    concl = PAPER.split(r"\section{Conclusion}")[1].split(r"\appendix")[0]
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
