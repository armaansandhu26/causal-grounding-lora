# Implementation checklist (final)

This file mirrors **what exists in the repo** as of the final submission. It replaces the older week-by-week task list.

## Stage 1 — Head discovery and causal screen

- [x] LLaVA-1.5-7B (`llava-hf/llava-1.5-7b-hf`) with reproducible decode settings
- [x] COCO val imagery + object vocabulary for weak grounded vs hallucinated labels
- [x] Per-step attention tracing and per-head **visual vs text** mass features
- [x] Ranking + visualization; **causal** one-head-at-a-time validation on candidates
- [x] Export: `results/final_hallucination_heads.json` (32 heads)

**Notebook:** `stage1_hallucination_heads.ipynb`

## Stage 2 — Targeted LoRA

- [x] 4-bit load + LoRA on Q/K/V in layers covering the 32 heads
- [x] Contrastive / DPO-style caption-pair training
- [x] Adapter save path: `results/stage2_lora_adapter/`
- [x] Baseline vs adapter eval artifacts: `results/stage2_baseline_eval.json`, `results/stage2_lora_eval.json`, `results/stage2_training_log.json`

**Notebook:** `stage2_lora.ipynb`

## Stage 3 — Inference-time grounding controller

- [x] Grounding score from attention in the shortlist heads; threshold **θ** and penalty **α**
- [x] Penalize logits for selected content-word classes when grounding is weak

**Notebook:** `stage3_inference_grounding.ipynb`

## Stage 4 — System comparison and ablations

- [x] Four conditions: baseline / LoRA / controller / LoRA+controller
- [x] Consolidated metrics: `results/stage4_all_results.json` (40 images, CHAIR + POPE)
- [x] Larger CHAIR run + θ sweep + head-count slice: `results/stage4_400img_results.json`

**Notebooks:** `stage4_comparison.ipynb`, `stage4_final_1.ipynb`

## Optional / extra

- [x] `validation_Experiments.ipynb` — additional validation experiments (not required for the core pipeline order above)

## Guardrails (documentation)

- [x] Attention and weak labels are **approximate**; CHAIR is **noisy**; combined method is evaluated empirically in Stage 4 JSON + notebooks.
