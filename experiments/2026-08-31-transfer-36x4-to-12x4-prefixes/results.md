# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.8708 |
| hashpool | 11/12 | 0.733 | 30/48 | 36/48 | 0.0004998 | 0.0558 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 42/48 | 24/48 | 0.875 | 0.500 |
| hashpool | in-sample-youden | 0.0000 | 30/48 | 36/48 | 0.625 | 0.750 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

| prefix tokens | method | prompt wins | file auc | marked>0 | unmarked<=0 |
|---|---|---|---|---|---|
| 16 | hits | 11/12 | 0.752 | 40/48 | 23/48 |
| 16 | hashpool | 9/12 | 0.692 | 31/48 | 30/48 |
| 32 | hits | 11/12 | 0.738 | 40/48 | 22/48 |
| 32 | hashpool | 10/12 | 0.719 | 28/48 | 34/48 |
| 64 | hits | 11/12 | 0.775 | 41/48 | 24/48 |
| 64 | hashpool | 9/12 | 0.681 | 29/48 | 33/48 |
| 96 | hits | 12/12 | 0.808 | 41/48 | 25/48 |
| 96 | hashpool | 10/12 | 0.730 | 27/48 | 35/48 |
| 128 | hits | 12/12 | 0.793 | 42/48 | 24/48 |
| 128 | hashpool | 11/12 | 0.733 | 30/48 | 36/48 |

hits auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
hashpool auc=0.733 mean_pos=0.0429 mean_neg=-0.0129 diff=0.0558 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0016 youden_sens=0.625 youden_spec=0.812 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
