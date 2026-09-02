# Isolated-file protocol (gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free)

This is a **methods freeze** for occupancy-free gpt2-medium tables
scoring gpt2-medium 12×4 files. It does not add a scorer. It is the
in-generator analog of [PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md)
at gpt2-medium. It is **not** leftover-15. gpt2-medium 12×4 texts are
gpt2-medium generations of the original 12 Grok seeds. Leftover-15 keys
name GPT-2 files and must not be applied here.

Occupancy-free leftover-15 on the original GPT-2 12 is
[PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md): leftover
coverage **0/15**; gpt2-medium→GPT-2 postokhits t=0 **16/48**. That
does not answer gpt2-medium→gpt2-medium isolated transfer.
PROTOCOL-next refused lock A interpolate on Distil/Qwen twins; this
freeze stays occupancy-free like dgen. Do **not** leftover-slice
gpt2-medium rankpath as leftover-file detection.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at gpt2-medium→gpt2-medium occupancy-free LRs until
this freeze is named in [LOGBOOK.md](LOGBOOK.md) and the analysis
commands have been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new `probe --methods`
name. Do not redefine leftover. Do **not** add family-12 paraphrases
of the original 12 after leftover peeking. Do **not** target leftover-15
openings after peeking. Do **not** apply leftover-15 GPT-2 keys to
gpt2-medium 12 files. Do **not** run lock A interpolate on gpt2-medium
twins.

## Why freeze now

mgen scored gpt2-medium tables on GPT-2 files. Leftover-15 coverage
was **0/15**. Isolated observed-token recall is still opening-atom
overlap. Distil→Distil occupancy-free was **16/48** equals coverage
**16/48**. The remaining occupancy-free question that is not leftover
targeting is whether gpt2-medium 100×4 tables cover gpt2-medium’s own
12×4 openings. Train prompts were committed before leftover membership
was named. Test prompts are the original 12, disjoint as strings from
the 100. Same BPE. Same generator. Not more unrelated GPT-2 scenes.
Not a leftover-15 re-slice.

## Primary scientific question

Do occupancy-free tables trained on gpt2-medium 100×4, with no detector
keys, `hash_iv`, or g-values, classify gpt2-medium 12×4 finished
strings from disjoint prompts, and does that isolated sign beat hard
**25/48**?

Not: leftover-15 GPT-2 coverage. Not: lock A on gpt2-medium. Not:
another `probe --methods` name. Not: leftover-slice gpt2-medium
rankpath.

## Frozen scorers

Existing readers only. gpt2-medium tokenizer (`--model gpt2-medium`).
Same BPE as GPT-2. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| B occupancy | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |

`--skip-hashpool` on the probe. Do **not** run lock A. Do **not** leftover-slice gpt2-medium rankpath. Do **not** apply leftover-15 keys.

## Hypotheses (stated before gpt2-medium→gpt2-medium LRs)

- **H-m12-cover.** gpt2-medium occupancy-free coverage on gpt2-medium
  12×4 is not **48/48**. Isolated observed-token recall equals
  gpt2-medium-to-gpt2-medium opening-atom overlap.
- **H-m12-B.** gpt2-medium→gpt2-medium postokhits t=0 does not beat
  hard **25/48**. Distil→Distil occupancy-free **16/48** and
  gpt2-medium→GPT-2 occupancy-free **16/48** used different test files;
  a higher gpt2-medium→gpt2-medium count is not leftover-15 recall and
  is not Distil→Distil.
- **H-m12-iso.** gpt2-medium in-generator occupancy-free transfer is
  not a universal isolated-file detector. Do not sell
  gpt2-medium→gpt2-medium t=0, gpt2-medium poshits nested Youden,
  gpt2-medium→GPT-2 **16/48**, leftover-15 coverage **0/15**, leftover
  official **15/15**, Distil→Distil **16/48**, Distil→GPT-2 **22/48**,
  leftover Distil **3/18**, or Qwen→Qwen **31/48** as replacing
  **25/48**. Do not apply leftover-15 keys to gpt2-medium 12 files. Do
  not target leftover-15 openings after peeking.

## Primary endpoint

gpt2-medium 12×4 occupancy-free postokhits t=0 (`n_positive_above_zero`
/ 48) and openings `n_covered` / 48. Report gpt2-medium poshits nested
Youden as secondary. `used_keys` must be false.

Official first-draw lamp on the gpt2-medium 12×4 twins is a positive
control (the mixin is on). It is not a key-free endpoint.

## Corpus

New `pair` on already-frozen original-12 prompts. Train already exists.
Local Hugging Face `gpt2-medium`, not a paid API.

| Role | Path |
|---|---|
| Train prompts | `experiments/2026-09-01-prompts-100/` |
| Train twins | `experiments/2026-09-01-pair-gpt2-medium-100x4/` |
| Test prompts | `experiments/2026-08-17-grok-prompts/` |
| Test twins | `experiments/2026-09-01-pair-gpt2-medium-12x4/` |
| Probe dump | `experiments/2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/` |
| Openings dump | `experiments/2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/` |

