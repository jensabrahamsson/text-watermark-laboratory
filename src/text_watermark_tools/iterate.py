"""Rewrite with a non-origin model; official-score until this instance is near 0.50.

Not a remover. Not a Claude check. The stop condition is our public DeepMind
30-key mean / weighted mean sitting at chance.
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

PARAPHRASE_PROMPT = (
    "Rewrite the following text so that it uses substantially different wording "
    "at the token level. Change clause order, connectors, and transition words; "
    "vary sentence boundaries and length; and replace both content words and "
    "function words where meaning allows. Preserve all facts, numbers, names, "
    "and technical identifiers. Do not add or remove claims. Output only the "
    "rewritten text.\n\n---\n{TEXT}"
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

    @property
    def source(self) -> IteratePass:
        return self.passes[0]

    @property
    def final(self) -> IteratePass:
        return self.passes[-1]


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
) -> IterateRun:
    """Score, rewrite, score again until chance or max_passes.

    `rewrite` is injected so tests drive the real scorer without a network.
    """
    run = IterateRun(
        operator=operator,
        model=model,
        via=via,
        mean_tol=mean_tol,
        min_unmasked_ngrams=min_unmasked_ngrams,
        max_passes=max_passes,
        stopped_at_chance=False,
    )
    current = text
    source_score = official_score_text(current)
    run.passes.append(
        IteratePass(
            n=0,
            text=current,
            score=source_score,
            at_chance=at_chance(
                source_score,
                mean_tol=mean_tol,
                min_unmasked_ngrams=min_unmasked_ngrams,
            ),
        )
    )
    if run.passes[0].at_chance:
        run.stopped_at_chance = True
        return run

    for n in range(1, max_passes + 1):
        current = rewrite(current)
        if not current.strip():
            raise OperatorError("rewrite produced empty text")
        score = official_score_text(current)
        done = at_chance(
            score, mean_tol=mean_tol, min_unmasked_ngrams=min_unmasked_ngrams
        )
        run.passes.append(
            IteratePass(n=n, text=current, score=score, at_chance=done)
        )
        if done:
            run.stopped_at_chance = True
            break
    return run


def print_iterate_run(run: IterateRun) -> str:
    lines = [
        (
            f"operator={run.operator} model={run.model} via={run.via} "
            f"stopped_at_chance={run.stopped_at_chance} "
            f"passes={len(run.passes) - 1}/{run.max_passes} "
            f"instance=public-deepmind-30"
        )
    ]
    for p in run.passes:
        label = "source" if p.n == 0 else f"pass-{p.n}"
        lines.append(format_score(label, p.score))
        lines.append(f"{label}_at_chance={p.at_chance}")
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
        "stopped_at_chance": run.stopped_at_chance,
        "note": (
            "Stop condition is official detector_mean near 0.50 on the public "
            "DeepMind 30-key instance. Not a vendor-oracle. Not a remover."
        ),
        "passes": [
            {
                "n": p.n,
                "mean": p.score.mean,
                "weighted_mean": p.score.weighted_mean,
                "n_tokens": p.score.n_tokens,
                "n_unmasked_ngrams": p.score.n_unmasked_ngrams,
                "at_chance": p.at_chance,
            }
            for p in run.passes
        ],
    }
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    md = [
        "# Iterate until this instance is at chance",
        "",
        f"Operator: `{run.operator}` / `{run.model}` / via `{run.via}`.",
        f"Stopped at chance: **{run.stopped_at_chance}**.",
        "",
        "Not a remover. Not Claude. Only whether *our* public key set went dark.",
        "",
        "| Pass | Mean | Weighted | Tokens | Unmasked n-grams | At chance |",
        "|---|---|---|---|---|---|",
    ]
    for p in run.passes:
        name = "source" if p.n == 0 else str(p.n)
        md.append(
            f"| {name} | {p.score.mean:.6f} | {p.score.weighted_mean:.6f} | "
            f"{p.score.n_tokens} | {p.score.n_unmasked_ngrams} | {p.at_chance} |"
        )
    md.append("")
    (out_dir / "results.md").write_text("\n".join(md) + "\n")
