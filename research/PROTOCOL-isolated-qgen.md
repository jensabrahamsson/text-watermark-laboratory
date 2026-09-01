# Isolated-file protocol (Qwen 100×4 → Qwen 12×4 occupancy-free)

This is a **methods freeze** for occupancy-free Qwen2-1.5B-Instruct
tables scoring Qwen 12×4 files. It does not add a scorer. It is the
in-generator analog of [PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md)
for Qwen. It is **not** leftover-18. Qwen 12×4 texts are Qwen
generations of the original 12 Grok seeds. Leftover-18 keys name GPT-2
files. Scoring those GPT-2 files with a Qwen tokenizer is a mismatch,
not a detector ([key-free-contrast.md](key-free-contrast.md)). Do not
apply leftover-18 keys here.

Distil→Distil occupancy-free is
[PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md): t=0 **16/48**
equals coverage **16/48**. Distil→GPT-2 leftover-18 is
[PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md). PROTOCOL-next
refused lock A interpolate on Qwen twins. Qwen in-domain first-token
opening is already published (**12/12**); this freeze does **not** use
`--include-first`. Occupancy-free postokhits starts at generated token
1, like Distil dgen.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at Qwen→Qwen occupancy-free LRs until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis commands have been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new `probe --methods`
name. Do not redefine leftover. Do **not** add family-12 paraphrases.
Do **not** target leftover-15 openings after peeking. Do **not** apply
leftover-18 GPT-2 keys to Qwen 12 files. Do **not** run lock A
interpolate on Qwen twins. Do **not** score GPT-2 files with the Qwen
tokenizer as leftover-file detection.

## Why freeze now

dgen asked whether Distil 100×4 copies Distil 12×4 openings. Coverage
was **16/48**, not denser than Distil→GPT-2 occupancy-free **22/48**.
The remaining in-generator occupancy-free question that is not leftover
targeting is Qwen: same 100 prompts, native tokenizer, Qwen 12×4 test
files. Train prompts were committed before leftover-18 membership was
named. Test prompts are the original 12, disjoint as strings from the
100. Not more unrelated GPT-2 scenes. Not a GPT-2 leftover-18 re-slice.

## Primary scientific question

Do occupancy-free tables trained on Qwen2-1.5B-Instruct 100×4, with no
detector keys, `hash_iv`, or g-values, classify Qwen 12×4 finished
strings from disjoint prompts, and does that isolated sign beat hard
**25/48**?

Not: leftover-18 GPT-2 coverage. Not: lock A on Qwen. Not: Qwen tables
on GPT-2 files. Not: another `probe --methods` name. Not:
`--include-first` first-token 12/12.

## Frozen scorers

Existing readers only. Qwen tokenizer
(`--model Qwen/Qwen2-1.5B-Instruct`). No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| B occupancy-free | Opening postokhits | `--methods postokhits --fit-prefix 4 --pos-bucket 1` |
| B occupancy | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| openings | Opening-overlap bound | `--methods postokhits --skip-stem-curve` |

`--skip-hashpool` on the probe. Do **not** run lock A. Do **not** use `--include-first`. Do **not** leftover-slice Qwen rankpath as leftover-18 GPT-2 detection. Do **not** apply leftover-18 keys.

## Hypotheses (stated before Qwen→Qwen LRs)

- **H-qgen-cover.** Qwen occupancy-free coverage on Qwen 12×4 is not
  **48/48**. Isolated observed-token recall equals Qwen-to-Qwen
  opening-atom overlap.
- **H-qgen-B.** Qwen→Qwen postokhits t=0 does not beat hard **25/48**.
  Distil→Distil occupancy-free **16/48** used different files and a
  different tokenizer; a higher Qwen→Qwen count is not leftover-18
  recall and is not Distil→Distil.
- **H-qgen-iso.** Qwen in-generator occupancy-free transfer is not a
  universal isolated-file detector. Do not sell Qwen→Qwen t=0, Qwen
  poshits nested Youden, Qwen in-domain first **12/12**, Distil→Distil
  **16/48**, Distil→GPT-2 **22/48**, leftover-18 Distil **3/18**, or
  leftover official **18/18** as replacing **25/48**.

## Primary endpoint

