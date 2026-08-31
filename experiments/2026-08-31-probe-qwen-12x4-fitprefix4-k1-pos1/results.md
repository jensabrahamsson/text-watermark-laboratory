# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-qwen-12x4 context_len=1 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 6/12 | 0.549 | 20/48 | 36/48 | 0.01249 | 0.2119 |
| poshits | 10/12 | 0.624 | 19/48 | 36/48 | 0.0004998 | 0.3258 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 20/48 | 40/48 | 0.0126 | 0.417 | 0.833 |
| poshits | 19/48 | 42/48 | 0.0264 | 0.396 | 0.875 |

hits auc=0.549 mean_pos=0.2043 mean_neg=-0.0076 diff=0.2119 pos>0=20/48 neg<=0=36/48 perm_p=0.01249 binom_p=0.9033 youden_t=0.0126 youden_sens=0.417 youden_spec=0.854 J=0.271
hits prompts_marked_above=6/12 instance=key-free-hits used_keys=False
poshits auc=0.624 mean_pos=0.2372 mean_neg=-0.0886 diff=0.3258 pos>0=19/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.9443 youden_t=0.0276 youden_sens=0.396 youden_spec=0.896 J=0.292
poshits prompts_marked_above=10/12 instance=key-free-poshits used_keys=False
