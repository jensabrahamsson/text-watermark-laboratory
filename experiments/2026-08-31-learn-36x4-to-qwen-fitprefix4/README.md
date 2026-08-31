# Key-free learned transfer

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 7/12 | 0.456 | 1/48 | 47/48 | 0.6657 | -0.1808 |
| tokmlp | 5/12 | 0.500 | 3/48 | 42/48 | 0.6032 | -0.0247 |
| charcnn | 6/12 | 0.496 | 5/48 | 44/48 | 0.4853 | 0.0058 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashlog | in-sample-youden | 0.0000 | 1/48 | 47/48 | 0.021 | 0.979 |
| tokmlp | in-sample-youden | 0.0625 | 3/48 | 43/48 | 0.062 | 0.896 |
| charcnn | in-sample-youden | -1.5504 | 34/48 | 18/48 | 0.708 | 0.375 |
| hashlog | nested-youden | -0.8097 | 1/48 | 46/48 | 0.021 | 0.958 |
| hashlog | nested-fpr10 | -0.2245 | 1/48 | 47/48 | 0.021 | 0.979 |
| tokmlp | nested-youden | -0.2212 | 8/48 | 39/48 | 0.167 | 0.812 |
| tokmlp | nested-fpr10 | -0.0982 | 3/48 | 41/48 | 0.062 | 0.854 |
| charcnn | nested-youden | 0.0488 | 5/48 | 44/48 | 0.104 | 0.917 |
| charcnn | nested-fpr10 | 0.0488 | 5/48 | 44/48 | 0.104 | 0.917 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashlog auc=0.456 mean_pos=-4.6195 mean_neg=-4.4387 diff=-0.1808 pos>0=1/48 neg<=0=47/48 perm_p=0.6657 binom_p=1 youden_t=-7.6008 youden_sens=1.000 youden_spec=0.125 J=0.125
hashlog prompts_marked_above=7/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.500 mean_pos=-0.7556 mean_neg=-0.7309 diff=-0.0247 pos>0=3/48 neg<=0=42/48 perm_p=0.6032 binom_p=1 youden_t=-0.6539 youden_sens=0.479 youden_spec=0.625 J=0.104
tokmlp prompts_marked_above=5/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.496 mean_pos=-1.1361 mean_neg=-1.1419 diff=0.0058 pos>0=5/48 neg<=0=44/48 perm_p=0.4853 binom_p=1 youden_t=0.2015 youden_sens=0.104 youden_spec=1.000 J=0.104
charcnn prompts_marked_above=6/12 instance=key-free-charcnn used_keys=False
