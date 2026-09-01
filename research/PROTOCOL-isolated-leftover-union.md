# Isolated-file protocol (leftover-20 ∪ short-medium-tails openings)

This is a **methods freeze** for a decode of published opening-zero
lists. It does not add a scorer. Mixed 100 one-liners + 36 Grok-length
families cover **28/48** original-12 openings and leave **20** leftover
([PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md)). A disjoint
GPT-2 train already exists: 24 short one-liners + 12 medium scenes +
12 tail-transplants
(`experiments/2026-08-31-openings-short-medium-tails/`). Those stems
do not overlap the original 12. Their occupancy-free zeros on the same
test files have not been crossed with leftover 20.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at leftover-after-union counts until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written. Do **not** mix grok12 into any train. Do **not**
add a new `probe --methods` name. Do not redefine leftover. Do **not**
add family-12 paraphrases of the original 12 after leftover peeking.

Leftover-20 files are officially marked
([PROTOCOL-isolated-leftover-bound.md](PROTOCOL-isolated-leftover-bound.md)).
This freeze asks whether published disjoint-topic twins cover any of
those 20 openings, not whether a new scorer lifts **25/48**.

## Why freeze now

Occupancy-free isolated recall equals opening-atom overlap. Mixed
100+grok36 stopped at leftover 20. Short+medium+tails is the remaining
published GPT-2 twin pile that does not include the original 12 stems
and was collected before leftover-20 membership was named. Set-union
of those zeros is determined by published JSON. It is not a new
reader. Neighborhood paraphrases of the original 12 are refused here:
that would target leftover stems after peeking.

## Primary scientific question

How many of the occupancy leftover 20 remain zeros after set-union
with short+medium+tails postokhits coverage on the original 12×4?

Not: can mixed tables invent combo atoms. Not: does union coverage
replace **25/48**.

## Frozen sources

Leftover membership stays mixed postokhits zeros. Short+medium+tails
zeros stay that dump’s postokhits list. No new tables.

| Role | Path |
|---|---|
| Coverage A (leftover 20) | `experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json` |
| Coverage B (short+medium+tails) | `experiments/2026-08-31-openings-short-medium-tails/coverage.json` |
| Holdout keys | `experiments/2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json` |
| Secondary leftover sign | same hard last-4 holdout |
| Secondary leftover sign | `experiments/2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free/postokhits/holdout.json` |

Helper: `summarize_coverage_union` in
`src/text_watermark_tools/openings.py`. Not a `probe --methods` name.
Method stays `postokhits`. Labels: `100plusgrok36` and `smt`.

## Hypotheses (stated before leftover-after-union counts)

- **H-union-smt.** Short+medium+tails covers a non-zero share of the
  occupancy leftover 20 (`covered_b_only` is not empty on that slice).
  Disjoint-topic twins can copy leftover openings.
- **H-union-left.** Leftover after union is not empty. Unmarked `lr≤0`
  on that leftover last-4 is not 20/20. Remaining leftover is not a
  leftover-file detector.
- **H-union-iso.** Union coverage does not replace **25/48**. Do not
  sell SMT postokhits **30/48**, postokbackoff **36/48**, leftover
  official **20/20**, or leftover interpolate **13/20**.

## Primary endpoint

`n_union` and `n_leftover` from `summarize_coverage_union` on
postokhits zeros. Report `covered_b_only` (SMT-only openings) and
leftover last-4 marked `lr>0` / leftover n. `used_keys` must be false.

## Corpus

No new `pair`. No new `probe`. Decode published JSON only.

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.openings import (
    persist_coverage_union,
    print_coverage_union,
    summarize_coverage_union,
)

root = Path("experiments")
payload = summarize_coverage_union(
    root / "2026-09-01-openings-100plusgrok36-to-12x4" / "coverage.json",
    root / "2026-08-31-openings-short-medium-tails" / "coverage.json",
    root / "2026-09-01-probe-12x4-recount-hard-last4" / "hard" / "holdout.json",
    leftover_holdouts={
        "12loo-hard-last4": root
        / "2026-09-01-probe-12x4-recount-hard-last4"
        / "hard"
        / "holdout.json",
        "mixed-postokhits": root
        / "2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free"
        / "postokhits"
        / "holdout.json",
    },
    label_a="100plusgrok36",
    label_b="smt",
)
out = root / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4"
persist_coverage_union(payload, out)
print(print_coverage_union(payload), end="")
PY
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Adding family-12 paraphrases of the original 12 after leftover peeking.
- Changing leftover membership after seeing the union.
- Selling union coverage, SMT **30/48** / **36/48**, or leftover
  official **20/20** as replacing **25/48**.
- Targeting new train prompts at leftover openings after peeking.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at leftover-after-union counts until this SHA is named in
  the logbook and the command above has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes the decode dump.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before leftover-after-union counts.
3. Run the command above, then append a dated logbook entry with the
   SHA, `n_union`, and `n_leftover`.
4. If the helper fails, fix it and re-run the **same** sources. Do not
   add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

*(empty until the SHA is named and the command has been run once)*
