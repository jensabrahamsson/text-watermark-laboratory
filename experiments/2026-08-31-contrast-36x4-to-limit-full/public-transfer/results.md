# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-limit n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.965 | 12/12 | 8/12 | 0.0004998 | 0.4872 |
| poshits | 11/12 | 0.806 | 10/12 | 9/12 | 0.04548 | 0.6963 |
| hashpool | 12/12 | 0.944 | 10/12 | 12/12 | 0.0004998 | 0.0335 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.965 mean_pos=0.4608 mean_neg=-0.0265 diff=0.4872 pos>0=12/12 neg<=0=8/12 perm_p=0.0004998 binom_p=0.0002441 youden_t=0.1735 youden_sens=0.833 youden_spec=1.000 J=0.833
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
poshits auc=0.806 mean_pos=0.7125 mean_neg=0.0162 diff=0.6963 pos>0=10/12 neg<=0=9/12 perm_p=0.04548 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=0.750 J=0.583
poshits prompts_marked_above=11/12 instance=key-free-poshits used_keys=False
hashpool auc=0.944 mean_pos=0.0191 mean_neg=-0.0143 diff=0.0335 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=1.000 J=0.833
hashpool prompts_marked_above=12/12 instance=key-free-hashpool used_keys=False
