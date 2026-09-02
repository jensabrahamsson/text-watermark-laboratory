# Key-free transfer

transfer n_methods=1 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=12 n_test=12 overlap_mode=keep dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| surface | 7/12 | 0.525 | 5/48 | 48/48 | 0.2799 | 0.0019 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| surface | in-sample-youden | 0.0000 | 5/48 | 48/48 | 0.104 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

surface auc=0.525 mean_pos=-0.0209 mean_neg=-0.0228 diff=0.0019 pos>0=5/48 neg<=0=48/48 perm_p=0.2799 binom_p=1 youden_t=0.0000 youden_sens=0.104 youden_spec=1.000 J=0.104
surface prompts_marked_above=7/12 instance=key-free-surface used_keys=False
