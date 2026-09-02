# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-36x4 context_len=5 model=gpt2 max_draws=None prefix_lens=[] used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 35/36 | 0.912 | 130/144 | 87/144 | 0.0004998 | 2.3584 |
| hashpool | 34/36 | 0.891 | 125/144 | 100/144 | 0.0004998 | 0.1088 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 124/144 | 130/144 | 0.6185 | 0.861 | 0.903 |
| hashpool | 113/144 | 126/144 | 0.0171 | 0.785 | 0.875 |

hits auc=0.912 mean_pos=2.1824 mean_neg=-0.1759 diff=2.3584 pos>0=130/144 neg<=0=87/144 perm_p=0.0004998 binom_p=4.937e-25 youden_t=0.6205 youden_sens=0.861 youden_spec=0.910 J=0.771
hits prompts_marked_above=35/36 instance=key-free-hits used_keys=False
hashpool auc=0.891 mean_pos=0.1015 mean_neg=-0.0073 diff=0.1088 pos>0=125/144 neg<=0=100/144 perm_p=0.0004998 binom_p=1.277e-20 youden_t=0.0157 youden_sens=0.826 youden_spec=0.882 J=0.708
hashpool prompts_marked_above=34/36 instance=key-free-hashpool used_keys=False
