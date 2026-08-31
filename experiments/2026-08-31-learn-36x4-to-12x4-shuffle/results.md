# Key-free learned transfer

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=0 used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 10/12 | 0.678 | 44/48 | 27/48 | 0.0004998 | 2.3395 |
| tokmlp | 5/12 | 0.471 | 6/48 | 40/48 | 0.5812 | -0.0000 |
| charcnn | 10/12 | 0.745 | 27/48 | 40/48 | 0.0004998 | 0.0936 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashlog | in-sample-youden | 0.0000 | 44/48 | 27/48 | 0.917 | 0.562 |
| tokmlp | in-sample-youden | -0.0001 | 15/48 | 31/48 | 0.312 | 0.646 |
| charcnn | in-sample-youden | -0.0482 | 34/48 | 34/48 | 0.708 | 0.708 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashlog auc=0.678 mean_pos=1.7240 mean_neg=-0.6155 diff=2.3395 pos>0=44/48 neg<=0=27/48 perm_p=0.0004998 binom_p=7.569e-10 youden_t=0.1005 youden_sens=0.917 youden_spec=0.604 J=0.521
hashlog prompts_marked_above=10/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.471 mean_pos=-0.0002 mean_neg=-0.0002 diff=-0.0000 pos>0=6/48 neg<=0=40/48 perm_p=0.5812 binom_p=1 youden_t=-0.0005 youden_sens=1.000 youden_spec=0.125 J=0.125
tokmlp prompts_marked_above=5/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.745 mean_pos=0.0540 mean_neg=-0.0395 diff=0.0936 pos>0=27/48 neg<=0=40/48 perm_p=0.0004998 binom_p=0.2354 youden_t=0.0257 youden_sens=0.562 youden_spec=0.896 J=0.458
charcnn prompts_marked_above=10/12 instance=key-free-charcnn used_keys=False
