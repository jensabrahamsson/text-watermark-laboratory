# Claude and text marking

Anthropic has announced text marking based on "a version of" DeepMind's SynthID-Text approach.

For this laboratory, the interesting question is not whether DeepMind's **public** keys score Claude text. They are a different watermark instance. The interesting question is whether a real production mark with unavailable keys can be detected statistically from paired data.

## What Anthropic has announced

As of August 2026, Anthropic says:

- the text mark is based on "a version of" SynthID-Text;
- models launched on or after **2 August 2026** are marked from day one in the surfaces they list;
- retrofit of older models is in progress;
- a detector is planned but is not yet publicly available;
- the mark is expressed through generated word/token choices rather than hidden characters.

Sources (web, not peer-reviewed; accessed 2026-09-01):

- Anthropic (2026a), [Claude text watermark](https://www.anthropic.com/news/claude-text-watermark)
- Anthropic (2026b), [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)

Bibliographic records: [annotated-bibliography.md](annotated-bibliography.md).

## Relevant launch dates

| Model | Launch |
|---|---|
| Fable 5 | 9 Jun 2026 |
| Sonnet 5 | **30 Jun 2026** |
| Opus 5 | 24 Jul 2026 |

Those releases predate the 2 August day-one policy. Their eventual retrofit status therefore has to be established separately rather than inferred from model name alone.

## What the public DeepMind scorer tells us

Almost nothing about Claude's own mark.

A Claude output near 0.50 under `public-deepmind-30` means it does not align with **that public key set**. It is not evidence that Claude contains no watermark.

We have used Claude as a rewriter of text carrying our known public-instance mark. That measures how rewriting affects **our** mark, which is a valid and separate experiment.

## The real Claude experiment

The key-free indicator gives us a more interesting route.

We already have a pre-mark/control corpus in:

```text
experiments/claude-premark-2026-08/
```

Once a comparable marked condition is available, the same prompt strings can be rerun. We can then fit the statistical shift between the two conditions without access to Anthropic's detector keys.

That is the experiment described in [paired-corpus.md](paired-corpus.md).

The goal is not to claim an Anthropic-equivalent detector. The goal is to test whether the key-free signal observed in the controlled DeepMind experiment transfers to a production watermark whose keys are actually unavailable.
