# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=16 pos_bucket=16 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 34/36 | 0.929 | 132/144 | 112/144 | 0.0004998 | 3.4462 |
| hashpool | 34/36 | 0.917 | 129/144 | 92/144 | 0.0004998 | 0.7827 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 121/144 | 136/144 | 0.7453 | 0.840 | 0.944 |
| hashpool | 117/144 | 137/144 | 0.1213 | 0.812 | 0.951 |

hits auc=0.929 mean_pos=2.8676 mean_neg=-0.5786 diff=3.4462 pos>0=132/144 neg<=0=112/144 perm_p=0.0004998 binom_p=5.103e-27 youden_t=0.7501 youden_sens=0.840 youden_spec=0.951 J=0.792
hits prompts_marked_above=34/36 instance=key-free-hits used_keys=False
hashpool auc=0.917 mean_pos=0.7486 mean_neg=-0.0340 diff=0.7827 pos>0=129/144 neg<=0=92/144 perm_p=0.0004998 binom_p=4.32e-24 youden_t=0.1281 youden_sens=0.812 youden_spec=0.979 J=0.792
hashpool prompts_marked_above=34/36 instance=key-free-hashpool used_keys=False
