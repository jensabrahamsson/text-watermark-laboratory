# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-distilgpt2-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 5/12 | 0.462 | 25/48 | 19/48 | 0.6892 | -0.0859 |
| hashpool | 9/12 | 0.615 | 20/48 | 38/48 | 0.01299 | 0.0123 |
| poshits | 9/12 | 0.585 | 18/48 | 29/48 | 0.001499 | 0.5471 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 25/48 | 19/48 | 0.521 | 0.396 |
| hashpool | in-sample-youden | 0.0000 | 20/48 | 38/48 | 0.417 | 0.792 |
| poshits | in-sample-youden | 0.1445 | 5/48 | 45/48 | 0.104 | 0.938 |
| hits | nested-youden | 0.5349 | 9/48 | 41/48 | 0.188 | 0.854 |
| hits | nested-fpr10 | 0.5901 | 9/48 | 41/48 | 0.188 | 0.854 |
| hashpool | nested-youden | 0.0434 | 3/48 | 48/48 | 0.062 | 1.000 |
| hashpool | nested-fpr10 | 0.0334 | 5/48 | 48/48 | 0.104 | 1.000 |
| poshits | nested-youden | 0.5833 | 5/48 | 47/48 | 0.104 | 0.979 |
| poshits | nested-fpr10 | 0.5509 | 5/48 | 47/48 | 0.104 | 0.979 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.462 mean_pos=-0.1007 mean_neg=-0.0148 diff=-0.0859 pos>0=25/48 neg<=0=19/48 perm_p=0.6892 binom_p=0.4427 youden_t=0.3283 youden_sens=0.229 youden_spec=0.854 J=0.083
hits prompts_marked_above=5/12 instance=key-free-hits used_keys=False
hashpool auc=0.615 mean_pos=-0.0059 mean_neg=-0.0182 diff=0.0123 pos>0=20/48 neg<=0=38/48 perm_p=0.01299 binom_p=0.9033 youden_t=0.0000 youden_sens=0.417 youden_spec=0.792 J=0.208
hashpool prompts_marked_above=9/12 instance=key-free-hashpool used_keys=False
poshits auc=0.585 mean_pos=0.2613 mean_neg=-0.2857 diff=0.5471 pos>0=18/48 neg<=0=29/48 perm_p=0.001499 binom_p=0.9703 youden_t=-0.0012 youden_sens=1.000 youden_spec=0.250 J=0.250
poshits prompts_marked_above=9/12 instance=key-free-poshits used_keys=False
