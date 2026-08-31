# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=1 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 7/12 | 0.500 | 5/12 | 3/12 | 0.1789 | 0.3614 |
| freqhits | 9/12 | 0.455 | 3/12 | 7/12 | 0.5512 | -0.0004 |
| hitmass | 7/12 | 0.503 | 5/12 | 3/12 | 0.1789 | 0.0028 |
| hashpool | 8/12 | 0.674 | 8/12 | 8/12 | 0.03898 | 0.0096 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 5/12 | 9/12 | 0.0145 | 0.417 | 0.750 |
| freqhits | 3/12 | 9/12 | 0.0119 | 0.250 | 0.750 |
| hitmass | 4/12 | 11/12 | 0.0001 | 0.333 | 0.917 |
| hashpool | 8/12 | 9/12 | 0.0030 | 0.667 | 0.750 |

hits auc=0.500 mean_pos=0.3703 mean_neg=0.0089 diff=0.3614 pos>0=5/12 neg<=0=3/12 perm_p=0.1789 binom_p=0.8062 youden_t=0.0146 youden_sens=0.417 youden_spec=0.833 J=0.250
hits prompts_marked_above=7/12 instance=key-free-hits used_keys=False
freqhits auc=0.455 mean_pos=0.0051 mean_neg=0.0055 diff=-0.0004 pos>0=3/12 neg<=0=7/12 perm_p=0.5512 binom_p=0.9807 youden_t=0.0121 youden_sens=0.250 youden_spec=0.833 J=0.083
freqhits prompts_marked_above=9/12 instance=key-free-freqhits used_keys=False
hitmass auc=0.503 mean_pos=0.0029 mean_neg=0.0001 diff=0.0028 pos>0=5/12 neg<=0=3/12 perm_p=0.1789 binom_p=0.8062 youden_t=0.0001 youden_sens=0.333 youden_spec=1.000 J=0.333
hitmass prompts_marked_above=7/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.674 mean_pos=0.0085 mean_neg=-0.0011 diff=0.0096 pos>0=8/12 neg<=0=8/12 perm_p=0.03898 binom_p=0.1938 youden_t=0.0032 youden_sens=0.667 youden_spec=0.833 J=0.500
hashpool prompts_marked_above=8/12 instance=key-free-hashpool used_keys=False
