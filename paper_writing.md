# Paper Writing Plan: Actionable Interpretability Workshop

Workshop: Actionable Interpretability @ COLM 2026  
Submission deadline: June 24, 2026 AOE  
Target type: short paper, up to 5 pages excluding references and appendix

Workshop page:

- https://actionable-interpretability.github.io/
- https://actionable-interpretability.github.io/cfp/

## Core Alignment

This project fits the workshop best as an actionable interpretability paper, not just a hallucination mitigation paper.

The central framing should be:

> We use an interpretable object-level failure signal to identify and reduce hallucination in LLaVA captions, and show that combining targeted LoRA adaptation with inference-time grounding produces measurable reductions in CHAIR hallucination on held-out images.

The workshop call explicitly asks for:

- Practical applications of interpretability insights to hallucinations and model reliability.
- Comparative analyses of interpretability-based approaches versus alternatives such as fine-tuning and prompting.
- Realistic benchmarking methods for measuring real-world impact.
- Critical discussion of limitations and whether interpretability insights translate into action.

Our paper should therefore emphasize:

- The intervention is motivated by understanding object hallucination behavior.
- The intervention is actionable because it changes model behavior, not just explains it.
- The evaluation is controlled: same 400 held-out images, paired tests, fixed-budget decoding comparisons.
- We include negative or mixed results for SPIN, and soon VCD, as honest external baselines.

## Proposed Title Options

1. Grounded Adaptation for Reducing Object Hallucination in Vision-Language Captioning
2. From Object-Level Diagnosis to Intervention: Reducing Hallucination in LLaVA Captions
3. Actionable Grounding for Vision-Language Hallucination Mitigation
4. Combining Lightweight Adaptation and Inference Grounding to Reduce Object Hallucination

Best current title:

> From Object-Level Diagnosis to Intervention: Reducing Hallucination in LLaVA Captions

This title sounds aligned with actionable interpretability because it makes the diagnosis-to-intervention arc explicit.

## Main Claim

Use this as the main result sentence:

> On a 400-image held-out COCO val2014 split, our combined LoRA + inference-grounding method reduces CHAIRs by 37.8% and CHAIRi by 38.5% relative to the greedy LLaVA baseline, with significant paired reductions for both CHAIRs and CHAIRi.

Be careful not to overclaim:

- Do not say the method universally improves captioning.
- Do not say SPIN fails generally.
- Do not say hallucination is solved.
- Say we reduce object hallucination under our controlled captioning protocol.

## Paper Story

The paper should tell this story:

1. Vision-language models hallucinate objects in image captions.
2. CHAIR gives an object-level way to diagnose these hallucinations.
3. We turn that diagnosis into two interventions:
   - Stage 2: LoRA adaptation on a small hallucination-focused training set.
   - Stage 3: inference-time grounding.
4. Each intervention helps, but the combined method helps most.
5. Compared against training-free decoding baselines such as SPIN and VCD, our method gives stronger and statistically supported reductions.
6. The main tradeoff is fluency and caption length, so we report average length and should add object recall/coverage if time allows.

## Experiment Table Plan

### Table 1: Main Results

Use the 400-image held-out split.

Rows:

- Baseline
- Stage 2: LoRA
- Stage 3: Grounding
- Stage 4: LoRA + Grounding

Columns:

- CHAIRs with 95% CI
- CHAIRi with 95% CI
- relative reduction vs baseline
- average caption length

Required note:

> Lower CHAIRs and CHAIRi are better. Confidence intervals are bootstrap 95% CIs over images.

### Table 2: Paired Significance

Rows:

- Stage 2 vs baseline
- Stage 3 vs baseline
- Stage 4 vs baseline

Columns:

- delta CHAIRs, 95% CI, p-value
- delta CHAIRi, 95% CI, p-value

Required note:

> Negative deltas indicate lower hallucination than the baseline. P-values are from paired sign-flip permutation tests over the same 400 images.

### Table 3: Decoding Baselines

Rows grouped by budget:

- Baseline 64
- SPIN 64
- VCD 64
- Baseline 80
- SPIN 80
- VCD 80
- Baseline 128
- SPIN 128
- VCD 128

