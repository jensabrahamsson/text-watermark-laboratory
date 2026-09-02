# Isolated-file protocol (gpt2-medium occupancy-free leftover-15)

This is a **methods freeze** for occupancy-free gpt2-medium tables
scoring the original 12 GPT-2 files. It does not add a scorer.
Occupancy-free leftover-15 after Distil ∪ SMT is closed for more
unrelated GPT-2 scenes
([PROTOCOL-isolated-leftover-15-closed.md](PROTOCOL-isolated-leftover-15-closed.md)).
Distil occupancy-free leftover-18 on those files is office **3/18**
([PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md)). The 100
confirmatory prompts were committed before leftover membership was
named (`experiments/2026-09-01-prompts-100/`). gpt2-medium shares
GPT-2 BPE (`is_gpt2_name` is true). That train is not "more GPT-2 scenes"
and it is not leftover targeting.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at gpt2-medium→original-12 occupancy-free LRs or
leftover-15 gpt2-medium coverage until this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis commands have been run once,
as written.
Do **not** mix grok12 into any train. Do **not** add a new `probe --methods`
name. Do not redefine leftover. Do **not** add family-12 paraphrases
of the original 12 after leftover peeking. Do **not** target leftover-15
openings after peeking. Do **not** leftover-slice gpt2-medium rankpath
as leftover-file detection. Do **not** run lock A interpolate on
gpt2-medium twins (PROTOCOL-next Phase B refused lock A on Distil;
this freeze stays occupancy-free like xgen).

Leftover membership stays Distil ∪ SMT leftover-15 keys. Official
leftover-15 is **15/15** at prefix-5 and uses keys.

## Why freeze now

Leftover-15 unique openings remain occupancy-free zeros after Distil
and published GPT-2 trains. More unrelated GPT-2 scenes are refused.
Neighborhood paraphrases would target leftover stems after peeking.
The remaining occupancy-free question that is not leftover targeting
is whether a **larger same-BPE generator**, trained on prompts frozen
before leftover peeking, copies any leftover-15 openings by accident.
That is the Distil xgen analog at gpt2-medium, not a new scorer on
12×4.

## Primary scientific question

Do occupancy-free tables trained on gpt2-medium 100×4, with no detector
keys, `hash_iv`, or g-values, cover leftover-15 original-12 openings,
and does gpt2-medium occupancy-free isolated sign on those 12 beat
hard **25/48**?

Not: can more GPT-2 scenes copy leftover-15. Not: does leftover-15
rankpath replace **25/48**. Not: can another `probe --methods` name
lift **25/48**. Not: lock A on gpt2-medium twins.

## Frozen scorers

Existing readers only. gpt2-medium tokenizer (`--model gpt2-medium`).
Same BPE as GPT-2 test files. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| B occupancy | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |

`--skip-hashpool` on the probe. Leftover-15 gpt2-medium coverage uses
`leftover_keys_from_union`, `leftover_openings_coverage`, and
`summarize_mgen_leftover` in `src/text_watermark_tools/leftover.py`.
Not a `probe --methods` name.

Do **not** run lock A interpolate on gpt2-medium twins. Do **not**
leftover-slice gpt2-medium rankpath as leftover-file detection.

## Hypotheses (stated before gpt2-medium→12 LRs)

- **H-mgen-cover.** gpt2-medium occupancy-free leftover-15 coverage is
  not **15/15**. Accidental gpt2-medium opening overlap does not exhaust
  leftover-15 unique GPT-2 openings.
- **H-mgen-B.** gpt2-medium occupancy-free postokhits t=0 on the original
  12×4 does not beat hard **25/48**. Isolated observed-token recall
  equals gpt2-medium opening-atom overlap. A count above Distil
  occupancy-free **22/48** or GPT-2 lock B occupancy-free **16/48** is
  not leftover-15 recall and is not **25/48**.
- **H-mgen-iso.** gpt2-medium leftover-15 coverage is not leftover-file
  detection. Do not sell gpt2-medium occupancy-free leftover coverage,
  gpt2-medium postokhits t=0, gpt2-medium poshits nested Youden,
  leftover official **15/15**, Distil occupancy-free **22/48**, leftover
  Distil **3/18**, Distil→Distil **16/48**, Qwen→Qwen **31/48**, union
  **33/48**, leftover last-4 **9/15**, or leftover-18 official **18/18**
  as replacing **25/48**. Do not target leftover-15 openings after
  peeking.

## Primary endpoint

Leftover-15 gpt2-medium occupancy-free openings coverage
(`n_covered` / 15) and leftover-15 gpt2-medium postokhits t=0
(`marked_above_zero` / 15). Report full-file gpt2-medium postokhits
t=0, gpt2-medium poshits nested Youden, and gpt2-medium openings
`n_covered` / 48 as secondary. `used_keys` must be false.

Official first-draw lamp on the gpt2-medium 100×4 twins is a positive
control (the mixin is on). It is not a key-free endpoint.

## Corpus

New `pair` on already-frozen prompts. Test is the original 12×4 GPT-2
twins. Leftover-15 keys stay the Distil ∪ SMT union dump.

| Role | Path |
|---|---|
| Train prompts | `experiments/2026-09-01-prompts-100/` |
| Train twins | `experiments/2026-09-01-pair-gpt2-medium-100x4/` |
| Test | `experiments/2026-08-17-pair-12x4/` |
| Leftover-15 keys | `experiments/2026-09-01-openings-union-distil100x4-and-smt-to-12x4/union.json` |
| Probe dump | `experiments/2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/` |
| Openings dump | `experiments/2026-09-01-openings-gpt2-medium-100x4-to-12x4/` |
| Leftover-15 gpt2-medium slice | `experiments/2026-09-01-isolated-mgen-leftover-15/` |

