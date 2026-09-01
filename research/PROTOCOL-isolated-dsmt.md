# Isolated-file protocol (Distil ∪ SMT openings)

This is a **methods freeze** for a decode of published opening-zero
lists. It does not add a scorer. DistilGPT2 100×4 occupancy-free tables
cover **23/48** original-12 openings and leftover-18 Distil coverage is
**3/18** ([PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md)).
Short+medium+tails occupancy-free coverage on the same files is
**30/48**, leftover **18**
([PROTOCOL-isolated-leftover-union.md](PROTOCOL-isolated-leftover-union.md)).
Those two published zero-lists have not been crossed as a set-union.
dgen and qgen refused this decode without a freeze before looking.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at leftover-after-union counts until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written. Do **not** mix grok12 into any train. Do **not**
add a new `probe --methods` name. Do not redefine leftover. Do **not**
add family-12 paraphrases of the original 12 after leftover peeking.
Do **not** target leftover-15 openings after peeking.

Leftover-18 files are officially marked (**18/18** at prefix-128) and
use keys. This freeze asks whether Distil occupancy-free coverage, from
prompts frozen before leftover peeking, covers any leftover-18 openings
that SMT missed. It is not leftover-18 Distil rankpath. It is not a
new isolated-file detector.

## Why freeze now

Occupancy-free isolated recall equals opening-atom overlap. SMT ∪ mixed
stopped at leftover 18. Distil 100×4 is the remaining published
same-BPE occupancy-free train on the original 12 that is not more
unrelated GPT-2 scenes. Set-union of those zeros is determined by
published JSON. It is not a new reader. Targeting leftover-15 stems
after peeking is refused here.

## Primary scientific question

How many of the occupancy leftover 18 remain zeros after set-union of
Distil 100×4 postokhits coverage with short+medium+tails postokhits
coverage on the original 12×4?

Not: can Distil tables invent combo atoms. Not: does union coverage
replace **25/48**. Not: leftover-18 Distil rankpath.

## Frozen sources

Leftover membership stays the union leftover of Distil zeros and SMT
zeros. Distil zeros stay that dump’s postokhits list. SMT zeros stay
that dump’s postokhits list. No new tables.

| Role | Path |
|---|---|
| Coverage A (Distil 100×4 → original 12) | `experiments/2026-09-01-openings-distil100x4-to-12x4/coverage.json` |
| Coverage B (short+medium+tails) | `experiments/2026-08-31-openings-short-medium-tails/coverage.json` |
| Holdout keys | `experiments/2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json` |
| Secondary leftover sign | same hard last-4 holdout |
| Secondary leftover sign | `experiments/2026-09-01-transfer-distil100x4-to-12x4-opening-poshits/postokhits/holdout.json` |

Helper: `summarize_coverage_union` in
`src/text_watermark_tools/openings.py`. Not a `probe --methods` name.
Method stays `postokhits`. Labels: `distil100x4` and `smt`.

## Hypotheses (stated before leftover-after-union counts)

- **H-dsmt-cover.** Distil occupancy-free covers a non-zero share of
  leftover-18 (`covered_a_only` is not empty). Same-BPE Distil twins,
  collected before leftover-18 membership was named, can copy leftover
  openings SMT missed.
- **H-dsmt-left.** Leftover after Distil ∪ SMT is not empty. Unmarked
  `lr≤0` on that leftover last-4 is not leftover-n / leftover-n as a
  leftover-file detector. Distil occupancy-free leftover sign on the
  union leftover is **0** by construction.
- **H-dsmt-iso.** Union coverage does not replace **25/48**. Do not
  sell Distil **22/48**, leftover Distil **3/18**, SMT **30/48**,
  leftover official **18/18**, Distil→Distil **16/48**, or Qwen→Qwen
  **31/48**.

## Primary endpoint

`n_union` and `n_leftover` from `summarize_coverage_union` on
postokhits zeros. Report `covered_a_only` (Distil-only openings) and
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
    root / "2026-09-01-openings-distil100x4-to-12x4" / "coverage.json",
    root / "2026-08-31-openings-short-medium-tails" / "coverage.json",
    root / "2026-09-01-probe-12x4-recount-hard-last4" / "hard" / "holdout.json",
    leftover_holdouts={
        "12loo-hard-last4": root
        / "2026-09-01-probe-12x4-recount-hard-last4"
        / "hard"
        / "holdout.json",
        "distil-postokhits": root
        / "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits"
        / "postokhits"
        / "holdout.json",
    },
    label_a="distil100x4",
    label_b="smt",
)
out = root / "2026-09-01-openings-union-distil100x4-and-smt-to-12x4"
persist_coverage_union(payload, out)
print(print_coverage_union(payload), end="")
PY
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Adding family-12 paraphrases of the original 12 after leftover peeking.
- Changing leftover membership after seeing the union.
- Targeting leftover-15 openings after peeking.
- Leftover-18 Distil rankpath as leftover-file detection.
- Selling union coverage, Distil **22/48**, leftover Distil **3/18**,
  SMT **30/48**, leftover official **18/18**, Distil→Distil **16/48**,
  or Qwen→Qwen **31/48** as replacing **25/48**.
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

## Results

*(empty until the SHA is named in LOGBOOK.md)*
