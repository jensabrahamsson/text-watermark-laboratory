# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-limit n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.854 | 10/12 | 8/12 | 0.0009995 | 1.1114 |
| poshits | 12/12 | 0.854 | 10/12 | 9/12 | 0.0009995 | 0.8766 |
| hashpool | 10/12 | 0.833 | 6/12 | 10/12 | 0.0009995 | 1.2173 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.854 mean_pos=0.8759 mean_neg=-0.2355 diff=1.1114 pos>0=10/12 neg<=0=8/12 perm_p=0.0009995 binom_p=0.01929 youden_t=0.1075 youden_sens=0.833 youden_spec=0.833 J=0.667
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
poshits auc=0.854 mean_pos=0.8685 mean_neg=-0.0081 diff=0.8766 pos>0=10/12 neg<=0=9/12 perm_p=0.0009995 binom_p=0.01929 youden_t=0.1075 youden_sens=0.833 youden_spec=0.833 J=0.667
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
hashpool auc=0.833 mean_pos=0.4920 mean_neg=-0.7253 diff=1.2173 pos>0=6/12 neg<=0=10/12 perm_p=0.0009995 binom_p=0.6128 youden_t=-0.6662 youden_sens=1.000 youden_spec=0.667 J=0.667
hashpool prompts_marked_above=10/12 instance=key-free-hashpool used_keys=False