If we run Stage 4 fixed-budget, add:

- Stage 4 64
- Stage 4 80
- Stage 4 128

Columns:

- CHAIRs with 95% CI
- CHAIRi with 95% CI
- average length
- paired delta vs matched baseline

This table is important because the workshop likes comparative analysis against alternative interventions.

## Experiments Still Worth Running

Highest priority:

1. VCD on the same 400 images at budgets 64, 80, and 128.
2. Stage 4 on the same 400 images at budgets 64, 80, and 128.
3. Object recall / coverage on all reported methods.

Useful if time remains:

4. Random-160 LoRA control using `stage2_random_lora_control.ipynb`.
5. Stage 2 fixed-budget runs at 64, 80, and 128.
6. Two more qualitative examples:
   - one clean Stage 4 win,
   - one Stage 4 failure case,
   - one case where SPIN or VCD helps but Stage 4 does not.

Do not expand to 500 images unless the existing 400-image protocol becomes a review concern. The current 400-image setup is already stronger than the earlier 40-image eval and supports paired significance.

## VCD Requirements For Co-Author

Ask the co-author to use exactly:

- Same 400 image IDs as `results/stage4_400img_results.json`.
- Same order if possible.
- Same prompt template as SPIN/baseline.
- Same budgets: 64, 80, 128.
- Save one JSON per budget.

Recommended filenames:

```text
cache/vcd_captions_budget64.json
cache/vcd_captions_budget80.json
cache/vcd_captions_budget128.json
```

Each row should include at least:

```text
image_id
caption
```

If possible, also include:

```text
file_name
max_new_tokens
method
```

Once these arrive, extend `scripts/bootstrap_chair_significance.py` to report VCD exactly like SPIN.

## Object Recall / Coverage

This is the best extra metric to address the concern that Stage 4 may reduce hallucination simply by becoming shorter.

Report:

- average number of ground-truth objects mentioned per caption,
- fraction of ground-truth objects mentioned,
- maybe precision/recall over object mentions if easy.

Interpretation:

- CHAIRs/CHAIRi measure hallucination.
- Object recall measures whether the model still mentions relevant image objects.
- Average length contextualizes the fluency/verbosity tradeoff.

Suggested text:

> Because shorter captions can mechanically reduce hallucination opportunities, we also report object coverage against COCO annotations. This distinguishes hallucination reduction from simply avoiding object mentions.

## Random-160 LoRA Control

Notebook:

```text
stage2_random_lora_control.ipynb
```

Purpose:

> Test whether using the hallucination diagnostic signal to choose intervention data is better than training the same LoRA intervention on a random 160-image control split.

Keep fixed:

- same base model,
- same LoRA target modules,
- same hallucination-head gradient mask,
- same DPO loss,
- same original Stage 2 held-out eval images.

Change only:

- training image selection: targeted 160 images vs random 160 eligible non-targeted images.

Expected outputs:

```text
cache/random160_train_imgs.json
results/stage2_random160_lora_adapter/
results/stage2_random160_baseline_eval.json
results/stage2_random160_lora_eval.json
results/stage2_random160_training_log.json
```

Paper comparison:

- Baseline
- Random-160 LoRA
- Hallucination-focused-160 LoRA
- Stage 4: hallucination-focused LoRA + grounding

If hallucination-focused LoRA outperforms random-160 LoRA, it directly supports the actionable-interpretability claim that the diagnostic signal helps select useful intervention data.

## Qualitative Figure

Use image `452793`.

Why it works:

- Ground-truth objects: refrigerator, sink.
- Baseline hallucinated oven.
- Stage 3 also hallucinated oven.
- SPIN hallucinated microwave and, at longer budget, furniture.
- Stage 4 keeps the core annotated objects, though with reduced fluency.

Figure asset:

```text
poster_figures/diagram4_qualitative_452793.png
```

Suggested caption:

> Qualitative example on a held-out COCO val2014 kitchen image. The baseline and grounding-only captions hallucinate an oven, while SPIN introduces a microwave and, at longer decoding budgets, additional furniture. The combined LoRA + grounding method retains the annotated refrigerator and sink while suppressing the main object hallucinations, though with reduced fluency.

