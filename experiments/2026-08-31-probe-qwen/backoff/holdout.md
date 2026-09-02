indicate holdout mode=rotate n_prompts=12 n_files=24 marked_above_unmarked=5 prompts_marked_above=5 marked_lr_positive=5 unmarked_lr_nonpositive=8 margin=0 context_len=4 score_kind=backoff auc=0.542 perm_p=0.2789 used_keys=False hash_iv=False g_values=False instance=key-free-backoff
single-file auc=0.542 mean_pos=0.0035 mean_neg=-0.0216 diff=0.0251 pos>0=5/12 neg<=0=8/12 perm_p=0.2789 binom_p=0.8062 youden_t=-0.0117 youden_sens=0.583 youden_spec=0.667 J=0.250
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
01-harbour-marked.txt: lr=0.076165 instance=key-free-backoff
01-harbour-unmarked-gen.txt: lr=0.042656 instance=key-free-backoff
01-harbour#1: marked_higher
02-night-bus-marked.txt: lr=-0.042910 instance=key-free-backoff
02-night-bus-unmarked-gen.txt: lr=-0.015766 instance=key-free-backoff
02-night-bus#1: unmarked_higher
03-library-marked.txt: lr=0.305286 instance=key-free-backoff
03-library-unmarked-gen.txt: lr=-0.044018 instance=key-free-backoff
03-library#1: marked_higher
04-market-marked.txt: lr=0.012392 instance=key-free-backoff
04-market-unmarked-gen.txt: lr=0.015766 instance=key-free-backoff
04-market#1: unmarked_higher
05-kitchen-marked.txt: lr=0.009815 instance=key-free-backoff
05-kitchen-unmarked-gen.txt: lr=0.040638 instance=key-free-backoff
05-kitchen#1: unmarked_higher
06-station-marked.txt: lr=-0.060391 instance=key-free-backoff
06-station-unmarked-gen.txt: lr=0.016127 instance=key-free-backoff
06-station#1: unmarked_higher
07-rain-marked.txt: lr=-0.107776 instance=key-free-backoff
07-rain-unmarked-gen.txt: lr=-0.023350 instance=key-free-backoff
07-rain#1: unmarked_higher
08-letter-marked.txt: lr=-0.167627 instance=key-free-backoff
08-letter-unmarked-gen.txt: lr=-0.072770 instance=key-free-backoff
08-letter#1: unmarked_higher
09-workshop-marked.txt: lr=0.101575 instance=key-free-backoff
09-workshop-unmarked-gen.txt: lr=-0.100381 instance=key-free-backoff
09-workshop#1: marked_higher
10-office-marked.txt: lr=-0.071347 instance=key-free-backoff
10-office-unmarked-gen.txt: lr=-0.011675 instance=key-free-backoff
10-office#1: unmarked_higher
11-garden-marked.txt: lr=-0.004629 instance=key-free-backoff
11-garden-unmarked-gen.txt: lr=-0.071748 instance=key-free-backoff
11-garden#1: marked_higher
12-ferry-queue-marked.txt: lr=-0.008654 instance=key-free-backoff
12-ferry-queue-unmarked-gen.txt: lr=-0.034356 instance=key-free-backoff
12-ferry-queue#1: marked_higher
