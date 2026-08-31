# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.737 | 28/48 | 30/48 | 0.0004998 | 1.1283 |
| hashpool | 11/12 | 0.716 | 35/48 | 29/48 | 0.0004998 | 0.0392 |
| poshits | 10/12 | 0.666 | 24/48 | 37/48 | 0.0004998 | 1.4173 |
| pospool | 9/12 | 0.669 | 28/48 | 24/48 | 0.0004998 | 0.0275 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 22/48 | 39/48 | 0.2626 | 0.458 | 0.812 |
| hashpool | 23/48 | 36/48 | 0.0220 | 0.479 | 0.750 |
| poshits | 24/48 | 45/48 | 0.3386 | 0.500 | 0.938 |
| pospool | 24/48 | 43/48 | 0.0134 | 0.500 | 0.896 |

hits auc=0.737 mean_pos=1.0491 mean_neg=-0.0793 diff=1.1283 pos>0=28/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.0080 youden_sens=0.562 youden_spec=0.854 J=0.417
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
hashpool auc=0.716 mean_pos=0.0355 mean_neg=-0.0037 diff=0.0392 pos>0=35/48 neg<=0=29/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.0258 youden_sens=0.500 youden_spec=0.938 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
poshits auc=0.666 mean_pos=1.2970 mean_neg=-0.1203 diff=1.4173 pos>0=24/48 neg<=0=37/48 perm_p=0.0004998 binom_p=0.5573 youden_t=0.3670 youden_sens=0.500 youden_spec=0.958 J=0.458
poshits prompts_marked_above=10/12 instance=key-free-poshits used_keys=False
pospool auc=0.669 mean_pos=0.0230 mean_neg=-0.0045 diff=0.0275 pos>0=28/48 neg<=0=24/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.0134 youden_sens=0.521 youden_spec=0.917 J=0.438
pospool prompts_marked_above=9/12 instance=key-free-pospool used_keys=False