Train and test prompt strings are disjoint. Seed `20260901` (same as
gpt2-medium 100×4; not Distil 12×4 seed `20260831`). `--n-samples 4`.
`--max-new-tokens 128`.

## Analysis commands

Do not change flags after the first run. Do not look at test LRs until
the logbook names this SHA. Official first-draw scores on the new pair
are a positive control and may be checked.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model gpt2-medium --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-gpt2-medium-12x4

python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-100x4 \
  --test-dir experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-gpt2-medium-100x4 \
  --test-dir experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model gpt2-medium --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-gpt2-medium-100x4-to-medium12x4
```

## What this protocol refuses

- Applying leftover-15 GPT-2 keys to gpt2-medium 12 files.
- Leftover-15 re-slices of published GPT-2 holdouts, including
  leftover-15 gpt2-medium rankpath.
- Targeting leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Mixing the new gpt2-medium 12×4 twins into the 100×4 train.
- Lock A interpolate on gpt2-medium twins.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Scoring leftover-15 GPT-2 files as leftover-file detection under
  this freeze; that analog is already
  [PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md).
- Selling gpt2-medium→gpt2-medium t=0, gpt2-medium poshits,
  gpt2-medium→GPT-2 **16/48**, leftover **0/15**, leftover official
  **15/15**, Distil→Distil **16/48**, Distil→GPT-2 **22/48**, leftover
  Distil **3/18**, or Qwen→Qwen **31/48** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the pair, probe, and openings commands above once.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

Protocol SHA `5be70f3`. Named `3610cef`. Official first-draw lamp on
the gpt2-medium 12×4 twins is **12/12**. `used_keys=false`. Local
Hugging Face gpt2-medium, not a paid API.

Probe: [experiments/2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/](../experiments/2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/).
Openings: [experiments/2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/](../experiments/2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/).
Pair: [experiments/2026-09-01-pair-gpt2-medium-12x4/](../experiments/2026-09-01-pair-gpt2-medium-12x4/).

| Reader | gpt2-medium 12×4 marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|
| gpt2-medium→gpt2-medium postokhits | **10/48** | **48/48** |
| gpt2-medium→gpt2-medium poshits | **39/48** | **41/48** |
| gpt2-medium→gpt2-medium openings postokhits | covered **13/48** (exact 10/48) | decided FP 0 |

H-m12-cover **holds** on coverage not **48/48**. Coverage is **13/48**.
Isolated t=0 is **10/48**, below coverage: three covered files have
negative observed-token LR. Recall is bounded by opening overlap on
this split; it is not equal to **13/48**. Exact 4-token copies are
**10/48**.

H-m12-B **holds**. gpt2-medium→gpt2-medium postokhits t=0 is **10/48 vs
48/48**, which does not beat hard **25/48**. Distil→Distil occupancy-free
was **16/48** on Distil files. gpt2-medium→GPT-2 occupancy-free was
**16/48** on original-12 GPT-2 files. Same-generator gpt2-medium 12 is
not leftover-15 recall and is not denser than those transfers. Nested
Youden postokhits **10/48 vs 48/48** at a train threshold ≈ 1.13; do
not sell 10/48 as a Youden win. Prompt ranking on postokhits is
**8/12** strict, with **3 ties** (harbour, night-bus, ferry-queue) and
four ranking wins with 0 isolated TPs (library, market, workshop,
garden). Historical `>=` would print 11/12. Do not sell **8/12**,
**11/12**, **10/48**, or **39/48**.

H-m12-iso **holds**. These are gpt2-medium 12×4 files, not the original
GPT-2 12. Do not apply leftover-15 GPT-2 keys here. Do not sell gpt2-medium→gpt2-medium **10/48**, coverage **13/48**, nested **10/48 vs 48/48**, gpt2-medium poshits **39/48**, gpt2-medium→GPT-2 **16/48**, leftover **0/15**, leftover official **15/15**, Distil→Distil **16/48**, Distil→GPT-2 **22/48**, leftover Distil **3/18**, Qwen→Qwen **31/48**, or official **12/12** as replacing **25/48**. Isolated-file remains open. Distil↔gpt2-medium occupancy-free transfer is opened in [PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md): Distil→gpt2-medium **20/48**, gpt2-medium→Distil **3/48**. Absolute-history H2 is opened in [PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): 0:4 **99/100** vs 16:32 **87/100**. Second-key in-domain lock A is opened in [PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md). Opened: interpolate **7/12**, isolated **30/48 vs 25/48**. H-xkey-iso **fails** as a raw count. Do not sell **30/48**. Absolute-history OOD windows are opened in [PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md): grok12 0:4 **7/12**; 32:64 **10/12** (rose versus reindexed **9/12**). Do not sell absolute **10/12**. The remaining honesty item that is not leftover targeting is 12-LOO mask-*k* absolute remasure of [PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md) (those dumps stay reindexed). Do not write `thesis/`.
