# Isolated-file protocol (Grok-register train → original 12)

This is a **methods freeze** for a register-matched isolated-file test.
It does not add a scorer. It asks whether isolated transfer of the
already-frozen PROTOCOL-next readers failed on the original 12 because
the 100-family train was one-liners, not because isolated classification
is weak in the same prose register as those 12 files.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
after the truncated-context recount remain **9/12**, **25/48**, and
**36/36**. Pre-fix **10/12** / **29/48** stay in historical JSON.
One-liner confirmatory ranking is [PROTOCOL-next.md](PROTOCOL-next.md):
lock A **99/100**. One-liner → old twins is
[PROTOCOL-isolated.md](PROTOCOL-isolated.md): lock A nested Youden
**23/48 vs 38/48**; occupancy-free lock B **16/48**; lock C **24/48 vs
41/48**. None of those replace **25/48**. That is not this file.

Do **not** write `thesis/` from this file. Do **not** run `pair` until
the prompt directory is on the remote SHA named in
[LOGBOOK.md](LOGBOOK.md).

## Why freeze now

PROTOCOL-isolated trained on 100 one-line families (same register as
seeds 13–36) and scored the original 12×4 files. Nested Youden did not
beat **25/48**. Observed-token recall equalled opening-atom overlap
(**18/48** covered). In-register one-liner transfer (100 → 36×4) ranked
**36/36** with nested **109/144 vs 122/144**. That split does not test
the Grok prose register.

The original 12 are mixed length: harbour / night-bus / library are
~220-word scenes; market through ferry-queue are ~40-word scenes. The
100 families are ~10–15 words. Lock A losses on 100→12 were harbour,
night-bus, library, ferry-queue — three of the four are the long
scenes. Medium ~40-word train already exists
(`experiments/2026-08-31-pair-long12x4/`) and was used for tokhits
discovery; it is not this confirmatory freeze.

The missing measurement is out-of-family, **register-matched**: fit on
new ~220–330 word English scene prompts, score the original 12×4. No
test prompt enters the fit. Nested Youden / 10% FPR choose the
threshold on **training** leave-one-out scores only.

## Primary scientific question

Do frozen key-free tables, trained on new GPT-2 twins from Grok-length
scene prompts disjoint from the original 12 and from the 100 one-liners,
classify those original 12×4 files without detector keys, `hash_iv`, or
g-values?

Not: can another `probe --methods` name lift **25/48**. Not: does
in-family ranking on the new 12 families work (that is a check, not the
isolated claim).

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

Official `score` on the new twins is a positive control (the mixin is
on). It is not a key-free endpoint.

Secondary occupancy-free readout of the **same** lock B tables uses
`--methods postokhits` with those flags. That name already exists. Do
not add a fourth scorer. Opening-overlap uses `openings` with
postokhits, `--skip-stem-curve`.

## Hypotheses (stated before generation)

- **H-reg-A.** Lock A nested Youden on the original 12×4, trained on
  these Grok-length families, is higher than one-liner lock A **23/48**.
  Register mismatch was a confound. This still does not have to beat
  **25/48**.
- **H-reg-iso.** Even with register-matched train, nested Youden does
  not beat **25/48**. Isolated classification on these 12 files remains
  weak.
- **H-reg-B.** Occupancy-free lock B (postokhits t=0 / nested Youden)
  still tracks opening-atom overlap, not a denser isolated detector.
- **H-reg-C.** Lock C (rankpath) remains more domain-specific than lock
  B, as in PROTOCOL-isolated H-iso-C.

Report `ranking_without_isolated_tp` and
`ranking_losses_with_isolated_tp`. Prompt ranking is not isolated
recall. Do not sell a union with the 100-family locks.

## Primary endpoint

**Isolated nested Youden** on the original 12×4 test files: marked files
above the train-LOO Youden threshold, unmarked files at or below it.

Report prompt-group ranking, file AUC, t=0 sign, ranking-versus-isolated
honesty, occupancy-free lock B, and opening-overlap as secondary. Do
**not** promote t=0 `lr>0` to the primary endpoint. Do **not** replace
**25/48**.

In-family leave-one-prompt-out on the new 12 families is a register
check (prompt ranking and nested-by-stem). It is not **25/48**.

## Corpus

Twelve **new** English multi-paragraph scene prompts, Grok register
(first person, everyday setting, ~220–330 words, no instruction to the
model). Disjoint as strings from `experiments/2026-08-17-grok-prompts/`,
`experiments/2026-08-17-more-prompts/`,
`experiments/2026-08-31-prompts-long12/`,
`experiments/2026-08-31-prompts-family12/`,
`experiments/2026-08-31-prompts-tails12/`, and
`experiments/2026-09-01-prompts-100/`. Topics are not harbour, night
bus, library, market, kitchen, station, rain, letter, workshop, office,
garden, or ferry queue.

