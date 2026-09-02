# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=True prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.702 | 16/48 | 42/48 | 0.0004998 | 1.1347 |
| first | 6/12 | 0.555 | 16/48 | 40/48 | 0.1784 | 0.2256 |
| poshits | 9/12 | 0.719 | 16/48 | 44/48 | 0.0004998 | 1.3671 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.4216 | 16/48 | 46/48 | 0.333 | 0.958 |
| first | in-sample-youden | 0.0000 | 16/48 | 40/48 | 0.333 | 0.833 |
| poshits | in-sample-youden | 0.4216 | 16/48 | 48/48 | 0.333 | 1.000 |
| hits | nested-youden | 0.4202 | 16/48 | 46/48 | 0.333 | 0.958 |
| hits | nested-fpr10 | 0.1431 | 16/48 | 46/48 | 0.333 | 0.958 |
| first | nested-youden | 0.0000 | 16/48 | 40/48 | 0.333 | 0.833 |
| first | nested-fpr10 | 0.9299 | 0/48 | 48/48 | 0.000 | 1.000 |
| poshits | nested-youden | 0.4202 | 16/48 | 48/48 | 0.333 | 1.000 |
| poshits | nested-fpr10 | 0.1431 | 16/48 | 48/48 | 0.333 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.702 mean_pos=0.5084 mean_neg=-0.6263 diff=1.1347 pos>0=16/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.9934 youden_t=-0.7465 youden_sens=1.000 youden_spec=0.417 J=0.417
hits prompts_marked_above=9/12 instance=key-free-hits used_keys=False
first auc=0.555 mean_pos=-0.5173 mean_neg=-0.7429 diff=0.2256 pos>0=16/48 neg<=0=40/48 perm_p=0.1784 binom_p=0.9934 youden_t=-2.1972 youden_sens=1.000 youden_spec=0.188 J=0.188
first prompts_marked_above=6/12 instance=key-free-first used_keys=False
poshits auc=0.719 mean_pos=0.5054 mean_neg=-0.8617 diff=1.3671 pos>0=16/48 neg<=0=44/48 perm_p=0.0004998 binom_p=0.9934 youden_t=-1.0986 youden_sens=1.000 youden_spec=0.438 J=0.438
poshits prompts_marked_above=9/12 instance=key-free-poshits used_keys=False
