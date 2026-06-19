# CHAIR Bootstrap and Paired Significance

Scorer: `regex`
Bootstrap resamples: `500`
Permutation resamples: `1000`

Negative paired deltas mean the method has lower hallucination than the reference.

**Warning:** this was run with the dependency-free regex scorer. Use `--scorer spacy` for paper numbers that match the project notebooks.

## Stage 4 Main Comparison

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.4000 [0.3550, 0.4463] | 0.1629 [0.1407, 0.1857] | 61.1 |
| stage2 | 400 | 0.2850 [0.2375, 0.3275] | 0.1104 [0.0928, 0.1295] | 27.6 |
| stage3 | 400 | 0.3525 [0.3087, 0.4013] | 0.1514 [0.1269, 0.1747] | 62.1 |
| stage4 | 400 | 0.2550 [0.2175, 0.2963] | 0.1054 [0.0848, 0.1247] | 29.6 |

### Paired Deltas vs Baseline

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| stage2 | -0.1150 [-0.1613, -0.0675], p=0.0010 | -0.0525 [-0.0746, -0.0322], p=0.0010 |
| stage3 | -0.0475 [-0.0975, +0.0000], p=0.0999 | -0.0114 [-0.0338, +0.0117], p=0.3377 |
| stage4 | -0.1450 [-0.1900, -0.0987], p=0.0010 | -0.0575 [-0.0808, -0.0352], p=0.0010 |

## SPIN Budgets

### budget_64

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.2850 [0.2425, 0.3275] | 0.1049 [0.0853, 0.1244] | 49.5 |
| spin | 400 | 0.3125 [0.2662, 0.3575] | 0.1227 [0.1007, 0.1445] | 48.8 |

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| spin | +0.0275 [-0.0113, +0.0600], p=0.1798 | +0.0178 [+0.0018, +0.0355], p=0.0330 |

### budget_128

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.5150 [0.4650, 0.5676] | 0.1797 [0.1576, 0.2076] | 84.2 |
| spin | 400 | 0.4800 [0.4250, 0.5225] | 0.1791 [0.1551, 0.2029] | 78.2 |

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| spin | -0.0350 [-0.0850, +0.0150], p=0.2408 | -0.0005 [-0.0207, +0.0184], p=0.9461 |
