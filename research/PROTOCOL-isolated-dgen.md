# Isolated-file protocol (Distil 100×4 → Distil 12×4 occupancy-free)

This is a **methods freeze** for occupancy-free DistilGPT2 tables
scoring DistilGPT2 12×4 files. It does not add a scorer. It is the
in-generator analog of [PROTOCOL-isolated.md](PROTOCOL-isolated.md)
for Distil occupancy-free readers. It is **not** leftover-18. Distil
12×4 texts are Distil generations of the original 12 Grok seeds;
leftover-18 keys name GPT-2 files and must not be applied here.

Occupancy-free leftover-18 on the original GPT-2 12 is
[PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md): Distil→GPT-2
postokhits t=0 **22/48**; leftover-18 Distil **3/18** (office). That
does not answer Distil→Distil isolated transfer. PROTOCOL-next refused
lock A interpolate on Distil twins. Distil in-domain 12×4 opening
rankpath is already published (**8/12**, isolated **28/48**). This
freeze does not leftover-slice Distil rankpath.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at Distil→Distil occupancy-free LRs until this freeze
is named in [LOGBOOK.md](LOGBOOK.md) and the analysis commands have
been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new `probe --methods`
name. Do not redefine leftover. Do **not** add family-12 paraphrases
of the original 12 after leftover peeking. Do **not** target leftover-15
openings after peeking. Do **not** apply leftover-18 GPT-2 keys to
Distil 12 files. Do **not** run lock A interpolate on Distil twins.

## Why freeze now

xgen scored Distil tables on GPT-2 files. Isolated observed-token
recall is still opening-atom overlap. The remaining occupancy-free
question that is not leftover targeting is whether Distil 100×4 tables
cover Distil’s own 12×4 openings. Train prompts were committed before
leftover-18 membership was named. Test prompts are the original 12,
disjoint as strings from the 100. Same BPE. Same generator. Not more
unrelated GPT-2 scenes.

## Primary scientific question

Do occupancy-free tables trained on DistilGPT2 100×4, with no detector
keys, `hash_iv`, or g-values, classify DistilGPT2 12×4 finished strings
from disjoint prompts, and does that isolated sign beat hard **25/48**?

Not: leftover-18 GPT-2 coverage. Not: lock A on Distil. Not: another
`probe --methods` name.

## Frozen scorers

Existing readers only. Distil tokenizer (`--model distilgpt2`). No new
method names.

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| B occupancy | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |

`--skip-hashpool` on the probe. Do **not** run lock A. Do **not** leftover-slice Distil rankpath. Do **not** apply leftover-18 keys.

## Hypotheses (stated before Distil→Distil LRs)

- **H-dgen-cover.** Distil occupancy-free coverage on Distil 12×4 is
  not **48/48**. Isolated observed-token recall equals Distil-to-Distil
  opening-atom overlap.
- **H-dgen-B.** Distil→Distil postokhits t=0 does not beat hard
  **25/48**. Distil→GPT-2 occupancy-free **22/48** used different test
  files; a higher Distil→Distil count is not leftover-18 recall.
- **H-dgen-iso.** Distil in-generator occupancy-free transfer is not a
  universal isolated-file detector. Do not sell Distil→Distil t=0,
  Distil poshits nested Youden, Distil→GPT-2 **22/48**, leftover-18
  Distil **3/18**, or leftover official **18/18** as replacing
  **25/48**.

## Primary endpoint

Distil 12×4 occupancy-free postokhits t=0 (`n_positive_above_zero` /
48) and openings `n_covered` / 48. Report Distil poshits nested Youden
as secondary. `used_keys` must be false.

## Corpus

No new `pair`. Train and test already exist.

| Role | Path |
|---|---|
| Train | `experiments/2026-09-01-pair-distil-100x4/` |
| Test | `experiments/2026-08-31-pair-distilgpt2-12x4/` |
| Probe dump | `experiments/2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits/` |
| Openings dump | `experiments/2026-09-01-openings-distil100x4-to-distil12x4/` |

Train prompts: `experiments/2026-09-01-prompts-100/`. Test prompts:
`experiments/2026-08-17-grok-prompts/` (same 12 seeds as GPT-2 12×4).
Those prompt strings are disjoint.

## Analysis commands

Do not change flags after the first run. Do not look at test LRs until
the logbook names this SHA.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-distil-100x4 \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-distil-100x4 \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model distilgpt2 --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-distil100x4-to-distil12x4
```

## What this protocol refuses

- Applying leftover-18 GPT-2 keys to Distil 12 files.
- Leftover-18 re-slices of published GPT-2 holdouts, including
  leftover-18 Distil rankpath.
- Targeting leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Lock A interpolate on Distil twins.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Distil ∪ SMT coverage union without a new freeze before looking.
- Qwen 100×4 → Qwen 12×4 occupancy-free transfer; that is
  [PROTOCOL-isolated-qgen.md](PROTOCOL-isolated-qgen.md), not leftover-18.
- Selling Distil→Distil t=0, Distil poshits, Distil→GPT-2 **22/48**,
  leftover-18 Distil **3/18**, or leftover official **18/18** as
  replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe and openings commands above once.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

Protocol SHA `6bb95a6`. Named `603e2bb`. `used_keys=false`.

Probe: [experiments/2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits/](../experiments/2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits/).
Openings: [experiments/2026-09-01-openings-distil100x4-to-distil12x4/](../experiments/2026-09-01-openings-distil100x4-to-distil12x4/).

| Reader | Distil 12×4 marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|
| Distil→Distil postokhits | **16/48** | **39/48** |
| Distil→Distil poshits | **25/48** | **25/48** |
| Distil→Distil openings postokhits | covered **16/48** (exact 9/48) | decided FP 9 |

H-dgen-cover **holds**. Coverage is **16/48**, not **48/48**. Isolated
observed-token recall equals Distil-to-Distil opening-atom overlap
(covered **16/48**; t=0 **16/48**).

H-dgen-B **holds**. Distil→Distil postokhits t=0 is **16/48 vs 39/48**,
which does not beat hard **25/48**. Distil→GPT-2 occupancy-free was
**22/48** on different test files; same-generator Distil 12 is not
leftover-18 recall and is not denser than that GPT-2 transfer.

H-dgen-iso **holds**. Nested Youden postokhits **48/48 vs 12/48** is a
negative train threshold; do not sell 48/48. Distil poshits **25/48 vs
25/48** includes occupancy; unmarked t=0 is chance. Prompt ranking
**9/12** is not isolated-file detection. Do not sell Distil→Distil **16/48**, Distil poshits **25/48**, Distil nested **48/48**, Distil→GPT-2 **22/48**, leftover-18 Distil **3/18**, or leftover official **18/18** as replacing **25/48**. Isolated-file remains open. Do not write `thesis/`.
