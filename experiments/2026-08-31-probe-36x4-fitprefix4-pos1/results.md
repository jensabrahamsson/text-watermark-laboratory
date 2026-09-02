# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 34/36 | 0.935 | 132/144 | 114/144 | 0.0004998 | 3.4568 |
| poshits | 34/36 | 0.935 | 131/144 | 132/144 | 0.0004998 | 3.3330 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 121/144 | 129/144 | 0.0768 | 0.840 | 0.896 |
| poshits | 121/144 | 132/144 | 0.0336 | 0.840 | 0.917 |

hits auc=0.935 mean_pos=2.7620 mean_neg=-0.6948 diff=3.4568 pos>0=132/144 neg<=0=114/144 perm_p=0.0004998 binom_p=5.103e-27 youden_t=0.0770 youden_sens=0.896 youden_spec=0.917 J=0.812
hits prompts_marked_above=34/36 instance=key-free-hits used_keys=False
poshits auc=0.935 mean_pos=2.7607 mean_neg=-0.5724 diff=3.3330 pos>0=131/144 neg<=0=132/144 perm_p=0.0004998 binom_p=5.228e-26 youden_t=0.0304 youden_sens=0.910 youden_spec=0.924 J=0.833
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
