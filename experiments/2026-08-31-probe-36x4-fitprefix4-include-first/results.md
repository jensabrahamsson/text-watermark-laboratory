# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=True prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 35/36 | 0.924 | 124/144 | 100/144 | 0.0004998 | 2.9204 |
| first | 34/36 | 0.687 | 114/144 | 92/144 | 0.0004998 | 1.2894 |
| poshits | 35/36 | 0.925 | 123/144 | 114/144 | 0.0004998 | 3.0015 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 121/144 | 137/144 | 0.3761 | 0.840 | 0.951 |
| first | 114/144 | 94/144 | 0.0877 | 0.792 | 0.653 |
| poshits | 121/144 | 137/144 | 0.3761 | 0.840 | 0.951 |

hits auc=0.924 mean_pos=1.9685 mean_neg=-0.9519 diff=2.9204 pos>0=124/144 neg<=0=100/144 perm_p=0.0004998 binom_p=8.069e-20 youden_t=0.3763 youden_sens=0.840 youden_spec=0.958 J=0.799
hits prompts_marked_above=35/36 instance=key-free-hits used_keys=False
first auc=0.687 mean_pos=0.6962 mean_neg=-0.5932 diff=1.2894 pos>0=114/144 neg<=0=92/144 perm_p=0.0004998 binom_p=4.966e-13 youden_t=0.0889 youden_sens=0.792 youden_spec=0.674 J=0.465
first prompts_marked_above=34/36 instance=key-free-first used_keys=False
poshits auc=0.925 mean_pos=1.9678 mean_neg=-1.0337 diff=3.0015 pos>0=123/144 neg<=0=114/144 perm_p=0.0004998 binom_p=4.818e-19 youden_t=0.3763 youden_sens=0.840 youden_spec=0.958 J=0.799
poshits prompts_marked_above=35/36 instance=key-free-poshits used_keys=False
