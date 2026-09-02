# Argmax snap scrub

scrub n_files=48 model=gpt2 snap_used_keys=False reference_instance=public-deepmind-30 hash_iv=False g_values=False
Argmax snap does not use watermark keys. Official scores are a reference check.

| file | flips | mean before | mean after |
|---|---|---|---|
| 01-harbour-marked-2.txt | 71/128 | 0.6288 | 0.5083 |
| 01-harbour-marked-3.txt | 86/128 | 0.6293 | 0.4930 |
| 01-harbour-marked-4.txt | 91/128 | 0.6272 | 0.5011 |
| 01-harbour-marked.txt | 72/126 | 0.6232 | 0.5028 |
| 02-night-bus-marked-2.txt | 80/128 | 0.6237 | 0.5124 |
| 02-night-bus-marked-3.txt | 79/128 | 0.6210 | 0.4844 |
| 02-night-bus-marked-4.txt | 91/128 | 0.6333 | 0.5056 |
| 02-night-bus-marked.txt | 76/128 | 0.6206 | 0.5041 |
| 03-library-marked-2.txt | 82/128 | 0.6339 | 0.4806 |
| 03-library-marked-3.txt | 77/128 | 0.6203 | 0.5011 |
| 03-library-marked-4.txt | 75/128 | 0.6231 | 0.5008 |
| 03-library-marked.txt | 73/128 | 0.6243 | 0.5134 |
| 04-market-marked-2.txt | 75/128 | 0.6130 | 0.4995 |
| 04-market-marked-3.txt | 63/128 | 0.5978 | 0.4997 |
| 04-market-marked-4.txt | 82/128 | 0.6276 | 0.5059 |
| 04-market-marked.txt | 68/128 | 0.6167 | 0.4880 |
| 05-kitchen-marked-2.txt | 75/128 | 0.6250 | 0.5203 |
| 05-kitchen-marked-3.txt | 81/128 | 0.6089 | 0.4968 |
| 05-kitchen-marked-4.txt | 64/128 | 0.5951 | 0.5072 |
| 05-kitchen-marked.txt | 65/128 | 0.6129 | 0.5156 |
| 06-station-marked-2.txt | 83/128 | 0.6196 | 0.4997 |
| 06-station-marked-3.txt | 83/126 | 0.6272 | 0.5072 |
| 06-station-marked-4.txt | 70/128 | 0.6107 | 0.4919 |
| 06-station-marked.txt | 75/128 | 0.6240 | 0.4935 |
| 07-rain-marked-2.txt | 76/128 | 0.6255 | 0.4892 |
| 07-rain-marked-3.txt | 71/128 | 0.6078 | 0.5054 |
| 07-rain-marked-4.txt | 84/128 | 0.6196 | 0.5083 |
| 07-rain-marked.txt | 79/128 | 0.6295 | 0.4734 |
| 08-letter-marked-2.txt | 65/128 | 0.5997 | 0.4981 |
| 08-letter-marked-3.txt | 75/128 | 0.6156 | 0.5065 |
| 08-letter-marked-4.txt | 76/128 | 0.6261 | 0.4970 |
| 08-letter-marked.txt | 91/128 | 0.6368 | 0.4987 |
| 09-workshop-marked-2.txt | 83/128 | 0.6201 | 0.5051 |
| 09-workshop-marked-3.txt | 78/128 | 0.6293 | 0.5140 |
| 09-workshop-marked-4.txt | 70/128 | 0.6172 | 0.4858 |
| 09-workshop-marked.txt | 75/128 | 0.6129 | 0.5040 |
| 10-office-marked-2.txt | 77/128 | 0.6202 | 0.4933 |
| 10-office-marked-3.txt | 66/128 | 0.6177 | 0.4828 |
| 10-office-marked-4.txt | 76/128 | 0.6263 | 0.5011 |
| 10-office-marked.txt | 67/128 | 0.6244 | 0.4831 |
| 11-garden-marked-2.txt | 76/128 | 0.6204 | 0.5156 |
| 11-garden-marked-3.txt | 86/128 | 0.6226 | 0.5005 |
| 11-garden-marked-4.txt | 91/128 | 0.6349 | 0.5032 |
| 11-garden-marked.txt | 82/128 | 0.6296 | 0.4956 |
| 12-ferry-queue-marked-2.txt | 77/128 | 0.6185 | 0.4875 |
| 12-ferry-queue-marked-3.txt | 80/128 | 0.6269 | 0.5027 |
| 12-ferry-queue-marked-4.txt | 84/126 | 0.6404 | 0.4934 |
| 12-ferry-queue-marked.txt | 84/128 | 0.6296 | 0.4944 |

mean official before=0.6216 after=0.4994
