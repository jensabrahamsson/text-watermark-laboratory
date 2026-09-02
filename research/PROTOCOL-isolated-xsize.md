# Isolated-file protocol (Distil ↔ gpt2-medium occupancy-free)

This is a **methods freeze** for occupancy-free DistilGPT2 tables
scoring gpt2-medium 12×4 files, and occupancy-free gpt2-medium tables
scoring DistilGPT2 12×4 files. It does not add a scorer. It is the
cross-size analog of [PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md)
and [PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md). Same GPT-2
BPE. Different generator sizes. It is **not** leftover-15 and **not**
leftover-18. Distil 12×4 and gpt2-medium 12×4 texts are Distil and
gpt2-medium generations of the original 12 Grok seeds. Leftover-15 and
leftover-18 keys name GPT-2 files and must not be applied here.

In-generator occupancy-free already exists: Distil→Distil **16/48**
equals coverage **16/48**; gpt2-medium→gpt2-medium **10/48** with
coverage **13/48**. Distil→GPT-2 leftover-18 was **3/18**; gpt2-medium→GPT-2
leftover-15 was **0/15**. Those do not answer whether occupancy atoms
copy across GPT-2 family sizes on the already-frozen 12×4 twins.
PROTOCOL-next refused lock A interpolate on Distil twins; this freeze
stays occupancy-free like dgen and m12. Do **not** leftover-slice Distil
or gpt2-medium rankpath. Do **not** freeze a Distil ∪ gpt2-medium union
in this file.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at Distil→gpt2-medium or gpt2-medium→Distil occupancy-free
LRs until this freeze is named in [LOGBOOK.md](LOGBOOK.md) and the
analysis commands have been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new `probe --methods`
name. Do not redefine leftover. Do **not** add family-12 paraphrases
of the original 12 after leftover peeking. Do **not** target leftover-15
openings after peeking. Do **not** apply leftover-15 or leftover-18 GPT-2
keys to Distil 12 or gpt2-medium 12 files. Do **not** run lock A interpolate
on Distil or gpt2-medium twins.

## Why freeze now

m12 scored gpt2-medium tables on gpt2-medium 12×4 files. Occupancy-free
t=0 was **10/48**. Distil→Distil was **16/48**. Isolated observed-token
recall is still opening-atom overlap. The remaining occupancy-free
question that is not leftover targeting is whether those same tables
cover the *other* generator’s 12×4 openings. Train prompts were
committed before leftover membership was named. Test prompts are the
original 12, disjoint as strings from the 100. Same BPE. Already-frozen
twins. Not more unrelated GPT-2 scenes. Not a leftover-15 re-slice.
Not a Distil ∪ gpt2-medium union after peeking.

## Primary scientific question

Do occupancy-free tables trained on DistilGPT2 100×4, with no detector
keys, `hash_iv`, or g-values, classify gpt2-medium 12×4 finished strings
from disjoint prompts, and do occupancy-free tables trained on
gpt2-medium 100×4 classify DistilGPT2 12×4 finished strings, and does
either isolated sign beat hard **25/48**?

Not: leftover-15 GPT-2 coverage. Not: leftover-18 Distil coverage.
Not: lock A on Distil or gpt2-medium. Not: another `probe --methods`
name. Not: leftover-slice Distil or gpt2-medium rankpath. Not: Distil ∪
gpt2-medium opening union.

## Frozen scorers

Existing readers only. Distil tokenizer (`--model distilgpt2`) on the
Distil train arm. gpt2-medium tokenizer (`--model gpt2-medium`) on the
gpt2-medium train arm. Same BPE as each other and as GPT-2. No new
method names.

| Arm | Train | Test | `--model` |
|---|---|---|---|
| Distil→medium | Distil 100×4 | gpt2-medium 12×4 | `distilgpt2` |
| medium→Distil | gpt2-medium 100×4 | Distil 12×4 | `gpt2-medium` |

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| B occupancy | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |

`--skip-hashpool` on the probe. Do **not** run lock A. Do **not** leftover-slice Distil or gpt2-medium rankpath. Do **not** apply leftover-15 or leftover-18 keys. Do **not** mix the two trains.

## Hypotheses (stated before Distil↔gpt2-medium LRs)

- **H-xsize-cover.** Occupancy-free coverage on each arm is not
  **48/48**. Isolated observed-token recall equals that arm’s
  opening-atom overlap.
