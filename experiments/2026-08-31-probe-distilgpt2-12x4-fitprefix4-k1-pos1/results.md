# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-distilgpt2-12x4 context_len=1 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.650 | 34/48 | 21/48 | 0.0004998 | 0.9901 |
| poshits | 9/12 | 0.596 | 27/48 | 24/48 | 0.0004998 | 1.0042 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 19/48 | 40/48 | 0.0640 | 0.396 | 0.833 |
| poshits | 18/48 | 47/48 | 0.7830 | 0.375 | 0.979 |

hits auc=0.650 mean_pos=1.0373 mean_neg=0.0472 diff=0.9901 pos>0=34/48 neg<=0=21/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0702 youden_sens=0.396 youden_spec=0.958 J=0.354
hits prompts_marked_above=9/12 instance=key-free-hits used_keys=False
poshits auc=0.596 mean_pos=1.0475 mean_neg=0.0434 diff=1.0042 pos>0=27/48 neg<=0=24/48 perm_p=0.0004998 binom_p=0.2354 youden_t=0.8043 youden_sens=0.375 youden_spec=1.000 J=0.375
poshits prompts_marked_above=9/12 instance=key-free-poshits used_keys=False
