# Confirmatory protocol (absolute-history H2)

This is a **methods freeze** for a bug-fix remasure of PROTOCOL-next
**H2**. It does not add a scorer. The committed 100×4 window dump
(`experiments/2026-09-01-probe-100x4-hard-windows/`) scored each
`--windows` slice as a **reindexed** substring. Probe now passes
absolute `score_span` and keeps preceding tokens as context
([`blind.py`](../src/text_watermark_tools/blind.py)
`likelihood_ratio`; [`transfer.py`](../src/text_watermark_tools/transfer.py)
`score_sequence`). Until this remasure, do not sell “the in-family
signal is front-loaded / does not accumulate.” Out-of-family interpolate
windows on Grok-length files are already **not** front-loaded
([PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md): 0:4
**7/12**; tail **9/12**).

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Reindexed H2 **0:4** **99/100** vs **16:32**
**89/100** stays in that historical dump. Do **not** overwrite it.
Do **not** write `thesis/` from this file.
Do **not** look at absolute-history window LRs until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** target leftover-15 openings.
Do **not** run lock A interpolate on Distil or gpt2-medium twins.

## Why freeze now

PROTOCOL-next H2 is still a reindexed measurement. The harness now
refuses to reindex a window as a new sequence. Occupancy-free leftover-15
is closed. Distil↔gpt2-medium occupancy-free is opened
([PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md): Distil→gpt2-medium
**20/48**, gpt2-medium→Distil **3/48**; not **25/48**). Isolated-file
detection is still not finished. The remaining confirmatory honesty item
that is not leftover targeting is whether lock A window **0:4** still
outranks **16:32** when mid-file 4-grams keep their real prefix.

## Primary scientific question

Under absolute generated-token history, does lock A interpolate last-4
window **0:4** still rank more of the 100 confirmatory prompt families
than window **16:32**?

Not: can another table classify the old 12×4 files. Not: leftover-15.
Not: Distil ∪ gpt2-medium union. Not: another `probe --methods` name.

## Frozen scorers

Existing interpolate last-4 only. Same flags as PROTOCOL-next H2. New
out-dir so the reindexed dump is not overwritten. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| A windows | Hard last-4 interpolate | `--methods interpolate --context-len 4 --windows 0:4,4:16,16:32,32:64` |

Windows use absolute `score_span`. Do **not** change the window list.
Do **not** add poshits, rankpath, hashtok, or cascades to this remasure.

## Hypotheses (stated before absolute-history LRs)

- **H2-abs.** Absolute-history window **0:4** ranks more prompt families
  than window **16:32** under lock A interpolate last-4 (strict `>`).
  File AUC is secondary. Isolated `lr>0` is not H2.
- **H2-abs-acc.** Absolute-history **16:32** is not a chance ranking. If
  it rises versus reindexed **89/100**, that is accumulation with
  history, not leftover-file detection and not isolated-file detection.
- **H2-abs-iso.** Absolute-history H2 is not a universal isolated-file
  detector. Do not sell absolute 0:4, absolute 16:32, reindexed
  **99/100** vs **89/100**, lock A **99/100**, nested **322/400**,
  Distil→gpt2-medium **20/48**, gpt2-medium→gpt2-medium **10/48**, or
  occupancy-free **16/48** as replacing **25/48**. Do not overwrite the
  reindexed dump. Do not rewrite PROTOCOL-next’s first-run flags.

## Primary endpoint

Prompt-level paired discrimination on window **0:4** versus **16:32**:
`n_prompts_marked_above` / 100 on each window, strict `>`. Report file
AUC and isolated `lr>0` as secondary. `used_keys` must be false.
Equality is a **tie**, not a win.

## Corpus

No new `pair`. Train/test is the already-frozen 100×4 GPT-2 confirmatory
twins. In-family leave-one-prompt-out, not out-of-family transfer.

| Role | Path |
|---|---|
| Twins | `experiments/2026-09-01-pair-100x4/` |
| Reindexed dump (keep) | `experiments/2026-09-01-probe-100x4-hard-windows/` |
| Absolute dump | `experiments/2026-09-01-probe-100x4-hard-windows-absolute/` |

