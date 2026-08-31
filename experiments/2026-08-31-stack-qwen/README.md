# Leave-one-prompt LDA stack of hits + hashpool (Qwen 12×1)

On Qwen2-1.5B, exact `hits` file AUC is below chance (0.417). Stacking it
with hashpool (AUC 0.750) does not help: stack AUC **0.729**, prompt
**10/12**, isolated 9/12. Hashpool alone remains the transferable reader
on this tokenizer.
