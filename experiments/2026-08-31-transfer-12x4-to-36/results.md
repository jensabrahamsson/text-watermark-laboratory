# Key-free transfer

transfer n_methods=6 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-17-pair-36 n_train=12 n_test=24 overlap_mode=drop-from-test dropped=12 context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. Thresholds are Youden on the training files (in-sample), then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 14/24 | 0.606 | 16/24 | 12/24 | 0.05447 | 0.0290 |
| hits | 24/24 | 0.986 | 24/24 | 14/24 | 0.0004998 | 1.1854 |
| hashpool | 23/24 | 0.924 | 21/24 | 20/24 | 0.0004998 | 0.0506 |
| hashvote | 14/24 | 0.537 | 14/24 | 11/24 | 0.3973 | 0.0044 |
| hybrid | 23/24 | 0.946 | 22/24 | 20/24 | 0.0004998 | 0.0569 |
| stack | 21/24 | 0.880 | 12/24 | 24/24 | 0.0004998 | 0.9841 |

| method | train Youden t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hard | 0.6101 | 0/24 | 24/24 | 0.000 | 1.000 |
| hits | -0.2541 | 24/24 | 6/24 | 1.000 | 0.250 |
| hashpool | 0.0000 | 21/24 | 20/24 | 0.875 | 0.833 |
| hashvote | 0.0000 | 14/24 | 11/24 | 0.583 | 0.458 |
| hybrid | 0.0000 | 22/24 | 20/24 | 0.917 | 0.833 |
| stack | 0.0000 | 12/24 | 24/24 | 0.500 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hard auc=0.606 mean_pos=0.0254 mean_neg=-0.0036 diff=0.0290 pos>0=16/24 neg<=0=12/24 perm_p=0.05447 binom_p=0.07579 youden_t=0.0630 youden_sens=0.250 youden_spec=1.000 J=0.250
hard prompts_marked_above=14/24 instance=key-free-counts used_keys=False
hits auc=0.986 mean_pos=1.0386 mean_neg=-0.1468 diff=1.1854 pos>0=24/24 neg<=0=14/24 perm_p=0.0004998 binom_p=5.96e-08 youden_t=0.3485 youden_sens=0.917 youden_spec=1.000 J=0.917
hits prompts_marked_above=24/24 instance=key-free-hits used_keys=False
hashpool auc=0.924 mean_pos=0.0343 mean_neg=-0.0163 diff=0.0506 pos>0=21/24 neg<=0=20/24 perm_p=0.0004998 binom_p=0.0001386 youden_t=-0.0034 youden_sens=0.917 youden_spec=0.833 J=0.750
hashpool prompts_marked_above=23/24 instance=key-free-hashpool used_keys=False
hashvote auc=0.537 mean_pos=0.0041 mean_neg=-0.0003 diff=0.0044 pos>0=14/24 neg<=0=11/24 perm_p=0.3973 binom_p=0.2706 youden_t=0.0234 youden_sens=0.417 youden_spec=0.708 J=0.125
hashvote prompts_marked_above=14/24 instance=key-free-hashvote used_keys=False
hybrid auc=0.946 mean_pos=0.0394 mean_neg=-0.0175 diff=0.0569 pos>0=22/24 neg<=0=20/24 perm_p=0.0004998 binom_p=1.794e-05 youden_t=0.0039 youden_sens=0.917 youden_spec=0.875 J=0.792
hybrid prompts_marked_above=23/24 instance=key-free-hybrid used_keys=False
stack auc=0.880 mean_pos=0.1896 mean_neg=-0.7945 diff=0.9841 pos>0=12/24 neg<=0=24/24 perm_p=0.0004998 binom_p=0.5806 youden_t=-0.2553 youden_sens=0.708 youden_spec=0.958 J=0.667
stack prompts_marked_above=21/24 instance=key-free-stack used_keys=False
