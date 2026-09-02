indicate holdout mode=transfer n_prompts=12 n_files=96 marked_above_unmarked=28 prompts_marked_above=9 prompts_marked_ge=9 prompt_ties=0 prompt_losses=3 ranking_without_isolated_tp=0/9 ranking_losses_with_isolated_tp=2 marked_lr_positive=24 unmarked_lr_nonpositive=31 margin=0 context_len=4 score_kind=interpolate@w4-16 auc=0.592 perm_p=0.07446 (file-level, descriptive) prompt_sign_p=0.1269 used_keys=False hash_iv=False g_values=False instance=key-free-interpolate
single-file auc=0.592 mean_pos=0.1329 mean_neg=-0.0874 diff=0.2202 pos>0=24/48 neg<=0=31/48 perm_p=0.07446 (file-level, descriptive) binom_p=0.5573 (file-level, descriptive) youden_t=-0.5915 youden_sens=0.938 youden_spec=0.292 J=0.229
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
01-harbour-marked.txt: lr=0.174863 instance=key-free-interpolate
01-harbour-unmarked-gen.txt: lr=-0.978773 instance=key-free-interpolate
01-harbour#1: marked_higher
01-harbour-marked-2.txt: lr=0.106743 instance=key-free-interpolate
01-harbour-unmarked-gen-2.txt: lr=-0.538194 instance=key-free-interpolate
01-harbour#2: marked_higher
01-harbour-marked-3.txt: lr=0.376402 instance=key-free-interpolate
01-harbour-unmarked-gen-3.txt: lr=1.000678 instance=key-free-interpolate
01-harbour#3: unmarked_higher
01-harbour-marked-4.txt: lr=-0.304203 instance=key-free-interpolate
01-harbour-unmarked-gen-4.txt: lr=-1.829792 instance=key-free-interpolate
01-harbour#4: marked_higher
02-night-bus-marked.txt: lr=-0.549265 instance=key-free-interpolate
02-night-bus-unmarked-gen.txt: lr=-0.384886 instance=key-free-interpolate
02-night-bus#1: unmarked_higher
02-night-bus-marked-2.txt: lr=-0.376948 instance=key-free-interpolate
02-night-bus-unmarked-gen-2.txt: lr=-0.805647 instance=key-free-interpolate
02-night-bus#2: marked_higher
02-night-bus-marked-3.txt: lr=0.114239 instance=key-free-interpolate
02-night-bus-unmarked-gen-3.txt: lr=-0.655136 instance=key-free-interpolate
02-night-bus#3: marked_higher
02-night-bus-marked-4.txt: lr=-0.543897 instance=key-free-interpolate
02-night-bus-unmarked-gen-4.txt: lr=0.432614 instance=key-free-interpolate
02-night-bus#4: unmarked_higher
03-library-marked.txt: lr=0.262422 instance=key-free-interpolate
03-library-unmarked-gen.txt: lr=0.556697 instance=key-free-interpolate
03-library#1: unmarked_higher
03-library-marked-2.txt: lr=0.567404 instance=key-free-interpolate
03-library-unmarked-gen-2.txt: lr=0.306696 instance=key-free-interpolate
03-library#2: marked_higher
03-library-marked-3.txt: lr=-0.173811 instance=key-free-interpolate
03-library-unmarked-gen-3.txt: lr=1.240153 instance=key-free-interpolate
03-library#3: unmarked_higher
03-library-marked-4.txt: lr=-0.824334 instance=key-free-interpolate
03-library-unmarked-gen-4.txt: lr=-0.060910 instance=key-free-interpolate
03-library#4: unmarked_higher
04-market-marked.txt: lr=0.331396 instance=key-free-interpolate
04-market-unmarked-gen.txt: lr=-0.196738 instance=key-free-interpolate
04-market#1: marked_higher
04-market-marked-2.txt: lr=-0.044822 instance=key-free-interpolate
04-market-unmarked-gen-2.txt: lr=-0.734507 instance=key-free-interpolate
04-market#2: marked_higher
04-market-marked-3.txt: lr=0.569185 instance=key-free-interpolate
04-market-unmarked-gen-3.txt: lr=-0.025908 instance=key-free-interpolate
04-market#3: marked_higher
04-market-marked-4.txt: lr=0.569185 instance=key-free-interpolate
04-market-unmarked-gen-4.txt: lr=0.839597 instance=key-free-interpolate
04-market#4: unmarked_higher
05-kitchen-marked.txt: lr=2.115914 instance=key-free-interpolate
05-kitchen-unmarked-gen.txt: lr=1.774541 instance=key-free-interpolate
05-kitchen#1: marked_higher
05-kitchen-marked-2.txt: lr=-0.185933 instance=key-free-interpolate
05-kitchen-unmarked-gen-2.txt: lr=1.320414 instance=key-free-interpolate
05-kitchen#2: unmarked_higher
05-kitchen-marked-3.txt: lr=0.800055 instance=key-free-interpolate
05-kitchen-unmarked-gen-3.txt: lr=-1.182291 instance=key-free-interpolate
05-kitchen#3: marked_higher
05-kitchen-marked-4.txt: lr=0.421941 instance=key-free-interpolate
05-kitchen-unmarked-gen-4.txt: lr=-0.891995 instance=key-free-interpolate
05-kitchen#4: marked_higher
06-station-marked.txt: lr=-0.310379 instance=key-free-interpolate
06-station-unmarked-gen.txt: lr=0.194252 instance=key-free-interpolate
06-station#1: unmarked_higher
06-station-marked-2.txt: lr=0.474531 instance=key-free-interpolate
06-station-unmarked-gen-2.txt: lr=-0.905340 instance=key-free-interpolate
06-station#2: marked_higher
06-station-marked-3.txt: lr=-0.310379 instance=key-free-interpolate
06-station-unmarked-gen-3.txt: lr=-0.633774 instance=key-free-interpolate
06-station#3: marked_higher
06-station-marked-4.txt: lr=0.033427 instance=key-free-interpolate
06-station-unmarked-gen-4.txt: lr=-0.667857 instance=key-free-interpolate
06-station#4: marked_higher
07-rain-marked.txt: lr=0.297385 instance=key-free-interpolate
07-rain-unmarked-gen.txt: lr=-0.319242 instance=key-free-interpolate
07-rain#1: marked_higher
07-rain-marked-2.txt: lr=-0.622054 instance=key-free-interpolate
07-rain-unmarked-gen-2.txt: lr=0.300831 instance=key-free-interpolate
07-rain#2: unmarked_higher
07-rain-marked-3.txt: lr=-0.137999 instance=key-free-interpolate
07-rain-unmarked-gen-3.txt: lr=-0.021924 instance=key-free-interpolate
07-rain#3: unmarked_higher
07-rain-marked-4.txt: lr=0.211689 instance=key-free-interpolate
07-rain-unmarked-gen-4.txt: lr=-0.529057 instance=key-free-interpolate
07-rain#4: marked_higher
08-letter-marked.txt: lr=-0.287566 instance=key-free-interpolate
08-letter-unmarked-gen.txt: lr=-0.315053 instance=key-free-interpolate
08-letter#1: marked_higher
08-letter-marked-2.txt: lr=-0.381382 instance=key-free-interpolate
08-letter-unmarked-gen-2.txt: lr=-0.155051 instance=key-free-interpolate
08-letter#2: unmarked_higher
08-letter-marked-3.txt: lr=0.422000 instance=key-free-interpolate
08-letter-unmarked-gen-3.txt: lr=-0.150997 instance=key-free-interpolate
08-letter#3: marked_higher
08-letter-marked-4.txt: lr=-0.058701 instance=key-free-interpolate
08-letter-unmarked-gen-4.txt: lr=-0.359975 instance=key-free-interpolate
08-letter#4: marked_higher
09-workshop-marked.txt: lr=0.642573 instance=key-free-interpolate
09-workshop-unmarked-gen.txt: lr=-0.232579 instance=key-free-interpolate
09-workshop#1: marked_higher
09-workshop-marked-2.txt: lr=0.793469 instance=key-free-interpolate
09-workshop-unmarked-gen-2.txt: lr=-0.793992 instance=key-free-interpolate
09-workshop#2: marked_higher
09-workshop-marked-3.txt: lr=0.309412 instance=key-free-interpolate
09-workshop-unmarked-gen-3.txt: lr=-0.071254 instance=key-free-interpolate
09-workshop#3: marked_higher
09-workshop-marked-4.txt: lr=3.783994 instance=key-free-interpolate
09-workshop-unmarked-gen-4.txt: lr=0.122047 instance=key-free-interpolate
09-workshop#4: marked_higher
10-office-marked.txt: lr=-0.511058 instance=key-free-interpolate
10-office-unmarked-gen.txt: lr=0.331279 instance=key-free-interpolate
10-office#1: unmarked_higher
10-office-marked-2.txt: lr=0.027972 instance=key-free-interpolate
10-office-unmarked-gen-2.txt: lr=-0.604680 instance=key-free-interpolate
10-office#2: marked_higher
10-office-marked-3.txt: lr=-0.179360 instance=key-free-interpolate
10-office-unmarked-gen-3.txt: lr=-0.099827 instance=key-free-interpolate
10-office#3: unmarked_higher
10-office-marked-4.txt: lr=-0.305067 instance=key-free-interpolate
10-office-unmarked-gen-4.txt: lr=-0.006357 instance=key-free-interpolate
10-office#4: unmarked_higher
11-garden-marked.txt: lr=-0.416177 instance=key-free-interpolate
11-garden-unmarked-gen.txt: lr=0.776727 instance=key-free-interpolate
11-garden#1: unmarked_higher
11-garden-marked-2.txt: lr=-0.002364 instance=key-free-interpolate
11-garden-unmarked-gen-2.txt: lr=-0.670027 instance=key-free-interpolate
11-garden#2: marked_higher
11-garden-marked-3.txt: lr=0.085853 instance=key-free-interpolate
11-garden-unmarked-gen-3.txt: lr=0.677738 instance=key-free-interpolate
11-garden#3: unmarked_higher
11-garden-marked-4.txt: lr=1.316235 instance=key-free-interpolate
11-garden-unmarked-gen-4.txt: lr=-0.198595 instance=key-free-interpolate
11-garden#4: marked_higher
12-ferry-queue-marked.txt: lr=-0.189287 instance=key-free-interpolate
12-ferry-queue-unmarked-gen.txt: lr=1.357679 instance=key-free-interpolate
12-ferry-queue#1: unmarked_higher
12-ferry-queue-marked-2.txt: lr=-0.845365 instance=key-free-interpolate
12-ferry-queue-unmarked-gen-2.txt: lr=0.140299 instance=key-free-interpolate
12-ferry-queue#2: unmarked_higher
12-ferry-queue-marked-3.txt: lr=-0.572577 instance=key-free-interpolate
12-ferry-queue-unmarked-gen-3.txt: lr=-0.591491 instance=key-free-interpolate
12-ferry-queue#3: marked_higher
12-ferry-queue-marked-4.txt: lr=-0.298356 instance=key-free-interpolate
12-ferry-queue-unmarked-gen-4.txt: lr=0.046672 instance=key-free-interpolate
12-ferry-queue#4: unmarked_higher
