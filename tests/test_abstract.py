"""The abstract is the shop window: what is new, first."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABSTRACT = ROOT / "research" / "abstract.md"
README = ROOT / "README.md"


def _readme_abstract() -> str:
    text = README.read_text()
    start = text.index("## Abstract")
    rest = text[start + len("## Abstract") :].lstrip("\n")
    return rest.split("\n\n", 1)[0].strip()


def test_abstract_is_the_shop_window() -> None:
    locked = ABSTRACT.read_text()
    assert "shop window" in locked
    assert "Not in the window" in locked
    assert "We have built an empirical indicator for watermark presence" in locked
    assert "without the detector keys" in locked
    assert "**prompt groups**" in locked
    assert "Jens Abrahamsson" in locked
    assert "Master of Science" in locked
    assert "**9/12**" in locked
    assert "**36/36**" in locked
    assert "**99/100**" in locked
    assert "**25/48**" in locked
    assert "**12/12**" in locked
    assert "Christ et al. (2024)" in locked
    assert "Zhang et al. (2024)" in locked
    assert "Wang et al. (2026)" in locked
    assert "thesis/" in locked
    assert "Do not write `thesis/`" in locked
    window = locked.split("## Shop window", 1)[1].split("## Not in the window", 1)[0]
    assert window.strip().startswith("We have built")
    assert not window.strip().startswith("Official")
    stock = locked.split("## Not in the window", 1)[1]
    assert "**31/48**" in stock
    assert "**22/48**" in stock
    assert "**16/48**" in stock
    assert "**33/48**" in stock
    assert "**15/15**" in stock
    assert "**6/12**" in stock
    assert "**52/96**" in stock
    assert "31/48" not in window
    assert "22/48" not in window
    assert "16/48" not in window
    assert "33/48" not in window
    assert "15/15" not in window
    assert "52/96" not in window


def test_readme_abstract_matches_the_window() -> None:
    pane = _readme_abstract()
    first = pane.split(".", 1)[0]
    assert first.startswith("We have built an empirical indicator for watermark presence")
    assert "without the detector keys" in first
    assert "**prompt groups**" in first
    assert not pane.startswith("Official")
    assert "**9/12**" in pane
    assert "**36/36**" in pane
    assert "**99/100**" in pane
    assert "**25/48**" in pane
    assert "**12/12**" in pane
    assert "31/48" not in pane
    assert "22/48" not in pane
    assert "16/48" not in pane
    assert "33/48" not in pane
    assert "15/15" not in pane
    assert "52/96" not in pane
    assert "6/12" not in pane
    assert "research/abstract.md" in pane
    assert "Master of Science" in README.read_text()
    assert "Jens Abrahamsson" in README.read_text()
    locked = ABSTRACT.read_text()
    window = locked.split("## Shop window", 1)[1].split("## Not in the window", 1)[0]
    for token in ("**9/12**", "**36/36**", "**99/100**", "**25/48**"):
        assert token in window
        assert token in pane
