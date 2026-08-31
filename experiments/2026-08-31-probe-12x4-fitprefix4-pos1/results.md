# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.691 | 23/48 | 48/48 | 0.0004998 | 1.7190 |
| poshits | 9/12 | 0.673 | 23/48 | 48/48 | 0.0004998 | 1.6902 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |
| poshits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |

hits auc=0.691 mean_pos=1.3906 mean_neg=-0.3285 diff=1.7190 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
hits prompts_marked_above=9/12 instance=key-free-hits used_keys=False
poshits auc=0.673 mean_pos=1.3906 mean_neg=-0.2996 diff=1.6902 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
poshits prompts_marked_above=9/12 instance=key-free-poshits used_keys=False
