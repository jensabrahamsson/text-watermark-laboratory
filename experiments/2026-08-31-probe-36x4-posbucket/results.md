# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 36/36 | 0.934 | 134/144 | 76/144 | 0.0004998 | 1.4896 |
| poshits | 34/36 | 0.925 | 134/144 | 97/144 | 0.0004998 | 2.1155 |
| pospool | 35/36 | 0.903 | 127/144 | 110/144 | 0.0004998 | 0.1030 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 119/144 | 134/144 | 0.7593 | 0.826 | 0.931 |
| poshits | 119/144 | 129/144 | 0.5637 | 0.826 | 0.896 |
| pospool | 107/144 | 128/144 | 0.0314 | 0.743 | 0.889 |

hits auc=0.934 mean_pos=1.4598 mean_neg=-0.0298 diff=1.4896 pos>0=134/144 neg<=0=76/144 perm_p=0.0004998 binom_p=3.714e-29 youden_t=0.7950 youden_sens=0.826 youden_spec=0.965 J=0.792
hits prompts_marked_above=36/36 instance=key-free-hits used_keys=False
poshits auc=0.925 mean_pos=1.8833 mean_neg=-0.2322 diff=2.1155 pos>0=134/144 neg<=0=97/144 perm_p=0.0004998 binom_p=3.714e-29 youden_t=0.5476 youden_sens=0.854 youden_spec=0.903 J=0.757
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
pospool auc=0.903 mean_pos=0.0896 mean_neg=-0.0134 diff=0.1030 pos>0=127/144 neg<=0=110/144 perm_p=0.0004998 binom_p=2.674e-22 youden_t=0.0361 youden_sens=0.743 youden_spec=0.972 J=0.715
pospool prompts_marked_above=35/36 instance=key-free-pospool used_keys=False
