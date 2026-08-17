# Claude and text marking

What follows is what Anthropic has written, plus launch dates. It is not a measurement of their mark. Our `score` uses DeepMind’s public keys. That is the **wrong instance** for Claude.

## Anthropic (Aug 2026)

- Method: “a version of” DeepMind SynthID-Text 2024. Nothing is inserted into the string. The mark sits in the word choices.
- Day-one: models launched **2 August 2026 or later**, everywhere they list (API, Claude, Claude Code, cloud partners), worldwide.
- Older models: retrofit “in progress”. They update the Help Center when there is news.
- Detector: promised, **not released** (no public Messages endpoint as of mid-August 2026).
- C2PA on image files is a different mark (file metadata), not text.

Sources: [Help Center](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), [news post](https://www.anthropic.com/news/claude-text-watermark).

## Launch dates (before the cutoff)

| Model | Launched |
|---|---|
| Fable 5 | 9 Jun 2026 |
| Sonnet 5 | **30 Jun 2026** |
| Opus 5 | 24 Jul 2026 |

Sonnet 5 is therefore **not** a day-one marked model. Whether a retrofit has already landed on it is unpublished. We do not have their detector, so we cannot check.

## What they say happens to text

| Situation | What they describe |
|---|---|
| Claude writes everything (including translation) | Full — every word is Claude’s choice |
| Light proofread / grammar only | Almost none; can miss even *their* detector |
| Full rewrite | Their mark can sit in the new words |
| Short / fact-heavy / exact code | Weak or none |
| A human edits further | Their signal thins |

They say a hit on *their* detector (when it exists) means “Claude was involved”, not “Claude is the original author”.

## Our lamp against Claude

DeepMind’s public 30 keys ≠ Claude’s keys. 0.50 on Sonnet 5 output means **our** 5-grams are gone. It does not mean Claude is unmarked.

We have used Claude as a rewriter to measure *our* mark ([experiments/2026-08-15-gpt2-sonnet5/](../experiments/2026-08-15-gpt2-sonnet5/)). Not as an oracle for theirs.

The control pile for a later same-prompt comparison: [paired-corpus.md](paired-corpus.md), `experiments/claude-premark-2026-08/`.
