# Key-free transfer

transfer n_methods=6 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 8/12 | 0.607 | 29/48 | 29/48 | 0.04548 | 0.0259 |
| hits | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.8708 |
| freqhits | 9/12 | 0.740 | 37/48 | 27/48 | 0.0009995 | 0.8403 |
| hitmass | 11/12 | 0.784 | 42/48 | 24/48 | 0.0004998 | 0.0394 |
| hashpool | 11/12 | 0.733 | 30/48 | 36/48 | 0.0004998 | 0.0558 |
| logit | 12/12 | 0.812 | 21/48 | 45/48 | 0.0004998 | 1.5527 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hard | in-sample-youden | -1.5873 | 48/48 | 0/48 | 1.000 | 0.000 |
| hits | in-sample-youden | 0.0000 | 42/48 | 24/48 | 0.875 | 0.500 |
| freqhits | in-sample-youden | 0.3863 | 24/48 | 42/48 | 0.500 | 0.875 |
| hitmass | in-sample-youden | 0.0000 | 42/48 | 24/48 | 0.875 | 0.500 |
| hashpool | in-sample-youden | 0.0000 | 30/48 | 36/48 | 0.625 | 0.750 |
| logit | in-sample-youden | 0.0000 | 21/48 | 45/48 | 0.438 | 0.938 |
| hard | nested-youden | 0.0514 | 17/48 | 38/48 | 0.354 | 0.792 |
| hard | nested-fpr10 | 0.1029 | 5/48 | 46/48 | 0.104 | 0.958 |
| hits | nested-youden | 0.5349 | 26/48 | 44/48 | 0.542 | 0.917 |
| hits | nested-fpr10 | 0.5901 | 21/48 | 45/48 | 0.438 | 0.938 |
| freqhits | nested-youden | 0.5336 | 24/48 | 42/48 | 0.500 | 0.875 |
| freqhits | nested-fpr10 | 0.9716 | 21/48 | 43/48 | 0.438 | 0.896 |
| hitmass | nested-youden | 0.0240 | 17/48 | 45/48 | 0.354 | 0.938 |
| hitmass | nested-fpr10 | 0.0171 | 17/48 | 44/48 | 0.354 | 0.917 |
| hashpool | nested-youden | 0.0434 | 16/48 | 47/48 | 0.333 | 0.979 |
| hashpool | nested-fpr10 | 0.0334 | 18/48 | 45/48 | 0.375 | 0.938 |
| logit | nested-youden | 0.2391 | 19/48 | 45/48 | 0.396 | 0.938 |
| logit | nested-fpr10 | -0.5011 | 30/48 | 38/48 | 0.625 | 0.792 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hard auc=0.607 mean_pos=0.0143 mean_neg=-0.0116 diff=0.0259 pos>0=29/48 neg<=0=29/48 perm_p=0.04548 binom_p=0.09671 youden_t=0.0034 youden_sens=0.604 youden_spec=0.667 J=0.271
hard prompts_marked_above=8/12 instance=key-free-counts used_keys=False
hits auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
freqhits auc=0.740 mean_pos=0.8314 mean_neg=-0.0088 diff=0.8403 pos>0=37/48 neg<=0=27/48 perm_p=0.0009995 binom_p=0.0001111 youden_t=0.0018 youden_sens=0.771 youden_spec=0.604 J=0.375
freqhits prompts_marked_above=9/12 instance=key-free-freqhits used_keys=False
hitmass auc=0.784 mean_pos=0.0394 mean_neg=0.0000 diff=0.0394 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.0000 youden_sens=0.875 youden_spec=0.583 J=0.458
hitmass prompts_marked_above=11/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.733 mean_pos=0.0429 mean_neg=-0.0129 diff=0.0558 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0016 youden_sens=0.625 youden_spec=0.812 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
logit auc=0.812 mean_pos=0.6215 mean_neg=-0.9312 diff=1.5527 pos>0=21/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.8438 youden_t=-0.3871 youden_sens=0.583 youden_spec=0.896 J=0.479
logit prompts_marked_above=12/12 instance=key-free-logit used_keys=False
