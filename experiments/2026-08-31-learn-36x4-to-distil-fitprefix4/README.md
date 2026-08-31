# Key-free learned transfer

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-distilgpt2-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 7/12 | 0.535 | 3/48 | 47/48 | 0.08846 | 0.6640 |
| tokmlp | 8/12 | 0.559 | 8/48 | 40/48 | 0.3073 | 0.0541 |
| charcnn | 2/12 | 0.421 | 2/48 | 43/48 | 0.9635 | -0.2598 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashlog | in-sample-youden | 0.0000 | 3/48 | 47/48 | 0.062 | 0.979 |
| tokmlp | in-sample-youden | -0.0947 | 9/48 | 38/48 | 0.188 | 0.792 |
| charcnn | in-sample-youden | 0.0013 | 2/48 | 43/48 | 0.042 | 0.896 |
| hashlog | nested-youden | -0.8097 | 4/48 | 47/48 | 0.083 | 0.979 |
| hashlog | nested-fpr10 | -0.2245 | 4/48 | 47/48 | 0.083 | 0.979 |
| tokmlp | nested-youden | -0.2212 | 9/48 | 38/48 | 0.188 | 0.792 |
| tokmlp | nested-fpr10 | -0.0982 | 9/48 | 38/48 | 0.188 | 0.792 |
| charcnn | nested-youden | 0.0488 | 2/48 | 43/48 | 0.042 | 0.896 |
| charcnn | nested-fpr10 | 0.0488 | 2/48 | 43/48 | 0.042 | 0.896 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashlog auc=0.535 mean_pos=-4.5015 mean_neg=-5.1656 diff=0.6640 pos>0=3/48 neg<=0=47/48 perm_p=0.08846 binom_p=1 youden_t=-2.6043 youden_sens=0.208 youden_spec=0.958 J=0.167
hashlog prompts_marked_above=7/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.559 mean_pos=-0.4967 mean_neg=-0.5508 diff=0.0541 pos>0=8/48 neg<=0=40/48 perm_p=0.3073 binom_p=1 youden_t=-0.6474 youden_sens=0.646 youden_spec=0.583 J=0.229
tokmlp prompts_marked_above=8/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.421 mean_pos=-1.2965 mean_neg=-1.0367 diff=-0.2598 pos>0=2/48 neg<=0=43/48 perm_p=0.9635 binom_p=1 youden_t=-1.6346 youden_sens=0.688 youden_spec=0.375 J=0.062
charcnn prompts_marked_above=2/12 instance=key-free-charcnn used_keys=False
