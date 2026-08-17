# AGENTS.md

Instructions for coding agents in this repository.
https://github.com/jensabrahamsson/text-watermark-laboratory

Humans start at [README.md](README.md) and [HOW-TO.md](HOW-TO.md).
Do not copy those files into this one.

## What this repo is

A research tool that scores text against DeepMind’s **public** SynthID-Text
instance (`public-deepmind-30`, `ngram_len=5`) and runs key-free twin
experiments (same prompt, mixin on vs off).

It is not a general AI detector, not a Claude/ChatGPT detector, and not a
watermark remover. ≈ 0.50 with enough n-grams means **not this key set**.

## Language and git

- English only in code, comments, CLI, docs, experiment notes, and commits.
  Historical Claude pre-mark *outputs* stay as collected.
- Author/committer: **Jens Abrahamsson** `<jens.abrahamsson@makeitso.se>`.
- Remote: `origin` → `jensabrahamsson/text-watermark-laboratory`. Do not
  create a second repository.
- Commit messages: plain English. Say what changed.

## Do not

- Edit the `synthid-text` checkout except `pip install -e … --no-deps`
- Reimplement `detector_mean` (`weighted_mean_score` mutates g; pass a fresh array)
- Call the code a remover, or use **attack** in user-facing text
- Treat `score` as a Claude oracle (wrong instance)
- Train a Claude detector on the pre-mark corpus alone
- Invert keys/IV from a string — `research/invertibility.md`
- Download DIPPER — `research/dipper-local.md`
- Commit secrets (`*-KEY.conf`, `.env`, `.browser-profile/`). Never put keys
  on argv. If a secret lands in git, delete it and rotate the key
- Change existing `PROMPTS` strings in `scripts/collect_claude_premark.py`

## Environment

- CPU JAX. Not `jax[cuda]`.
- `transformers==4.57.6` (shim in `generate.py`; 5.x stops GPT-2 at EOS too early).
- `pip install -e <synthid-text-checkout> --no-deps`
- `min_new_tokens=max_new_tokens` when generating with the mixin.

```bash
source .venv/bin/activate
python -m pytest tests/ -q
```

## Commands that matter

```bash
python -m text_watermark_tools score FILE.txt
python -m text_watermark_tools pair DIR --out-dir experiments/pair
python -m text_watermark_tools blind experiments/pair --out-dir experiments/blind
python -m text_watermark_tools indicate score FILE.txt --tables experiments/indicator-gpt2
python -m text_watermark_tools iterate FILE.txt --backend qwen --out-dir experiments/iterate
```

`score` is the official key-based measurement. `indicate` is a weak
token-count tilt on one file (held-out marked `lr>0`: 29/48). Do not treat
`indicate` as `score`.

Current twin result: official **12/12**; key-free last-4 **10/12**
(`--margin 0.02` → **11/12**). Write-up: `research/key-free-twins.md`.

## Code

| Module | Role |
|---|---|
| `score.py` | Official mean / weighted mean via `synthid_text.detector_mean` |
| `generate.py` | GPT-2 + mixin, temp 1.0, `min_new_tokens` |
| `pair.py` | Same prompt, unmarked vs marked |
| `blind.py` | Key-free leave-one-out on twins |
| `indicator.py` | Frozen count tables; single-file `lr` |
| `iterate.py` | Rewrite a *known-marked* file; official score again |
| `surrogate.py` / `experiment.py` | Older known-mark rewrite harness |

Mixin `get_gvals` docstring is wrong. Trust the code: 12× LCG, then
`(hash >> 30) % 2`.

## Claude

Day-one marking: models launched **2 Aug 2026** or later. Sonnet 5 (30 Jun)
is not day-one; retrofit unpublished; no public detector. Pre-mark corpus:
`experiments/claude-premark-2026-08/` (40 A/B texts). After they announce
marking, rerun the same `PROMPTS` into `experiments/claude-mark-<date>/`.

