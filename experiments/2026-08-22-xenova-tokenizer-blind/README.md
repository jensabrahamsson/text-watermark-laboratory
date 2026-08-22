# 2026-08-22 — Xenova/claude-tokenizer on existing twins

`Xenova/claude-tokenizer` is Anthropic’s **Claude 1/2** 65k BPE (old SDK),
not Claude 3+/Sonnet 5. Same twin files as the 21 Aug GPT-2 run.
`used_keys=false`. Not a detector.

| Contrast | GPT-2 last-1 | GPT-2 last-4 | Xenova last-1 | Xenova last-4 |
|---|---|---|---|---|
| 15 Aug vs 21 | 33/40 | 34/40 | 35/40 | 35/40 |
| 19b vs 21 | 31/40 | 35/40 | 30/40 | 32/40 |
| 19a vs 19b | 19/38 | 19/38 | 21/38 | 20/38 |
