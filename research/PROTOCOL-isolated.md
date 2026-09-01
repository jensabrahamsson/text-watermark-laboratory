# Isolated-file protocol (100-family tables → old twins)

This is a **methods freeze** for single-file classification. It does not
add a scorer. It asks whether the already-frozen PROTOCOL-next readers,
fit on the 100 new GPT-2 families, classify finished strings whose
prompts never entered the fit.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
after the truncated-context recount remain **9/12**, **25/48**, and
**36/36**. Pre-fix **10/12** / **29/48** stay in historical JSON.
Confirmatory prompt-grain is [PROTOCOL-next.md](PROTOCOL-next.md): lock
A **99/100**. That is not this file.

Do **not** write `thesis/` from this file.

## Why freeze now

PROTOCOL-next answered prompt-group ranking on new families. Isolated
`lr>0` at threshold 0 is the weak claim: original hard last-4 is
**25/48**. On the 100×4 GPT-2 twins, lock A file ranking is already
strong (AUC **0.898**), and nested-by-stem Youden is **322/400 vs
338/400**. Lock B nested-by-stem Youden is **392/400 vs 382/400**.
Those operating points are still **in-family leave-one-prompt-out**.
They do not replace **25/48**. Nested-by-stem is a threshold nest on
already-OOF scores (other stems' models still trained on H).

The missing measurement is out-of-family: fit on the 100 new prompts,
score the original 12×4 and 36×4 files. No test prompt enters the fit.
The nested Youden / 10% FPR rows from `probe --test-dir` choose the
threshold on **training** leave-one-out scores only.

## Primary scientific question

Do frozen key-free tables, trained on 100 new GPT-2 scene families,
classify held-out finished strings from a disjoint prompt pool without
detector keys, `hash_iv`, or g-values?

Not: can another `probe --methods` name lift **25/48** on the old
12×4 twins.

## Frozen scorers

Same three readers as PROTOCOL-next. Exact CLI. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| A | Hard last-4 interpolate | `--methods interpolate --context-len 4` |
| B | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| C | Opening rankpath | `--methods rankpath --fit-prefix 4 --pos-bucket 1` |

Lock C here is **only** rankpath (not `--rankpath`, which also emits
default count methods). Rankpath needs the unmarked LM; do not start
lock C while a large native-generator `pair` is holding RAM.

Official `score` is a positive control on those twins already. It is
not a key-free endpoint.

## Hypotheses (stated before these transfer runs)

- **H-iso-A.** Lock A tables from the 100 families rank the original 12
  prompt groups above chance (prompt wins > 6/12). The primary
  isolated-file endpoint is nested Youden on the 48 marked / 48
  unmarked test files (threshold from train LOO only).
- **H-iso-B.** Lock B prompt ranking on that split is at least as high
  as lock A, because the mark is front-loaded (PROTOCOL-next H2).
  Isolated nested Youden is reported with occupancy (`n_used=0`). Do
  not treat Laplace-on-unseen TPs as observed-token TPs.
- **H-iso-C.** Lock C (rankpath) is more domain-specific than lock B.
  Deferred until the Qwen Phase B pair releases RAM.
- **H-iso-36.** The same lock A/B commands, test directory 36×4
  (prompt strings disjoint from the 100; stem names `01-harbour` /
  `13`… do not collide with `001`…`100`).

## Primary endpoint

**Isolated nested Youden** on the test files: marked files above the
train-LOO Youden threshold, unmarked files at or below it.

Report prompt-group ranking, file AUC, t=0 sign, and nested 10% FPR as
secondary. Do **not** promote t=0 `lr>0` to the primary endpoint. Do
**not** replace **25/48**.

## Analysis commands

Train is always `experiments/2026-09-01-pair-100x4`. Do not change
flags after the first run. Do not look at key-free test LRs until each
command has been run once, as written.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-12x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-36x4-hard-last4

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-36x4-opening-poshits
```

Lock C (after Qwen pair is no longer resident):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-12x4-opening-rankpath

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-36x4-opening-rankpath
```

`used_keys=false`. Overlap mode stays `drop-from-train` (default).
Stem names do not overlap, so training keeps all 100 families.

## In-family numbers this protocol does not promote

Already measured on 100×4 GPT-2 LOO. Keep them here so transfer is
compared against the right in-family baseline, not against t=0.

| Lock | Prompt wins | File AUC | t=0 | Nested-by-stem Youden |
|---|---|---|---|---|
| A interpolate last-4 | 99/100 | 0.898 | 352/400 vs 290/400 | **322/400 vs 338/400** |
| B opening poshits | 100/100 | 0.980 | 393/400 vs 344/400 | **392/400 vs 382/400** |
| C opening rankpath | 96/100 | 0.822 | 314/400 vs 302/400 | **312/400 vs 319/400** |

Lock B occupancy: 198/400 unmarked files have `n_used=0` on that
opening reader. Distil lock B isolated t=0 is **216/400 vs 247/400**;
that is not a Distil isolated-file detector.

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4 or 36×4.
- Fishing `--n-hashes`, mixer `seed`, or `--context-len` after looking
  at the transfer LRs.
- Selling in-family 322/400, 392/400, 352/400, or 393/400 as replacing
  **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Training a Claude marked/unmarked classifier on the pre-mark corpus.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Run the lock A/B commands above, then append a dated
   [LOGBOOK.md](LOGBOOK.md) entry with the SHA.
3. Run lock C after the Qwen Phase B pair is no longer resident.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a fourth scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Outcome (2026-09-01)

Protocol SHA `eb00f92`. Frozen lock A/B commands above were run once,
flags unchanged. `used_keys=false`. Overlap dropped 0 stems. Lock C
not opened (Qwen pair still resident).

| Test | Lock | Prompt wins | File AUC | t=0 | Nested Youden (primary) |
|---|---|---|---|---|---|
| 12×4 | A interpolate | **8/12** | 0.663 | 27/48 vs 33/48 | **23/48 vs 38/48** |
| 12×4 | B opening poshits | **11/12** | 0.844 | 37/48 vs 42/48 | **36/48 vs 42/48** |
| 36×4 | A interpolate | **36/36** | 0.858 | 117/144 vs 102/144 | **109/144 vs 122/144** |
| 36×4 | B opening poshits | **35/36** | 0.955 | 134/144 vs 127/144 | **134/144 vs 129/144** |

H-iso-A holds only as prompt ranking above chance (8/12; binomial
P(≥8) ≈ 0.19). Isolated nested Youden **23/48** does **not** beat
recounted hard **25/48**. More one-line train families do not calibrate
the original 12 Grok-prompt files.

Lock A prompt losses are **harbour, night-bus, library, ferry-queue**
(not the 12-LOO misses station/office/ferry-queue). Ferry-queue is the
stable miss: 0/4 marked files above 0. Lock B's only prompt loss is
**letter**. Stem table:
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/stems.json`.

H-iso-B holds on the original 12: poshits ranks **11/12** ≥ interpolate
**8/12**. Nested Youden **36/48 vs 42/48** has occupancy (9 marked /
33 unmarked `n_used=0`). Occupancy-free readout of those same frozen
tables (`occupancy-free.json`): postokhits t=0 **16/48 vs 48/48**.
**21** of the poshits marked TPs were Laplace-on-unseen (`The`→` ferry`
and kin). Do not sell 36/48 as observed-token isolated recall.

H-iso-36: lock A ranks **36/36** on the 36-topic pool (same one-line
register as the 100). Nested Youden **109/144 vs 122/144** is the
honest out-of-family isolated operating point for interpolate. It does
not replace **25/48**. Lock B **35/36** is slightly below lock A on that
split. Occupancy-free postokhits on those same tables is **114/144 vs
139/144**; 20 occupancy marked TPs. Shared observed openings
(`"This is the"`) are register overlap, not a universal detector.

JSON: `experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-opening-poshits/`.

