# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.8708 |
| poshits | 12/12 | 0.861 | 39/48 | 40/48 | 0.0004998 | 1.5143 |
| hashpool | 11/12 | 0.733 | 30/48 | 36/48 | 0.0004998 | 0.0558 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
poshits auc=0.861 mean_pos=1.2773 mean_neg=-0.2370 diff=1.5143 pos>0=39/48 neg<=0=40/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.833 J=0.646
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
hashpool auc=0.733 mean_pos=0.0429 mean_neg=-0.0129 diff=0.0558 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0016 youden_sens=0.625 youden_spec=0.812 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
