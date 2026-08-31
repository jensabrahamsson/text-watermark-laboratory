# Key-free learned transfer

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 7/12 | 0.606 | 14/48 | 47/48 | 0.004498 | 2.4400 |
| tokmlp | 8/12 | 0.714 | 28/48 | 38/48 | 0.0004998 | 0.7763 |
| charcnn | 7/12 | 0.557 | 16/48 | 41/48 | 0.001499 | 0.6800 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashlog | in-sample-youden | 0.0000 | 14/48 | 47/48 | 0.292 | 0.979 |
| tokmlp | in-sample-youden | -0.0720 | 30/48 | 38/48 | 0.625 | 0.792 |
| charcnn | in-sample-youden | 0.0013 | 16/48 | 41/48 | 0.333 | 0.854 |
| hashlog | nested-youden | -0.8097 | 15/48 | 45/48 | 0.312 | 0.938 |
| hashlog | nested-fpr10 | -0.2245 | 14/48 | 46/48 | 0.292 | 0.958 |
| tokmlp | nested-youden | -0.2212 | 30/48 | 37/48 | 0.625 | 0.771 |
| tokmlp | nested-fpr10 | -0.0982 | 30/48 | 38/48 | 0.625 | 0.792 |
| charcnn | nested-youden | 0.0488 | 16/48 | 41/48 | 0.333 | 0.854 |
| charcnn | nested-fpr10 | 0.0488 | 16/48 | 41/48 | 0.333 | 0.854 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashlog auc=0.606 mean_pos=-2.4896 mean_neg=-4.9297 diff=2.4400 pos>0=14/48 neg<=0=47/48 perm_p=0.004498 binom_p=0.999 youden_t=0.0000 youden_sens=0.292 youden_spec=0.979 J=0.271
hashlog prompts_marked_above=7/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.714 mean_pos=0.1307 mean_neg=-0.6457 diff=0.7763 pos>0=28/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.1562 youden_t=-0.4251 youden_sens=0.708 youden_spec=0.750 J=0.458
tokmlp prompts_marked_above=8/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.557 mean_pos=-0.4094 mean_neg=-1.0894 diff=0.6800 pos>0=16/48 neg<=0=41/48 perm_p=0.001499 binom_p=0.9934 youden_t=-0.5692 youden_sens=0.500 youden_spec=0.792 J=0.292
charcnn prompts_marked_above=7/12 instance=key-free-charcnn used_keys=False
