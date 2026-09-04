# Confirmatory protocol (longer watermark history on Qwen2-1.5B, 100 families)

This is a **methods freeze** for a 100-family generator-transfer of the
already opened Qwen2-1.5B $\Hw=12$ 12-LOO lock
([PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md)).
It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. Qwen original-12 interpolate **4/12** /
isolated **41/96** and DistilGPT2 100-family interpolate **88/100** /
**557/800** stay in those dumps. This file asks whether the same
public keys and $\Hw=12$ still rank prompt groups on
Qwen2-1.5B-Instruct when the prompt frame is the 100 one-liners.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with the public `ngram_len=5` processor.
Do **not** apply a chat template after peeking.

## Why freeze now

Sol (2026-09-03) asked for a preregistered longer-context two-grain
replication. GPT-2 $\Hw=12$ 100-family interpolate is **76/100**. Distil
$\Hw=12$ 100-family interpolate is **88/100**. Qwen $\Hw=12$ 12-LOO
interpolate is **4/12**. The remaining generator-scale check that is
not leftover targeting is the same `ngram_len=13` on Qwen2-1.5B with
the 100 one-liners. Kirchenbauer and Aaronson Qwen 100-family runs are
different mixins and are **not** this file.

## Primary scientific question

On Qwen2-1.5B-Instruct with public keys and `ngram_len=13` ($\Hw=12$),
under leave-one-family-out interpolate last-4 and hard last-4 on 100
one-liners, do marked prompt-group means still outrank unmarked means?

Not: can Qwen 12-LOO $\Hw=12$ tables classify the 100 files. Not:
leftover targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `Qwen/Qwen2-1.5B-Instruct` (pin Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`) |
| Mixin keys | public-deepmind-30 (default) |
| `ngram_len` | **13** (same $\Hw=12$ as PROTOCOL-next-longctx) |
| Prompts | `experiments/2026-09-01-prompts-100/` (plain strings; no chat template) |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260903** |
| Pair out-dir | `experiments/2026-09-04-pair-qwen-100x4-ngram13/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-qwen-100x4-ngram13-hard-last4/` |
| Fold | leave-one-family-out |
| Official control | matching `ngram_len=13` `detector_mean` |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

`pair --ngram-len 13` must generate **and** official-score with the
same `ngram_len`. Scoring Qwen $\Hw=12$ twins with `ngram_len=5` is a
harness bug. Probe and `atoms` must pass `--model
Qwen/Qwen2-1.5B-Instruct`; the default GPT-2 tokenizer is a harness
bug on these twins.

## Hypotheses (stated before generation)

- **H-long-q100-ctrl.** Official matching mean with `ngram_len=13` is
  above $0.55$ on every first marked file. Unmarked first-draw stays
  near $1/2$. If marked first-draws fail, stop; harness bug.
- **H-long-q100-group.** Interpolate last-4 100-LOO ranking is reported
  beside GPT-2 $\Hw=12$ **76/100** and Distil $\Hw=12$ **88/100**.
  Either drop or hold is informative. It does not replace **25/48**.
- **H-long-q100-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-long-q100-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260903 --ngram-len 13 \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-100x4-ngram13
```

Do not look at key-free LRs until `pair` has written official
first-draw scores and the probe command has been run once, as written.
Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-100x4-ngram13 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-qwen-100x4-ngram13-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --model Qwen/Qwen2-1.5B-Instruct \
  --test-dir experiments/2026-09-04-pair-qwen-100x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-qwen-100x4-ngram13
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / Aaronson generator in this file.
- New `probe --methods` names.
- Scoring Qwen $\Hw=12$ twins with `ngram_len=5`.
- Scoring Qwen twins with the default GPT-2 tokenizer.
- Adding a chat template after peeking.
- Leftover targeting.
- Selling any Qwen $\Hw=12$ 100-family count as replacing **25/48**.
- Paid chat APIs (`iterate --backend qwen` included).
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.
