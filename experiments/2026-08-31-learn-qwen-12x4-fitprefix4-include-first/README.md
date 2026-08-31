# Key-free learned scorers

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=True prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 12/12 | 0.826 | 25/48 | 43/48 | 0.0004998 | 3.2670 |
| tokmlp | 9/12 | 0.678 | 30/48 | 38/48 | 0.003498 | 0.2300 |
| charcnn | 9/12 | 0.646 | 25/48 | 34/48 | 0.01049 | 0.3358 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashlog | 36/48 | 36/48 | -1.5898 | 0.750 | 0.750 |
| tokmlp | 30/48 | 39/48 | 0.0411 | 0.625 | 0.812 |
| charcnn | 30/48 | 26/48 | -0.1940 | 0.625 | 0.542 |

hashlog auc=0.826 mean_pos=0.1984 mean_neg=-3.0686 diff=3.2670 pos>0=25/48 neg<=0=43/48 perm_p=0.0004998 binom_p=0.4427 youden_t=-1.6132 youden_sens=0.833 youden_spec=0.750 J=0.583
hashlog prompts_marked_above=12/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.678 mean_pos=-0.0279 mean_neg=-0.2579 diff=0.2300 pos>0=30/48 neg<=0=38/48 perm_p=0.003498 binom_p=0.0557 youden_t=0.0432 youden_sens=0.625 youden_spec=0.833 J=0.458
tokmlp prompts_marked_above=9/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.646 mean_pos=-0.0765 mean_neg=-0.4124 diff=0.3358 pos>0=25/48 neg<=0=34/48 perm_p=0.01049 binom_p=0.4427 youden_t=-0.0766 youden_sens=0.625 youden_spec=0.688 J=0.312
charcnn prompts_marked_above=9/12 instance=key-free-charcnn used_keys=False
