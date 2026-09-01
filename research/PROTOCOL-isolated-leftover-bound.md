# Isolated-file protocol (occupancy leftover-20 bound)

This is a **methods freeze** for a decode of published JSON plus one
`atoms` remeasure of already-frozen grok36 interpolate tables. It does
not add a scorer. Occupancy-free pooling leaves **20** original-12 files
uncovered
([PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md)). In-domain hard
last-4 on that slice is chance (**10/20 vs 11/20**). Mixed opening
rankpath is **12/20 vs 14/20**. Hard tail **4:128** leftover is
**11/20 vs 11/20**. Those leftover files may still be watermarked on
the official keyed detector; interpolate may still score leftover
bodies with Witten–Bell backoff or unbucketed copies such as `Closing`.
Those two facts have not been crossed on the occupancy leftover 20.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at occupancy leftover-20 official means or leftover-only
atom windows until this freeze is named in [LOGBOOK.md](LOGBOOK.md) and
the analysis command has been run once, as written. Do **not** mix grok12 into any train. Do **not** add a new `probe --methods` name.
Do not redefine leftover.

The cascade leftover eight in
`experiments/2026-09-01-official-prefix-leftover/` is a **different**
leftover set. This freeze uses mixed postokhits zeros (20 files).

## Why freeze now

Key-free leftover last-4 is chance. That can mean the mixin missed those
files, or it can mean the files are officially marked and the key-free
tables cannot see them. Official prefix scores for all 48 files already
exist. Occupancy leftover membership already exists. Crossing them does
not use a new reader.

Grok36 → original 12 interpolate atoms already showed `'Cl'→'osing'` as
an unbucketed body copy on leftover library. A leftover-only window
summary of the same tables asks whether leftover interpolate mass is
still backoff, not whether `Closing` becomes a detector.

## Primary scientific question

On the occupancy leftover 20, is the official keyed mean still a marked
score (similar to the covered 28), and is leftover-only interpolate
atom mass still mostly unseen next tokens?

Not: can a new method lift **25/48**. Not: does official leftover
detection replace key-free isolated-file indication.

## Frozen sources

Leftover membership stays mixed postokhits zeros. Official per-file
prefix scores stay the published dump. Interpolate tables stay the
frozen grok36 lock A counts. No new `pair`. No new `probe --methods`.

| Role | Path |
|---|---|
| Leftover membership | `experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json` |
| Official prefixes (keyed) | `experiments/2026-09-01-official-prefix-leftover/results.json` |
| Interpolate tables | `experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/tables-counts/` |
| Test twins | `experiments/2026-08-17-pair-12x4/` |

Helpers: `summarize_occupancy_leftover_official` and
`summarize_leftover_interpolate_atoms` in
`src/text_watermark_tools/leftover.py`. `atoms` CLI is the existing
decoder (`--store-rows`). Not a `probe --methods` name.

## Hypotheses (stated before leftover-20 official means and leftover atoms)

- **H-bound-lamp.** Occupancy leftover-20 marked files have official
  full-file mean similar to covered-28 (both well above 0.55). Unmarked
  stays near 0.50. Leftover key-free chance is not “the mixin missed
  these files.”
- **H-bound-open.** Leftover-20 official prefix-5 is also marked (mean
  above 0.55). Occupancy-free tables failing leftover openings is not
  because leftover openings are unmarked at the keyed detector.
- **H-bound-atom.** Leftover-only grok36 interpolate atoms in 0:4 are
  still mostly `unseen_next`. Any leftover seen atoms (unbucketed body
  copies) do not make leftover occupancy-free.
- **H-bound-iso.** This bound does not replace **25/48**. Official
  leftover detection uses keys. Leftover atoms are not a leftover-file
  detector. Do not sell leftover official means, leftover interpolate
  `lr>0`, or `Closing`.

## Primary endpoint

Official prefix **128** leftover-20 marked mean vs covered-28 marked
mean vs unmarked mean, with counts `>0.55`. Secondary: official prefix
**5** and **16**. Leftover-only interpolate windows **0:4**, **4:16**,
**16:32**, **32:64**, **64:128** (`n_seen` vs `n_unseen`; leftover
marked `lr>0`). Official slice `used_keys` must be true. Atom slice
`used_keys` must be false.

## Corpus

