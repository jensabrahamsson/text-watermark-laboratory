# Key-free probe

probe n_methods=15 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 12/12 | 0.862 | 36/48 | 33/48 | 0.0004998 | 0.7785 |
| hard | 12/12 | 0.873 | 36/48 | 36/48 | 0.0004998 | 1.1725 |
| backoff | 12/12 | 0.881 | 36/48 | 37/48 | 0.0004998 | 1.1990 |
| interpolate | 10/12 | 0.835 | 31/48 | 33/48 | 0.0004998 | 2.2388 |
| hits | 9/12 | 0.671 | 23/48 | 46/48 | 0.0004998 | 1.0855 |
| freqhits | 9/12 | 0.672 | 23/48 | 48/48 | 0.0004998 | 1.0931 |
| hitmass | 9/12 | 0.671 | 23/48 | 46/48 | 0.0004998 | 0.3587 |
| gated | 9/12 | 0.668 | 23/48 | 46/48 | 0.0004998 | 1.0263 |
| shrinkage | 9/12 | 0.671 | 23/48 | 46/48 | 0.0004998 | 1.0737 |
| mix | 12/12 | 0.879 | 36/48 | 36/48 | 0.0004998 | 1.1972 |
| hashpool | 12/12 | 0.882 | 36/48 | 34/48 | 0.0004998 | 1.1933 |
| rankpath | 11/12 | 0.874 | 41/48 | 35/48 | 0.0004998 | 1.4395 |
| rankuni | 11/12 | 0.759 | 33/48 | 32/48 | 0.0004998 | 0.2775 |
| stack | 12/12 | 0.861 | 34/48 | 38/48 | 0.0004998 | 0.0310 |
| logit | 12/12 | 0.859 | 34/48 | 38/48 | 0.0004998 | 2.6820 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| unigram | 8/48 | 7/48 | 36/4 | 15/26 | 0.706 |
| hard | 0/48 | 1/48 | 36/12 | 12/35 | 0.750 |
| backoff | 0/48 | 1/48 | 36/12 | 11/36 | 0.766 |
| interpolate | 0/48 | 1/48 | 31/17 | 15/32 | 0.674 |
| hits | 9/48 | 30/48 | 23/16 | 2/16 | 0.920 |
| freqhits | 9/48 | 33/48 | 23/16 | 0/15 | 1.000 |
| hitmass | 9/48 | 30/48 | 23/16 | 2/16 | 0.920 |
| gated | 9/48 | 30/48 | 23/16 | 2/16 | 0.920 |
| shrinkage | 9/48 | 30/48 | 23/16 | 2/16 | 0.920 |
| mix | 0/48 | 1/48 | 36/12 | 12/35 | 0.750 |
| hashpool | 0/48 | 0/48 | 36/12 | 14/34 | 0.720 |
| rankpath | 0/48 | 0/48 | 41/7 | 13/35 | 0.759 |
| rankuni | 0/48 | 0/48 | 33/15 | 16/32 | 0.673 |
| stack | 0/48 | 0/48 | 34/14 | 10/38 | 0.773 |
| logit | 0/48 | 0/48 | 34/14 | 10/38 | 0.773 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| unigram | 30/48 | 43/48 | 0.3317 | 0.625 | 0.896 |
| hard | 31/48 | 35/48 | 0.0797 | 0.646 | 0.729 |
| backoff | 34/48 | 45/48 | 0.3076 | 0.708 | 0.938 |
| interpolate | 27/48 | 40/48 | 0.4827 | 0.562 | 0.833 |
| hits | 23/48 | 47/48 | 0.2642 | 0.479 | 0.979 |
| freqhits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |
| hitmass | 23/48 | 47/48 | 0.1761 | 0.479 | 0.979 |
| gated | 23/48 | 46/48 | 0.0000 | 0.479 | 0.958 |
| shrinkage | 23/48 | 47/48 | 0.5581 | 0.479 | 0.979 |
| mix | 36/48 | 39/48 | 0.1253 | 0.750 | 0.812 |
| hashpool | 41/48 | 29/48 | -0.2935 | 0.854 | 0.604 |
| rankpath | 37/48 | 41/48 | 0.2275 | 0.771 | 0.854 |
| rankuni | 29/48 | 36/48 | 0.1287 | 0.604 | 0.750 |
| stack | 41/48 | 28/48 | -0.0161 | 0.854 | 0.583 |
| logit | 33/48 | 28/48 | -0.7118 | 0.688 | 0.583 |

