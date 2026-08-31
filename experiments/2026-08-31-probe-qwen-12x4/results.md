# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=4 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 8/12 | 0.602 | 24/48 | 19/48 | 0.0004998 | 1.1801 |
| freqhits | 7/12 | 0.495 | 15/48 | 23/48 | 0.0004998 | 0.4975 |
| hitmass | 8/12 | 0.604 | 24/48 | 19/48 | 0.0004998 | 0.0099 |
| hashpool | 7/12 | 0.638 | 36/48 | 20/48 | 0.009995 | 0.0088 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 14/48 | 46/48 | 0.9332 | 0.292 | 0.958 |
| freqhits | 48/48 | 9/48 | -0.0421 | 1.000 | 0.188 |
| hitmass | 15/48 | 47/48 | 0.0085 | 0.312 | 0.979 |
| hashpool | 34/48 | 27/48 | 0.0052 | 0.708 | 0.562 |

hits auc=0.602 mean_pos=0.9222 mean_neg=-0.2579 diff=1.1801 pos>0=24/48 neg<=0=19/48 perm_p=0.0004998 binom_p=0.5573 youden_t=1.1140 youden_sens=0.292 youden_spec=1.000 J=0.292
hits prompts_marked_above=8/12 instance=key-free-hits used_keys=False
freqhits auc=0.495 mean_pos=0.2572 mean_neg=-0.2403 diff=0.4975 pos>0=15/48 neg<=0=23/48 perm_p=0.0004998 binom_p=0.9972 youden_t=-0.0009 youden_sens=1.000 youden_spec=0.208 J=0.208
freqhits prompts_marked_above=7/12 instance=key-free-freqhits used_keys=False
hitmass auc=0.604 mean_pos=0.0078 mean_neg=-0.0021 diff=0.0099 pos>0=24/48 neg<=0=19/48 perm_p=0.0004998 binom_p=0.5573 youden_t=0.0087 youden_sens=0.312 youden_spec=1.000 J=0.312
hitmass prompts_marked_above=8/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.638 mean_pos=0.0132 mean_neg=0.0044 diff=0.0088 pos>0=36/48 neg<=0=20/48 perm_p=0.009995 binom_p=0.0003586 youden_t=0.0053 youden_sens=0.708 youden_spec=0.583 J=0.292
hashpool prompts_marked_above=7/12 instance=key-free-hashpool used_keys=False
