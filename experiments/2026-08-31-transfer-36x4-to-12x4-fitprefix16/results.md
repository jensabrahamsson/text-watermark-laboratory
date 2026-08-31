# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.818 | 39/48 | 31/48 | 0.0004998 | 1.4989 |
| hashpool | 9/12 | 0.636 | 27/48 | 26/48 | 0.0004998 | 0.2600 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.6770 | 16/48 | 44/48 | 0.333 | 0.917 |
| hashpool | in-sample-youden | 0.0000 | 27/48 | 26/48 | 0.562 | 0.542 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.818 mean_pos=1.2024 mean_neg=-0.2966 diff=1.4989 pos>0=39/48 neg<=0=31/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0108 youden_sens=0.812 youden_spec=0.771 J=0.583
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
hashpool auc=0.636 mean_pos=0.2470 mean_neg=-0.0130 diff=0.2600 pos>0=27/48 neg<=0=26/48 perm_p=0.0004998 binom_p=0.2354 youden_t=0.0570 youden_sens=0.417 youden_spec=0.938 J=0.354
hashpool prompts_marked_above=9/12 instance=key-free-hashpool used_keys=False
