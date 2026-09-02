# Isolated-file protocol (second-key in-domain lock A)

This is a **methods freeze** for in-domain lock A interpolate last-4 on a
**second SynthID key instance**, using already-frozen files. It does not
add a scorer. Control-shuffled-30 12×4 generations are copied to
`*-marked.txt` names so `load_twins` can read them. Unmarked files are
the original public 12×4 unmarked pile. It is **not** leftover-15,
**not** leftover-18, and **not** a new `pair()` run.

[key-free-contrast.md](key-free-contrast.md) already scores those
control files with tables fit on *public* marked vs unmarked: control
ranks with unmarked (the key-free reader is instance-specific without
reconstructing keys). This freeze asks the complementary question: if
control-shuffled-30 is the **marked** class under leave-one-prompt-out,
does that second instance leave its own last-4 count-table footprint
against the original unmarked texts?

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at control-as-marked interpolate LRs until this freeze
is named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice control rankpath.
Do **not** target leftover-15 openings. Do **not** Distil ∪ gpt2-medium
union. Do **not** run lock A interpolate on Distil or gpt2-medium twins.
Do **not** generate a matched-seed multi-key `pair()` in this file.

## Why freeze now

Occupancy-free leftover-15 is closed. Distil↔gpt2-medium occupancy-free
is opened ([PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md):
Distil→gpt2-medium **20/48**, gpt2-medium→Distil **3/48**; not
**25/48**). Absolute-history H2 is opened
([PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): 0:4 **99/100** vs
16:32 **87/100**; not **25/48**). Isolated-file detection is still not
finished. The remaining honesty item that is not leftover targeting and
not a new generator is whether the published lock A reader still ranks
held-out prompt groups when the *marked* side is a different key
instance of the same mixin. Control files already exist
(`experiments/2026-08-31-pair-12x4-controlkeys/`, seed **20260931**).
Unmarked files already exist (`experiments/2026-08-17-pair-12x4/`, seed
**0**). Seeds differ: this is **not** a matched `pair()` twin. A miss
does not prove tournament sampling has no second-key footprint.

## Primary scientific question

Under leave-one-prompt-out lock A interpolate last-4, with no detector
keys, `hash_iv`, or g-values, do 12 Grok stems × 4 control-shuffled-30
draws rank above the original unmarked pile, and does isolated `lr>0`
beat hard **25/48**?

Not: leftover-15. Not: Distil ∪ gpt2-medium. Not: another
`probe --methods` name. Not: public tables scored on control (that is
contrast). Not: a matched-seed multi-key `pair()`.

## Frozen scorers

Existing interpolate last-4 only. No new method names. Lock A only.

| Lock | Reader | Flags |
|---|---|---|
| A | Hard last-4 interpolate | `--methods interpolate --context-len 4` |

Do **not** add poshits, rankpath, hashtok, or cascades. Do **not** run
occupancy-free postokhits on this constructed pair after peeking.

## Hypotheses (stated before control-as-marked LRs)

- **H-xkey-A.** Interpolate last-4 prompt ranking is strictly above
  **6/12** (strict `>`). Seed mismatch (control **20260931**, unmarked
  seed **0**) may lower it versus public-key **9/12**. File AUC is
  secondary.
- **H-xkey-iso.** Isolated t=0 (`n_positive_above_zero` / 48) does not
  beat hard **25/48**. Report Clopper–Pearson 95% on that isolated count
  and on the prompt-win count. Do not sell the isolated count as
  **25/48**.
- **H-xkey-seed.** A miss is not proof that tournament sampling has no
  second-key footprint. Official public lamp on these control files is
  chance (mean of means **0.501**); matching control keys **0.624**.
  Those lamps use keys. This freeze does not reconstruct them. A later
  matched-seed multi-key `pair()` is out of scope here.

## Primary endpoint

Prompt-level paired discrimination: `n_prompts_marked_above` / 12,
strict `>`. Isolated t=0 / 48 is secondary. `used_keys` must be false.
Equality is a **tie**, not a win.

## Corpus

No new `pair`. Construction copies existing files. Helper:
`materialize_control_as_marked` in
[`contrast.py`](../src/text_watermark_tools/contrast.py).

| Role | Path |
|---|---|
| Control (second key) | `experiments/2026-08-31-pair-12x4-controlkeys/` |
| Original unmarked | `experiments/2026-08-17-pair-12x4/` |
| Constructed twins | `experiments/2026-09-02-pair-12x4-control-as-marked/` |
| Probe dump | `experiments/2026-09-02-probe-12x4-control-as-marked-hard-last4/` |