Prompts: `experiments/2026-09-01-prompts-100/`. Seed `20260901`.

## Analysis command

Do not change flags after the first run. Do not look at window LRs until
the logbook names this SHA. Do not write into the reindexed out-dir.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods interpolate --context-len 4 \
  --windows 0:4,4:16,16:32,32:64 \
  --out-dir experiments/2026-09-01-probe-100x4-hard-windows-absolute
```

## What this protocol refuses

- Overwriting `experiments/2026-09-01-probe-100x4-hard-windows/`.
- Changing PROTOCOL-next’s first-run flags.
- New hashed / backoff / cascade / learned scorers on 12×4 or 100×4.
- Leftover-15 re-slices and leftover-slice rankpath.
- Targeting leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Distil ∪ gpt2-medium opening union.
- Lock A interpolate on Distil or gpt2-medium twins.
- Mixing grok12 into any train.
- Selling absolute 0:4, absolute 16:32, reindexed **99/100** vs
  **89/100**, lock A **99/100**, nested **322/400**, Distil→gpt2-medium
  **20/48**, or occupancy-free **16/48** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe command above once.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

Protocol SHA `89cb62d`. Named `450658c`. `used_keys=false`. In-family
leave-one-prompt-out on `experiments/2026-09-01-pair-100x4/`. Same flags
as PROTOCOL-next H2. New out-dir. The reindexed dump is unchanged.

Dump: [experiments/2026-09-01-probe-100x4-hard-windows-absolute/](../experiments/2026-09-01-probe-100x4-hard-windows-absolute/).
Reindexed (keep): [experiments/2026-09-01-probe-100x4-hard-windows/](../experiments/2026-09-01-probe-100x4-hard-windows/).

| Window | Absolute prompt | Absolute AUC | Absolute t=0 | Reindexed prompt | Reindexed AUC |
|---|---|---|---|---|---|
| 0:4 | **99/100** | **0.885** | 372/400 vs 272/400 | **99/100** | **0.885** |
| 4:16 | 94/100 | 0.803 | 314/400 vs 226/400 | 95/100 | 0.775 |
| 16:32 | **87/100** | **0.695** | 267/400 vs 240/400 | **89/100** | **0.689** |
| 32:64 | 85/100 | 0.680 | 255/400 vs 243/400 | 84/100 | 0.671 |

Full-file interpolate is still **99/100**, AUC **0.898**, isolated
352/400 vs 290/400, nested **322/400 vs 338/400**. Window 0:4 equals
the reindexed opening: no preceding generated tokens. `n_prompt_ties`
is 0 on every absolute window. Nested Youden 0:4 **361/400 vs 311/400**;
16:32 **215/400 vs 313/400**.

H2-abs **holds**. Absolute 0:4 ranks **99/100** prompt families; 16:32
ranks **87/100**. Strict `>` holds. An opening is still sufficient
in-domain. Absolute history does not reverse that comparison.

H2-abs-acc **holds**. Absolute 16:32 **87/100** is not a chance ranking.
It did **not** rise versus reindexed **89/100**. File AUC 0.695 versus
0.689. Keeping real prefix did not accumulate mid-file prompt ranking
above the reindexed scorer. Isolated 16:32 t=0 is **267/400 vs 240/400**;
that is not leftover-file detection and not isolated-file detection on
the original 12.

H2-abs-iso **holds**. Do not sell absolute 0:4 **99/100**, absolute
16:32 **87/100**, isolated 0:4 **372/400**, isolated 16:32 **267/400**,
reindexed **99/100** vs **89/100**, lock A **99/100**, nested
**322/400**, Distil→gpt2-medium **20/48**, gpt2-medium→gpt2-medium
**10/48**, occupancy-free **16/48**, or official **100/100** as replacing
**25/48**. Do not overwrite the reindexed dump. Do not rewrite
PROTOCOL-next’s first-run flags. Isolated-file detection is still not
finished. Do not write `thesis/`.