- **H-xsize-B.** Distil→gpt2-medium postokhits t=0 does not beat hard
  **25/48**. gpt2-medium→Distil postokhits t=0 does not beat hard
  **25/48**. Distil→Distil **16/48**, gpt2-medium→gpt2-medium **10/48**,
  Distil→GPT-2 **22/48**, and gpt2-medium→GPT-2 **16/48** used different
  test files; a higher cross-size count is not leftover-15 recall and is
  not leftover-18 recall.
- **H-xsize-iso.** Cross-size occupancy-free transfer is not a
  universal isolated-file detector. Do not sell Distil→gpt2-medium t=0,
  gpt2-medium→Distil t=0, either arm’s poshits nested Youden, Distil→Distil
  **16/48**, gpt2-medium→gpt2-medium **10/48**, Distil→GPT-2 **22/48**,
  leftover Distil **3/18**, gpt2-medium→GPT-2 **16/48**, leftover-15
  **0/15**, leftover official **15/15**, or Qwen→Qwen **31/48** as
  replacing **25/48**. Do not apply leftover-15 or leftover-18 keys to
  Distil 12 or gpt2-medium 12 files. Do not target leftover-15 openings
  after peeking. Do not freeze Distil ∪ gpt2-medium union in this file.

## Primary endpoint

Each arm’s occupancy-free postokhits t=0 (`n_positive_above_zero` / 48)
and openings `n_covered` / 48. Report poshits nested Youden as
secondary. `used_keys` must be false.

Official first-draw lamp on Distil 12×4 and gpt2-medium 12×4 is already
opened (mixin on). It is not a key-free endpoint of this freeze.

## Corpus

No new `pair`. All four corpora already exist.

| Role | Path |
|---|---|
| Distil train | `experiments/2026-09-01-pair-distil-100x4/` |
| gpt2-medium train | `experiments/2026-09-01-pair-gpt2-medium-100x4/` |
| Distil test | `experiments/2026-08-31-pair-distilgpt2-12x4/` |
| gpt2-medium test | `experiments/2026-09-01-pair-gpt2-medium-12x4/` |
| Distil→medium probe | `experiments/2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits/` |
| Distil→medium openings | `experiments/2026-09-01-openings-distil100x4-to-medium12x4/` |
| medium→Distil probe | `experiments/2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits/` |
| medium→Distil openings | `experiments/2026-09-01-openings-gpt2-medium-100x4-to-distil12x4/` |

Train prompts: `experiments/2026-09-01-prompts-100/`. Test prompts:
`experiments/2026-08-17-grok-prompts/` (same 12 seeds as GPT-2 12×4).
Those prompt strings are disjoint.

## Analysis commands

Do not change flags after the first run. Do not look at test LRs until
the logbook names this SHA.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-distil-100x4 \
  --test-dir experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-distil-100x4 \
  --test-dir experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model distilgpt2 --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-distil100x4-to-medium12x4

