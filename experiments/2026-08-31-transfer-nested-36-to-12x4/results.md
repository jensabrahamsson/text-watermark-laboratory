# Key-free transfer

transfer n_methods=8 train=experiments/2026-08-17-pair-36 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 10/12 | 0.640 | 32/48 | 27/48 | 0.002999 | 0.0428 |
| hits | 8/12 | 0.769 | 39/48 | 28/48 | 0.0004998 | 0.6630 |
| freqhits | 7/12 | 0.763 | 39/48 | 28/48 | 0.001999 | 0.6593 |
| hitmass | 10/12 | 0.771 | 39/48 | 28/48 | 0.0004998 | 0.0298 |
| hashpool | 11/12 | 0.766 | 34/48 | 30/48 | 0.0004998 | 0.0483 |
| hybrid | 10/12 | 0.757 | 34/48 | 31/48 | 0.0004998 | 0.0523 |
| hashmix | 11/12 | 0.681 | 33/48 | 23/48 | 0.0004998 | 0.0409 |
| stack | 10/12 | 0.754 | 27/48 | 35/48 | 0.0004998 | 0.7293 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hard | in-sample-youden | -0.8246 | 48/48 | 0/48 | 1.000 | 0.000 |
| hits | in-sample-youden | 0.0000 | 39/48 | 28/48 | 0.812 | 0.583 |
| freqhits | in-sample-youden | 0.0000 | 39/48 | 28/48 | 0.812 | 0.583 |
| hitmass | in-sample-youden | 0.0000 | 39/48 | 28/48 | 0.812 | 0.583 |
| hashpool | in-sample-youden | 0.0000 | 34/48 | 30/48 | 0.708 | 0.625 |
| hybrid | in-sample-youden | 0.0000 | 34/48 | 31/48 | 0.708 | 0.646 |
| hashmix | in-sample-youden | 0.0000 | 33/48 | 23/48 | 0.688 | 0.479 |
| stack | in-sample-youden | 0.0000 | 27/48 | 35/48 | 0.562 | 0.729 |
| hard | nested-youden | 0.0074 | 30/48 | 27/48 | 0.625 | 0.562 |
| hard | nested-fpr10 | 0.0516 | 17/48 | 36/48 | 0.354 | 0.750 |
| hits | nested-youden | 0.3676 | 22/48 | 40/48 | 0.458 | 0.833 |
| hits | nested-fpr10 | 0.3676 | 22/48 | 40/48 | 0.458 | 0.833 |
| freqhits | nested-youden | 0.5532 | 21/48 | 41/48 | 0.438 | 0.854 |
| freqhits | nested-fpr10 | 0.5297 | 21/48 | 40/48 | 0.438 | 0.833 |
| hitmass | nested-youden | 0.0130 | 17/48 | 44/48 | 0.354 | 0.917 |
| hitmass | nested-fpr10 | 0.0120 | 19/48 | 43/48 | 0.396 | 0.896 |
| hashpool | nested-youden | 0.0053 | 33/48 | 34/48 | 0.688 | 0.708 |
| hashpool | nested-fpr10 | 0.0155 | 26/48 | 41/48 | 0.542 | 0.854 |
| stack | nested-youden | 0.0033 | 27/48 | 35/48 | 0.562 | 0.729 |
| stack | nested-fpr10 | -0.0262 | 27/48 | 35/48 | 0.562 | 0.729 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hard auc=0.640 mean_pos=0.0292 mean_neg=-0.0136 diff=0.0428 pos>0=32/48 neg<=0=27/48 perm_p=0.002999 binom_p=0.01465 youden_t=-0.0225 youden_sens=0.771 youden_spec=0.479 J=0.250
hard prompts_marked_above=10/12 instance=key-free-counts used_keys=False
hits auc=0.769 mean_pos=0.6757 mean_neg=0.0127 diff=0.6630 pos>0=39/48 neg<=0=28/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0009 youden_sens=0.812 youden_spec=0.667 J=0.479
hits prompts_marked_above=8/12 instance=key-free-hits used_keys=False
freqhits auc=0.763 mean_pos=0.7244 mean_neg=0.0651 diff=0.6593 pos>0=39/48 neg<=0=28/48 perm_p=0.001999 binom_p=7.611e-06 youden_t=0.0041 youden_sens=0.750 youden_spec=0.729 J=0.479
freqhits prompts_marked_above=7/12 instance=key-free-freqhits used_keys=False
hitmass auc=0.771 mean_pos=0.0291 mean_neg=-0.0007 diff=0.0298 pos>0=39/48 neg<=0=28/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.792 youden_spec=0.667 J=0.458
hitmass prompts_marked_above=10/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.766 mean_pos=0.0412 mean_neg=-0.0071 diff=0.0483 pos>0=34/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0143 youden_sens=0.562 youden_spec=0.854 J=0.417
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
hybrid auc=0.757 mean_pos=0.0445 mean_neg=-0.0078 diff=0.0523 pos>0=34/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.002758 youden_t=-0.0032 youden_sens=0.771 youden_spec=0.604 J=0.375
hybrid prompts_marked_above=10/12 instance=key-free-hybrid used_keys=False
hashmix auc=0.681 mean_pos=0.0353 mean_neg=-0.0056 diff=0.0409 pos>0=33/48 neg<=0=23/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.0277 youden_sens=0.479 youden_spec=0.875 J=0.354
hashmix prompts_marked_above=11/12 instance=key-free-hashmix used_keys=False
stack auc=0.754 mean_pos=0.5365 mean_neg=-0.1928 diff=0.7293 pos>0=27/48 neg<=0=35/48 perm_p=0.0004998 binom_p=0.2354 youden_t=-0.2101 youden_sens=0.833 youden_spec=0.604 J=0.438
stack prompts_marked_above=10/12 instance=key-free-stack used_keys=False
