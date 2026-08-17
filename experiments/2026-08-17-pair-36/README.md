# 2026-08-17 — 36 GPT-2 twins × 256 tokens

Twelve Grok seeds plus 24 new short lines (`../2026-08-17-prompts-36/`). Mixin on/off, public keys. Wall clock 385 s.

Official lamp: marked **0.57–0.63**, unmarked **≈ 0.50**. All 36 marked twins above their unmarked twin.

Key-free sweep (leave-one-prompt-out):

| context_len | backoff | Wins |
|---|---|---|
| 1 | no | **22/36** |
| 2 | no | 21/36 |
| 3 | no | 16/36 |
| 4 | no | 20/36 |
| 1 or 2 or 4 | yes | 22/36 |

More prompts did not beat Qwen last-2 **10/12**. Rate 22/36 = 0.61 vs 8/12 = 0.67.
