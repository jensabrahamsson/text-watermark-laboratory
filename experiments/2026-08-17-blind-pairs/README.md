# Same-prompt twins (public DeepMind 30)

This is the with/without corpus. Each `*-prompt.txt` is the seed. `*-marked.txt` is **new** text from GPT-2 + mixin. `*-unmarked-gen.txt` is new text from the same prompt without the mixin.

Official `score` (we have the keys): marked **0.61–0.65**, unmarked **≈ 0.50**. **12/12**.

Key-free `blind` on these files: [../2026-08-17-blind/](../2026-08-17-blind/). **8/12**. Write-up: [research/key-free-twins.md](../../research/key-free-twins.md).

Not a stamp on the same string. Not Claude. Not a remover.

```bash
python -m text_watermark_tools score .
python -m text_watermark_tools blind . --out-dir ../2026-08-17-blind
```
