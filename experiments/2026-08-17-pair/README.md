# Same-prompt twins (3-prompt smoke)

First `pair` smoke: harbour / night-bus / library only. The full 12-prompt corpus used by `blind` is [../2026-08-17-blind-pairs/](../2026-08-17-blind-pairs/). Protocol: [research/key-free-twins.md](../../research/key-free-twins.md).

Each `*-prompt.txt` is the seed. `*-marked.txt` is **new** text from GPT-2 + mixin. `*-unmarked-gen.txt` is new text from the same prompt without the mixin.

Not a stamp on the same string. Not Claude. Not a remover.

```bash
python -m text_watermark_tools score .
```
