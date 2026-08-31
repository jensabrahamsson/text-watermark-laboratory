# Key-free probe

probe n_methods=1 pair_dir=/workspace/experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=16 pos_bucket=2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 34/36 | 0.938 | 132/144 | 132/144 | 0.0004998 | 3.4784 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshits | 124/144 | 132/144 | 0.0162 | 0.861 | 0.917 |

poshits auc=0.938 mean_pos=2.9855 mean_neg=-0.4929 diff=3.4784 pos>0=132/144 neg<=0=132/144 perm_p=0.0004998 binom_p=5.103e-27 youden_t=0.0000 youden_sens=0.917 youden_spec=0.917 J=0.833
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
