# Isolated-file protocol (in-domain 25/48 vs leftover vs covered)

This is a **methods freeze** for a decode of published JSON. It does
not add a scorer. Mixed 100 one-liners + 36 Grok-length families cover
**28/48** original-12 openings
([PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md)). Twenty files
remain zeros ([PROTOCOL-isolated-leftover.md](PROTOCOL-isolated-leftover.md)).
The locked isolated-file headline is in-domain 12-LOO hard last-4
marked `lr>0` **25/48**. Those two facts have not been crossed.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at leftover-versus-covered counts of the 25 TPs until
this freeze is named in [LOGBOOK.md](LOGBOOK.md) and the analysis
command has been run once, as written. Do **not** mix grok12 into any
train. Do **not** add a new `probe --methods` name.

## Why freeze now

Occupancy-free pooling stopped at **28/48** coverage. Mixed opening
rankpath on the leftover 20 was **12/20 vs 14/20**, not a calibrated
detector. Ranking-honesty already names stems where 9/12 and 25/48
disagree (garden ranks with 0 TPs; station/office/ferry-queue hold 5
of 25 TPs on ranking losses). Leftover membership is harbour, library,
station-4, letter 2–3, office 1/3/4, garden 1/4, ferry-queue. The
unanswered grain is whether the 25 in-domain TPs sit on leftover
openings (same-register LOO can sign files later OOD trains never
copy) or on the 28 later covered by 100+grok36 (in-domain isolated
sign includes openings that occupancy-free pooling later copies).
That split is determined by published holdout JSON. It is not a new
reader.

## Primary scientific question

Of the 25 in-domain 12-LOO hard last-4 marked files with `lr>0` in
`experiments/2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json`,
how many sit on the 20 leftover original-12 files (mixed postokhits
zeros in `experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json`)
versus the complementary 28 occupancy-covered files?

Not: can another `probe --methods` name lift **25/48**. Not: does
leftover rankpath **12/20** become a detector.

## Frozen sources

Leftover membership is frozen from mixed postokhits zeros. Do not
redefine leftover after seeing the 25-file split. The primary scorer
is the already-published 12-LOO hard last-4 holdout. No new tables.

| Role | Path |
|---|---|
| Leftover membership | `experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json` |
| Primary holdout (headline 25/48) | `experiments/2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json` |
| Secondary: interpolate sibling | `experiments/2026-09-01-probe-12x4-recount-hard-last4/interpolate/holdout.json` |
| Secondary: in-domain opening rankpath | `experiments/2026-09-01-probe-12x4-recount-opening-rankpath/rankpath/holdout.json` |

Helper: `summarize_isolated_coverage_split` in
`src/text_watermark_tools/openings.py`. Not a `probe --methods` name.

## Hypotheses (stated before leftover-versus-covered TP counts)

- **H-split-left.** The leftover 20 hold a non-zero share of the 25
  TPs. Same-register 12-LOO last-4 can sign files occupancy-free
  pooling never covers. Unmarked `lr≤0` on leftover is not 20/20;
  leftover TPs are not a calibrated leftover-file detector.
- **H-split-cov.** The covered 28 hold a non-zero share of the 25 TPs.
  Those files later have opening-atom overlap with mixed 100+grok36.
  In-domain isolated sign is not only leftover-file detection.
- **H-split-iso.** The two slices add to 25. Neither slice replaces
  **25/48**. Do not sell leftover-TP count, covered-TP count, leftover
  rankpath **12/20**, or coverage **28/48** as replacing **25/48**.

## Primary endpoint

Leftover marked `lr>0` / 20 and covered marked `lr>0` / 28 on the
12-LOO hard last-4 holdout. Report unmarked `lr≤0` on each slice.
Secondary: the same split on interpolate last-4 (sibling **24/48**)
and in-domain opening rankpath (**41/48**). `used_keys` must be false.

## Corpus

No new `pair`. No new `probe`. Decode published JSON only.

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.openings import (
    persist_isolated_coverage_split,
    print_isolated_coverage_split,
    summarize_isolated_coverage_split,
)

root = Path("experiments")
payload = summarize_isolated_coverage_split(
    root / "2026-09-01-openings-100plusgrok36-to-12x4" / "coverage.json",
    root / "2026-09-01-probe-12x4-recount-hard-last4" / "hard" / "holdout.json",
    extra_holdouts={
        "12loo-interpolate-last4": (
            root / "2026-09-01-probe-12x4-recount-hard-last4"
            / "interpolate" / "holdout.json"
        ),
        "12loo-opening-rankpath": (
            root / "2026-09-01-probe-12x4-recount-opening-rankpath"
            / "rankpath" / "holdout.json"
        ),
    },
)
out = root / "2026-09-01-isolated-split-25-leftover-vs-covered"
persist_isolated_coverage_split(payload, out)
print(print_isolated_coverage_split(payload), end="")
PY
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4, 36×4, or
  grok12×4.
- Mixing grok12 into any train.
- Changing leftover membership after seeing the 25-file split.
  Do not redefine leftover.
- Selling leftover-TP count, covered-TP count, leftover **12/20**, or
  coverage **28/48** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at leftover-versus-covered counts of the 25 TPs until this
  SHA is named in the logbook and the command above has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes the decode dump.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before leftover-versus-covered TP counts.
3. Run the command above, then append a dated logbook entry with the
   SHA and leftover / covered marked `lr>0`.
4. If the helper fails, fix it and re-run the **same** sources. Do not
   add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

Protocol SHA `f09d0e2`. `used_keys=false`.

Primary 12-LOO hard last-4 (headline **25/48**): leftover marked `lr>0`
**10/20**, unmarked `lr≤0` **11/20** (9 leftover FPs). Covered marked
`lr>0` **15/28**, unmarked `lr≤0` **11/28**. The slices add to 25.

H-split-left **holds**. Ten leftover TPs are a non-zero share. Unmarked
11/20 is not 20/20. Leftover hard last-4 is chance, not a leftover-file
detector. Leftover TPs and FNs share openings (`Closing is the`,
`The ferry was so` / `in`). Letter leftover (`Now` / `While`) and
garden leftover are **0/2**. Ranking-loss TPs (station-4, office-4,
ferry-queue 1–3) are all leftover and account for the published **5**
TPs on ranking losses.

H-split-cov **holds**. Fifteen covered TPs sit on files occupancy-free
pooling later copies (workshop 4/4 with 0 unmarked `lr≤0` among them).
In-domain isolated sign is not only leftover-file detection.

H-split-iso **holds**. Do not sell leftover **10/20**, covered **15/28**,
in-domain leftover rankpath **16/20**, mixed leftover rankpath **12/20**,
or coverage **28/48**. Isolated-file detection is not finished. The
leftover core that even in-domain opening rankpath misses is letter-2
(`Now in the second`), office-4, garden 1/4.

Secondary interpolate last-4: leftover **10/20 vs 11/20** (different
files; harbour leftover 4/4 marked with 0 unmarked `lr≤0`), covered
**14/28 vs 13/28**. Secondary in-domain opening rankpath: leftover
**16/20 vs 16/20**, covered **25/28 vs 19/28**.

JSON: `experiments/2026-09-01-isolated-split-25-leftover-vs-covered/`.

