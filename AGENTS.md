# AGENTS.md

Instructions for coding agents working in this repository.

Human-facing entry points are [README.md](README.md) and [HOW-TO.md](HOW-TO.md).

## Project purpose

This repository studies statistical text watermarking using Google DeepMind's public SynthID-Text reference implementation.

It has two distinct detection paths:

1. **`score`** — the ordinary key-based reference measurement for `public-deepmind-30`.
2. **`indicate` / `blind`** — a key-free experimental indicator learned from matched marked/unmarked generations.

The key-free work is a central result of the repository. Describe it accurately: **we have built an indicator for watermark presence without the detector keys**. After correcting truncated-context overcount, hard last-4 ranks held-out prompt groups **9/12** times, or **10/12** with a 0.02 comparison margin. Isolated hard sign is **25/48**. In-domain hits on 36 topics × 4 draws is still **36/36**. Frozen lock A on 100 new GPT-2 families is **99/100**; that does not replace **25/48**. Distil Phase B is official **70/100**, lock B **89/100**, lock C **69/100**. In-family nested-by-stem Youden on 100×4 lock A is **322/400 vs 338/400**; lock B **392/400 vs 382/400** (occupancy). Out-of-family isolated transfer is [research/PROTOCOL-isolated.md](research/PROTOCOL-isolated.md). Qwen Phase B is still generating. The pre-fix published numbers **10/12** / **29/48** overweighted openings (`(10,)→20` counted four times at `context_len=4`). Later protocols must not be sold as a universal detector. Do not sell hashed or opening-rankpath signs as replacing **25/48**. Do not add new `probe --methods` names on the 12×4 / 36×4 twins except bug-fix remeasures. Phase B of [research/PROTOCOL-next.md](research/PROTOCOL-next.md) is Distil/Qwen on the same 100 prompts. Headlines vs ablations: [research/results-ledger.md](research/results-ledger.md).

Do not weaken that result into vague wording such as "there may be traces". Equally, do not present it as a universal detector.

## Language and git

