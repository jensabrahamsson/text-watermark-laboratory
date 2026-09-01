"""36 Grok-length prompts frozen before pair."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-grok36"
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-scale.md"
OTHER_PROMPT_DIRS = (
    ROOT / "experiments" / "2026-08-17-grok-prompts",
    ROOT / "experiments" / "2026-08-17-more-prompts",
    ROOT / "experiments" / "2026-08-31-prompts-long12",
    ROOT / "experiments" / "2026-08-31-prompts-family12",
    ROOT / "experiments" / "2026-08-31-prompts-tails12",
    ROOT / "experiments" / "2026-09-01-prompts-100",
    ROOT / "experiments" / "2026-09-01-prompts-grok12",
)


def _prompt_files() -> list[Path]:
    return sorted(p for p in PROMPTS.glob("*.txt") if p.name != "README.md")


def test_grok36_prompts_are_thirty_six_long_scenes() -> None:
    files = _prompt_files()
    assert [p.name[:3] for p in files] == [f"{n:03d}" for n in range(201, 237)]
    counts = [len(p.read_text().split()) for p in files]
    assert len(files) == 36
    assert min(counts) >= 220
    assert max(counts) <= 330


def test_grok36_prompts_are_disjoint_from_earlier_seeds() -> None:
    new = {p.read_text().strip() for p in _prompt_files()}
    old: set[str] = set()
    for folder in OTHER_PROMPT_DIRS:
        for path in folder.glob("*.txt"):
            old.add(path.read_text().strip())
    assert new.isdisjoint(old)
    assert len(new) == 36


def test_protocol_scale_names_frozen_locks_before_pair() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods postokhits --fit-prefix 4 --pos-bucket 1" in text
    assert "H-scale-A" in text
    assert "H-scale-grok" in text
    assert "H-scale-B" in text
    assert "H-scale-iso" in text
    assert "20260905" in text
    assert "2026-09-01-prompts-grok36" in text
    assert "2026-09-01-pair-grok12x4" in text
    assert "Do **not** mix" in text
    assert "thesis/" in text
    assert "Not yet" in text
    assert "pair-grok36x4" in text
