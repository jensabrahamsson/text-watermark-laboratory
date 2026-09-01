# Isolated-file protocol (Distil occupancy-free leftover-18)

This is a **methods freeze** for occupancy-free DistilGPT2 tables
scoring the original 12 GPT-2 files. It does not add a scorer.
Occupancy-free leftover-18 is closed for more unrelated GPT-2 scenes
([PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md)).
Leftover-18 published key-free GPT-2 readers are exhausted
([PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md)).
The 100 confirmatory prompts already have native Distil twins
(`experiments/2026-09-01-pair-distil-100x4/`). Those prompts were
committed before leftover-18 membership was named. Distil shares GPT-2
BPE. That train is not “more GPT-2 scenes” and it is not leftover
targeting.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at Distil→original-12 occupancy-free LRs or leftover-18
Distil coverage until this freeze is named in [LOGBOOK.md](LOGBOOK.md)
and the analysis commands have been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new `probe --methods`
name. Do not redefine leftover. Do **not** add family-12 paraphrases
of the original 12 after leftover peeking. Do **not** target new train
prompts at leftover-18 openings after peeking leftover-18 stems. Do
**not** re-slice leftover-18 Distil rankpath as leftover-file detection.

Leftover membership stays leftover-union leftover-18 keys. Official
leftover-18 is **18/18** at prefix-128 and uses keys.

## Why freeze now

The remaining occupancy-free question on leftover-18 unique openings is
whether a **different generator** with the same tokenizer, trained on
prompts frozen before leftover peeking, copies any of those openings by
accident. Distil Phase B already exists. Isolated Distil t=0 on the 100
families is **216/400 vs 247/400**; that is not a Distil isolated-file
detector. This freeze scores the original 12 GPT-2 files, not Distil
in-family nested Youden.

## Primary scientific question

Do occupancy-free tables trained on DistilGPT2 100×4, with no detector
keys, `hash_iv`, or g-values, cover leftover-18 original-12 openings,
and does Distil occupancy-free isolated sign on those 12 beat GPT-2
lock B occupancy-free **16/48** or hard **25/48**?

Not: can more GPT-2 scenes copy leftover-18. Not: does Distil leftover
rankpath replace **25/48**. Not: can another `probe --methods` name
lift **25/48**.

## Frozen scorers

Existing readers only. Distil tokenizer (`--model distilgpt2`). Same
BPE as GPT-2 test files. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| B occupancy | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |

`--skip-hashpool` on the probe. Leftover-18 Distil coverage uses
`leftover_keys_from_union`, `summarize_leftover_holdouts`,
`leftover_openings_coverage`, and `summarize_xgen_leftover` in
`src/text_watermark_tools/leftover.py`. Not a `probe --methods` name.

Do **not** run lock A interpolate on Distil twins (PROTOCOL-next Phase B
refused lock A on Distil). Do **not** leftover-slice Distil rankpath as
leftover-file detection.

## Hypotheses (stated before Distil→12 LRs)

- **H-xgen-cover.** Distil occupancy-free leftover-18 coverage is not
  **18/18**. Accidental Distil opening overlap does not exhaust
  leftover-18 unique GPT-2 openings.
- **H-xgen-B.** Distil occupancy-free postokhits t=0 on the original
  12×4 does not beat GPT-2 lock B occupancy-free **16/48** and does not
  beat **25/48**. Isolated observed-token recall equals Distil
  opening-atom overlap.
- **H-xgen-iso.** Distil leftover-18 coverage is not leftover-file
  detection. Do not sell Distil occupancy-free leftover coverage,
  Distil postokhits t=0, Distil poshits nested Youden, leftover official
  **18/18**, leftover-18 rankpath **12/18**, or union **30/48** as
  replacing **25/48**.

## Primary endpoint

Leftover-18 Distil occupancy-free openings coverage
(`n_covered` / 18) and leftover-18 Distil postokhits t=0
(`marked_above_zero` / 18). Report full-file Distil postokhits t=0,
Distil poshits nested Youden, and Distil openings `n_covered` / 48 as
secondary. `used_keys` must be false.

## Corpus

No new `pair`. Train is already-generated Distil 100×4. Test is the
original 12×4 GPT-2 twins. Leftover-18 keys stay the union dump.

| Role | Path |
|---|---|
| Train | `experiments/2026-09-01-pair-distil-100x4/` |
| Test | `experiments/2026-08-17-pair-12x4/` |
| Leftover-18 keys | `experiments/2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/union.json` |
| Probe dump | `experiments/2026-09-01-transfer-distil100x4-to-12x4-opening-poshits/` |
| Openings dump | `experiments/2026-09-01-openings-distil100x4-to-12x4/` |
| Leftover-18 Distil slice | `experiments/2026-09-01-isolated-xgen-leftover-18/` |

## Analysis commands

Do not change flags after the first run. Do not look at test LRs until
the logbook names this SHA.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-distil-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-distil100x4-to-12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-distil-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --model distilgpt2 --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-distil100x4-to-12x4
```

Leftover-18 slice after those dumps exist:

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    persist_xgen_leftover,
    print_xgen_leftover,
    summarize_xgen_leftover,
)

root = Path("experiments")
keys = leftover_keys_from_union(
    root / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4" / "union.json"
)
payload = summarize_xgen_leftover(
    keys,
    holdouts={
        "distil-postokhits": root
        / "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits"
        / "postokhits"
        / "holdout.json",
        "distil-poshits": root
        / "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits"
        / "poshits"
        / "holdout.json",
    },
    openings=root / "2026-09-01-openings-distil100x4-to-12x4" / "coverage.json",
)
out = root / "2026-09-01-isolated-xgen-leftover-18"
persist_xgen_leftover(payload, out)
print(print_xgen_leftover(payload), end="")
PY
```

## What this protocol refuses

- More leftover-18 re-slices of published GPT-2 holdouts sold as
  leftover-file detection, including leftover-18 mask-*k* and leftover-18
  Distil rankpath.
- New occupancy-free GPT-2 trains aimed at leftover-18 openings after
  peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Re-running PROTOCOL-isolated-scale; that protocol is already open.
- Running lock A interpolate on Distil twins.
- Selling Distil leftover-18 occupancy-free coverage, Distil postokhits
  t=0, leftover official **18/18**, leftover-18 rankpath **12/18**, or
  union **30/48** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe and openings commands above once, then the leftover-18
   Distil slice.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

*(empty until the SHA is named in [LOGBOOK.md](LOGBOOK.md).)*