python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-100x4 \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-gpt2-medium-100x4 \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model gpt2-medium --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-gpt2-medium-100x4-to-distil12x4
```

## What this protocol refuses

- Applying leftover-15 or leftover-18 GPT-2 keys to Distil 12 or
  gpt2-medium 12 files.
- Leftover-15 or leftover-18 re-slices of published GPT-2 holdouts,
  including leftover Distil or gpt2-medium rankpath.
- Targeting leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Distil ∪ gpt2-medium opening union in this freeze.
- Mixing Distil 12×4 or gpt2-medium 12×4 twins into either 100×4 train.
- Lock A interpolate on Distil or gpt2-medium twins.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Scoring leftover-15 GPT-2 files as leftover-file detection under
  this freeze; that analog is already
  [PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md).
- Scoring leftover-18 GPT-2 files as leftover-file detection under
  this freeze; that analog is already
  [PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md).
- Selling Distil→gpt2-medium t=0, gpt2-medium→Distil t=0, either
  poshits nested Youden, Distil→Distil **16/48**, gpt2-medium→gpt2-medium
  **10/48**, Distil→GPT-2 **22/48**, leftover Distil **3/18**,
  gpt2-medium→GPT-2 **16/48**, leftover **0/15**, leftover official
  **15/15**, or Qwen→Qwen **31/48** as replacing **25/48**.
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

Protocol SHA `3bb8430`. Named `fbf2cb5`. `used_keys=false`. Same BPE.
Already-frozen twins. Local Hugging Face DistilGPT2 and gpt2-medium, not
a paid API.

Distil→medium probe: [experiments/2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits/](../experiments/2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits/).
Distil→medium openings: [experiments/2026-09-01-openings-distil100x4-to-medium12x4/](../experiments/2026-09-01-openings-distil100x4-to-medium12x4/).
medium→Distil probe: [experiments/2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits/](../experiments/2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits/).
medium→Distil openings: [experiments/2026-09-01-openings-gpt2-medium-100x4-to-distil12x4/](../experiments/2026-09-01-openings-gpt2-medium-100x4-to-distil12x4/).

| Reader | Test files | marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|---|
| Distil→gpt2-medium postokhits | gpt2-medium 12×4 | **20/48** | **48/48** |
| Distil→gpt2-medium poshits | gpt2-medium 12×4 | **42/48** | **26/48** |
| Distil→gpt2-medium openings postokhits | gpt2-medium 12×4 | covered **22/48** (exact 4/48) | decided FP 0 |
| gpt2-medium→Distil postokhits | Distil 12×4 | **3/48** | **47/48** |
| gpt2-medium→Distil poshits | Distil 12×4 | **11/48** | **39/48** |
| gpt2-medium→Distil openings postokhits | Distil 12×4 | covered **5/48** (exact 2/48) | decided FP 1 |

H-xsize-cover **holds** on coverage not **48/48**. Distil→gpt2-medium
coverage is **22/48**. Isolated t=0 is **20/48**, below coverage: two
covered files have negative observed-token LR. Exact 4-token copies are
**4/48**. gpt2-medium→Distil coverage is **5/48**. Isolated t=0 is
**3/48**, below coverage. Exact copies are **2/48**. Recall is bounded
by opening overlap on each arm; it is not **48/48**.

H-xsize-B **holds**. Distil→gpt2-medium postokhits t=0 is **20/48 vs
48/48**, which does not beat hard **25/48**. gpt2-medium→Distil
postokhits t=0 is **3/48 vs 47/48**, which does not beat hard **25/48**.
Distil→Distil occupancy-free was **16/48** on Distil files.
gpt2-medium→gpt2-medium was **10/48** on gpt2-medium files. Distil→GPT-2
was **22/48** on original-12 GPT-2 files. gpt2-medium→GPT-2 was
**16/48** on original-12 GPT-2 files. Distil→gpt2-medium **20/48** is
denser than Distil→Distil **16/48** and gpt2-medium→gpt2-medium
**10/48** on different test files; that is not leftover-15 recall and is
not leftover-18 recall. Nested Youden Distil→gpt2-medium **46/48 vs
11/48** is a negative train threshold ≈ −0.003; do not sell 46/48.
Nested Youden gpt2-medium→Distil **3/48 vs 48/48** at a train threshold
≈ 1.13. Prompt ranking Distil→gpt2-medium postokhits is **11/12**
strict with **1 tie** (garden) and four ranking wins with 0 isolated TPs
(harbour, night-bus, letter, ferry-queue). Historical `>=` would print
12/12. Prompt ranking gpt2-medium→Distil postokhits is **6/12** strict
with **6 ties**; historical `>=` would print 12/12. Do not sell
**20/48**, **22/48**, **11/12**, **12/12**, **3/48**, **5/48**,
**6/12**, **42/48**, or **46/48**.

H-xsize-iso **holds**. These are Distil 12×4 and gpt2-medium 12×4 files,
not the original GPT-2 12. Do not apply leftover-15 or leftover-18 GPT-2
keys here. Do not freeze Distil ∪ gpt2-medium union after peeking. Do not sell Distil→gpt2-medium **20/48**, coverage **22/48**, nested
**46/48**, gpt2-medium→Distil **3/48**, coverage **5/48**, Distil→Distil
**16/48**, gpt2-medium→gpt2-medium **10/48**, Distil→GPT-2 **22/48**,
leftover Distil **3/18**, gpt2-medium→GPT-2 **16/48**, leftover **0/15**,
leftover official **15/15**, or Qwen→Qwen **31/48** as replacing
**25/48**. Isolated-file remains open. Absolute-history H2 is opened in
[PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): 0:4 **99/100** vs
16:32 **87/100**. Second-key in-domain lock A is opened in
[PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md): interpolate
**7/12**, isolated **30/48 vs 25/48**. H-xkey-iso **fails** as a raw
count. Do not sell **30/48**. The remaining honesty item that is not leftover
targeting is [PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md):
absolute-history remasure of 100→grok12 interpolate windows. Reindexed
dumps stay (0:4 **7/12**; tail **9/12**). Do not overwrite them.
Isolated-file remains open. Do not write `thesis/`.
