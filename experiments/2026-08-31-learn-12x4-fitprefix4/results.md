# Key-free learned scorers

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

probe n_methods=3 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 11/12 | 0.894 | 35/48 | 45/48 | 0.0004998 | 4.6401 |
| tokmlp | 9/12 | 0.604 | 26/48 | 34/48 | 0.1029 | 0.1143 |
| charcnn | 9/12 | 0.757 | 34/48 | 38/48 | 0.0004998 | 0.9106 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashlog | 36/48 | 43/48 | -0.4764 | 0.750 | 0.896 |
| tokmlp | 24/48 | 36/48 | 0.0650 | 0.500 | 0.750 |
| charcnn | 32/48 | 43/48 | 0.5326 | 0.667 | 0.896 |

hashlog auc=0.894 mean_pos=1.6894 mean_neg=-2.9507 diff=4.6401 pos>0=35/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.001044 youden_t=-0.5140 youden_sens=0.812 youden_spec=0.917 J=0.729
hashlog prompts_marked_above=11/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.604 mean_pos=-0.0624 mean_neg=-0.1768 diff=0.1143 pos>0=26/48 neg<=0=34/48 perm_p=0.1029 binom_p=0.3327 youden_t=0.0642 youden_sens=0.542 youden_spec=0.771 J=0.312
tokmlp prompts_marked_above=9/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.757 mean_pos=0.4053 mean_neg=-0.5053 diff=0.9106 pos>0=34/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.5396 youden_sens=0.667 youden_spec=0.917 J=0.583
charcnn prompts_marked_above=9/12 instance=key-free-charcnn used_keys=False
