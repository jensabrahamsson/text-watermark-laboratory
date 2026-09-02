# Key-free transfer

transfer n_methods=1 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.516 | 10/48 | 38/48 | 0.1529 | 0.1002 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.7314 | 0/48 | 48/48 | 0.000 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

poshits auc=0.516 mean_pos=0.0231 mean_neg=-0.0771 diff=0.1002 pos>0=10/48 neg<=0=38/48 perm_p=0.1529 binom_p=1 youden_t=-2.0866 youden_sens=1.000 youden_spec=0.042 J=0.042
poshits prompts_marked_above=8/12 instance=key-free-poshits used_keys=False