unigram auc=0.862 mean_pos=0.5041 mean_neg=-0.2744 diff=0.7785 pos>0=36/48 neg<=0=33/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.3242 youden_sens=0.667 youden_spec=0.917 J=0.583
unigram prompts_marked_above=12/12 instance=key-free-unigram used_keys=False
hard auc=0.873 mean_pos=0.8332 mean_neg=-0.3393 diff=1.1725 pos>0=36/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.1122 youden_sens=0.750 youden_spec=0.833 J=0.583
hard prompts_marked_above=12/12 instance=key-free-counts used_keys=False
backoff auc=0.881 mean_pos=0.7827 mean_neg=-0.4162 diff=1.1990 pos>0=36/48 neg<=0=37/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.3084 youden_sens=0.708 youden_spec=0.958 J=0.667
backoff prompts_marked_above=12/12 instance=key-free-backoff used_keys=False
interpolate auc=0.835 mean_pos=1.6977 mean_neg=-0.5411 diff=2.2388 pos>0=31/48 neg<=0=33/48 perm_p=0.0004998 binom_p=0.02973 youden_t=0.7445 youden_sens=0.562 youden_spec=0.979 J=0.542
interpolate prompts_marked_above=10/12 instance=key-free-interpolate used_keys=False
hits auc=0.671 mean_pos=0.9596 mean_neg=-0.1259 diff=1.0855 pos>0=23/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.2718 youden_sens=0.479 youden_spec=1.000 J=0.479
hits prompts_marked_above=9/12 instance=key-free-hits used_keys=False
freqhits auc=0.672 mean_pos=0.9596 mean_neg=-0.1335 diff=1.0931 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
freqhits prompts_marked_above=9/12 instance=key-free-freqhits used_keys=False
hitmass auc=0.671 mean_pos=0.3199 mean_neg=-0.0388 diff=0.3587 pos>0=23/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.1812 youden_sens=0.479 youden_spec=1.000 J=0.479
hitmass prompts_marked_above=9/12 instance=key-free-hitmass used_keys=False
gated auc=0.668 mean_pos=0.9596 mean_neg=-0.0667 diff=1.0263 pos>0=23/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=0.958 J=0.438
gated prompts_marked_above=9/12 instance=key-free-gated used_keys=False
shrinkage auc=0.671 mean_pos=0.9596 mean_neg=-0.1140 diff=1.0737 pos>0=23/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.5677 youden_sens=0.479 youden_spec=1.000 J=0.479
shrinkage prompts_marked_above=9/12 instance=key-free-shrinkage used_keys=False
mix auc=0.879 mean_pos=0.8189 mean_neg=-0.3783 diff=1.1972 pos>0=36/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.1425 youden_sens=0.750 youden_spec=0.875 J=0.625
mix prompts_marked_above=12/12 instance=key-free-mix used_keys=False
hashpool auc=0.882 mean_pos=0.8244 mean_neg=-0.3689 diff=1.1933 pos>0=36/48 neg<=0=34/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=-0.3615 youden_sens=1.000 youden_spec=0.625 J=0.625
hashpool prompts_marked_above=12/12 instance=key-free-hashpool used_keys=False
rankpath auc=0.874 mean_pos=0.4357 mean_neg=-1.0038 diff=1.4395 pos>0=41/48 neg<=0=35/48 perm_p=0.0004998 binom_p=3.12e-07 youden_t=0.2152 youden_sens=0.854 youden_spec=0.875 J=0.729
rankpath prompts_marked_above=11/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.759 mean_pos=0.1299 mean_neg=-0.1476 diff=0.2775 pos>0=33/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.1271 youden_sens=0.688 youden_spec=0.771 J=0.458
rankuni prompts_marked_above=11/12 instance=key-free-rankuni used_keys=False
stack auc=0.861 mean_pos=0.0150 mean_neg=-0.0160 diff=0.0310 pos>0=34/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.002758 youden_t=-0.0179 youden_sens=1.000 youden_spec=0.604 J=0.604
stack prompts_marked_above=12/12 instance=key-free-stack used_keys=False
logit auc=0.859 mean_pos=1.6888 mean_neg=-0.9932 diff=2.6820 pos>0=34/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.002758 youden_t=-0.9137 youden_sens=0.917 youden_spec=0.625 J=0.542
logit prompts_marked_above=12/12 instance=key-free-logit used_keys=False
