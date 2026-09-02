# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 7/12 | 0.576 | 15/48 | 38/48 | 0.002999 | 0.2467 |
| first | 12/12 | 0.901 | 28/48 | 47/48 | 0.0004998 | 2.6159 |
| poshits | 7/12 | 0.576 | 15/48 | 38/48 | 0.002999 | 0.2467 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 15/48 | 42/48 | 0.0360 | 0.312 | 0.875 |
| first | 28/48 | 38/48 | -0.3201 | 0.583 | 0.792 |
| poshits | 15/48 | 42/48 | 0.0360 | 0.312 | 0.875 |

hits auc=0.576 mean_pos=0.2641 mean_neg=0.0174 diff=0.2467 pos>0=15/48 neg<=0=38/48 perm_p=0.002999 binom_p=0.9972 youden_t=0.0360 youden_sens=0.312 youden_spec=0.896 J=0.208
hits prompts_marked_above=7/12 instance=key-free-hits used_keys=False
first auc=0.901 mean_pos=1.2634 mean_neg=-1.3525 diff=2.6159 pos>0=28/48 neg<=0=47/48 perm_p=0.0004998 binom_p=0.1562 youden_t=-0.0910 youden_sens=0.792 youden_spec=0.812 J=0.604
first prompts_marked_above=12/12 instance=key-free-first used_keys=False
poshits auc=0.576 mean_pos=0.2641 mean_neg=0.0174 diff=0.2467 pos>0=15/48 neg<=0=38/48 perm_p=0.002999 binom_p=0.9972 youden_t=0.0360 youden_sens=0.312 youden_spec=0.896 J=0.208
poshits prompts_marked_above=7/12 instance=key-free-poshits used_keys=False
