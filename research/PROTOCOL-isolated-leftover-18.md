# Isolated-file protocol (leftover-18 remaining readers)

This is a **methods freeze** for a decode of published holdouts on the
occupancy leftover **18**. It does not add a scorer. After leftover-20 ∪
short+medium+tails
([PROTOCOL-isolated-leftover-union.md](PROTOCOL-isolated-leftover-union.md)),
leftover is harbour, library, station-4, letter 2–3, office 1/3/4, and
ferry-queue. Occupancy-free coverage from published disjoint-topic
GPT-2 trains is closed
([PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md)).
Leftover-18 files are officially marked (**18/18** at prefix-128 by
subset). Key-free leftover last-4 is **10/18 vs 10/18**. Mixed opening
rankpath and grok36 interpolate on leftover-20 were chance-like
(**12/20 vs 14/20** and leftover interpolate **13/20**). Those leftover-20
signs have not been re-sliced on leftover-18 after garden 1/4 left
leftover.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at leftover-18 mixed rankpath signs, leftover-18
interpolate `lr>0`, or leftover-18 atom windows until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written. Do **not** mix grok12 into any train. Do **not**
add a new `probe --methods` name. Do not redefine leftover. Do **not**
add family-12 paraphrases of the original 12 after leftover peeking.
Do **not** target new train prompts at leftover-18 openings after
peeking leftover-18 stems.

## Why freeze now

Occupancy-free isolated recall cannot see leftover-18 unique openings
without copying them. The remaining published readers that score a
novel opening without an observed next-token copy are mixed opening
rankpath (lock C) and grok36 interpolate (lock A, Witten–Bell backoff
plus unbucketed body copies). Re-slicing those already-opened holdouts
on leftover-18 asks whether dropping garden occupancy coverage turns
leftover rankpath or leftover interpolate into a leftover-file
detector. It does not add a scorer.

## Primary scientific question

On leftover-18, is mixed opening rankpath a leftover-file detector,
and is leftover-18 grok36 interpolate still backoff rather than
occupancy-free opening overlap?

Not: can more unrelated GPT-2 scenes copy leftover-18 openings. Not:
does leftover official **18/18** replace key-free **25/48**.

## Frozen sources

Leftover membership stays leftover-union leftover-18 keys. No new
tables.

| Role | Path |
|---|---|
| Leftover-18 keys | `experiments/2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/union.json` |
| Mixed opening rankpath | `experiments/2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath/rankpath/holdout.json` |
| Grok36 interpolate | `experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/interpolate/holdout.json` |
| Already-opened last-4 | `experiments/2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json` |
| Grok36 interpolate tables | `experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/tables-counts` |

Helper: `summarize_leftover_holdouts` and
`summarize_leftover_interpolate_atoms` in
`src/text_watermark_tools/leftover.py`. Not a `probe --methods` name.
Already-opened 12-LOO hard last-4 leftover-18 is **10/18 vs 10/18**;
the command must reprint that check. Mixed occupancy-free leftover
sign stays **0/18** by construction and is not a primary endpoint.

## Hypotheses (stated before leftover-18 rankpath and interpolate counts)

- **H-left18-C.** Leftover-18 mixed rankpath marked `lr>0` is not a
  leftover-file detector: unmarked `lr≤0` on those files is not
  18/18, and marked recall does not replace **25/48**.
- **H-left18-A.** Leftover-18 grok36 interpolate marked `lr>0` is not
  18/18. Leftover-18 interpolate 0:4 is still mostly `unseen_next`
  (Witten–Bell backoff), not occupancy-free opening overlap.
- **H-left18-iso.** Do not sell leftover-18 rankpath, leftover-18
  interpolate, leftover official **18/18**, union **30/48**, leftover
  last-4 **10/18**, leftover-20 rankpath **12/20**, or leftover
  interpolate **13/20** as replacing **25/48**.

## Primary endpoint

Leftover-18 mixed rankpath marked `lr>0` / unmarked `lr≤0`. Secondary:
leftover-18 grok36 interpolate marked `lr>0` and leftover-18 interpolate
0:4 seen vs unseen. `used_keys` must be false on those slices.
12-LOO hard last-4 leftover-18 must reprint **10/18 vs 10/18**.

