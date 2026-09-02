# Threat model (auditor access)

This file locks **who the auditor is** and **what they may use**. It is
not `thesis/`, not a detector spec, and not a claim that the method is
fully blind. Isolated-file research is not finished. Author–year:
[CITING.md](CITING.md). Shop window: [abstract.md](abstract.md).

The core measurement is a two-grain indication, not a slogan:

> SynthID-like tournament sampling can leave a key-free and cheaply
> detectable **population** footprint, while detection of a **single**
> text remains weak.

That sentence is the seriousness bar. Prompt-group ranking without
keys is real (**9/12**, **36/36**, lock A **99/100**). Isolated hard
sign on the original 12 is **25/48**. Collapsing those grains into
“detection works” or “detection fails” is how a reviewer stops taking
the notebook seriously.

## What the auditor has

The laboratory auditor is a third party who does **not** have:

- the SynthID instance keys;
- `hash_iv`;
- g-values;
- DeepMind’s `detector_mean` at decision time (`score` is a keyed
  positive control, not the contribution).

The same auditor **does** have, for the public mixin:

- the ability to run the same prompts through a marked generator and
  an unmarked generator (matched twins);
- repeated draws per prompt family;
- finished strings, not live next-token queries to an unknown API.

So the method is **key-free**. It is **not reference-free** and **not fully blind**. `blind` in this repository means leave-one-prompt-out
on those twins, not “no reference text.” Gloaguen et al. (2025) ask
whether a *generator* is watermarked with black-box queries. Wang et
al. (2026) (TTP-Detect) verify finished strings from paired
watermarked/unwatermarked references. This notebook is in that second
family: paired references, count-table LR, public SynthID-Text
instance. Placement: [related-work.md](related-work.md).

A reviewer who writes “you needed marked and unmarked training pairs”
is describing the threat model correctly. That is a legitimate audit
setting (before/after, or a lab that can toggle the mixin). It is not
the setting “one stranger’s file, no corpus, no keys.”

## What this does not buy

| Claim | Status |
|---|---|
| Key recovery / invert `hash_iv` | Rejected ([invertibility.md](invertibility.md)) |
| Calibrated isolated-file detector | Not shown. Original-12 hard sign is **25/48** |
| Universal / cross-generator detector | Not shown. Distil/Qwen are robustness checks |
| Refutation of Christ et al. (2024) or Zhang et al. (2024) | This laboratory did not refute those theorems |
| Production Gemini or Anthropic keys | Not measured. Claude is a future before/after test ([paired-corpus.md](paired-corpus.md); do not call paid chat APIs) |
| Field-defining novelty of “detection without keys” | Already published (Gloaguen et al., 2025; Wang et al., 2026; SRI Lab, 2024, on SynthID). This notebook’s contribution is a cheap count-table, a prospective **99/100**, and an honest isolated-file miss |

## What would make the measurement harder to dismiss

Do not run these on the old 12×4 / 36×4 twins except bug-fix
remeasures. Do not write `thesis/` from this list.

1. **Keep the endpoints honest.** Prompt ranking uses strict `>`
   (win / loss / tie). File-level permutation and binomial p-values
   are descriptive; the independent unit is the prompt family.
2. **Say the access model in every abstract.** Key-free ≠
   reference-free ≠ fully blind.
3. **Center prospective lock A **99/100**** (protocol SHA `7001489`,
   analysis-code SHA `bbc802e`) and keep isolated **25/48** in the
   same pane.
4. **Same-data baselines** against Gloaguen et al. (2025) and Wang et
   al. (2026) belong on a *new* frozen corpus, not a reslice of the
   original 12. This repository does not reimplement TTP-Detect.
5. **Multi-key / multi-config replication** of the public mixin is the
   next venue-level experiment. Not started here.
6. **Anthropic before/after** only if a model shift can be separated
   from the mark. Future external test. Local Hugging Face generators
   only unless Jens asks.

Taken seriously means: a scoped empirical indication with an exact
auditor, exact grain, and exact non-claims — not a larger adjective.

## Manuscript position

This repository is a **strong empirical notebook**, interesting to the
watermarking literature. It is **not field-defining**. It is **not a finished conference paper**.

The contribution to position, in this order:

1. A cheap, fully checked-in **count-table likelihood ratio** on Google
   DeepMind’s public SynthID-Text mixin.
2. A crystal-clear auditor: **key-free, not reference-free, not fully blind.**
   Matched marked/unmarked twins; finished strings.
3. A two-grain result: **population** prompt-group ranking without keys
   (**9/12**, **36/36**, lock A **99/100**) while a **single** original-12
   file at `t=0` remains **25/48**.

What is *not* the contribution: inventing “detection without keys”
(Gloaguen et al. (2025); Wang et al. (2026); SRI Lab (2024)); a calibrated
isolated-file detector; a theorem refutation; a production Gemini or
Anthropic measurement.

Until a *new* frozen corpus carries same-data baselines against those
published detectors, and until multi-key replication of the public mixin
exists, the honest artifact is a **workshop, artifact, or focused empirical report** with that two-grain sentence in the first paragraph.
A serious NLP venue still needs those experiments. Anthropic
before/after could be significant if a model shift can be separated
from the mark. None of that is started here. Do not reimplement
TTP-Detect on the old 12×4. Do not write `thesis/` from a positioning
note. Isolated-file research is not finished.
