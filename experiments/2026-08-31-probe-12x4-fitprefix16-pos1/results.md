# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=16 pos_bucket=1 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 10/12 | 0.678 | 23/48 | 41/48 | 0.0004998 | 1.7871 |
| poshits | 9/12 | 0.673 | 23/48 | 48/48 | 0.0004998 | 1.7951 |
| poshitmass | 9/12 | 0.673 | 23/48 | 48/48 | 0.0004998 | 0.1197 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 23/48 | 47/48 | 1.0967 | 0.479 | 0.979 |
| poshits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |
| poshitmass | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |

hits auc=0.678 mean_pos=1.5647 mean_neg=-0.2224 diff=1.7871 pos>0=23/48 neg<=0=41/48 perm_p=0.0004998 binom_p=0.6673 youden_t=1.1882 youden_sens=0.479 youden_spec=1.000 J=0.479
hits prompts_marked_above=10/12 instance=key-free-hits used_keys=False
poshits auc=0.673 mean_pos=1.5661 mean_neg=-0.2291 diff=1.7951 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
poshits prompts_marked_above=9/12 instance=key-free-poshits used_keys=False
poshitmass auc=0.673 mean_pos=0.1044 mean_neg=-0.0153 diff=0.1197 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
poshitmass prompts_marked_above=9/12 instance=key-free-poshitmass used_keys=False
