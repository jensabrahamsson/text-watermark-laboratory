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
    ):
        assert banned not in body


def test_readme_matches_revised_title() -> None:
    assert "Paired-Reference, Key-Free Indication" in README
    assert "47/96" in README
    assert "Not a valid $1/2$ null test" in README
    assert "25/51" in README


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
