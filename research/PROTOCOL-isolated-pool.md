# Isolated-file protocol (pooled 100 one-liners + 36 Grok-length)

This is a **methods freeze** for a pooled occupancy-free bound. It does
not add a scorer. Published opening zeros on the original 12×4 files
are **disjoint** across the two trains already opened: 100 one-liners
cover **18/48**, 36 Grok-length families cover **10/48**, intersection
**0**, set-union **28/48**. Twenty files are leftover. That arithmetic
is determined from
`experiments/2026-09-01-openings-100x4-to-12x4/` and
`experiments/2026-09-01-openings-grok36x4-to-12x4/` before this file's
mixed tables exist.

[PROTOCOL-isolated-scale.md](PROTOCOL-isolated-scale.md) refused mixing
those corpora after seeing separate LRs. This file is the mix cell,
with that peek named: occupancy-free union **28/48** is already
readable from published zeros. The frozen commands below ask whether
mixed `postokhits` equals that union (no combo atoms), and what mixed
interpolate nested Youden does. Do **not** sell **28/48** as replacing
**25/48**.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at mixed key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis commands have been run once,
as written. Do **not** mix grok12 into the train.

## Why freeze now

Isolated observed-token recall has tracked opening-atom overlap on
every opened split. The two trains cover complementary original-12
openings (one-liner kitchen/rain/workshop vs Grok-length night-bus /
market / garden 2–3). Set-union **28/48** would numerically exceed
in-domain hard sign **25/48**. That is still two-register opening
overlap, not a detector for leftover files (`Closing`, `The ferry`,
`Now in the second`, `The printer`, ferry-queue). Mixed tables could
in principle add combo atoms neither train had alone. That is the
only occupancy-free unknown. Mixed interpolate nested Youden is not
determined by the zero lists.

## Primary scientific question

Do frozen key-free tables trained on the **concatenation** of
`experiments/2026-09-01-pair-100x4/` and
`experiments/2026-09-01-pair-grok36x4/`, with no detector keys,
`hash_iv`, or g-values, classify the original 12×4 files at
occupancy-free t=0 equal to the published set-union **28/48**?

Not: can another `probe --methods` name lift **25/48**. Not: does
pooling after seeing both separate LRs invent a universal detector.

## Frozen scorers

Same readers as [PROTOCOL-isolated.md](PROTOCOL-isolated.md). Exact
CLI. `--extra-train` concatenates the second twin directory. No new
method names.

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |
| A | Hard last-4 interpolate | `--methods interpolate --context-len 4` |

Lock B here is occupancy-free `postokhits`, not Laplace poshits.
Openings extra-train is the coverage curve for the same concatenation.

## Hypotheses (stated before mixed LRs)

- **H-pool-B.** Mixed occupancy-free postokhits t=0 on the original
  12×4 equals the published set-union **28/48**, and openings
  extra-train coverage equals **28/48**. No combo atoms.
- **H-pool-A.** Mixed interpolate nested Youden on the original 12×4
  is at least grok36-only **26/48**. More train mass. This still does
  not have to beat **25/48**.
- **H-pool-iso.** **28/48** is opening-atom overlap of two registers.
  Leftover files remain. Do not sell 28/48, mixed nested Youden, or
  leftover interpolate **13/20** (Closing / backoff on published
  grok36 holdouts) as replacing **25/48**.

## Primary endpoint

Occupancy-free postokhits t=0 marked files on
`experiments/2026-08-17-pair-12x4/`, compared to the published
set-union **28/48**. Secondary: mixed interpolate nested Youden on
those same files. Leftover-file interpolate/rankpath signs on the
published holdouts are already recorded in
`experiments/2026-09-01-openings-union-100-and-grok36-to-12x4/`; they
are not this mix.

## Corpus

No new `pair`. Train is the two existing twin directories. Test is
the original 12×4. Optional check: same mixed tables on grok12×4
(published union **40/48**).

```bash
python -m text_watermark_tools openings experiments/2026-09-01-pair-100x4 \
  --extra-train experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-100plusgrok36-to-12x4

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --extra-train experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods postokhits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --extra-train experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-100plusgrok36-to-12x4-hard-last4
```

Optional grok12 check (same flags, not the primary endpoint):

```bash
python -m text_watermark_tools openings experiments/2026-09-01-pair-100x4 \
  --extra-train experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-100plusgrok36-to-grok12x4
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4, 36×4, or
  grok12×4.
- Mixing grok12 into the train.
- Selling set-union **28/48**, leftover **13/20**, or mixed nested
  Youden as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at mixed test LRs until this SHA is named in the logbook
  and the commands above have been run once.

## Preregistration mechanic

1. Commit this file (and the published-zero union dump) in a commit
   that still precedes mixed `probe` / mixed `openings`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before mixed LRs.
3. Run the analysis commands above, then append a dated logbook entry
   with the SHA and the occupancy-free t=0 count.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a fourth scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.
