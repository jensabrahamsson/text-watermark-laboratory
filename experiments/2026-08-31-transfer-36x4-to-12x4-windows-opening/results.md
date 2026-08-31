# Key-free transfer

transfer n_methods=1 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.8708 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 42/48 | 24/48 | 0.875 | 0.500 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

| window tokens | method | prompt wins | file auc | marked>0 | unmarked<=0 |
|---|---|---|---|---|---|
| 0:4 | hits | 11/12 | 0.752 | 40/48 | 23/48 |
| 0:16 | hits | 11/12 | 0.752 | 40/48 | 23/48 |
| 4:16 | hits | 9/12 | 0.617 | 26/48 | 30/48 |
| 16:32 | hits | 8/12 | 0.512 | 27/48 | 22/48 |

hits auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
