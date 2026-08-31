# Key-free learned transfer

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=True prompt_context=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 5/12 | 0.560 | 15/48 | 47/48 | 0.004498 | 2.6212 |
| tokmlp | 8/12 | 0.647 | 15/48 | 43/48 | 0.001499 | 0.4989 |
| charcnn | 8/12 | 0.655 | 15/48 | 43/48 | 0.0009995 | 0.7259 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashlog | in-sample-youden | 0.0000 | 15/48 | 47/48 | 0.312 | 0.979 |
| tokmlp | in-sample-youden | 0.0504 | 15/48 | 43/48 | 0.312 | 0.896 |
| charcnn | in-sample-youden | 0.0843 | 15/48 | 44/48 | 0.312 | 0.917 |
| hashlog | nested-youden | 0.0000 | 15/48 | 47/48 | 0.312 | 0.979 |
| hashlog | nested-fpr10 | -0.1613 | 15/48 | 47/48 | 0.312 | 0.979 |
| tokmlp | nested-youden | -0.1052 | 15/48 | 41/48 | 0.312 | 0.854 |
| tokmlp | nested-fpr10 | 0.0695 | 15/48 | 43/48 | 0.312 | 0.896 |
| charcnn | nested-youden | 0.3131 | 15/48 | 45/48 | 0.312 | 0.938 |
| charcnn | nested-fpr10 | 0.5586 | 15/48 | 45/48 | 0.312 | 0.938 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashlog auc=0.560 mean_pos=-3.5489 mean_neg=-6.1701 diff=2.6212 pos>0=15/48 neg<=0=47/48 perm_p=0.004498 binom_p=0.9972 youden_t=0.1081 youden_sens=0.312 youden_spec=1.000 J=0.312
hashlog prompts_marked_above=5/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.647 mean_pos=-0.2762 mean_neg=-0.7750 diff=0.4989 pos>0=15/48 neg<=0=43/48 perm_p=0.001499 binom_p=0.9972 youden_t=-1.2167 youden_sens=0.979 youden_spec=0.292 J=0.271
tokmlp prompts_marked_above=8/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.655 mean_pos=-0.6773 mean_neg=-1.4032 diff=0.7259 pos>0=15/48 neg<=0=43/48 perm_p=0.0009995 binom_p=0.9972 youden_t=-1.8819 youden_sens=0.896 youden_spec=0.417 J=0.312
charcnn prompts_marked_above=8/12 instance=key-free-charcnn used_keys=False
