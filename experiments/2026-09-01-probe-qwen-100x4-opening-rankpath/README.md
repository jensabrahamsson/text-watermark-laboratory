# Qwen Phase B lock C — opening rankpath

Native Qwen2-1.5B-Instruct, `--rankpath --fit-prefix 4 --pos-bucket 1`.
Lock C is **rankpath only** (**84/100**, AUC **0.706**, isolated
**275/400 vs 259/400**). Nested-by-stem Youden **315/400 vs 232/400**.
The default count methods this flag also emits are not lock C.

Drop from GPT-2 Phase A lock C (**96/100**) is **12**. Rankpath drops more
than poshits (drop 5). H3 holds. Not **25/48**.
