"""Claude resample: same PROMPTS, last-1 / last-4 vs pre-mark and previous sample.

Not a Claude detector. Not a watermark claim. Append-only logbook.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from text_watermark_tools.blind import (
    leave_one_prompt_out,
    load_twins,
    persist_blind_eval,
)
from text_watermark_tools.score import load_tokenizer

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "experiments"
PREMARK_DIR = EXPERIMENTS / "claude-premark-2026-08"
LOGBOOK_PATH = ROOT / "research" / "LOGBOOK.md"
COLLECT_SCRIPT = ROOT / "scripts" / "collect_claude_premark.py"
CHAT_ONLY = (
    " Write the full text in the chat only. "
    "Do not create a file, artifact, or document."
)
MIN_CHARS = 800
LABEL = "se.makeitso.text-watermark-claude-resample"
PLIST_NAME = "se.makeitso.text-watermark-claude-resample.plist"


def normalize_prompt(prompt: str) -> str:
    text = (prompt or "").strip()
    return text.replace(CHAT_ONLY, "").strip()


def load_manifest_rows(corpus_dir: Path) -> list[dict]:
    man = Path(corpus_dir) / "manifest.jsonl"
    if not man.is_file():
        return []
    rows: list[dict] = []
    for line in man.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if int(row.get("n_chars") or 0) < MIN_CHARS:
            continue
        if not row.get("prompt"):
            continue
        rows.append(row)
    return rows


def corpus_by_prompt(corpus_dir: Path) -> dict[str, dict]:
    by_prompt: dict[str, dict] = {}
    for row in load_manifest_rows(corpus_dir):
        by_prompt[normalize_prompt(row["prompt"])] = row
    return by_prompt


def stemify(index: int, prompt: str) -> str:
    words = re.sub(r"[^a-z0-9]+", "-", prompt.lower()).strip("-").split("-")[:6]
    return f"{index:02d}-" + "-".join(words)


def pair_by_prompt(
    older_dir: Path,
    newer_dir: Path,
    out_dir: Path,
) -> int:
    """Write twins: older = unmarked-gen, newer = marked. Returns pair count."""
    older = corpus_by_prompt(older_dir)
    newer_rows = load_manifest_rows(newer_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for i, row in enumerate(newer_rows, 1):
        key = normalize_prompt(row["prompt"])
        if key not in older:
            continue
        prev = older[key]
        stem = stemify(i, key)
        (out_dir / f"{stem}-unmarked-gen.txt").write_text(
            (Path(older_dir) / prev["file"]).read_text()
        )
        (out_dir / f"{stem}-marked.txt").write_text(
            (Path(newer_dir) / row["file"]).read_text()
        )
        n += 1
    return n


def list_sample_dirs(experiments: Path = EXPERIMENTS) -> list[Path]:
    found: list[Path] = []
    if not experiments.is_dir():
        return found
    for path in experiments.iterdir():
        if not path.is_dir():
            continue
        if not (
            path.name.startswith("claude-sample-")
            or path.name.startswith("claude-mark-")
        ):
            continue
        if (path / "manifest.jsonl").is_file():
            found.append(path)
    return sorted(found, key=lambda p: p.name)


def new_sample_dir(experiments: Path, day: str) -> Path:
    base = experiments / f"claude-sample-{day}"
    if not base.exists():
        return base
    for suffix in "bcdefghijklmnopqrstuvwxyz":
        cand = experiments / f"claude-sample-{day}{suffix}"
        if not cand.exists():
            return cand
    raise RuntimeError(f"no free sample dir for {day}")


def previous_sample_dir(
    experiments: Path,
    *,
    excluding: Path | None = None,
) -> Path | None:
    dirs = list_sample_dirs(experiments)
    if excluding is not None:
        exc = Path(excluding).resolve()
        dirs = [d for d in dirs if d.resolve() != exc]
    return dirs[-1] if dirs else None


@dataclass
class ContrastResult:
    name: str
    n_pairs: int
    last1_wins: int
    last4_wins: int
    used_keys: bool
    twin_dir: str
    last1_dir: str
    last4_dir: str


@dataclass
class ResampleReport:
    date: str
    new_dir: str
    n_collected: int
    collected: bool
    contrasts: list[ContrastResult] = field(default_factory=list)
    logbook_path: str = ""
    note: str = ""


def run_loo(
    twin_dir: Path,
    *,
    context_len: int,
    out_dir: Path,
    tokenizer=None,
) -> tuple[int, int, bool]:
    twins = load_twins(twin_dir, tokenizer=tokenizer)
    ev = leave_one_prompt_out(twins, context_len=context_len)
    persist_blind_eval(ev, out_dir)
    return ev.n_marked_wins, ev.n_pairs, bool(ev.used_keys)


def measure_contrast(
    name: str,
    older_dir: Path,
    newer_dir: Path,
    work_dir: Path,
    *,
    tokenizer=None,
) -> ContrastResult | None:
    twin_dir = work_dir / f"twins-{name}"
    n = pair_by_prompt(older_dir, newer_dir, twin_dir)
    if n < 2:
        return None
    k1_dir = work_dir / f"blind-{name}-k1"
    k4_dir = work_dir / f"blind-{name}-k4"
    w1, n1, keys1 = run_loo(
        twin_dir, context_len=1, out_dir=k1_dir, tokenizer=tokenizer
    )
    w4, n4, keys4 = run_loo(
        twin_dir, context_len=4, out_dir=k4_dir, tokenizer=tokenizer
    )
    return ContrastResult(
        name=name,
        n_pairs=n1,
        last1_wins=w1,
        last4_wins=w4,
        used_keys=keys1 or keys4,
        twin_dir=str(twin_dir),
        last1_dir=str(k1_dir),
        last4_dir=str(k4_dir),
    )


def format_logbook_entry(report: ResampleReport) -> str:
    lines = [
        f"## {report.date} resample",
        "",
        f"**Collection.** `{report.new_dir}` — **{report.n_collected}** long texts"
        f"{'' if report.collected else ' (collection skipped; existing corpus)'}.",
        "`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.",
        "Not a Claude detector. Not a watermark claim.",
        "",
    ]
    if report.contrasts:
        lines += [
            "| Contrast | last-1 | last-4 |",
            "|---|---|---|",
        ]
        for c in report.contrasts:
            lines.append(
                f"| {c.name} ({c.n_pairs} prompts) | "
                f"{c.last1_wins}/{c.n_pairs} | {c.last4_wins}/{c.n_pairs} |"
            )
        lines.append("")
        lines.append(
            "Last-1 ahead of last-4 is the style-shift order. "
            "Last-4 ahead of last-1 is the public-mixin watermark-window order. "
            "Do not call either a vendor detector. Same-day chance means draw noise."
        )
        lines.append("")
    if report.note:
        lines.append(report.note)
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def append_logbook(path: Path, block: str) -> None:
    """Append only. Never rewrite earlier entries."""
    path = Path(path)
    old = path.read_text() if path.is_file() else ""
    if old and not old.endswith("\n"):
        old += "\n"
    if not block.endswith("\n"):
        block += "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(old + block)


def collect_into(out_dir: Path, *, pause_s: int = 25) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(COLLECT_SCRIPT),
        "--via",
        "applescript",
        "--n",
        "0",
        "--pause",
        str(pause_s),
        "--out-dir",
        str(out_dir),
        "--suffix",
        "sonnet5-sample",
        "--assumed-watermark",
        "rumored",
        "--no-seed",
    ]
    if not (ROOT / ".venv" / "bin" / "python").is_file():
        cmd[0] = "python3"
    subprocess.run(cmd, cwd=str(ROOT), check=False)
    return len(load_manifest_rows(out_dir))


def analyze_and_append(
    *,
    new_dir: Path,
    premark_dir: Path = PREMARK_DIR,
    previous_dir: Path | None = None,
    logbook: Path = LOGBOOK_PATH,
    experiments: Path = EXPERIMENTS,
    date: str | None = None,
    collected: bool = False,
    tokenizer=None,
) -> ResampleReport:
    """Pair, last-1 / last-4 leave-one-out, append logbook. No network."""
    new_dir = Path(new_dir)
    day = date or datetime.now().strftime("%Y-%m-%d")
    n_collected = len(load_manifest_rows(new_dir))
    tok = tokenizer or load_tokenizer()
    work = experiments / f"{day}-resample-work"
    work.mkdir(parents=True, exist_ok=True)
    contrasts: list[ContrastResult] = []
    if premark_dir is not None and Path(premark_dir).is_dir():
        c = measure_contrast(
            "premark-vs-new",
            Path(premark_dir),
            new_dir,
            work,
            tokenizer=tok,
        )
        if c is not None:
            contrasts.append(c)
    if previous_dir is None:
        previous_dir = previous_sample_dir(experiments, excluding=new_dir)
    if previous_dir is not None and Path(previous_dir).resolve() != new_dir.resolve():
        c = measure_contrast(
            "previous-vs-new",
            Path(previous_dir),
            new_dir,
            work,
            tokenizer=tok,
        )
        if c is not None:
            contrasts.append(c)
    note = (
        "Do not train a Claude detector on the pre-mark pile alone. "
        f"Work dir: `{work}`."
    )
    if any(c.used_keys for c in contrasts):
        raise RuntimeError("resample consulted keys / hash_iv / g-values")
    report = ResampleReport(
        date=day,
        new_dir=str(new_dir),
        n_collected=n_collected,
        collected=collected,
        contrasts=contrasts,
        logbook_path=str(logbook),
        note=note,
    )
    append_logbook(Path(logbook), format_logbook_entry(report))
    (work / "report.json").write_text(
        json.dumps(
            {
                "date": report.date,
                "new_dir": report.new_dir,
                "n_collected": report.n_collected,
                "collected": report.collected,
                "contrasts": [
                    {
                        "name": c.name,
                        "n_pairs": c.n_pairs,
                        "last1_wins": c.last1_wins,
                        "last4_wins": c.last4_wins,
                        "used_keys": c.used_keys,
                    }
                    for c in contrasts
                ],
            },
            indent=2,
        )
        + "\n"
    )
    return report


def run_resample(
    *,
    skip_collect: bool = False,
    new_dir: Path | None = None,
    previous_dir: Path | None = None,
    premark_dir: Path = PREMARK_DIR,
    logbook: Path = LOGBOOK_PATH,
    experiments: Path = EXPERIMENTS,
    date: str | None = None,
    pause_s: int = 25,
    tokenizer=None,
) -> ResampleReport:
    day = date or datetime.now().strftime("%Y-%m-%d")
    collected = False
    if skip_collect:
        if new_dir is None:
            samples = list_sample_dirs(experiments)
            if not samples:
                raise FileNotFoundError("no existing Claude sample corpus")
            new_dir = samples[-1]
    else:
        if new_dir is None:
            new_dir = new_sample_dir(experiments, day)
        collect_into(new_dir, pause_s=pause_s)
        collected = True
    return analyze_and_append(
        new_dir=new_dir,
        premark_dir=premark_dir,
        previous_dir=previous_dir,
        logbook=logbook,
        experiments=experiments,
        date=day,
        collected=collected,
        tokenizer=tokenizer,
    )
