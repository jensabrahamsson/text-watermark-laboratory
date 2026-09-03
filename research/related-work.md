# Related work

This laboratory studies **key-free indication** on Google DeepMind’s
**public** SynthID-Text instance. It did not invent watermarking, key-free
detection, or watermark stealing. The map below uses author–year citations
([CITING.md](CITING.md)). Full records and critical annotations:
[annotated-bibliography.md](annotated-bibliography.md). BibTeX:
[references.bib](references.bib).

These notes are not a literature review of every sampling watermark, and
they are not the dissertation. Do not write `thesis/` until the isolated-file
research is actually finished. Headlines after the truncated-context
recount are **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON.

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

## Those theorems are not a refutation target we have hit

How to write an indication rather than a slogan:
[CITING.md](CITING.md). This laboratory **did not refute** Christ et al.
(2024) or Zhang et al. (2024). Do not write that it did. Clustered
binomial intervals and exact McNemar on already-opened prompt-family
signs (Clopper & Pearson, 1934; McNemar, 1947) are allowed when they
change a claim and are labelled post-open. A frontier-model sketch is
not a proof that tournament sampling is distinguishable in their sense.

Christ et al. (2024) prove *cryptographic undetectability* for a stated
PRF-based construction: a polynomial-time algorithm without the key
cannot distinguish watermarked from unwatermarked text with
non-negligible advantage, even with adaptive queries. A refutation would
be a proof error or an efficient distinguisher against *that*
construction. This laboratory did not implement that construction and
did not exhibit such a distinguisher.

Zhang et al. (2024) prove impossibility of *strong* watermarking given a
quality oracle and a mixing perturbation oracle. A refutation would be a
scheme that remains detectable after the oracles they allow, or a hole
in that argument. This laboratory did not run those oracles. Official
keyed leftover-18 is **18/18** at prefix-128; that is not a mixing
attack.

Two slogans *sound* like those theorems: “detection without keys is
impossible” and “watermarking cannot be strong.” They are not theorems
about `public-deepmind-30`. Mapping them onto this mixin is a category
error, not a citation.

**Measurement (scoped).** Under frozen lock A on `public-deepmind-30`
GPT-2 twins, prompt-group interpolate ranking was **99/100**. Under
12-LOO hard last-4 on the original 12, prompt-group ranking was **9/12**
and isolated sign at threshold 0 was **25/48**. Lengthening the public
mixin to `ngram_len=13` ($\Hw=12$) on the same 100 prompt strings
(new twins) attenuates interpolate ranking to **76/100**; official
matching scores remain **400/400** above 0.55
([PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md)). `used_keys=false`
for those key-free readers. Do not sell **76/100** as replacing
**25/48**.

**Indication (not a theorem).** Those prompt-group counts are consistent
with a learnable next-token footprint of this public tournament
instance, without reconstructing the g-function. Isolated **25/48** is
compatible with chance at that grain (binomial *p* ≈ 0.44 under a fair
coin). The two grains are not one claim.

**Non-claim.** This is not a complexity-theoretic proof that tournament
sampling is distinguishable in the sense of Christ et al. (2024). It is
not a proof that production Gemini is key-free detectable. It is not a
calibrated isolated-file detector. A suggested title of the form “Why
Key-Free Watermark Detection Fails” collapses the grains and is wrong
for this laboratory ([narrative.md](narrative.md)). Do not claim we know
any model’s training mix.

## Keyed theory is not this lab’s isolated-file reader

Omidi et al. (2026) analyse SynthID-Text’s **keyed** scores: mean-score TPR
is unimodal in tournament layers; the Bayesian score is nondecreasing then
saturates; Bernoulli(0.5) is optimal for detection. That preprint also
studies a layer-inflation removal attack on the mean score. This laboratory
does **not** implement that attack. Their object is official g-value
detection with keys. It is not a key-free isolated-file classifier, and it
does not replace **25/48**.

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
| Wang et al. (2026) | Third-party file verification from paired references | **Closest published finished-string paired-reference analog.** Same audit problem. Different method (proxy model + relative tests, not count-table LR). |
| Duan et al. (2025) | ZK that keyed detection ran | No. Still uses keys internally. |
| This repository | Finished-string count LR on public twins | An empirical notebook of that second measurement. Not TTP-Detect. Not Gloaguen. |

What this repo *does* add is a small, fully checked-in instance on the
public mixin: GPT-2 and Qwen twins, leave-one-out, frozen tables, tests,
raw JSON, and later occupancy-free / rank-path protocols. The interesting
claim is an **indication**, not a theorem: on the measured generators and
protocols, the keyed tournament leaves a distributional footprint that a
count-based LR can learn **without reconstructing the g-function**.
Writing rules: [CITING.md](CITING.md). This laboratory did not refute
Christ et al. (2024) or Zhang et al. (2024).

That is not “more than” Dathathri et al. (2024) (they built the scheme),
not “more than” Jovanović et al. (2024) (they steal; we do not), and not
a calibrated isolated-file detector that beats Wang et al. (2026) on a
shared benchmark. Isolated hard last-4 remains **25/48** (pre-fix
**29/48** overcounted truncated openings). Opening
occupancy-free hashing is **24/48** marked `lr>0`, which is below that
headline. Treat this as an empirical notebook, not a priority claim, not a
field-defining result, and not a finished conference paper. Manuscript
position: [threat-model.md](threat-model.md).

## Later benchmark, not a method race

A useful next comparison with Wang et al. (2026) is not “is our scorer
smarter?” It is: given **identical** paired reference twins and a
held-out finished-string corpus, how much of TTP-Detect’s third-party
discrimination does an embarrassingly simple count/opening LR recover?
If the simple reader gets a large share of the effect, that is itself
a result. This repository does not reimplement TTP-Detect. Do not add
a proxy-model detector on the old 12×4 files. Prompt-grain confirmation
is [PROTOCOL-next.md](PROTOCOL-next.md). Out-of-family isolated-file
transfer is [PROTOCOL-isolated.md](PROTOCOL-isolated.md).

## What this repository adds

A small, fully checked-in instance of **finished-string** key-free
indication on the public mixin: GPT-2 and Qwen twins, leave-one-out,
frozen tables, tests, and raw JSON. Headlines after the truncated-context
recount are **9/12** (hard last-4 prompt grain), **25/48** (that scorer’s
isolated sign), and **36/36** (in-domain hits on 36×4). Pre-fix **10/12** /
**29/48** stay in historical JSON. Occupancy-free hashing, rank-path tables, and
cascades are later protocols. None of them is a universal detector, and
none reconstructs keys ([invertibility.md](invertibility.md)).

Anthropic’s announced Claude mark (Anthropic, 2026a, 2026b) remains a
**future external test**, not something `score` can read
([claude.md](claude.md)).