## Corpus

No new `pair`. No new `probe`. Decode published JSON. Remeasure
existing grok36 interpolate tables with `atoms --store-rows`, then
restrict rows to leftover-18 keys.

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.atoms import dump_interpolate_atoms
from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    persist_leftover_readers,
    print_leftover_readers,
    summarize_leftover_holdouts,
    summarize_leftover_interpolate_atoms,
)

root = Path("experiments")
keys = leftover_keys_from_union(
    root / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4" / "union.json"
)
payload = summarize_leftover_holdouts(
    keys,
    {
        "mixed-rankpath": root
        / "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath"
        / "rankpath"
        / "holdout.json",
        "grok36-interpolate": root
        / "2026-09-01-transfer-grok36x4-to-12x4-hard-last4"
        / "interpolate"
        / "holdout.json",
        "12loo-hard-last4": root
        / "2026-09-01-probe-12x4-recount-hard-last4"
        / "hard"
        / "holdout.json",
    },
)
atoms_full = dump_interpolate_atoms(
    root / "2026-09-01-transfer-grok36x4-to-12x4-hard-last4" / "tables-counts",
    Path("experiments/2026-08-17-pair-12x4"),
    store_rows=True,
    windows=((0, 4), (4, 16), (16, 32), (32, 64), (64, 128)),
)
payload["atoms"] = summarize_leftover_interpolate_atoms(atoms_full, keys)
out = root / "2026-09-01-isolated-leftover-18-readers"
persist_leftover_readers(payload, out)
print(print_leftover_readers(payload), end="")
PY
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Adding family-12 paraphrases of the original 12 after leftover peeking.
- Changing leftover membership after seeing leftover-18 rankpath signs.
- New occupancy-free trains aimed at leftover-18 openings after peeking.
- Selling leftover-18 rankpath, leftover-18 interpolate, leftover
  official **18/18**, union **30/48**, or leftover last-4 **10/18** as
  replacing **25/48**.
- Targeting new train prompts at leftover openings after peeking.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at leftover-18 mixed rankpath signs, leftover-18 interpolate
  `lr>0`, or leftover-18 atom windows until this SHA is named in the
  logbook and the command above has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes the decode dump.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before leftover-18 rankpath counts.
3. Run the command above, then append a dated logbook entry with the
   SHA, leftover-18 rankpath marked `lr>0` / unmarked `lr≤0`, and
   leftover-18 interpolate 0:4 seen vs unseen.
4. If the helper fails, fix it and re-run the **same** sources. Do not
   add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

Protocol SHA `5621544`. Named `f1782dc`. `used_keys=false`.

Dump: [experiments/2026-09-01-isolated-leftover-18-readers/](../experiments/2026-09-01-isolated-leftover-18-readers/).

| Reader | Leftover-18 marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|
| Mixed opening rankpath | **12/18** | **13/18** |
| Grok36 interpolate | **12/18** | **12/18** |
| 12-LOO hard last-4 (check) | **10/18** | **10/18** |

H-left18-C **holds**. Leftover-18 mixed rankpath unmarked `lr≤0` is
**13/18**, not 18/18. Marked **12/18** does not replace **25/48**.
Garden leftover had 0 mixed rankpath TPs (leftover-20 **12/20** stays
**12/18**). Occupancy-covering garden did not carry leftover rankpath.

H-left18-A **holds**. Leftover-18 grok36 interpolate marked `lr>0` is
**12/18**, not 18/18. Leftover-18 interpolate 0:4 is seen 19 vs unseen
**89**. Seen mass is still library `'Cl'→'osing'` (n=4). Garden leftover
had 1 interpolate TP (leftover-20 **13/20** becomes **12/18**). That is
backoff plus an unbucketed body copy, not occupancy-free opening overlap.

H-left18-iso **holds**. Do not sell leftover-18 rankpath **12/18**,
leftover-18 interpolate **12/18**, leftover official **18/18**, union
**30/48**, leftover last-4 **10/18**, leftover-20 rankpath **12/20**, or
leftover interpolate **13/20**. Isolated-file remains open. Do not write
`thesis/`.
