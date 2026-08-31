# AGENTS.md

Instructions for coding agents working in this repository.

Human-facing entry points are [README.md](README.md) and [HOW-TO.md](HOW-TO.md).

## Project purpose

This repository studies statistical text watermarking using Google DeepMind's public SynthID-Text reference implementation.

It has two distinct detection paths:

1. **`score`** — the ordinary key-based reference measurement for `public-deepmind-30`.
2. **`indicate` / `blind`** — a key-free experimental indicator learned from matched marked/unmarked generations.

The key-free work is a central result of the repository. Describe it accurately: **we have built an indicator for watermark presence without the detector keys**. It performs well at matched/repeated prompt grain (currently 10/12 hard last-4, or 11/12 with a 0.02 comparison margin on that scorer; hits/hashpool 11/12 on the same 12×4 twins; **36/36** hits on 36 topics × 4 draws). The original hard last-4 isolated sign is **29/48**. Later protocols are stronger (nested hits 10% FPR **83/96** vs **85/96** on new 36×4 files; in-domain nested-by-stem hits **119/144** vs **134/144**) but must not be sold as a universal detector.

Do not weaken that result into vague wording such as "there may be traces". Equally, do not present it as a universal detector.

## Language and git

- Use English in code, comments, CLI output, documentation, experiment notes, and commits.
- Historical collected outputs stay as collected.
- Author/committer: **Jens Abrahamsson** `<jens.abrahamsson@makeitso.se>`.
- Remote: `origin` → `jensabrahamsson/text-watermark-laboratory`.
- Commit messages should be plain English and state what changed.

## Technical invariants

- Do not edit the `synthid-text` checkout except for installing it with `pip install -e … --no-deps`.
- Do not reimplement `detector_mean`.
- `weighted_mean_score` mutates g-values; pass a fresh array.
- `score` is tied to the public DeepMind instance. It is not a Claude/ChatGPT oracle.
- Do not train a Claude marked/unmarked classifier on the pre-mark corpus alone.
- Do not attempt to infer the keys or SHA-256 IV from a static string; see [research/invertibility.md](research/invertibility.md).
- Keep secrets out of git and argv: `*-KEY.conf`, `.env`, `.browser-profile/`.
- Do not change existing `PROMPTS` strings in `scripts/collect_claude_premark.py`; add new prompts instead.
- Do not download DIPPER for the current workflow; see [research/dipper-local.md](research/dipper-local.md).

## Environment

- CPU JAX, not `jax[cuda]` for the standard setup.
- `transformers==4.57.6`.
- Install SynthID-Text with `--no-deps`.
- When generating with the mixin, use `min_new_tokens=max_new_tokens`.

```bash
source .venv/bin/activate
python -m pytest tests/ -q
```

## Main commands

```bash
python -m text_watermark_tools score FILE.txt
python -m text_watermark_tools pair DIR --out-dir experiments/pair
python -m text_watermark_tools blind experiments/pair --out-dir experiments/blind
python -m text_watermark_tools indicate score FILE.txt --tables experiments/indicator-gpt2
python -m text_watermark_tools indicate fit PAIR --method hashpool --out-dir experiments/hashpool
python -m text_watermark_tools probe PAIR --out-dir experiments/probe
python -m text_watermark_tools probe PAIR --test-dir OTHER --out-dir experiments/transfer
python -m text_watermark_tools scrub experiments/pair --out-dir experiments/scrub
python -m text_watermark_tools iterate FILE.txt --backend qwen --out-dir experiments/iterate
python -m text_watermark_tools resample --skip-collect --new-dir experiments/claude-sample-YYYY-MM-DD
```

## Current benchmark

| Path | Result |
|---|---|
| Official public-key detector | **12/12** |
| Key-free 12 prompts × 4 draws, last-4 | **10/12** |
| Same comparison with margin 0.02 | **11/12** |
| Key-free hits (shared 4-grams only) | **11/12**, AUC **0.737** |
| Key-free hashpool | **11/12**, isolated **35/48** |
| Key-free hashpool, 36 topics | **31/36**, AUC **0.877** |
| Key-free hits, other topics → 12×4 | isolated **39/48**, AUC **0.769** |
| Nested hashpool Youden, 36→12×4 | **33/48** marked / **34/48** unmarked |
| Key-free hits, 24×4 new stems → 12×4 | **12/12** ranking, isolated **42/48**, AUC **0.793** |
| Nested hits Youden, 4-draw train | **26/48** vs **44/48** |
| Nested hits FPR10, 12×4 → 36×4 | **83/96** vs **85/96** |
| Key-free hits, 36 topics × 4 draws LOO | **36/36**, AUC **0.934**; nested-by-stem **119/144** vs **134/144** |
| UTF-8 surface, 12×4 leave-one-out | **10/12**, AUC **0.602** |
| Same-topic GPT-2 hits → Qwen | **11/12** paired (isolated 1/12) |
| New Qwen 12×4 sample, GPT-2 hits | **5/12** (11/12 did not replicate) |
| Qwen 12×4 in-domain hits | **8/12**, AUC **0.602** |
| Key-free hits, 12×4 → 24 new topics | **24/24** ranking, AUC **0.986** |
| Nested freqhits Youden, reverse | **23/24** and **23/24** |
| Single held-out marked file, hard `lr > 0` | **29/48** |
| Argmax snap, official mean on 48 marked files | **0.622 → 0.499** |

See [research/key-free-twins.md](research/key-free-twins.md) and [research/key-free-probe.md](research/key-free-probe.md).

## Code map

| Module | Role |
|---|---|
| `score.py` | DeepMind mean / weighted mean |
| `generate.py` | GPT-2 generation with the mixin |
| `pair.py` | Same-prompt marked/unmarked generation |
| `blind.py` | Key-free leave-one-out comparison |
| `indicator.py` | Frozen count tables and single-file LR |
| `stats.py` | AUC, permutation, binomial, Youden on key-free scores |
| `transfer.py` | Interpolated, gated, hash-pool, and UTF-8 surface scorers |
| `pivot.py` | Unmarked-LM choice geometry and argmax snap |
| `probe.py` | Compare scorers; transfer; nested thresholds; shuffle control; scrub |
| `iterate.py` | Rewrite and re-measure known-marked text |
| `surrogate.py` / `experiment.py` | Older known-mark rewrite workflow |

The mixin's `get_gvals` docstring is inconsistent with the implementation. Trust the code: 12 LCG mixes, then `(hash >> 30) % 2`.

## Claude

Anthropic's announced marking is a future external test case, not something the public DeepMind keys can directly detect.

Keep the distinction clean:

- public DeepMind instance → `score`
- learned key-free statistical signal → `blind` / `indicate` / `probe`
- key-free argmax snap (removal attempt) → `scrub`
- Claude pre-mark corpus → control data for a future before/after experiment

After every Claude resample or measurement, append a dated entry to
[research/LOGBOOK.md](research/LOGBOOK.md). Resample the same `PROMPTS`
often while the voice or mark may be moving. Host schedule: Wednesday,
Friday, Sunday at 04:00 (`scripts/install_claude_resample_schedule.sh`).
Cancel with `uninstall`. Do not use a 7-day Grok interval loop for this.