Seed `20260901`. `--n-samples 4`. `--max-new-tokens 128`. Local Hugging
Face `gpt2-medium`, not a paid API.

## Analysis commands

Do not change flags after the first run. Do not look at test LRs until
the logbook names this SHA.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model gpt2-medium --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-gpt2-medium-100x4

python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-gpt2-medium-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --model gpt2-medium --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-gpt2-medium-100x4-to-12x4
```

Leftover-15 slice after those dumps exist:

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    persist_mgen_leftover,
    print_mgen_leftover,
    summarize_mgen_leftover,
)

root = Path("experiments")
keys = leftover_keys_from_union(
    root / "2026-09-01-openings-union-distil100x4-and-smt-to-12x4" / "union.json"
)
payload = summarize_mgen_leftover(
    keys,
    holdouts={
        "medium-postokhits": root
        / "2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits"
        / "postokhits"
        / "holdout.json",
        "medium-poshits": root
        / "2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits"
        / "poshits"
        / "holdout.json",
    },
    openings=root / "2026-09-01-openings-gpt2-medium-100x4-to-12x4" / "coverage.json",
)
out = root / "2026-09-01-isolated-mgen-leftover-15"
persist_mgen_leftover(payload, out)
print(print_mgen_leftover(payload), end="")
PY
```

## What this protocol refuses

- More unrelated GPT-2 occupancy-free scenes for leftover-15.
- New occupancy-free trains aimed at leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Leftover-15 re-slices of published holdouts sold as leftover-file
  detection, including leftover-15 rankpath, leftover-15 interpolate,
  and leftover-15 mask-*k*.
- Leftover-slice gpt2-medium rankpath as leftover-file detection.
- Lock A interpolate on gpt2-medium twins.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Scoring GPT-2 leftover-15 with the Qwen tokenizer.
- Re-running PROTOCOL-isolated-scale; that protocol is already open.
- Selling leftover official **15/15**, union **33/48**, leftover last-4
  **9/15**, Distil occupancy-free **22/48**, leftover Distil **3/18**,
  Distil→Distil **16/48**, or Qwen→Qwen **31/48** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the pair, probe, and openings commands above once, then the
   leftover-15 gpt2-medium slice.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

Protocol SHA `cc9c4ca`. Named `883532b`. Official first-draw lamp on
the gpt2-medium 100×4 twins is **100/100**. `used_keys=false`.

Dump: [experiments/2026-09-01-isolated-mgen-leftover-15/](../experiments/2026-09-01-isolated-mgen-leftover-15/).
Probe: [experiments/2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/](../experiments/2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/).
Openings: [experiments/2026-09-01-openings-gpt2-medium-100x4-to-12x4/](../experiments/2026-09-01-openings-gpt2-medium-100x4-to-12x4/).

| Reader | Full 48 marked `lr>0` | Unmarked `lr≤0` | Leftover-15 marked `lr>0` | Leftover-15 unmarked `lr≤0` |
|---|---|---|---|---|
| gpt2-medium postokhits | **16/48** | **48/48** | **0/15** | **15/15** |
| gpt2-medium poshits | **39/48** | **41/48** | **9/15** | **12/15** |
| gpt2-medium openings postokhits | covered **16/48** (exact 14/48) | decided FP 0 | leftover covered **0/15** | leftover uncovered **15/15** |

H-mgen-cover **holds**. gpt2-medium occupancy-free leftover-15 coverage
is **0/15**, not **15/15**. Accidental gpt2-medium opening overlap did
not copy leftover-15 unique GPT-2 openings. Remaining leftover-15 is
still harbour 1–4, library 1–4, station-4, letter 2–3, ferry-queue 1–4.
Do not target those openings after peeking.

H-mgen-B **holds**. Occupancy-free postokhits t=0 is **16/48 vs 48/48**.
That equals gpt2-medium opening-atom overlap (**16/48** covered; exact
**14/48**; decided 16 TP / 0 FP), equals GPT-2 lock B occupancy-free
**16/48**, stays below Distil occupancy-free **22/48**, and does not
beat hard **25/48**. Nested Youden **15/48 vs 48/48** used a train
threshold ≈ 1.13; do not sell 15/48. Prompt ranking on postokhits is
**7/12** strict, with **5 ties** at 0=0 (harbour, night-bus, letter,
garden, ferry-queue). Historical `>=` would print 12/12. Do not sell
**7/12**, **12/12**, **16/48**, or **39/48**.

H-mgen-iso **holds**. Leftover-15 gpt2-medium coverage is **0/15**.
Occupancy-free leftover sign is **0/15 vs 15/15**. That is not
leftover-file detection. Official leftover-15 **15/15** uses keys. Do
not sell leftover official **15/15**, Distil occupancy-free **22/48**,
leftover Distil **3/18**, Distil→Distil **16/48**, gpt2-medium
**16/48**, or leftover **0/15** as replacing **25/48**. Isolated-file
detection is still not finished. Distil↔gpt2-medium occupancy-free
transfer is [PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md):
Distil→gpt2-medium **20/48**, gpt2-medium→Distil **3/48**. The remaining
confirmatory remasure is [PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md).
Do not write `thesis/`.
