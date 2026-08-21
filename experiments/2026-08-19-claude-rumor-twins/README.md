# 2026-08-19 — rumored Claude mark vs pre-mark twins

Same-prompt pairing of `claude-premark-2026-08` (unmarked-gen) and
`claude-mark-2026-08-19` (treated as marked for this hypothesis only).
37 of 40 prompts. `assumed_watermark=rumored`. GPT-2 tokenizer.

Not Anthropic’s detector. Not `public-deepmind-30`. Do not read a win as
“Claude is marked”.

| Path | Marked twin ranks higher |
|---|---|
| last-1 leave-one-out | **28/37** |
| last-4 leave-one-out | **24/37** |
| indicate rotate last-4, isolated marked `lr>0` | 26/37 |
| indicate rotate last-4, isolated unmarked `lr≤0` | 15/37 |

On the public mixin, last-4 beat last-1 once the watermark window had reuse.
Here last-1 is stronger. That is the wrong order for a keyed 5-gram tournament
and the right order for a style or model shift between 15 Aug and 19 Aug.

Public `score` on both sides is ≈ 0.50 (wrong instance).
