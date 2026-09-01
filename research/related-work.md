# Related work

This laboratory studies **key-free indication** on Google DeepMind’s
**public** SynthID-Text instance. It did not invent watermarking, key-free
detection, or watermark stealing. The map below uses author–year citations
([CITING.md](CITING.md)). Full records and critical annotations:
[annotated-bibliography.md](annotated-bibliography.md). BibTeX:
[references.bib](references.bib).

These notes are not a literature review of every sampling watermark, and
they are not the dissertation. Do not write `thesis/` until the isolated-file
research is actually finished. Headlines stay **10/12**, **29/48**, and
**36/36**.

## Official keyed detection

Dathathri et al. (2024) is SynthID-Text: tournament sampling, g-values,
mean / weighted-mean / Bayesian detectors. This repository’s `score` path
is the public reference implementation (Google DeepMind, 2024). Do not
reimplement `detector_mean`. Trust the code for `get_gvals`: 12 LCG mixes,
then `(hash >> 30) % 2`.

Kirchenbauer et al. (2023) (KGW) and Aaronson and Kirchner (2023) are the
earlier sampling-watermark family. Kuditipudi et al. (2024) and Christ et al.
(2024) give distortion-free / cryptographically undetectable variants.
SynthID is a tournament member of that family, not a hidden-character tag.
Christ et al. (2024) prove undetectability for a *different* construction;
they are not a proof that this lab’s count tables must fail on
SynthID-Text.

## Keyed theory is not this lab’s isolated-file reader

Omidi et al. (2026) analyse SynthID-Text’s **keyed** scores: mean-score TPR
is unimodal in tournament layers; the Bayesian score is nondecreasing then
saturates; Bernoulli(0.5) is optimal for detection. That preprint also
studies a layer-inflation removal attack on the mean score. This laboratory
does **not** implement that attack. Their object is official g-value
detection with keys. It is not a key-free isolated-file classifier, and it
does not replace **29/48**.

Han et al. (2025) stress SynthID-Text with paraphrase, copy-paste, and
back-translation. That robustness gap is cited, not re-run: the current
workflow does not download DIPPER (Krishna et al., 2023;
[dipper-local.md](dipper-local.md)).

## Public verifiability still uses keys internally

Duan et al. (2025) wrap keyed detectors (including SynthID-Text) in a
zero-knowledge proof so a third party can check that detection ran
faithfully without seeing the key. The detector still uses the key. That
is not `indicate` / `blind`. Google DeepMind (2024, issue 22) is a feature
request for publicly verifiable detection. Official `detector_mean` still
requires the instance keys.

## Stealing, probing, third-party detection

Jovanović et al. (2024) learn a spoof/remove model from black-box samples
(*Watermark Stealing*; arXiv **2402.19361**). Concurrent stealing and
spoofing include Wu and Chandrasekaran (2024) and Pang et al. (2024).
Zhang et al. (2024) prove impossibility of *strong* watermarking given
quality and perturbation oracles (arXiv **2311.04378** — not the stealing
paper). This lab does not steal keys, train a spoof generator, or run
those attacks.

Gloaguen et al. (2025) detect a watermarking scheme as a **generator
property** with limited black-box queries (ICLR 2025; arXiv 2405.20777).
SRI Lab (2024) applies those tests to a local SynthID-Text deployment.
That is not scoring a finished string against count tables. Do not
attribute 2405.20777 to other authors.

Wang et al. (2026) (TTP-Detect, ACL 2026 Findings) formulate third-party,
key-agnostic verification from observable outputs and paired
watermarked/unwatermarked reference sets — the same audit problem, a
different method.

## Same problem, not a priority claim

Neither Jens nor this laboratory invented the *question*. Independent
work already asked whether a third party can detect a sampling watermark
without the vendor’s keys.

| Work | What it measures | Same as this lab? |
|---|---|---|
| Dathathri et al. (2024) | Keyed official detection of SynthID-Text | No. This is `score`. |
| Jovanović et al. (2024) | Steal the keyed mapping from API samples | No. Not key recovery, not implemented. |
| Gloaguen et al. (2025) | Is *this generator* watermarked? Black-box queries | Same *family* of key-free questions. Different measurement: not a finished file. |
| Wang et al. (2026) | Third-party file verification from paired references | **Closest published analog.** Same audit problem. Different method (proxy model + relative tests, not count-table LR). |
| Duan et al. (2025) | ZK that keyed detection ran | No. Still uses keys internally. |
| This repository | Finished-string count LR on public twins | An empirical notebook of that second measurement. Not TTP-Detect. Not Gloaguen. |

What this repo *does* add is a small, fully checked-in instance on the
public mixin: GPT-2 and Qwen twins, leave-one-out, frozen tables, tests,
raw JSON, and later occupancy-free / rank-path protocols. The interesting
claim is narrow: the keyed tournament leaves a distributional footprint
that a count-based LR can learn **without reconstructing the g-function**.

That is not “more than” Dathathri et al. (2024) (they built the scheme),
not “more than” Jovanović et al. (2024) (they steal; we do not), and not
a calibrated isolated-file detector that beats Wang et al. (2026) on a
shared benchmark. Isolated hard last-4 remains **29/48**. Opening
occupancy-free hashing is **24/48** marked `lr>0`, which is below that
headline. Treat this as an empirical notebook, not a priority claim.

## What this repository adds

A small, fully checked-in instance of **finished-string** key-free
indication on the public mixin: GPT-2 and Qwen twins, leave-one-out,
frozen tables, tests, and raw JSON. Headlines stay **10/12** (hard last-4
prompt grain), **29/48** (that scorer’s isolated sign), and **36/36**
(in-domain hits on 36×4). Occupancy-free hashing, rank-path tables, and
cascades are later protocols. None of them is a universal detector, and
none reconstructs keys ([invertibility.md](invertibility.md)).

Anthropic’s announced Claude mark (Anthropic, 2026a, 2026b) remains a
**future external test**, not something `score` can read
([claude.md](claude.md)).
