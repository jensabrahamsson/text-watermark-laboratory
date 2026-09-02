# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=True used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 34/36 | 0.784 | 85/144 | 142/144 | 0.0004998 | 2.0146 |
| poshits | 34/36 | 0.784 | 85/144 | 142/144 | 0.0004998 | 2.0146 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 85/144 | 142/144 | 0.0065 | 0.590 | 0.986 |
| poshits | 85/144 | 142/144 | 0.0065 | 0.590 | 0.986 |

hits auc=0.784 mean_pos=2.0342 mean_neg=0.0196 diff=2.0146 pos>0=85/144 neg<=0=142/144 perm_p=0.0004998 binom_p=0.01843 youden_t=0.0067 youden_sens=0.590 youden_spec=0.993 J=0.583
hits prompts_marked_above=34/36 instance=key-free-hits used_keys=False
poshits auc=0.784 mean_pos=2.0342 mean_neg=0.0196 diff=2.0146 pos>0=85/144 neg<=0=142/144 perm_p=0.0004998 binom_p=0.01843 youden_t=0.0067 youden_sens=0.590 youden_spec=0.993 J=0.583
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
