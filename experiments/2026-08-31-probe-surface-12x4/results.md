# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.737 | 28/48 | 30/48 | 0.0004998 | 1.1283 |
| hashpool | 11/12 | 0.716 | 35/48 | 29/48 | 0.0004998 | 0.0392 |
| surface | 10/12 | 0.602 | 12/48 | 42/48 | 0.03698 | 0.0066 |
| logit | 10/12 | 0.735 | 23/48 | 41/48 | 0.0004998 | 1.5626 |

hits auc=0.737 mean_pos=1.0491 mean_neg=-0.0793 diff=1.1283 pos>0=28/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.0080 youden_sens=0.562 youden_spec=0.854 J=0.417
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
hashpool auc=0.716 mean_pos=0.0355 mean_neg=-0.0037 diff=0.0392 pos>0=35/48 neg<=0=29/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.0258 youden_sens=0.500 youden_spec=0.938 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
surface auc=0.602 mean_pos=-0.0108 mean_neg=-0.0174 diff=0.0066 pos>0=12/48 neg<=0=42/48 perm_p=0.03698 binom_p=0.9999 youden_t=-0.0044 youden_sens=0.417 youden_spec=0.854 J=0.271
surface prompts_marked_above=10/12 instance=key-free-surface used_keys=False
logit auc=0.735 mean_pos=0.9915 mean_neg=-0.5711 diff=1.5626 pos>0=23/48 neg<=0=41/48 perm_p=0.0004998 binom_p=0.6673 youden_t=-0.2179 youden_sens=0.583 youden_spec=0.854 J=0.438
logit prompts_marked_above=10/12 instance=key-free-logit used_keys=False
