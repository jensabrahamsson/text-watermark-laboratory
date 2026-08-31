# Key-free transfer

transfer n_methods=6 train=experiments/2026-08-17-pair-36 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. Thresholds are Youden on the training files (in-sample), then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 10/12 | 0.640 | 32/48 | 27/48 | 0.002999 | 0.0428 |
| hits | 8/12 | 0.769 | 39/48 | 28/48 | 0.0004998 | 0.6630 |
| hashpool | 11/12 | 0.766 | 34/48 | 30/48 | 0.0004998 | 0.0483 |
| hashvote | 5/12 | 0.535 | 28/48 | 25/48 | 0.2804 | 0.0130 |
| hybrid | 10/12 | 0.757 | 34/48 | 31/48 | 0.0004998 | 0.0523 |
| stack | 10/12 | 0.754 | 27/48 | 35/48 | 0.0004998 | 0.7293 |

| method | train Youden t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hard | -0.8246 | 48/48 | 0/48 | 1.000 | 0.000 |
| hits | 0.0000 | 39/48 | 28/48 | 0.812 | 0.583 |
| hashpool | 0.0000 | 34/48 | 30/48 | 0.708 | 0.625 |
| hashvote | 0.0000 | 28/48 | 25/48 | 0.583 | 0.521 |
| hybrid | 0.0000 | 34/48 | 31/48 | 0.708 | 0.646 |
| stack | 0.0000 | 27/48 | 35/48 | 0.562 | 0.729 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hard auc=0.640 mean_pos=0.0292 mean_neg=-0.0136 diff=0.0428 pos>0=32/48 neg<=0=27/48 perm_p=0.002999 binom_p=0.01465 youden_t=-0.0225 youden_sens=0.771 youden_spec=0.479 J=0.250
hard prompts_marked_above=10/12 instance=key-free-counts used_keys=False
hits auc=0.769 mean_pos=0.6757 mean_neg=0.0127 diff=0.6630 pos>0=39/48 neg<=0=28/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0009 youden_sens=0.812 youden_spec=0.667 J=0.479
hits prompts_marked_above=8/12 instance=key-free-hits used_keys=False
hashpool auc=0.766 mean_pos=0.0412 mean_neg=-0.0071 diff=0.0483 pos>0=34/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0143 youden_sens=0.562 youden_spec=0.854 J=0.417
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
hashvote auc=0.535 mean_pos=0.0125 mean_neg=-0.0005 diff=0.0130 pos>0=28/48 neg<=0=25/48 perm_p=0.2804 binom_p=0.1562 youden_t=0.0000 youden_sens=0.583 youden_spec=0.521 J=0.104
hashvote prompts_marked_above=5/12 instance=key-free-hashvote used_keys=False
hybrid auc=0.757 mean_pos=0.0445 mean_neg=-0.0078 diff=0.0523 pos>0=34/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.002758 youden_t=-0.0032 youden_sens=0.771 youden_spec=0.604 J=0.375
hybrid prompts_marked_above=10/12 instance=key-free-hybrid used_keys=False
stack auc=0.754 mean_pos=0.5365 mean_neg=-0.1928 diff=0.7293 pos>0=27/48 neg<=0=35/48 perm_p=0.0004998 binom_p=0.2354 youden_t=-0.2101 youden_sens=0.833 youden_spec=0.604 J=0.438
stack prompts_marked_above=10/12 instance=key-free-stack used_keys=False