No new `pair`. No new `probe`. Decode published official JSON. Remeasure
existing grok36 interpolate tables with `atoms --store-rows`, then
restrict rows to leftover keys.

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.atoms import dump_interpolate_atoms
from text_watermark_tools.leftover import (
    leftover_keys_from_coverage,
    persist_leftover_bound,
    print_leftover_bound,
    summarize_leftover_interpolate_atoms,
    summarize_occupancy_leftover_official,
)

root = Path("experiments")
coverage = root / "2026-09-01-openings-100plusgrok36-to-12x4" / "coverage.json"
official = summarize_occupancy_leftover_official(
    coverage,
    root / "2026-09-01-official-prefix-leftover" / "results.json",
)
keys = leftover_keys_from_coverage(coverage)
atoms_full = dump_interpolate_atoms(
    root / "2026-09-01-transfer-grok36x4-to-12x4-hard-last4" / "tables-counts",
    Path("experiments/2026-08-17-pair-12x4"),
    store_rows=True,
    windows=((0, 4), (4, 16), (16, 32), (32, 64), (64, 128)),
)
atoms = summarize_leftover_interpolate_atoms(atoms_full, keys)
out = root / "2026-09-01-isolated-leftover-bound"
persist_leftover_bound(official=official, atoms=atoms, out_dir=out)
print(print_leftover_bound(official=official, atoms=atoms), end="")
PY
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Changing leftover membership after seeing leftover-20 official means.
- Selling official leftover detection as key-free **25/48**.
- Selling leftover interpolate `Closing` / leftover `lr>0` as replacing
  **25/48**.
- Targeting new train prompts at leftover openings after peeking.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at occupancy leftover-20 official means or leftover-only atom
  windows until this SHA is named in the logbook and the command above
  has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes the decode dump.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before leftover-20 official means.
3. Run the command above, then append a dated logbook entry with the
   SHA, official leftover-20 prefix-128 mean, and leftover 0:4 seen vs
   unseen.
4. If the helper fails, fix it and re-run the **same** sources. Do not
   add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

Protocol SHA `802186e`. Official slice `used_keys=true`. Atom slice
`used_keys=false`.

Dump: [experiments/2026-09-01-isolated-leftover-bound/](../experiments/2026-09-01-isolated-leftover-bound/).

Official public-deepmind-30 mean on occupancy leftover 20 vs covered 28:

| prefix | leftover marked mean | >0.55 | covered marked mean | >0.55 | unmarked mean | >0.55 |
|---|---|---|---|---|---|---|
| 5 | 0.6533 | **18/20** | 0.6202 | 27/28 | 0.4813 | 14/48 |
| 16 | 0.6272 | **20/20** | 0.6252 | **28/28** | 0.4955 | 3/48 |
| 128 | 0.6242 | **20/20** | 0.6198 | **28/28** | 0.5000 | 0/48 |

H-bound-lamp **holds**. Leftover-20 full-file official mean is **0.624**,
**20/20** above 0.55, matching covered-28 (**0.620**, 28/28). Unmarked
is **0.500**. Leftover key-free chance is not “the mixin missed these
files.”

H-bound-open **holds**. Leftover prefix-5 mean is **0.653**, **18/20**
above 0.55 (stronger than covered 0.620). The two prefix-5 misses are
office-1 and office-3 (`The printer worked.`) at **0.500** on one
5-gram; both are marked by prefix-16 (**0.656 / 0.644**) and full-file
(**0.624 / 0.618**). Occupancy-free tables failing leftover openings is
not because leftover openings are unmarked at the keyed detector.

Leftover-only grok36 interpolate atoms (`n_rows=40`; leftover marked
`lr>0` **13/20**):

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.079 | −0.213 | 21 | **99** |
| 4:16 | 0.266 | −0.084 | 15 | 465 |
| 16:32 | 0.028 | 0.119 | 7 | 633 |
| 32:64 | 0.237 | −0.080 | 31 | 1249 |
| 64:128 | 0.043 | −0.111 | 52 | 2502 |

H-bound-atom **holds**. Leftover 0:4 is still mostly `unseen_next`
(99 vs 21). The only leftover marked positive seen 0:4 atoms are
library `'Cl'→'osing'` and the two following Closing 4-grams (n=4
each). That is the published unbucketed body copy, not occupancy-free
opening overlap.

H-bound-iso **holds**. Do not sell leftover official **20/20**, leftover
interpolate **13/20**, or `Closing` as replacing **25/48**. Official
leftover detection uses keys. Isolated-file remains open.
Do not write `thesis/`.