Qwen 12×4 occupancy-free postokhits t=0 (`n_positive_above_zero` / 48)
and openings `n_covered` / 48. Report Qwen poshits nested Youden as
secondary. `used_keys` must be false.

## Corpus

No new `pair`. Train and test already exist. Local Hugging Face Qwen,
not Dashscope.

| Role | Path |
|---|---|
| Train | `experiments/2026-09-01-pair-qwen-100x4/` |
| Test | `experiments/2026-08-31-pair-qwen-12x4/` |
| Probe dump | `experiments/2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits/` |
| Openings dump | `experiments/2026-09-01-openings-qwen100x4-to-qwen12x4/` |

Train prompts: `experiments/2026-09-01-prompts-100/`. Test prompts:
`experiments/2026-08-17-grok-prompts/`. Those prompt strings are
disjoint.

## Analysis commands

Do not change flags after the first run. Do not look at test LRs until
the logbook names this SHA.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-qwen-100x4 \
  --test-dir experiments/2026-08-31-pair-qwen-12x4 \
  --model Qwen/Qwen2-1.5B-Instruct --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits \
  --out-dir experiments/2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits

python -m text_watermark_tools openings experiments/2026-09-01-pair-qwen-100x4 \
  --test-dir experiments/2026-08-31-pair-qwen-12x4 \
  --model Qwen/Qwen2-1.5B-Instruct --skip-stem-curve \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits \
  --out-dir experiments/2026-09-01-openings-qwen100x4-to-qwen12x4
```

## What this protocol refuses

- Applying leftover-18 GPT-2 keys to Qwen 12 files.
- Scoring GPT-2 leftover-18 with the Qwen tokenizer.
- Leftover-18 re-slices of published GPT-2 holdouts.
- Targeting leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Lock A interpolate on Qwen twins.
- `--include-first` on this transfer.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Mixing grok12 into any train.
- Distil ∪ SMT coverage union except as
  [PROTOCOL-isolated-dsmt.md](PROTOCOL-isolated-dsmt.md), frozen before
  leftover-after-union counts.
- Paid chat APIs, including Dashscope `qwen-plus`.
- Selling Qwen→Qwen t=0, Qwen poshits, Qwen first **12/12**,
  Distil→Distil **16/48**, Distil→GPT-2 **22/48**, leftover-18 Distil
  **3/18**, or leftover official **18/18** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe and openings commands above once.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

Protocol SHA `3c0a5c9`. Named `c3964ea`. `used_keys=false`. Local
Hugging Face Qwen, not Dashscope.

Probe: [experiments/2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits/](../experiments/2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits/).
Openings: [experiments/2026-09-01-openings-qwen100x4-to-qwen12x4/](../experiments/2026-09-01-openings-qwen100x4-to-qwen12x4/).

| Reader | Qwen 12×4 marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|
| Qwen→Qwen postokhits | **31/48** | **48/48** |
| Qwen→Qwen poshits | **33/48** | **37/48** |
| Qwen→Qwen openings postokhits | covered **37/48** (exact 12/48) | decided FP 0 |

H-qgen-cover **holds** on coverage not **48/48**. Coverage is **37/48**.
Isolated t=0 is **31/48**, below coverage: six covered files have
negative observed-token LR. Recall is bounded by opening overlap on
this split; it is not equal to **37/48**.

H-qgen-B **fails** as a raw marked count on these Qwen files:
**31/48** > **25/48**. That is a cross-corpus comparison. Distil→Distil
occupancy-free was **16/48** on Distil files. Nested Youden postokhits
**31/48 vs 48/48** at a positive train threshold (≈ 0.022). Unmarked
t=0 is **48/48**. Decided precision **1.000**.

H-qgen-iso **holds**. These are Qwen 12×4 files, not the original GPT-2
12. Do not sell Qwen→Qwen **31/48**, coverage **37/48**, nested
**31/48 vs 48/48**, Qwen poshits **33/48**, Qwen first **12/12**,
Distil→Distil **16/48**, Distil→GPT-2 **22/48**, leftover-18 Distil
**3/18**, or leftover official **18/18** as replacing **25/48**.
Isolated-file remains open. Do not write `thesis/`.
