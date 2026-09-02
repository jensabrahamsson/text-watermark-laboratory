# Isolated-file protocol (leftover vs covered on mask-*k* windows)

This is a **methods freeze** for a decode of published JSON. It does
not add a scorer. Headline 12-LOO hard last-4 isolated **25/48** splits
leftover **10/20 vs 11/20** and occupancy-covered **15/28**
([PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md)). Mask-*k*
windows ([PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md)) then
showed that hard prompt ranking **9/12** survives tails **4:128** and
**8:128**, while prefix **0:4** is **5/12**. Those two facts have not
been crossed: we do not yet know whether tail isolated TPs sit on the
20 leftover openings or on the 28 later covered by 100+grok36.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at leftover-versus-covered counts on the window
holdouts until this freeze is named in [LOGBOOK.md](LOGBOOK.md) and
the analysis command has been run once, as written. Do **not** mix grok12 into any train. Do **not** add a new `probe --methods` name.
Do not redefine leftover.

## Why freeze now

Tail hard ranking **9/12** looks like body signal. Occupancy-free
pooling only copies openings. If tail isolated TPs sit on the 28
covered files, tail 9/12 is still opening-overlap families scored on
later tokens, not leftover-file detection. If they sit on leftover 20,
same-register last-4 has body mass that occupancy-free pooling never
covers — still not a leftover detector unless unmarked `lr≤0` on
leftover is 20/20. Prefix 0:4 hard isolated **29/48** with ranking
**5/12** is the other slice. This decode uses the existing helper.

## Primary scientific question

On hard window **4:128** (prompt rank still **9/12**, isolated 27/48),
how many leftover-20 files have `lr>0` versus how many of the 28
occupancy-covered files?

Not: can a new method lift **25/48**. Not: does tail **9/12** replace
isolated-file detection.

## Frozen sources

Leftover membership stays mixed postokhits zeros. Window holdouts stay
the mask-*k* dump. No new tables.

| Role | Path |
|---|---|
| Leftover membership | `experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json` |
| Primary: hard 4:128 | `experiments/2026-09-01-probe-12x4-headline-windows/window-4-128/hard/holdout.json` |
| Secondary: hard 8:128 | `experiments/2026-09-01-probe-12x4-headline-windows/window-8-128/hard/holdout.json` |
| Secondary: hard 0:4 | `experiments/2026-09-01-probe-12x4-headline-windows/window-0-4/hard/holdout.json` |
| Secondary: interpolate 4:128 | `experiments/2026-09-01-probe-12x4-headline-windows/window-4-128/interpolate/holdout.json` |

Helper: `summarize_isolated_coverage_split`. Not a `probe --methods`
name. Primary holdout is the tail window; leftover keys still come from
coverage zeros.

## Hypotheses (stated before leftover-versus-covered window counts)

- **H-wsplit-tail.** Hard 4:128 leftover marked `lr>0` is not a
  leftover-file detector: unmarked `lr≤0` on leftover is not 20/20.
  Tail ranking **9/12** is not isolated leftover recall.
- **H-wsplit-open.** Hard 0:4 isolated TPs are not leftover-only.
  Prefix isolated **29/48** includes occupancy-covered openings.
- **H-wsplit-iso.** No window leftover slice replaces **25/48**. Do
  not sell tail **9/12**, leftover window TP counts, or prefix isolated
  **29/48**.

## Primary endpoint

Leftover marked `lr>0` / 20 and covered marked `lr>0` / 28 on hard
4:128. Report unmarked `lr≤0` on each slice. Secondary: the same split
on hard 8:128, hard 0:4, and interpolate 4:128. `used_keys` must be
false.

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
win = root / "2026-09-01-probe-12x4-headline-windows"
payload = summarize_isolated_coverage_split(
    root / "2026-09-01-openings-100plusgrok36-to-12x4" / "coverage.json",
    win / "window-4-128" / "hard" / "holdout.json",
    extra_holdouts={
        "hard-8:128": win / "window-8-128" / "hard" / "holdout.json",
        "hard-0:4": win / "window-0-4" / "hard" / "holdout.json",
        "interpolate-4:128": win / "window-4-128" / "interpolate" / "holdout.json",
    },
)
out = root / "2026-09-01-isolated-split-windows-leftover-vs-covered"
persist_isolated_coverage_split(payload, out)
print(print_isolated_coverage_split(payload), end="")
PY
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Changing leftover membership after seeing window splits.
- Selling tail **9/12**, leftover window TPs, or prefix **29/48** as
  replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at leftover-versus-covered window counts until this SHA is
  named in the logbook and the command above has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes the decode dump.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before leftover-versus-covered window
   counts.
3. Run the command above, then append a dated logbook entry with the
   SHA and hard 4:128 leftover / covered marked `lr>0`.
4. If the helper fails, fix it and re-run the **same** sources. Do not
   add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

Protocol SHA `3e30e70`. `used_keys=false`.

Dump: [experiments/2026-09-01-isolated-split-windows-leftover-vs-covered/](../experiments/2026-09-01-isolated-split-windows-leftover-vs-covered/).

Opening coverage of 12-LOO last-4 interpolate is still **28/48** covered
and **20/48** leftover (same occupancy atoms as
[PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md)). Primary =
hard **4:128** (prompt still **9/12**, isolated **27/48 vs 22/48**).

| Slice | Marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|
| Leftover 20 | **11/20** | **11/20** |
| Occupancy-covered 28 | **16/28** | **11/28** |

H-wsplit-tail **holds**. Leftover tail is chance (**11/20 vs 11/20**).
Unmarked leftover `lr≤0` is 11/20, not 20/20. The 27 isolated TPs are
**11 leftover + 16 covered**. Tail prompt **9/12** is occupancy-covered
ranking, not leftover-file recall.

Leftover **4:128** TPs (11): harbour 2–3, library 3–4, station-4,
letter-2, office-4, garden 1 and 4, ferry-queue 1–2. Unique leftover TP
stems on the tail: harbour, library, station, letter, office, garden,
ferry-queue. Full-file leftover last-4 had garden leftover **0/2** and
letter leftover **0/2**; dropping the opening lets garden leftover and
letter-2 sign. Ranking-loss TPs from the headline split (station-4,
office-4, ferry-queue 1–3) stay leftover on the tail except
ferry-queue-3, which goes FN.

Secondary:

| Holdout | Leftover marked / unmarked | Covered marked / unmarked | Isolated total |
|---|---|---|---|
| hard 8:128 | **12/20 vs 12/20** | **17/28 vs 11/28** | 29/48 vs 23/48 |
| hard 0:4 | **12/20 vs 9/20** | **17/28 vs 17/28** | 29/48 vs 26/48 |
| interpolate 4:128 | **7/20 vs 12/20** | **13/28 vs 14/28** | 20/48 vs 26/48 |

H-wsplit-open **holds**. Prefix 0:4 isolated **29/48** is **12 leftover
+ 17 covered**, not leftover-only. Leftover 0:4 is **12/20 vs 9/20**,
not a leftover core.

H-wsplit-iso **holds**. Do not sell leftover **11/20**, **12/20**,
covered **16/28**, isolated window **29/48**, interpolate tail **20/48**,
or tail prompt **9/12** as replacing **25/48**. Interpolate **4:128**
stays weak (**20/48**), matching the mask freeze: interpolate is
front-loaded; hard tails are not leftover-file recall.

The leftover core is still unsolved. Isolated-file remains open.
Do not write `thesis/`.
