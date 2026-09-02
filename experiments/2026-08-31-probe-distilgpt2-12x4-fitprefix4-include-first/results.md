# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=True prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 6/12 | 0.650 | 23/48 | 40/48 | 0.001499 | 0.9384 |
| first | 8/12 | 0.676 | 21/48 | 42/48 | 0.001999 | 0.7596 |
| poshits | 6/12 | 0.647 | 23/48 | 40/48 | 0.002499 | 0.8670 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 21/48 | 40/48 | 0.2289 | 0.438 | 0.833 |
| first | 17/48 | 42/48 | 0.7657 | 0.354 | 0.875 |
| poshits | 21/48 | 40/48 | 0.2289 | 0.438 | 0.833 |

hits auc=0.650 mean_pos=0.8705 mean_neg=-0.0679 diff=0.9384 pos>0=23/48 neg<=0=40/48 perm_p=0.001499 binom_p=0.6673 youden_t=0.0801 youden_sens=0.479 youden_spec=0.854 J=0.333
hits prompts_marked_above=6/12 instance=key-free-hits used_keys=False
first auc=0.676 mean_pos=0.4903 mean_neg=-0.2693 diff=0.7596 pos>0=21/48 neg<=0=42/48 perm_p=0.001999 binom_p=0.8438 youden_t=0.2007 youden_sens=0.438 youden_spec=0.896 J=0.333
first prompts_marked_above=8/12 instance=key-free-first used_keys=False
poshits auc=0.647 mean_pos=0.7995 mean_neg=-0.0675 diff=0.8670 pos>0=23/48 neg<=0=40/48 perm_p=0.002499 binom_p=0.6673 youden_t=0.0801 youden_sens=0.479 youden_spec=0.854 J=0.333
poshits prompts_marked_above=6/12 instance=key-free-poshits used_keys=False
