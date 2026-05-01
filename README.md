# 682 Project: Hallucination Mitigation in LLaVA-1.5-7B

## TL;DR Status

- [x] **Stage 1 complete:** identified 32 hallucination-prone attention heads (from 1024 total).
- [x] **Stage 2 complete (first pass):** targeted LoRA training finished and adapter saved.
- [ ] **Stage 3 not done yet:** inference-time grounding controller still needs to be implemented/evaluated.
- [ ] **Combined claim not confirmed yet:** we do not yet have LoRA + inference-time results.

## What We Are Building

- Reduce object hallucinations in LLaVA-1.5-7B by combining:
- 1. **Targeted LoRA** on causally identified heads.
- 2. **Inference-time grounding control** that penalizes risky token generation when visual grounding is weak.
- Core hypothesis (proposal + dump): the combined method should outperform either method alone on hallucination metrics (especially CHAIR), while staying efficient.

## Where We Are Right Now

- **Stage 1 (`stage1_hallucination_heads.ipynb`)**
- [x] Screened 200 COCO val images.
- [x] Collected 4,263 content-word generation steps.
- [x] Ran causal validation on top-50 candidate heads.
- [x] Found 44/50 heads with negative causal delta.
- [x] Produced final shortlist: **32 heads**.
- [x] Saved artifact: `results/final_hallucination_heads.json`.

- **Stage 2 (`stage2_lora.ipynb`)**
- [x] Loaded LLaVA-1.5-7B in 4-bit (QLoRA setting).
- [x] Applied LoRA only to Q/K/V in target layers (17 layers containing the 32 heads).
- [x] Trained with DPO-style contrastive caption pairs (321 pairs used in run shown).
- [x] Saved adapter to `results/stage2_lora_adapter`.
- [x] Ran baseline and post-training eval on CHAIR (primary metric).

## Current Results (Important)

- **CHAIR improved a lot after Stage 2 LoRA**
- Baseline CHAIRs: `0.35` -> LoRA CHAIRs: `0.05`
- Baseline CHAIRi: `0.1097` -> LoRA CHAIRi: `0.0167`
- This supports your statement that CHAIR results are good.

## Next Steps (Priority Order)

- [ ] **Stage 3 implementation**
- Implement inference-time grounding score based on visual attention ratio in the 32 risky heads.
- Add threshold and penalty hyperparameters (`theta`, `alpha`) with easy tuning.

- [ ] **Run 3-way ablation**
- Evaluate:
- 1. Baseline (no LoRA, no grounding control)
- 2. LoRA-only
- 3. Grounding-only
- 4. LoRA + grounding (combined)
- Report CHAIR for all four settings.

- [ ] **Stability checks**
- Re-run evaluation with larger held-out split (beyond current 40-image eval subset).
- Run at least 2-3 seeds for variance estimates.
- Save all result JSONs in a consistent naming scheme.

- [ ] **Final deliverables**
- Prepare final comparison plots (CHAIR deltas only).
- Add qualitative examples: fixed hallucinations and remaining failures.
- Write final conclusion only after combined ablation confirms the hypothesis.

## Quick Run Order

- [ ] Run/update `stage1_hallucination_heads.ipynb` only if head shortlist changes.
- [ ] Run `stage2_lora.ipynb` to train/evaluate LoRA adapter.
- [ ] Implement and run Stage 3 controller notebook/script.
- [ ] Run unified ablation script/notebook for final table.

## Key Artifacts

- `stage1_hallucination_heads.ipynb`
- `stage2_lora.ipynb`
- `682_project_proposal.pdf`
- `682 project dump.pdf`
- `results/final_hallucination_heads.json`
- `results/stage2_baseline_eval.json`
- `results/stage2_lora_eval.json`
- `results/stage2_training_log.json`