Prompts: same 12 Grok seeds (`*-prompt.txt` copied from the original
pair). Mapping: `*-control-gen.txt` → `*-marked.txt`;
`*-control-gen-N.txt` → `*-marked-N.txt`. Unmarked names unchanged.

## Construction command

Do not change the mapping after the first copy. This step does not
score files.

```bash
python - <<'PY'
from pathlib import Path
from text_watermark_tools.contrast import materialize_control_as_marked

materialize_control_as_marked(
    Path("experiments/2026-08-31-pair-12x4-controlkeys"),
    Path("experiments/2026-08-17-pair-12x4"),
    Path("experiments/2026-09-02-pair-12x4-control-as-marked"),
)
PY
```

## Analysis command

Do not change flags after the first run. Do not look at interpolate LRs
until the logbook names this SHA.

```bash
python -m text_watermark_tools probe experiments/2026-09-02-pair-12x4-control-as-marked \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-02-probe-12x4-control-as-marked-hard-last4
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- Occupancy-free postokhits / leftover-slice rankpath on this pair
  after peeking.
- Leftover-15 re-slices and targeting leftover-15 openings.
- Distil ∪ gpt2-medium opening union.
- Lock A interpolate on Distil or gpt2-medium twins.
- Mixing grok12 into any train.
- A matched-seed multi-key `pair()` sold as this freeze.
- Re-running contrast (`--control-dir`) as if it answered H-xkey-A.
- Selling control-as-marked prompt ranking, isolated t=0, public
  **9/12**, contrast control-with-unmarked, Distil→gpt2-medium
  **20/48**, H2 **99/100**, or occupancy-free **16/48** as replacing
  **25/48**.
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

Protocol SHA `d25e495`. Named `9ec3b0c`. `used_keys=false`. Leave-one-prompt-out
on constructed `experiments/2026-09-02-pair-12x4-control-as-marked/`.
Control-shuffled-30 files are the marked class. Unmarked files are the
original 12×4 pile. Seeds **20260931** vs **0**. Not a matched `pair()`
run.

Dump: [experiments/2026-09-02-probe-12x4-control-as-marked-hard-last4/](../experiments/2026-09-02-probe-12x4-control-as-marked-hard-last4/).

| Reader | Prompt | Isolated t=0 | Unmarked ≤0 | File AUC |
|---|---|---|---|---|
| Interpolate last-4 | **7/12** | **30/48** | **25/48** | **0.590** |

`n_prompt_ties` is 0. Nested-by-stem Youden **33/48 vs 20/48** at a
negative train threshold ≈ −0.036; do not sell 33/48. Garden ranks with
0 isolated TPs. Ranking losses with isolated TP: harbour, night-bus,
letter, workshop, ferry-queue (11 of 30 TPs). File-level permutation p
= 0.135 is descriptive.

Clopper–Pearson 95%:

| Count | Interval | Includes ½? |
|---|---|---|
| Prompt **7/12** | **[0.277, 0.848]** | yes |
| Isolated **30/48** | **[0.474, 0.760]** | yes |
| Original isolated **25/48** | **[0.372, 0.667]** | yes |

H-xkey-A **holds**. Prompt ranking **7/12** is strictly above **6/12**.
It is lower than public-key **9/12**, as the seed-mismatch clause
allowed. The interval includes ½.

H-xkey-iso **fails** as a raw count: isolated t=0 is **30/48**, which
exceeds hard **25/48**. These are control-shuffled-30 files, not the
original public marked 12. The **30/48** interval still includes ½.
Nested **33/48** is a negative threshold. Do not sell **30/48**,
**33/48**, or **7/12** as replacing **25/48**.

H-xkey-seed **holds**. This is not a matched `pair()` run. Official
public lamp on these control files is chance (**0.501**); matching
control keys **0.624**. Those lamps use keys. **7/12** / **30/48** is
not a matched-seed second-key proof. A later matched-seed multi-key
`pair()` is still out of scope here.

Isolated-file detection on the original 12 is still not finished.
Absolute-history OOD windows are opened in
[PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md):
grok12 0:4 **7/12** (equals reindexed); 32:64 **10/12** (rose versus
reindexed **9/12**); 64:128 **9/12**. Original 12 0:4 **9/12**
outranks 16:32 **6/12**. Do not sell absolute **10/12**. Reindexed
dumps stay. The remaining honesty item that is not leftover targeting
is 12-LOO mask-*k* absolute remasure of
[PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md) (those dumps
stay reindexed). Do not write `thesis/`.
