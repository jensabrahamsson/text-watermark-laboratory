"""Grok-register isolated protocol: prompts frozen before pair."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-grok12"
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-register.md"
OTHER_PROMPT_DIRS = (
    ROOT / "experiments" / "2026-08-17-grok-prompts",
    ROOT / "experiments" / "2026-08-17-more-prompts",
    ROOT / "experiments" / "2026-08-31-prompts-long12",
    ROOT / "experiments" / "2026-08-31-prompts-family12",
    ROOT / "experiments" / "2026-08-31-prompts-tails12",
    ROOT / "experiments" / "2026-09-01-prompts-100",
)


def _prompt_files() -> list[Path]:
    return sorted(p for p in PROMPTS.glob("*.txt") if p.name != "README.md")


def test_grok12_prompts_are_twelve_long_scenes() -> None:
    files = _prompt_files()
    assert [p.name[:3] for p in files] == [f"{n:03d}" for n in range(101, 113)]
    counts = [len(p.read_text().split()) for p in files]
    assert len(files) == 12
    assert min(counts) >= 220
    assert max(counts) <= 360


def test_grok12_prompts_are_disjoint_from_earlier_seeds() -> None:
    new = {p.read_text().strip() for p in _prompt_files()}
    old: set[str] = set()
    for folder in OTHER_PROMPT_DIRS:
        for path in folder.glob("*.txt"):
            if path.name == "README.md":
                continue
            old.add(path.read_text().strip())
    assert new.isdisjoint(old)
    assert len(new) == 12


def test_protocol_isolated_register_freezes_locks_and_forbids_pair() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "Do **not** run `pair` until" in text
    assert "H-reg-iso" in text
    assert "seed" in text.lower() and "20260904" in text
    assert "thesis/" in text
