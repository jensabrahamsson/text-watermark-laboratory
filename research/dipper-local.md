# DIPPER locally

## Decision

**Do not download DIPPER for the current experiments.**

The official DIPPER paraphraser is an 11B T5-XXL model. There is no official 7B/3B/770M variant that would give comparable DIPPER results.

## What DIPPER is

[DIPPER](https://arxiv.org/abs/2303.13408) is the paragraph paraphraser of Krishna et al. (2023), used in later watermark-robustness work. Full record: [annotated-bibliography.md](annotated-bibliography.md).

Official checkpoint:

[`kalpeshk2011/dipper-paraphraser-xxl`](https://huggingface.co/kalpeshk2011/dipper-paraphraser-xxl)

Practical footprint:

- 11.27B parameters;
- F32 weights;
- roughly 45 GB of checkpoint data;
- reference setup expects a CUDA GPU with at least ~40 GB memory;
- reference code calls `.cuda()`.

That is disproportionate to what the current laboratory needs.

## Do we need it?

| Experiment | DIPPER needed? |
|---|---|
| Public reference scoring | No |
| Key-free twin indicator | No |
| Measure our watermark before/after a rewrite | No |
| Reproduce a DIPPER-specific literature benchmark | Yes |

We already have local/API paraphrasers sufficient for studying whether rewriting degrades the public-instance mark.

DIPPER only becomes necessary if we want numbers directly comparable to studies that specify that exact checkpoint and paraphrase setting.

## If we revisit it

Use a machine with a suitable CUDA GPU and keep the checkpoint outside the repository, under a gitignored `models/` directory.

Until then, the correct engineering decision is simply: **skip DIPPER**.
