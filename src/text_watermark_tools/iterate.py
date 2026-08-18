"""Rewrite a known-marked file; official-score every pass.

Not a remover. Not a Claude check. Default stop is official mean / weighted
mean near 0.50 on public-deepmind-30. Optional stop is the key-free
single-file indicator (indicate LR). Stop-on-indicate is not official score.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urlparse

from text_watermark_tools.score import (
    OfficialScore,
    format_score,
    official_score_text,
)

DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MEAN_TOL = 0.03
DEFAULT_MIN_NGRAMS = 80
DEFAULT_MAX_PASSES = 4
DEFAULT_INDICATE_THRESHOLD = 0.0
STOP_CHANCE = "chance"
STOP_INDICATE = "indicate"

PARAPHRASE_PROMPT = (
    "Rewrite the following text so that it uses substantially different wording "
    "at the token level. Change clause order, connectors, and transition words; "
    "vary sentence boundaries and length; and replace both content words and "
    "function words where meaning allows. Preserve all facts, numbers, names, "
    "and technical identifiers. Do not add or remove claims. Output only the "
    "rewritten text.\n\n---\n{TEXT}"
)
POLISH_PROMPT = (
    "Lightly correct the word choice in the following text so that it sounds "
    "better. Make only small lexical edits. Do not reorder clauses, do not "
    "change sentence boundaries, and do not paraphrase. Preserve all facts, "
    "numbers, names, and technical identifiers. Do not add or remove claims. "
    "Output only the lightly edited text.\n\n---\n{TEXT}"
)
ZH_OUT_PROMPT = (
    "Translate the following text to Simplified Chinese. "
    "Output only the translation.\n\n---\n{TEXT}"
)
ZH_BACK_PROMPT = (
    "Translate the following text to English. Preserve meaning; use natural "
    "phrasing. Output only the English text.\n\n---\n{TEXT}"
)


class OperatorError(RuntimeError):
    """The rewrite backend could not produce a new text."""


def at_chance(
    score: OfficialScore,
    *,
    mean_tol: float = DEFAULT_MEAN_TOL,
    min_unmasked_ngrams: int = DEFAULT_MIN_NGRAMS,
) -> bool:
    """True when this instance looks like chance, with enough n-grams to say so."""
    if score.n_unmasked_ngrams < min_unmasked_ngrams:
        return False
    return (
        abs(score.mean - 0.5) < mean_tol
        and abs(score.weighted_mean - 0.5) < mean_tol
    )


def paraphrase_prompt(text: str) -> str:
    return PARAPHRASE_PROMPT.format(TEXT=text)


def polish_prompt(text: str) -> str:
    return POLISH_PROMPT.format(TEXT=text)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEEPSEEK_KEY_FILE = "DEEPSEEK-KEY.conf"
DASHSCOPE_KEY_FILE = "DASHSCOPE-KEY.conf"


def env_api_key(*names: str) -> Optional[str]:
    for name in names:
        key = os.environ.get(name, "").strip()
        if key:
            return key
    return None


def read_key_conf(path: Path) -> Optional[str]:
    """Read a local key file: comment lines skipped; KEY=value or a bare key."""
    if not path.is_file():
        return None
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            _name, _, value = line.partition("=")
            line = value.strip().strip('"').strip("'")
        if line and not line.startswith("${"):
            return line
    return None


def _key_search_dirs() -> list[Path]:
    extra = os.environ.get("TEXT_WATERMARK_KEY_DIR", "").strip()
    if extra:
        return [Path(extra).resolve()]
    seen: list[Path] = []
    for d in (Path.cwd(), REPO_ROOT):
        resolved = d.resolve()
        if resolved not in seen:
            seen.append(resolved)
    return seen


def key_from_conf(filename: str) -> Optional[str]:
    for directory in _key_search_dirs():
        found = read_key_conf(directory / filename)
        if found:
            return found
    return None


def deepseek_api_key() -> Optional[str]:
    return env_api_key("DEEPSEEK_API_KEY") or key_from_conf(DEEPSEEK_KEY_FILE)


def dashscope_api_key() -> Optional[str]:
    return env_api_key("DASHSCOPE_API_KEY") or key_from_conf(DASHSCOPE_KEY_FILE)


def _no_redirect_opener() -> urllib.request.OpenerDirector:
    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)

    return urllib.request.build_opener(_NoRedirect())


def chat_complete(
    prompt: str,
    *,
    api_key: str,
    model: str = DEFAULT_MODEL,
    base_url: str = DEFAULT_BASE_URL,
    timeout: float = 120.0,
    extra: Optional[dict] = None,
) -> str:
    """One OpenAI-compatible chat completion."""
    base = base_url.rstrip("/")
    url = base + "/chat/completions"
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise OperatorError(f"refusing non-http(s) rewrite URL: {url}")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    if extra:
        payload.update(extra)
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(  # noqa: S310 — scheme checked above
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with _no_redirect_opener().open(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise OperatorError(f"chat request failed: {exc}") from exc
    choices = data.get("choices") or []
    if not choices:
        raise OperatorError(f"chat empty choices: {data!r}"[:400])
    content = (choices[0].get("message") or {}).get("content")
    if not content or not str(content).strip():
        raise OperatorError("chat returned empty content")
    return str(content).strip()


def rewrite_once(
    text: str,
    *,
    via: str,
    chat: Callable[..., str],
) -> str:
    if via == "paraphrase":
        return chat(paraphrase_prompt(text))
    if via == "polish":
        return chat(polish_prompt(text))
    if via == "zh":
        zh = chat(ZH_OUT_PROMPT.format(TEXT=text))
        return chat(ZH_BACK_PROMPT.format(TEXT=zh))
    raise ValueError(f"unknown via: {via}")


@dataclass
class IteratePass:
    n: int
    text: str
    score: OfficialScore
    at_chance: bool
    lr: Optional[float] = None
    indicate_dark: Optional[bool] = None


@dataclass
class IterateRun:
    operator: str
    model: str
    via: str
    mean_tol: float
    min_unmasked_ngrams: int
    max_passes: int
    stopped_at_chance: bool
    passes: list[IteratePass] = field(default_factory=list)
    stop_on: str = STOP_CHANCE
    indicate_threshold: float = DEFAULT_INDICATE_THRESHOLD
    stopped_on_indicate: bool = False

    @property
    def source(self) -> IteratePass:
        return self.passes[0]

    @property
    def final(self) -> IteratePass:
        return self.passes[-1]

    @property
    def met_stop(self) -> bool:
        if self.stop_on == STOP_INDICATE:
            return self.stopped_on_indicate
        return self.stopped_at_chance


def _make_pass(
    n: int,
    text: str,
    score: OfficialScore,
    *,
    mean_tol: float,
    min_unmasked_ngrams: int,
    indicate: Optional[Callable[[str], float]],
    indicate_threshold: float,
) -> IteratePass:
    lr = indicate(text) if indicate is not None else None
    dark = None if lr is None else lr <= indicate_threshold
    return IteratePass(
        n=n,
        text=text,
        score=score,
        at_chance=at_chance(
            score,
            mean_tol=mean_tol,
            min_unmasked_ngrams=min_unmasked_ngrams,
        ),
        lr=lr,
        indicate_dark=dark,
    )


def _stop_now(run: IterateRun, step: IteratePass) -> bool:
    if run.stop_on == STOP_INDICATE:
        if step.indicate_dark:
            run.stopped_on_indicate = True
            return True
        return False
    if step.at_chance:
        run.stopped_at_chance = True
        return True
    return False


def run_iterate(
    text: str,
    *,
    rewrite: Callable[[str], str],
    operator: str,
    model: str,
    via: str = "paraphrase",
    max_passes: int = DEFAULT_MAX_PASSES,
    mean_tol: float = DEFAULT_MEAN_TOL,
    min_unmasked_ngrams: int = DEFAULT_MIN_NGRAMS,
    indicate: Optional[Callable[[str], float]] = None,
    indicate_threshold: float = DEFAULT_INDICATE_THRESHOLD,
    stop_on: str = STOP_CHANCE,
) -> IterateRun:
    """Official-score every pass; rewrite until the chosen stop or max_passes.

    `rewrite` (and optional `indicate`) are injected so tests drive the real
    loop without a network. Official mean / weighted mean are always stored.
    `stop_on=indicate` is not official score.
    """
    if stop_on not in (STOP_CHANCE, STOP_INDICATE):
        raise ValueError(f"unknown stop_on: {stop_on}")
    if stop_on == STOP_INDICATE and indicate is None:
        raise ValueError("stop_on=indicate needs an indicate function")
    run = IterateRun(
        operator=operator,
        model=model,
        via=via,
        mean_tol=mean_tol,
        min_unmasked_ngrams=min_unmasked_ngrams,
        max_passes=max_passes,
        stopped_at_chance=False,
        stop_on=stop_on,
        indicate_threshold=indicate_threshold,
        stopped_on_indicate=False,
    )
    current = text
    source_pass = _make_pass(
        0,
        current,
        official_score_text(current),
        mean_tol=mean_tol,
        min_unmasked_ngrams=min_unmasked_ngrams,
        indicate=indicate,
        indicate_threshold=indicate_threshold,
    )
    run.passes.append(source_pass)
    if _stop_now(run, source_pass):
        return run

    for n in range(1, max_passes + 1):
        current = rewrite(current)
        if not current.strip():
            raise OperatorError("rewrite produced empty text")
        step = _make_pass(
            n,
            current,
            official_score_text(current),
            mean_tol=mean_tol,
            min_unmasked_ngrams=min_unmasked_ngrams,
            indicate=indicate,
            indicate_threshold=indicate_threshold,
        )
        run.passes.append(step)
        if _stop_now(run, step):
            break
    return run


def print_iterate_run(run: IterateRun) -> str:
    lines = [
        (
            f"operator={run.operator} model={run.model} via={run.via} "
            f"stop_on={run.stop_on} "
            f"stopped_at_chance={run.stopped_at_chance} "
            f"stopped_on_indicate={run.stopped_on_indicate} "
            f"passes={len(run.passes) - 1}/{run.max_passes} "
            f"instance=public-deepmind-30"
        )
    ]
    for p in run.passes:
        label = "source" if p.n == 0 else f"pass-{p.n}"
        lines.append(format_score(label, p.score))
        lines.append(f"{label}_at_chance={p.at_chance}")
        if p.lr is not None:
            lines.append(
                f"{label}_lr={p.lr:.6f} {label}_indicate_dark={p.indicate_dark} "
                f"indicate_threshold={run.indicate_threshold} "
                f"not_official_score=true"
            )
    return "\n".join(lines)


def persist_iterate_run(run: IterateRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "source.txt").write_text(run.source.text.rstrip() + "\n")
    (out_dir / "final.txt").write_text(run.final.text.rstrip() + "\n")
    for p in run.passes:
        if p.n == 0:
            continue
        (out_dir / f"pass-{p.n}.txt").write_text(p.text.rstrip() + "\n")
    table = {
        "operator": run.operator,
        "model": run.model,
        "via": run.via,
        "instance": "public-deepmind-30",
        "ngram_len": 5,
        "mean_tol": run.mean_tol,
        "min_unmasked_ngrams": run.min_unmasked_ngrams,
        "max_passes": run.max_passes,
        "stop_on": run.stop_on,
        "indicate_threshold": run.indicate_threshold,
        "stopped_at_chance": run.stopped_at_chance,
        "stopped_on_indicate": run.stopped_on_indicate,
        "note": (
            "Official detector_mean is recorded every pass. Default stop is "
            "that mean near 0.50 on the public DeepMind 30-key instance. "
            "Stop-on-indicate is the key-free single-file LR, not official "
            "score. Not a vendor-oracle. Not a remover."
        ),
        "passes": [
            {
                "n": p.n,
                "mean": p.score.mean,
                "weighted_mean": p.score.weighted_mean,
                "n_tokens": p.score.n_tokens,
                "n_unmasked_ngrams": p.score.n_unmasked_ngrams,
                "at_chance": p.at_chance,
                "lr": p.lr,
                "indicate_dark": p.indicate_dark,
            }
            for p in run.passes
        ],
    }
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    md = [
        "# Iterate rewrite measurement",
        "",
        f"Operator: `{run.operator}` / `{run.model}` / via `{run.via}`.",
        f"Stop on: `{run.stop_on}`.",
        f"Stopped at chance: **{run.stopped_at_chance}**.",
        f"Stopped on indicate: **{run.stopped_on_indicate}**.",
        "",
        "Not a remover. Not Claude. Official mean is this public key set. "
        "Stop-on-indicate is not official `score`. Light polish is the control.",
        "",
        "| Pass | Mean | Weighted | Tokens | Unmasked n-grams | At chance | LR | Indicate dark |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in run.passes:
        name = "source" if p.n == 0 else str(p.n)
        lr = "" if p.lr is None else f"{p.lr:.6f}"
        dark = "" if p.indicate_dark is None else str(p.indicate_dark)
        md.append(
            f"| {name} | {p.score.mean:.6f} | {p.score.weighted_mean:.6f} | "
            f"{p.score.n_tokens} | {p.score.n_unmasked_ngrams} | {p.at_chance} | "
            f"{lr} | {dark} |"
        )
    md.append("")
    (out_dir / "results.md").write_text("\n".join(md) + "\n")
