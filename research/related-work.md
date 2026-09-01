# Related work (this lab's place)

This laboratory studies **key-free indication** on Google DeepMind's
**public** SynthID-Text instance. It did not invent watermarking, key-free
detection, or watermark stealing. The notes below keep that map honest.
They are not a literature review of every sampling watermark.

## Official keyed detection

[Dathathri et al., Nature 2024](https://www.nature.com/articles/s41586-024-08025-4)
is SynthID-Text: tournament sampling, g-values, mean / weighted-mean /
Bayesian detectors. This repo's `score` path is that public reference.
Do not reimplement `detector_mean`.

[Kirchenbauer et al. (KGW)](https://arxiv.org/abs/2301.10226) and
[Aaronson's Gumbel/exponential scheme](https://www.scottaaronson.com/blog/?p=6823)
are the earlier sampling-watermark family. SynthID is a tournament
variant of that idea, not a hidden-character tag.

## Keyed theory is not this lab's isolated-file reader

[Omidi, Dong, and Wang, arXiv:2603.03410](https://arxiv.org/abs/2603.03410)
give a theoretical analysis of SynthID-Text's **keyed** scores: mean-score
TPR is unimodal in tournament layers; the Bayesian score is nondecreasing
then saturates; Bernoulli(0.5) is optimal for detection. That paper also
studies a layer-inflation **removal** attack on the mean score. This
laboratory does **not** implement that attack. Their object is official
g-value detection with keys. It is not a key-free isolated-file
classifier, and it does not replace **29/48**.

## Public verifiability still uses keys internally

[PVMark, arXiv:2510.26274](https://arxiv.org/abs/2510.26274) wraps keyed
detectors (including SynthID-Text) in a zero-knowledge proof so a third
party can check that detection ran faithfully **without seeing the key**.
The detector still uses the key. That is not `indicate` / `blind`.
DeepMind's public tracker also has a feature request for publicly
verifiable detection ([google-deepmind/synthid-text#22](https://github.com/google-deepmind/synthid-text/issues/22)).
Official `detector_mean` still requires the instance keys.

## Stealing, probing, third-party detection

[Jovanović, Staab, and Vechev, ICML 2024](https://arxiv.org/abs/2311.04378)
(*Watermark Stealing*) learns a spoof/remove model from black-box samples.
Concurrent stealing/spoofing includes Wu & Chandrasekaran and Pang et al.
This lab does not steal keys or train a spoof generator.

[Sabanayagam, Hörl, and Dobriban 2024](https://arxiv.org/abs/2405.20777)
([ETH/SRI SynthID probe](https://www.sri.inf.ethz.ch/blog/probingsynthid))
detects SynthID as a **generator property** with repeated fixed-context
queries. That is not scoring a finished string against count tables.

[TTP-Detect, arXiv:2603.14968](https://arxiv.org/abs/2603.14968)
(*Rethinking LLM Watermark Detection in Black-Box Settings*) formulates
third-party, key-agnostic verification from observable outputs and paired
watermarked/unwatermarked reference sets — the same audit problem, a
different method.

## What this repository adds

A small, fully checked-in instance of **finished-string** key-free
indication on the public mixin: GPT-2 and Qwen twins, leave-one-out,
frozen tables, tests, and raw JSON. Headlines stay **10/12** (hard
last-4 prompt grain), **29/48** (that scorer's isolated sign), and
**36/36** (in-domain hits on 36×4). Occupancy-free hashing, rank-path
tables, and cascades are later protocols. None of them is a universal
detector, and none reconstructs keys. See
[invertibility.md](invertibility.md).

Anthropic's announced Claude mark remains a **future external test**,
not something `score` can read. See [claude.md](claude.md).
