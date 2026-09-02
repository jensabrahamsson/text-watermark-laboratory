# Key-free learned scorers

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 11/12 | 0.738 | 18/48 | 44/48 | 0.0004998 | 2.2029 |
| tokmlp | 6/12 | 0.433 | 19/48 | 28/48 | 0.964 | -0.0440 |
| charcnn | 7/12 | 0.497 | 15/48 | 34/48 | 0.5337 | -0.0107 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashlog | 29/48 | 29/48 | -1.8118 | 0.604 | 0.604 |
| tokmlp | 23/48 | 17/48 | -0.0330 | 0.479 | 0.354 |
| charcnn | 11/48 | 29/48 | -0.0147 | 0.229 | 0.604 |

hashlog auc=0.738 mean_pos=-0.3957 mean_neg=-2.5986 diff=2.2029 pos>0=18/48 neg<=0=44/48 perm_p=0.0004998 binom_p=0.9703 youden_t=-1.3752 youden_sens=0.667 youden_spec=0.729 J=0.396
hashlog prompts_marked_above=11/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.433 mean_pos=-0.0590 mean_neg=-0.0150 diff=-0.0440 pos>0=19/48 neg<=0=28/48 perm_p=0.964 binom_p=0.9443 youden_t=-0.0083 youden_sens=0.521 youden_spec=0.562 J=0.083
tokmlp prompts_marked_above=6/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.497 mean_pos=-0.2336 mean_neg=-0.2228 diff=-0.0107 pos>0=15/48 neg<=0=34/48 perm_p=0.5337 binom_p=0.9972 youden_t=-0.1304 youden_sens=0.521 youden_spec=0.562 J=0.083
charcnn prompts_marked_above=7/12 instance=key-free-charcnn used_keys=False
