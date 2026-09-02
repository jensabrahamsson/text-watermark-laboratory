# Matched 4-token prompt-as-context

36×4 leave-one-out. `--fit-prefix 4 --pos-bucket 1 --prompt-context`.
Token 0 sees last-4 of `*-prompt.txt`, the way the mixin does.
`used_keys=false`. Isolated `indicate score` of a lone file cannot
reconstruct that prompt.

| Method | wins | AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| hits / poshits | 34/36 | 0.784 | 85/144 | **142/144** |

Mixin-aligned context is a specificity knob, not a better ranking
(AUC 0.784 vs 0.935 without the prompt). Held-out prompts have unseen
last-4, so hits skip most opening tokens.
