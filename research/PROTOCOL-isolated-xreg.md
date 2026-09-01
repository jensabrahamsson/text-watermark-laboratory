# Isolated-file protocol (100 one-liners → Grok-register 12)

This is a **methods freeze** for the reverse cross-register split.
It does not add a scorer. It asks whether the original 12×4 files are
a uniquely hard isolated-file test set, or whether out-of-family
isolated classification also fails on Grok-length held-out files.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
after the truncated-context recount remain **9/12**, **25/48**, and
**36/36**. Pre-fix **10/12** / **29/48** stay in historical JSON.
One-liner confirmatory ranking is [PROTOCOL-next.md](PROTOCOL-next.md):
lock A **99/100**. One-liner → original 12 is
[PROTOCOL-isolated.md](PROTOCOL-isolated.md): lock A nested Youden
**23/48 vs 38/48**. Grok-length train → original 12 is
[PROTOCOL-isolated-register.md](PROTOCOL-isolated-register.md): lock A
nested **16/48 vs 41/48**. None of those replace **25/48**. That is not
this file.

Do **not** write `thesis/` from this file. Do **not** look at key-free
test LRs until the git SHA of this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis commands below have been run
once, as written.

## Why freeze now

The missing cell in the cross-register square is **100 one-liner
tables → Grok-length test files**. Already opened:

| Train | Test | Lock A nested Youden |
|---|---|---|
| 100 one-liners | original 12×4 | **23/48 vs 38/48** |
| 100 one-liners | 36×4 one-liners | **109/144 vs 122/144** |
| Grok-register 12 | original 12×4 | **16/48 vs 41/48** |
| Grok-register 12 | 36×4 one-liners | **50/144 vs 115/144** |
| Grok-register 12 | Grok-register 12 (in-family) | nested-by-stem **24/48 vs 40/48** |

The 100-family tables have never scored `experiments/2026-09-01-pair-grok12x4/`.
In-family interpolate on those 12 stems, and Grok-train → original 12,
are already open. Those fits are not this transfer.

If 100→grok12 nested Youden is strong, the original 12 are a special
hard evaluation set. If it is also near chance, out-of-family isolated
fails on Grok-length test files too. Either way this does not replace
**25/48** (those are different files).

No new generation. Both pair directories already exist.

## Primary scientific question

Do frozen key-free tables, trained on the 100 GPT-2 one-liner families,
classify the 12 Grok-length × 4-draw files without detector keys,
`hash_iv`, or g-values?

Not: can another `probe --methods` name lift **25/48** on the original
12. Not: does pooling the 100 one-liners with the 12 Grok stems after
seeing both LRs help (that mix is refused).

## Frozen scorers

Same three readers as [PROTOCOL-isolated.md](PROTOCOL-isolated.md).
Exact CLI. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| A | Hard last-4 interpolate | `--methods interpolate --context-len 4` |
| B | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| C | Opening rankpath | `--methods rankpath --fit-prefix 4 --pos-bucket 1` |

Lock C here is **only** rankpath (not `--rankpath`, which also emits
default count methods). Rankpath needs the unmarked LM.

Secondary occupancy-free readout of the **same** lock B tables uses
`--methods postokhits` with those flags. Opening-overlap uses `openings`
with postokhits, `--skip-stem-curve`.

Official `score` on the Grok twins is already **12/12**. It is not a
key-free endpoint.

## Hypotheses (stated before these transfer runs)

- **H-xreg-A.** Lock A nested Youden on grok12×4, trained on the 100
  one-liners, is higher than Grok-train → original 12 lock A **16/48**.
  More train mass, different test register.
- **H-xreg-hard.** If lock A nested marked recall on grok12×4 is at or
  below in-family nested-by-stem **24/48**, the original 12 are not
  uniquely cursed: out-of-family isolated fails on Grok-length files
  too.
- **H-xreg-iso.** This split does not replace **25/48**. Do not sell a
  grok12 nested Youden as the original-12 isolated headline.
- **H-xreg-B.** Occupancy-free lock B (postokhits t=0) still tracks
  opening-atom overlap on these 48 files, not a denser isolated
  detector.

Report `ranking_without_isolated_tp` and
`ranking_losses_with_isolated_tp`. Prompt ranking is not isolated
recall. Do not sell a union of locks A/B/C.

## Primary endpoint

**Isolated nested Youden** on the grok12×4 test files: marked files
above the train-LOO Youden threshold, unmarked files at or below it.

Report prompt-group ranking, file AUC, t=0 sign, ranking-versus-isolated
honesty, occupancy-free lock B, and opening-overlap as secondary. Do
**not** promote t=0 `lr>0` to the primary endpoint. Do **not** replace
**25/48**.

## Corpus

| Item | Value |
|---|---|
| Train | `experiments/2026-09-01-pair-100x4/` (PROTOCOL-next Phase A) |
| Test | `experiments/2026-09-01-pair-grok12x4/` (PROTOCOL-isolated-register) |
| Generator | GPT-2 + public DeepMind 30 mixin (both dirs) |

No test prompt entered the 100-family fit. Stem names do not overlap
(`001`…`100` vs `101-service-station`…`112-taxi-rank`). Overlap mode
stays `drop-from-train` (default).

## Analysis commands

Train is always `experiments/2026-09-01-pair-100x4`. Test is always
`experiments/2026-09-01-pair-grok12x4`. Do not change flags after the
first run. Do not look at key-free test LRs until each command has been
run once, as written.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-last4

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-grok12x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-grok12x4-opening-rankpath

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods postokhits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-grok12x4-occupancy-free

python -m text_watermark_tools openings experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-100x4-to-grok12x4
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4, 36×4, or
  grok12×4.
- Mixing the 100 one-liners with the 12 Grok stems as one train after
  seeing both directions.
- Selling a grok12 nested Youden as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs. Local Hugging Face GPT-2 only for rankpath.
- Writing `thesis/`.
- New `pair` generation.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name that SHA in [LOGBOOK.md](LOGBOOK.md) before looking at test LRs.
3. Run the analysis commands above, then append a dated logbook entry
   with the SHA and the nested Youden counts.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a fourth scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.
