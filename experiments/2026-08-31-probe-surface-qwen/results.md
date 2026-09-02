# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-17-pair-qwen context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| surface | 9/12 | 0.674 | 9/12 | 3/12 | 0.04648 | 0.0165 |

surface auc=0.674 mean_pos=0.0214 mean_neg=0.0049 diff=0.0165 pos>0=9/12 neg<=0=3/12 perm_p=0.04648 binom_p=0.073 youden_t=0.0203 youden_sens=0.417 youden_spec=1.000 J=0.417
surface prompts_marked_above=9/12 instance=key-free-surface used_keys=False
