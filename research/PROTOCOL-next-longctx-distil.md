# Confirmatory protocol (longer watermark history on DistilGPT2)

This is a **methods freeze** for a generator-transfer of the already
opened longer-context lock
([PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md)). It does not add
a `probe --methods` name. It does not edit the `synthid-text` checkout.
GPT-2 `ngram_len=13` original-12 interpolate **6/12** and 100-family
interpolate **76/100** stay in those dumps. This file asks whether the
same public keys and $\Hw=12$ still rank prompt groups when the
generator is DistilGPT2.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with the public `ngram_len=5` processor.

## Why freeze now

Sol (2026-09-03) asked for a preregistered longer-context two-grain
replication. That lock is opened on GPT-2. The remaining cheap
generator check that is not leftover targeting is the same
`ngram_len=13` on DistilGPT2, same 12 prompt strings, same two grains.
Kirchenbauer and Aaronson Distil runs are different mixins and are
**not** this file.

A finished 100×4 Distil $\Hw=12$ corpus is not required.

## Primary scientific question

On DistilGPT2 with public keys and `ngram_len=13` ($\Hw=12$), under
leave-one-family-out interpolate last-4 and hard last-4, do marked
prompt-group means still outrank unmarked means?

Not: can GPT-2 $\Hw=12$ tables classify Distil files. Not: leftover
targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `distilgpt2` (pin Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`) |
| Mixin keys | public-deepmind-30 (default) |
| `ngram_len` | **13** (same $\Hw=12$ as PROTOCOL-next-longctx) |
| Prompts | `experiments/2026-08-17-grok-prompts/` |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260903** |
| Pair out-dir | `experiments/2026-09-04-pair-distil-12x4-ngram13/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4/` |
| Fold | leave-one-family-out |
| Official control | matching `ngram_len=13` `detector_mean` |
| Primary group metric | $D_p$ sign count / 12, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

`pair --ngram-len 13` must generate **and** official-score with the
same `ngram_len`. Scoring Distil $\Hw=12$ twins with `ngram_len=5` is
a harness bug.

## Hypotheses (stated before generation)

- **H-long-d-ctrl.** Official matching mean with `ngram_len=13` is
  above $0.55$ on every first marked file. Unmarked first-draw stays
  near $1/2$. If marked first-draws fail, stop; harness bug.
- **H-long-d-group.** Interpolate last-4 12-LOO ranking is reported
  beside GPT-2 $\Hw=12$ **6/12**. Either drop or hold is informative.
  It does not replace **25/48**.
- **H-long-d-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-long-d-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260903 \
  --ngram-len 13 --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-12x4-ngram13
```

Do not look at key-free LRs until `pair` has written official
first-draw scores and the probe command has been run once, as written.
Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-distil-12x4-ngram13
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / Aaronson generator in this file.
- New `probe --methods` names.
- Scoring Distil $\Hw=12$ twins with `ngram_len=5`.
- Leftover targeting.
- Selling any Distil $\Hw=12$ count as replacing **25/48**.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.

## Results

Protocol SHA `bae6d81`. Named `c120dc4`. Pair seed **20260903**.
`ngram_len=13`. `model=distilgpt2`. `used_keys=false`. Hub SHA
`2290a62682d06624634c1f46a6ad5be0f47f38aa`.

Pair dump: [experiments/2026-09-04-pair-distil-12x4-ngram13/](../experiments/2026-09-04-pair-distil-12x4-ngram13/).
Probe dump: [experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4/](../experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4/).

H-long-d-ctrl **holds**. Official matching mean with `ngram_len=13` is
above $0.55$ on all 12 first marked files (min $0.605$). Unmarked
first-draw is **0/12** above $0.55$ (max $0.519$). Mixin is on.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **9/12** | 0.563 | 21/48 | 28/48 | 21 27 28 20 | **49/96** |
| hard last-4 | **6/12** | 0.485 | 16/48 | 26/48 | 16 32 26 22 | **42/96** |

GPT-2 $\Hw=12$ interpolate on these prompt *strings* (different twins)
was **6/12**. Distil interpolate is **9/12**, the public-mixin
diagnostic on these strings (also different twins). Mean $D_p=0.057$
(interpolate) / $-0.010$ (hard). Interpolate losses harbour, station,
rain.

Clopper–Pearson 95% (not a second freeze): interpolate **9/12** is
**[0.428, 0.945]** and includes ½; hard **6/12** is **[0.211, 0.789]**;
BA **49/96** is **[0.406, 0.614]**. Isolated **25/48** still includes ½.

H-long-d-group **holds** as an informative comparison with GPT-2
$\Hw=12$ **6/12**. It does not replace **25/48**.

H-long-d-iso **holds**. Isolated interpolate **49/96** is a different
generator and $\Hw$ from the original-12 SynthID **47/96**. Do not sell
**9/12**, **6/12**, **49/96**, or **42/96** as replacing **25/48**.

H-long-d-occ **holds**. Leave-one-family-out interpolate atoms
(`used_keys=false`). File LRs match interpolate **21/48**. Exact
next-token overlap is **175** seen versus **11994** unseen (opening
$[0{:}4)$ is 111 versus 177). Occupancy is not a detector. Do not sell
**175** as replacing **25/48**.

JSON: [experiments/2026-09-04-atoms-distil-12x4-ngram13/](../experiments/2026-09-04-atoms-distil-12x4-ngram13/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.

