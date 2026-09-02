# Isolated-file protocol (leftover openings after pooled coverage)

This is a **methods freeze** for the files occupancy-free pooling
cannot cover. It does not add a scorer. Mixed 100 one-liners + 36
Grok-length families cover **28/48** original-12 openings
([PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md)). Twenty files
remain zeros: harbour (`The ferry…`), library (`Closing is the`),
station-4, letter 2–3 (`Now` / `While`), office 1/3/4 (`The printer`),
garden 1/4, ferry-queue. Those leftovers are the isolated-file core.
Count tables that need an observed next token are done there by
construction.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at mixed rankpath test LRs until this freeze is named
in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been run
once, as written. Do **not** mix grok12 into the train. Do **not** add
a new `probe --methods` name.

Separate-train leftover rankpath on published holdouts was already
logged in `experiments/2026-09-01-openings-union-100-and-grok36-to-12x4/`
(9/20 and 9/20). That is not this mix.

## Why freeze now

Occupancy-free pooling added complementary openings and stopped at
**28/48** coverage, **26/48** t=0. Interpolate nested **27/48** still
uses Witten–Bell backoff and unbucketed body copies (`Closing`) on the
leftover slice. The remaining existing reader that scores a novel
opening without copying the next token is **opening rankpath** (five
symbol ranks from the unmarked LM). Mixed rankpath tables have not
been scored on these 12×4 files. This freeze asks whether that
geometry classifies the leftover 20, not whether another hashed scorer
can copy more openings.

## Primary scientific question

Do frozen opening rankpath tables, trained on the concatenation of
`experiments/2026-09-01-pair-100x4/` and
`experiments/2026-09-01-pair-grok36x4/`, classify the 20 leftover
original-12 files (mixed postokhits zeros) without detector keys,
`hash_iv`, g-values, or observed-token copies?

Not: can rankpath prompt-rank the full 48. Not: does leftover
interpolate **13/20** become a detector.

## Frozen scorer

Same lock C as [PROTOCOL-isolated.md](PROTOCOL-isolated.md). Exact CLI.
`--extra-train` concatenates the second twin directory. No new method
names. Rankpath needs the unmarked LM.

| Lock | Reader | Train flags |
|---|---|---|
| C | Opening rankpath | `--methods rankpath --fit-prefix 4 --pos-bucket 1` |

Leftover membership is frozen from mixed postokhits zeros in
`experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json`
(the same 20 files as the published set-union leftover). Do not redefine leftover after seeing rankpath LRs.

## Hypotheses (stated before mixed rankpath LRs)

- **H-left-C.** On the leftover 20, mixed rankpath marked `lr>0` is
  not a calibrated isolated-file detector: unmarked `lr≤0` on those
  same stems does not land at 20/20, and marked recall does not
  replace **25/48**.
- **H-left-full.** Mixed rankpath nested Youden on the full 48 does
  not beat **25/48**. Prompt ranking on leftovers is not isolated
  recall.
- **H-left-iso.** Do not sell leftover rankpath, leftover interpolate
  **13/20**, or pooled coverage **28/48** as replacing **25/48**.

## Primary endpoint

Isolated sign on the leftover 20 marked files (`lr>0`) and unmarked
files (`lr≤0`), using mixed rankpath LRs. Report the full-48 nested
Youden as secondary. `used_keys` must be false.

## Corpus

No new `pair`. Same mixed train as PROTOCOL-isolated-pool. Test is
`experiments/2026-08-17-pair-12x4/`.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --extra-train experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4, 36×4, or
  grok12×4.
- Mixing grok12 into the train.
- Changing leftover membership after seeing LRs.
- Selling leftover signs, **28/48**, or nested Youden as replacing
  **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at mixed rankpath test LRs until this SHA is named in the
  logbook and the command above has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes mixed rankpath
   `probe`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before mixed rankpath LRs.
3. Run the command above, then append a dated logbook entry with the
   SHA and leftover marked `lr>0` / unmarked `lr≤0`.
4. If the command fails, fix the harness and re-run the **same**
   flags. Do not add a second scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

Protocol SHA `7afd049`. `used_keys=false`.

Leftover 20 (primary): mixed rankpath marked `lr>0` **12/20**, unmarked
`lr≤0` **14/20** (6 leftover FPs). Library leftover is **0/4**. Harbour
and ferry-queue leftover are **4/4** marked with unmarked FPs on those
stems. Office leftover is **3/3** both sides.

H-left-C **holds**. 12/20 with 6 leftover FPs is not a calibrated
isolated-file detector. 12/20 is not **25/48**.

Full 48 (secondary): prompt **10/12**, t=0 **35/48 vs 38/48**, nested
Youden **35/48 vs 38/48**. Library ranks with 0 isolated TPs. H-left-full
**fails as a raw nested count** (35>25). That 35/48 includes the 28
covered openings plus leftover geometry. It is not leftover recall.
Do not sell **35/48**.

H-left-iso **holds**. Do not sell leftover **12/20**, full **35/48**,
pooled coverage **28/48**, or interpolate leftover **13/20**. Isolated-file
detection is not finished.

JSON: `experiments/2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath/`.

In-domain **25/48** vs leftover is
[PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md): leftover
hard last-4 **10/20 vs 11/20**.
