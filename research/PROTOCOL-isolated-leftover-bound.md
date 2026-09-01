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

*(empty until the SHA is named and the command has been run once)*
