# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 6/12 | 0.445 | 25/48 | 23/48 | 0.6982 | -0.0767 |
| hashpool | 3/12 | 0.447 | 8/48 | 37/48 | 0.7656 | -0.0027 |
| surface | 6/12 | 0.461 | 0/48 | 48/48 | 0.6827 | -0.0011 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 25/48 | 23/48 | 0.521 | 0.479 |
| hashpool | in-sample-youden | 0.0000 | 8/48 | 37/48 | 0.167 | 0.771 |
| surface | in-sample-youden | 0.0000 | 0/48 | 48/48 | 0.000 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.445 mean_pos=-0.1581 mean_neg=-0.0814 diff=-0.0767 pos>0=25/48 neg<=0=23/48 perm_p=0.6982 binom_p=0.4427 youden_t=-0.0066 youden_sens=0.688 youden_spec=0.396 J=0.083
hits prompts_marked_above=6/12 instance=key-free-hits used_keys=False
hashpool auc=0.447 mean_pos=-0.0146 mean_neg=-0.0119 diff=-0.0027 pos>0=8/48 neg<=0=37/48 perm_p=0.7656 binom_p=1 youden_t=0.0108 youden_sens=0.146 youden_spec=0.917 J=0.062
hashpool prompts_marked_above=3/12 instance=key-free-hashpool used_keys=False
surface auc=0.461 mean_pos=-0.0273 mean_neg=-0.0262 diff=-0.0011 pos>0=0/48 neg<=0=48/48 perm_p=0.6827 binom_p=1 youden_t=-0.0459 youden_sens=0.958 youden_spec=0.104 J=0.062
surface prompts_marked_above=6/12 instance=key-free-surface used_keys=False
