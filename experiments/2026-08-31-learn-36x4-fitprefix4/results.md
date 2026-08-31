# Key-free learned scorers

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 34/36 | 0.864 | 113/144 | 129/144 | 0.0004998 | 7.0167 |
| tokmlp | 32/36 | 0.835 | 89/144 | 118/144 | 0.0004998 | 0.6685 |
| charcnn | 34/36 | 0.834 | 97/144 | 130/144 | 0.0004998 | 1.3026 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashlog | 108/144 | 130/144 | 0.5884 | 0.750 | 0.903 |
| tokmlp | 98/144 | 106/144 | -0.1013 | 0.681 | 0.736 |
| charcnn | 96/144 | 128/144 | 0.1660 | 0.667 | 0.889 |

hashlog auc=0.864 mean_pos=2.8621 mean_neg=-4.1547 diff=7.0167 pos>0=113/144 neg<=0=129/144 perm_p=0.0004998 binom_p=1.853e-12 youden_t=0.5772 youden_sens=0.785 youden_spec=0.910 J=0.694
hashlog prompts_marked_above=34/36 instance=key-free-hashlog used_keys=False
tokmlp auc=0.835 mean_pos=0.3292 mean_neg=-0.3393 diff=0.6685 pos>0=89/144 neg<=0=118/144 perm_p=0.0004998 binom_p=0.002884 youden_t=-0.1355 youden_sens=0.833 youden_spec=0.722 J=0.556
tokmlp prompts_marked_above=32/36 instance=key-free-tokmlp used_keys=False
charcnn auc=0.834 mean_pos=0.5975 mean_neg=-0.7051 diff=1.3026 pos>0=97/144 neg<=0=130/144 perm_p=0.0004998 binom_p=1.878e-05 youden_t=0.2108 youden_sens=0.667 youden_spec=0.931 J=0.597
charcnn prompts_marked_above=34/36 instance=key-free-charcnn used_keys=False