- Use English in code, comments, CLI output, documentation, experiment notes, and commits.
- Citations in research notes follow author–year ([research/CITING.md](research/CITING.md)); do not invent papers.
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
python -m text_watermark_tools probe PAIR --prefix-lens 16,32,64,96,128 --windows 0:16,16:32,32:64,64:128
python -m text_watermark_tools probe PAIR --fit-prefix 16 --methods hits,hashpool
python -m text_watermark_tools probe PAIR --methods hits,poshits,pospool --pos-bucket 16
python -m text_watermark_tools probe PAIR --coverage --windows 0:16,16:32,32:64,64:128
python -m text_watermark_tools probe PAIR --fit-prefix 4 --methods hits,poshits --pos-bucket 1
python -m text_watermark_tools probe PAIR --test-dir OTHER --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits,postokbackoff,postokbackoff2
python -m text_watermark_tools probe PAIR --fit-prefix 4 --pos-bucket 1 --methods postokbackoff --skip-hashpool --pivot --rankpath --cascade postokbackoff --cascade-fallback rankuni
python -m text_watermark_tools openings TRAIN --test-dir TEST --extra-train OTHER --fit-prefix 4 --pos-bucket 1
python -m text_watermark_tools probe PAIR --fit-prefix 4 --methods first,poshits --pos-bucket 1 --include-first
python -m text_watermark_tools probe PAIR --fit-prefix 4 --methods hits,poshits --pos-bucket 1 --prompt-context
python -m text_watermark_tools pair DIR --model distilgpt2 --n-samples 4 --out-dir experiments/pair-distil
python -m text_watermark_tools learn PAIR --fit-prefix 4 --pos-bucket 1 --out-dir experiments/learn
python -m text_watermark_tools learn PAIR --test-dir OTHER --fit-prefix 4 --pos-bucket 1 --out-dir experiments/learn-xfer
python -m text_watermark_tools pair DIR --control-only --n-samples 4 --out-dir experiments/pair-control
python -m text_watermark_tools contrast TRAIN --test-dir TEST --control-dir CONTROL --fit-prefix 4 --pos-bucket 1 --out-dir experiments/contrast
python -m text_watermark_tools contrast TRAIN --test-dir TEST --control-dir CONTROL --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits
python -m text_watermark_tools contrast TRAIN --test-dir TEST --control-dir CONTROL --fit-prefix 5 --pos-bucket 0 --methods rankpath,rankuni
python -m text_watermark_tools probe PAIR --test-dir OTHER --fit-prefix 4 --pos-bucket 1 --methods postokbackoff --skip-hashpool --cascade postokbackoff --cascade-fallback rankpath --cascade-rankpath-end 4 --rankpath-pos-bucket 0 --cascade-when positive
python -m text_watermark_tools probe PAIR --fit-prefix 16 --methods poshits,poshitmass --pos-bucket 4
python -m text_watermark_tools scrub experiments/pair --out-dir experiments/scrub
python -m text_watermark_tools iterate FILE.txt --backend qwen --out-dir experiments/iterate
python -m text_watermark_tools resample --skip-collect --new-dir experiments/claude-sample-YYYY-MM-DD
```

## Current benchmark

| Path | Result |
|---|---|
| Official public-key detector | **12/12** |
| Key-free 12 prompts × 4 draws, last-4 (recount) | **9/12** |
| Same comparison with margin 0.02 | **10/12** |
| Confirmatory 100×4 lock A interpolate last-4 | **99/100** (official keyed first-draw **100/100**) |
| DistilGPT2 100×4 official / lock B / lock C | **70/100** / **89/100** / **69/100** (H3: rankpath drops more) |
| 100×4 lock A nested-by-stem Youden | **322/400 vs 338/400** (in-family; not **25/48**) |
| 100×4 lock B nested-by-stem Youden | **392/400 vs 382/400** (occupancy 198/400 unmarked `n_used=0`) |
| Key-free hits (shared 4-grams only, recount) | **10/12**, AUC **0.718** |
| Key-free hashpool | **11/12**, isolated **35/48** |
| Key-free hashpool, 36 topics | **31/36**, AUC **0.877** |
| Key-free hits, other topics → 12×4 | isolated **39/48**, AUC **0.769** |
| Nested hashpool Youden, 36→12×4 | **33/48** marked / **34/48** unmarked |
| Key-free hits, 24×4 new stems → 12×4 | **12/12** ranking, isolated **42/48**, AUC **0.793** |
| Nested hits Youden, 4-draw train | **26/48** vs **44/48** |
| Nested hits FPR10, 12×4 → 36×4 | **83/96** vs **85/96** |
| Key-free hits, 36 topics × 4 draws LOO (recount) | **36/36**, AUC **0.930** |
| Key-free hits, first 16 tokens, 36×4 | **34/36**, AUC **0.916** |
| Key-free hits, matched 16-token fit, 36×4 | **34/36**, AUC **0.929**; unmarked ≤0 **112/144** |
| Key-free poshits (bucket=16), 36×4 | **34/36**, AUC **0.925**; t=0 spec **97/144** |
| Key-free hits, tokens 16–32 only, 36×4 | **22/36**, AUC **0.549** |
| Key-free hits, matched 16-token 24×4 → 12×4 | **11/12**, AUC **0.818**; nested-by-stem 39/48 vs 36/48 |
| Key-free poshits, 24×4 → 12×4 | **10/12**, AUC **0.811**; nested-by-stem 37/48 vs 35/48 |
| Key-free poshits, matched 16-token bucket 4, 36×4 | **34/36**, AUC **0.937**; unmarked ≤0 **114/144** |
| Key-free hits, tokens 0:4 only, 36×4 | **34/36**, AUC **0.917** (matches 0:16) |
| Key-free poshits, matched 4-token bucket 1 | **34/36**, AUC **0.935**; t=0 **131/144 vs 132/144** |
| Same reader, 24×4 → 12×4 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| Key-free postokhits on that OOD gate | **12/12**, isolated **16/48**, decided precision **1.000** (The-Laplace TPs become zeros) |
| Same postokhits, 36×4 LOO | 34/36, AUC 0.912; t=0 **122/144 vs 132/144** (9 of 131 poshits TPs were occupancy) |
| Key-free postokhits, 12 medium scenes → 12×4 | **12/12**, isolated **19/48**, decided precision **1.000** |
| Same plus 24 short one-liners | **12/12**, isolated **20/48**, decided precision **1.000** |
| Key-free postokbackoff, 12 medium scenes → 12×4 | **12/12**, isolated **21/48**, decided precision **1.000** (harbour last-1 `' was' → ' in'`) |
| Key-free postokbackoff plus 24 short one-liners | **12/12**, isolated **22/48**, decided precision **1.000** |
| Key-free postokhits, tail-matched → 12×4 | **12/12**, isolated **30/48**, decided precision **1.000** |
| Key-free postokbackoff, short+medium+tails → 12×4 | **12/12**, isolated **36/48**, AUC **0.888**, decided precision **1.000** |
| Key-free postokbackoff2 on that combined train | **13/48** last-2+ core (same on 24 short stems) |
| Opening-overlap bound, same twins | Isolated recall = train atom overlap; two short stems cover 13/48 |
| Unbucketed tokbackoff on that combined train | **36/48** marked, **3** unmarked FP |
| `--include-first` postokhits on that combined train | **43/48** marked, **10** unmarked FP (first-token unigram) |
| Neighborhood paraphrases, 12 scenes × 4 | Official **12/12**; no Closing/Now/While/The ferry openings |
| Same plus short+medium+tails → 12×4 | postokbackoff **42/48** covered, last-2+ **15/48**, precision **1.000** |
| That 42/48 covered, isolated `lr>0` | **34/48** (eight covered files have negative observed-token LR) |
| Opening pivot-lda, 12×4 LOO, 4 generated tokens | **10/12**, AUC **0.672**, isolated **27/48** (full-file pivot-lda was 17/48) |
| Same geometry with prompt context | 7/12, AUC 0.468 (worse than chance; not an isolated-file protocol) |
| Opening pivot-lda, 24-short → 12×4 | 4/12, AUC 0.422 (does not transfer) |
| poshits on those medium-seed tables | 8/12; The-Laplace δ flips to ≈ −0.365 |
| Key-free last-k coverage, 36×4 LOO | 0:16 **13.7%** (i=1–2); full last-4 from i=4 ~4% |
| Key-free poshitmass, matched 16-token bucket 4 | **34/36**, AUC **0.943**; unmarked ≤0 **114/144** |
| Key-free poshits, matched 16-token bucket 1, 36×4 | **34/36**, AUC **0.938**; t=0 **132/144 vs 132/144** |
| Same 16-token reader, 24×4 → 12×4 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| Key-free last-1, matched 4-token 24×4 → 12×4 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| `--include-first` on that 4-token OOD gate | 9/12, AUC 0.719 (hurts) |
| Qwen 12×4 first-token opening | **12/12**, AUC **0.901** (hits without token 0: 7/12) |
| Qwen native opening rankpath | **8/12**, AUC **0.590** (not first-token 12/12) |
| Qwen native prefix-4 rankpath | **9/12**, AUC **0.662**, isolated 25/48 |
| DistilGPT2 12×4 official / in-domain hits | **12/12** / **9/12**, AUC 0.705 |
| Distil native opening rankpath | **8/12**, AUC **0.579** (chance; official 12/12) |
| GPT-2 36×4 → DistilGPT2 (same BPE) | hits **5/12**, AUC **0.462** |
| GPT-2 36×4 rankpath → Distil (GPT-2 LM) | **9/12**, AUC 0.636, isolated **21/48** |
| Key-free tokmlp, 4-token 24×4 → 12×4 | 8/12, AUC 0.714 (does not beat poshits **0.873**) |
| Key-free hashlog on that OOD gate | 7/12, AUC 0.606 |
| GPT-2 learned scorers → Distil / Qwen | chance |
| Key-free poshits, 4-token 24×4 → 12×4, control-shuffled-30 | **0/48** control `lr>0`; public vs control **12/12**, AUC **0.906** |
| Key-free postokhits on that control pile | **0/48** control `lr>0`; public vs control **12/12**, AUC 0.667 |
| Key-free postokbackoff on that control pile | **0/48** control `lr>0`; public vs control **12/12**, AUC 0.667 |
| Official lamp on those 48 control files | public **0.501**; matching control keys **0.624** |
| Mixin last-5 vs last-4, 36×4 hits | **35/36**, AUC **0.912** (does not beat last-4) |
| UTF-8 surface, 12×4 leave-one-out | **10/12**, AUC **0.602** |
| Same-topic GPT-2 hits → Qwen | **11/12** paired (isolated 1/12) |
| New Qwen 12×4 sample, GPT-2 hits | **5/12** (11/12 did not replicate) |
| Qwen 12×4 in-domain hits | **8/12**, AUC **0.602** |
| New topics GPT-2 36×4 → new Qwen | chance (hits **6/12**, AUC 0.445) |
| Key-free hits, 12×4 → 24 new topics | **24/24** ranking, AUC **0.986** |
| Nested freqhits Youden, reverse | **23/24** and **23/24** |
| Single held-out marked file, hard `lr > 0` (recount) | **25/48** |
| Opening rankpath, 12×4 LOO 4-token (recount) | **11/12**, isolated **41/48** |
| Opening occupancy-free hashtok, 12×4 LOO `--fit-prefix 4` | **12/12**, isolated **24/48 vs 47/48** (tokhits **23/48**; extra TP letter d3; nested **23/48 vs 47/48**); marked recall below recounted hard **25/48**; not rankpath 41/48 |
| In-domain full-file hashtok, 12×4 LOO last-4 | **9/12**, isolated **33/48 vs 22/48**, nested **22/48 vs 30/48** |
| In-domain hashtok2 (min_count=2) | **8/12**, **34/48 vs 21/48**, nested **19/48 vs 35/48** (sign reshuffle, not a singleton core) |
| Prefix-5 OOD hashtok / hashtoklen / hashtoklen2 | hashtok **30/48** equals postokhits; hashtoklen **21/48**; hashtoklen2 **10/48 vs 48/48** |
| OR indicate × hashtok | **39/48 vs 12/48**, combined **51/96** (worse than indicate 52/96); do not sell 39/48 |
| Opening rankpath, 24-short → 12×4 | **10/12**, isolated **28/48** |
| Unbucketed full-file rankpath, 12×4 LOO | **8/12**, AUC 0.559 (front-loaded; 16:32 chance) |
| Unbucketed prefix-4 rankpath, 24-short → 12×4 | **11/12**, isolated **25/48 vs 43/48** |
| 60-stem prefix-4 rankpath standalone → 12×4 | **10/12**, **28/48 vs 40/48** (same 68/96 as 24-short) |
| Prefix-4 rankpath vs control-shuffled-30 | control AUC **0.511**, isolated **6/48** (not poshits 0/48) |
| 60-stem count + prefix-4 rankpath leftover | **1/6** leftover; cascade **35/48 vs 43/48** |
| Same rows, `--cascade-when positive` | **40/48 vs 40/48** (8 rankpath FPs; not 39/48) |
| Argmax snap, official mean on 48 marked files | **0.622 → 0.499** |

See [research/key-free-twins.md](research/key-free-twins.md), [research/key-free-probe.md](research/key-free-probe.md), [research/key-free-learn.md](research/key-free-learn.md), [research/key-free-contrast.md](research/key-free-contrast.md), [research/key-free-tokhits.md](research/key-free-tokhits.md), [research/key-free-hashtok.md](research/key-free-hashtok.md), [research/key-free-cascade.md](research/key-free-cascade.md), [research/key-free-rankpath.md](research/key-free-rankpath.md), [research/key-free-snaprate.md](research/key-free-snaprate.md), [research/related-work.md](research/related-work.md), [research/CITING.md](research/CITING.md), and [research/annotated-bibliography.md](research/annotated-bibliography.md).

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
| `pivot.py` | Unmarked-LM choice geometry, entropy pooling, argmax snap, table-free snap-rate |
| `rankpath.py` | Five-symbol unmarked-LM rank tables (no token identity) |
| `probe.py` | Compare scorers; transfer; cascade; nested thresholds; scrub |
| `learn.py` | Key-free hashed logistic / token MLP / char CNN on the same twins |
| `contrast.py` | Key-free public vs control-shuffled-30 instance check |
| `atoms.py` | Decode hits atoms (The-Laplace occupancy vs observed tokens) |
| `openings.py` | Opening-overlap bound: isolated recall vs train atom coverage |
| `iterate.py` | Rewrite and re-measure known-marked text |
| `surrogate.py` / `experiment.py` | Older known-mark rewrite workflow |

The mixin's `get_gvals` docstring is inconsistent with the implementation. Trust the code: 12 LCG mixes, then `(hash >> 30) % 2`.

## Claude

Anthropic's announced marking is a future external test case, not something the public DeepMind keys can directly detect.

Keep the distinction clean:

- public DeepMind instance → `score`
- learned key-free statistical signal → `blind` / `indicate` / `probe`
- key-free instance contrast (public vs control-shuffled-30) → `contrast`
- key-free argmax snap (removal attempt) → `scrub`
- Claude pre-mark corpus → control data for a future before/after experiment

After every Claude resample or measurement, append a dated entry to
[research/LOGBOOK.md](research/LOGBOOK.md). Resample the same `PROMPTS`
often while the voice or mark may be moving. Host schedule: Wednesday,
Friday, Sunday at 04:00 (`scripts/install_claude_resample_schedule.sh`).
Cancel with `uninstall`. Do not use a 7-day Grok interval loop for this.
