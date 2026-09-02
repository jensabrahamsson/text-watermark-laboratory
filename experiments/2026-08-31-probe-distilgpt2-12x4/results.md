# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.705 | 33/48 | 27/48 | 0.0009995 | 1.2200 |
| hashpool | 9/12 | 0.754 | 27/48 | 39/48 | 0.0004998 | 0.0394 |
| poshits | 10/12 | 0.605 | 27/48 | 25/48 | 0.0004998 | 1.4565 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 29/48 | 38/48 | 0.0277 | 0.604 | 0.792 |
| hashpool | 27/48 | 35/48 | -0.0021 | 0.562 | 0.729 |
| poshits | 20/48 | 45/48 | 0.0266 | 0.417 | 0.938 |

hits auc=0.705 mean_pos=1.1860 mean_neg=-0.0340 diff=1.2200 pos>0=33/48 neg<=0=27/48 perm_p=0.0009995 binom_p=0.006642 youden_t=0.0283 youden_sens=0.604 youden_spec=0.812 J=0.417
hits prompts_marked_above=9/12 instance=key-free-hits used_keys=False
hashpool auc=0.754 mean_pos=0.0207 mean_neg=-0.0187 diff=0.0394 pos>0=27/48 neg<=0=39/48 perm_p=0.0004998 binom_p=0.2354 youden_t=-0.0039 youden_sens=0.646 youden_spec=0.771 J=0.417
hashpool prompts_marked_above=9/12 instance=key-free-hashpool used_keys=False
poshits auc=0.605 mean_pos=1.4491 mean_neg=-0.0073 diff=1.4565 pos>0=27/48 neg<=0=25/48 perm_p=0.0004998 binom_p=0.2354 youden_t=0.0266 youden_sens=0.417 youden_spec=0.958 J=0.375
poshits prompts_marked_above=10/12 instance=key-free-poshits used_keys=False
