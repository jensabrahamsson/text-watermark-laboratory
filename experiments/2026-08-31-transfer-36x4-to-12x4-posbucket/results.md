# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.8708 |
| poshits | 10/12 | 0.811 | 39/48 | 31/48 | 0.0004998 | 0.9198 |
| pospool | 9/12 | 0.642 | 26/48 | 29/48 | 0.0004998 | 0.0376 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 42/48 | 24/48 | 0.875 | 0.500 |
| poshits | in-sample-youden | 0.1445 | 17/48 | 42/48 | 0.354 | 0.875 |
| pospool | in-sample-youden | 0.0000 | 26/48 | 29/48 | 0.542 | 0.604 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
poshits auc=0.811 mean_pos=0.8445 mean_neg=-0.0753 diff=0.9198 pos>0=39/48 neg<=0=31/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0098 youden_sens=0.792 youden_spec=0.771 J=0.562
poshits prompts_marked_above=10/12 instance=key-free-poshits used_keys=False
pospool auc=0.642 mean_pos=0.0284 mean_neg=-0.0092 diff=0.0376 pos>0=26/48 neg<=0=29/48 perm_p=0.0004998 binom_p=0.3327 youden_t=0.0308 youden_sens=0.375 youden_spec=0.958 J=0.333
pospool prompts_marked_above=9/12 instance=key-free-pospool used_keys=False