## Suggested Paper Outline

### Abstract

Structure:

1. VLMs hallucinate objects in captioning.
2. We study whether object-level hallucination diagnosis can be turned into an actionable intervention.
3. We combine lightweight LoRA adaptation with inference-time grounding.
4. On 400 held-out COCO images, Stage 4 reduces CHAIRs/CHAIRi substantially and significantly.
5. We compare against SPIN and VCD under fixed decoding budgets and discuss the length/fluency tradeoff.

### Introduction

Main points:

- Interpretability should help change model behavior, not only explain failures.
- Object hallucination in VLM captions is a concrete reliability failure.
- CHAIR gives a measurable object-level failure signal.
- We ask whether this signal can guide practical mitigation.

End introduction with contributions:

- A small-scale but controlled intervention pipeline for reducing object hallucination in LLaVA captions.
- A comparison of LoRA-only, grounding-only, and combined interventions.
- A matched 400-image evaluation with bootstrap CIs and paired significance.
- A comparison against training-free decoding baselines, including SPIN and VCD.

### Method

Subsections:

- Task and model
- CHAIR object-level hallucination signal
- Stage 2: LoRA adaptation
- Stage 3: inference grounding
- Stage 4: combined intervention
- Baselines: greedy LLaVA, SPIN, VCD

Keep method concise. This is a short workshop paper.

### Experiments

Include:

- Dataset split:
  - 160 images for LoRA training.
  - 400 held-out images for final evaluation.
- Metrics:
  - CHAIRs
  - CHAIRi
  - average length
  - object recall/coverage if available
- Statistical reporting:
  - bootstrap 95% CIs,
  - paired sign-flip permutation tests.

### Results

Lead with Stage 4:

- Stage 2 helps.
- Stage 3 helps less strongly.
- Stage 4 helps most.
- Stage 4 paired deltas are significant.

Then decoding baselines:

- SPIN does not consistently improve under our fixed-budget protocol.
- VCD results pending.
- If Stage 4 fixed-budget is run, compare it directly.

### Discussion

Be honest:

- Stage 4 reduces hallucination but captions are shorter and sometimes less fluent.
- CHAIR focuses on object hallucination, not all forms of factuality.
- COCO object annotations are incomplete, so CHAIR can over-penalize some valid mentions.
- The experiment is small enough for a workshop paper but not a definitive benchmark.

Make the actionable interpretability point:

> The result illustrates both the promise and the difficulty of actionable interpretability: an object-level diagnostic signal can guide useful intervention, but gains come with tradeoffs that require broader evaluation beyond a single hallucination metric.

## Claims To Avoid

Avoid:

- "Our method solves hallucination."
- "SPIN does not work."
- "VCD is worse" unless the results support it.
- "Interpretability guarantees reliability."
- "Stage 4 improves caption quality overall" unless object recall / human eval supports it.

Prefer:

- "reduces object hallucination under CHAIR"
- "under our fixed-budget protocol"
- "on the same 400 held-out images"
- "with a fluency/length tradeoff"
- "suggests a practical route from diagnosis to intervention"

## Current Status

Done:

- Stage 2, Stage 3, Stage 4 comparison on 400 held-out images.
- SPIN at budgets 64, 80, 128 on the same 400 images.
- Bootstrap 95% CIs.
- Paired significance tests.
- Paper-ready Markdown and LaTeX result tables.
- Qualitative example image `452793`.

In progress / next:

- VCD at budgets 64, 80, 128.
- Stage 4 fixed-budget eval if time allows.
- Object recall / coverage metric.
- Two additional qualitative examples.

## One-Paragraph Positioning

This work studies whether object-level hallucination diagnostics can be converted into actionable interventions for vision-language models. Using LLaVA captioning as a testbed, we compare a greedy baseline, lightweight LoRA adaptation, inference-time grounding, and their combination on a 400-image held-out COCO split. The combined method substantially reduces CHAIR object hallucination relative to baseline, with bootstrap confidence intervals and paired significance tests. We further compare against training-free decoding interventions such as SPIN and VCD under matched token budgets, highlighting both the promise of targeted intervention and the practical tradeoffs between hallucination reduction, caption length, and fluency.
