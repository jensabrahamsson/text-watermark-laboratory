# Confirmatory protocol (longer watermark history on Qwen2-1.5B)

This is a **methods freeze** for a generator-transfer of the already
opened longer-context lock
([PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md)). It does not add
a `probe --methods` name. It does not edit the `synthid-text` checkout.
GPT-2 `ngram_len=13` original-12 interpolate **6/12** and DistilGPT2
interpolate **9/12** stay in those dumps. This file asks whether the
same public keys and $\Hw=12$ still rank prompt groups when the
generator is Qwen2-1.5B-Instruct.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with the public `ngram_len=5` processor.
Do **not** apply a chat template after peeking.

## Why freeze now

Sol (2026-09-03) asked for a preregistered longer-context two-grain
replication. That lock is opened on GPT-2 and DistilGPT2. The remaining
local generator in the laboratory's native Phase B set is Qwen2-1.5B.
Same public keys, same `ngram_len=13`, same 12 prompt strings, same two
grains. Kirchenbauer and Aaronson Qwen runs are different mixins and
are **not** this file.

A finished 100×4 Qwen $\Hw=12$ corpus is not required.

## Primary scientific question

On Qwen2-1.5B-Instruct with public keys and `ngram_len=13` ($\Hw=12$),
under leave-one-family-out interpolate last-4 and hard last-4, do marked
prompt-group means still outrank unmarked means?

Not: can GPT-2 $\Hw=12$ tables classify Qwen files. Not: leftover
targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `Qwen/Qwen2-1.5B-Instruct` (pin Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`) |
| Mixin keys | public-deepmind-30 (default) |
| `ngram_len` | **13** (same $\Hw=12$ as PROTOCOL-next-longctx) |
| Prompts | `experiments/2026-08-17-grok-prompts/` (plain strings; no chat template) |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260903** |
| Pair out-dir | `experiments/2026-09-04-pair-qwen-12x4-ngram13/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4/` |
| Fold | leave-one-family-out |
| Official control | matching `ngram_len=13` `detector_mean` |
| Primary group metric | $D_p$ sign count / 12, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

`pair --ngram-len 13` must generate **and** official-score with the
same `ngram_len`. Scoring Qwen $\Hw=12$ twins with `ngram_len=5` is a
harness bug. Probe and `atoms` must pass `--model
Qwen/Qwen2-1.5B-Instruct`; the default GPT-2 tokenizer is a harness
bug on these twins.

## Hypotheses (stated before generation)

- **H-long-q-ctrl.** Official matching mean with `ngram_len=13` is
  above $0.55$ on every first marked file. Unmarked first-draw stays
  near $1/2$. If marked first-draws fail, stop; harness bug.
- **H-long-q-group.** Interpolate last-4 12-LOO ranking is reported
  beside GPT-2 $\Hw=12$ **6/12** and Distil $\Hw=12$ **9/12**. Either
  drop or hold is informative. It does not replace **25/48**.
- **H-long-q-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-long-q-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260903 --ngram-len 13 \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-12x4-ngram13
```

Do not look at key-free LRs until `pair` has written official
first-draw scores and the probe command has been run once, as written.
Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-ngram13 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --model Qwen/Qwen2-1.5B-Instruct \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-qwen-12x4-ngram13
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / Aaronson generator in this file.
- New `probe --methods` names.
- Scoring Qwen $\Hw=12$ twins with `ngram_len=5`.
- Scoring Qwen twins with the default GPT-2 tokenizer.
- Adding a chat template after peeking.
- Leftover targeting.
- Selling any Qwen $\Hw=12$ count as replacing **25/48**.
- Paid chat APIs (`iterate --backend qwen` included).
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.

## Results

Protocol SHA `d7303a2`. Named `21a3e1b`. Pair seed **20260903**.
`ngram_len=13`. `model=Qwen/Qwen2-1.5B-Instruct`. `used_keys=false`.
Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`. Probe and atoms used
`--model Qwen/Qwen2-1.5B-Instruct`.

Pair dump: [experiments/2026-09-04-pair-qwen-12x4-ngram13/](../experiments/2026-09-04-pair-qwen-12x4-ngram13/).
Probe dump: [experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4/](../experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4/).

H-long-q-ctrl **fails** as the preregistered 12/12 first-draw. Official
matching mean with `ngram_len=13` is above $0.55$ on **11/12** first
marked files. Library first-draw is $0.515$. Unmarked first-draw is
**0/12** above $0.55$ (max $0.510$). `n_unmasked_ngrams=116` on every
first marked file. This is not a `ngram_len=5` scoring bug. Mixin is
on for the other eleven stems. Do not sell **11/12**.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **4/12** | 0.400 | 14/48 | 27/48 | 14 34 27 21 | **41/96** |
| hard last-4 | **4/12** | 0.415 | 16/48 | 31/48 | 16 32 31 17 | **47/96** |

GPT-2 $\Hw=12$ interpolate on these prompt *strings* (different twins)
was **6/12**. Distil interpolate was **9/12**. Qwen interpolate is
**4/12**. Mean $D_p=-0.083$ (interpolate) / $-0.032$ (hard). Interpolate
wins market, rain, office, garden. Hard wins night-bus, market,
kitchen, station (market has 0 isolated TPs).

Clopper–Pearson 95% (not a second freeze): interpolate **4/12** is
**[0.099, 0.651]** and includes ½; hard **4/12** is the same interval;
BA **41/96** is **[0.327, 0.532]**. Isolated **25/48** still includes ½.

H-long-q-group **holds** as an informative comparison with GPT-2
$\Hw=12$ **6/12** and Distil $\Hw=12$ **9/12**. It does not replace
**25/48**.

H-long-q-iso **holds**. Isolated interpolate **41/96** is a different
generator and $\Hw$ from the original-12 SynthID **47/96**. Do not sell
**4/12**, **41/96**, or **47/96** as replacing **25/48**. Nested
interpolate Youden **44/48** is a negative train threshold; do not sell
**44/48**.

H-long-q-occ **holds**. Leave-one-family-out interpolate atoms
(`used_keys=false`). File LRs match interpolate **14/48**. Exact
next-token overlap is **65** seen versus **12127** unseen (opening
$[0{:}4)$ is 41 versus 247). Occupancy is not a detector. Do not sell
**65** as replacing **25/48**.

JSON: [experiments/2026-09-04-atoms-qwen-12x4-ngram13/](../experiments/2026-09-04-atoms-qwen-12x4-ngram13/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.