| Item | Value |
|---|---|
| Prompts | `experiments/2026-09-01-prompts-grok12/` (committed **before** `pair`) |
| Generator | GPT-2 + public DeepMind 30 mixin |
| Draws | `--n-samples 4` |
| Length | `--max-new-tokens 128` |
| Seed | `20260904` |
| Output | `experiments/2026-09-01-pair-grok12x4/` |
| Test | `experiments/2026-08-17-pair-12x4/` |

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-grok12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 \
  --out-dir experiments/2026-09-01-pair-grok12x4
```

Do not look at key-free LRs until `pair` has written official first-draw
scores and this protocol's analysis commands have been run once, as
written. Twelve train families are smaller than the 100 one-liners; the
nested threshold will be noisier. That is part of the measurement, not
a reason to add families after seeing LRs.

## Analysis commands

Train is always `experiments/2026-09-01-pair-grok12x4`. Test is always
the original 12×4. Do not change flags after the first run. Do not look
at key-free test LRs until each command has been run once, as written.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-grok12x4-to-12x4-hard-last4

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok12x4-to-12x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok12x4-to-12x4-opening-rankpath

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods postokhits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok12x4-to-12x4-occupancy-free

python -m text_watermark_tools openings experiments/2026-09-01-pair-grok12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-grok12x4-to-12x4
```

In-family check (not the isolated headline):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-probe-grok12x4-hard-last4
```

Cross-register check, same tables, one-line 36×4 (not the headline):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-grok12x4-to-36x4-hard-last4
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4 or 36×4.
- Adding train families, mixing in the 100 one-liners, or grafting
  neighborhood paraphrases after seeing LRs.
- Selling a union with locks A/B/C from the 100-family tables.
- Selling in-family nested-by-stem on these 12 new stems as **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs. Local Hugging Face GPT-2 only for this freeze.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file and the 12 prompt texts in a commit that still
   precedes `pair`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then the analysis commands above, then append a dated
   logbook entry with the SHA and the nested Youden counts.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a fourth scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen commands)

Official first-draw lamp on the new twins is **12/12**. `used_keys=false`
on every key-free path below.

| Split | Lock | Prompt | Nested Youden | t=0 marked |
|---|---|---|---|---|
| original 12×4 | A interpolate | **5/12** | **16/48 vs 41/48** | **23/48 vs 30/48** |
| original 12×4 | B opening poshits | 7/12 | **6/48 vs 47/48** | **6/48 vs 47/48** |
| original 12×4 | C opening rankpath | **10/12** | **45/48 vs 22/48** | **22/48 vs 31/48** |
| original 12×4 | occupancy-free postokhits | 11/12 | **5/48 vs 47/48** | **5/48 vs 47/48** |

H-reg-A **fails**: lock A nested **16/48** is below one-liner lock A
**23/48**. Harbour and library now rank; night-bus and ferry-queue still
lose; medium stems 07–12 mostly lose. Register match is not the missing
isolated detector.

H-reg-iso **holds**: no nested Youden here beats **25/48**. Lock C nested
**45/48 vs 22/48** used a negative train threshold (≈ −0.41). Do not
sell 45/48. Isolated t=0 on rankpath is **22/48**.

H-reg-B **holds**: occupancy-free t=0 **5/48** equals opening coverage
**5/48** (0 exact 4-token copies; decided 5 TP / 1 FP). Prompt **11/12**
on postokhits is **2 strict wins + 9 occupancy-free 0=0 ties**. Historical
persist counted those ties as ranking wins with 0 isolated TPs. Strict
ranking wins with 0 isolated TPs: **0**.

H-reg-C: rankpath still ranks **10/12**, as in PROTOCOL-isolated, and is
not an isolated-file detector at t=0.

In-family interpolate on the new 12: prompt **11/12**, nested-by-stem
Youden **24/48 vs 40/48**, t=0 **31/48 vs 29/48**. Ranking works
in-family. That is not **25/48**.

Cross-register interpolate → 36×4: prompt **24/36**, nested
**50/144 vs 115/144**. Weaker than 100 one-liners → 36×4.

The reverse split (100 one-liners → these Grok-length files) is
[PROTOCOL-isolated-xreg.md](PROTOCOL-isolated-xreg.md). Lock A nested
**22/48 vs 41/48**. H-xreg-hard holds: the original 12 are not uniquely
cursed. Occupancy-free t=0 **0/48**. Does not replace **25/48**.

JSON: `experiments/2026-09-01-transfer-grok12x4-to-12x4-hard-last4/`,
`experiments/2026-09-01-transfer-grok12x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-grok12x4-to-12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-grok12x4-to-12x4-occupancy-free/`,
`experiments/2026-09-01-openings-grok12x4-to-12x4/`,
`experiments/2026-09-01-probe-grok12x4-hard-last4/`,
`experiments/2026-09-01-transfer-grok12x4-to-36x4-hard-last4/`.

