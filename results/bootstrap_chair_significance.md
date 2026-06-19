# CHAIR Bootstrap and Paired Significance

Scorer: `spacy`
Bootstrap resamples: `5000`
Permutation resamples: `10000`

Negative paired deltas mean the method has lower hallucination than the reference.

## Stage 4 Main Comparison

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.3700 [0.3225, 0.4175] | 0.1558 [0.1327, 0.1800] | 61.1 |
| stage2 | 400 | 0.2650 [0.2225, 0.3075] | 0.1043 [0.0857, 0.1245] | 27.6 |
| stage3 | 400 | 0.3100 [0.2650, 0.3575] | 0.1407 [0.1174, 0.1654] | 62.1 |
| stage4 | 400 | 0.2300 [0.1900, 0.2700] | 0.0958 [0.0761, 0.1163] | 29.6 |

### Paired Deltas vs Baseline

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| stage2 | -0.1050 [-0.1575, -0.0550], p=0.0002 | -0.0515 [-0.0738, -0.0295], p=0.0001 |
| stage3 | -0.0600 [-0.1125, -0.0075], p=0.0287 | -0.0151 [-0.0386, +0.0082], p=0.2096 |
| stage4 | -0.1400 [-0.1900, -0.0900], p=0.0001 | -0.0601 [-0.0837, -0.0369], p=0.0001 |

## SPIN Budgets

### budget_64

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.2800 [0.2350, 0.3250] | 0.1066 [0.0872, 0.1274] | 49.5 |
| spin | 400 | 0.3025 [0.2575, 0.3475] | 0.1216 [0.1000, 0.1445] | 48.8 |

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| spin | +0.0225 [-0.0150, +0.0600], p=0.2996 | +0.0150 [-0.0011, +0.0326], p=0.0812 |

### budget_80

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.3650 [0.3175, 0.4125] | 0.1382 [0.1167, 0.1609] | 60.8 |
| spin | 400 | 0.3675 [0.3200, 0.4150] | 0.1419 [0.1194, 0.1657] | 58.4 |

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| spin | +0.0025 [-0.0400, +0.0450], p=1.0000 | +0.0037 [-0.0128, +0.0195], p=0.6737 |

### budget_128

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |
|---|---:|---:|---:|---:|
| baseline | 400 | 0.5125 [0.4625, 0.5600] | 0.1794 [0.1563, 0.2045] | 84.2 |
| spin | 400 | 0.4750 [0.4250, 0.5225] | 0.1786 [0.1551, 0.2033] | 78.2 |

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| spin | -0.0375 [-0.0875, +0.0125], p=0.1811 | -0.0008 [-0.0192, +0.0181], p=0.9380 |
