# Random-32 Head LoRA Control Bundle

Upload this `llava_hallucination_heads` folder to:

```text
/content/drive/MyDrive/llava_hallucination_heads
```

The notebook already uses:

```python
WORK_DIR = '/content/drive/MyDrive/llava_hallucination_heads'
```

If you are using the shared Drive shortcut from the screenshot, your working folder is probably:

```python
WORK_DIR = '/content/drive/MyDrive/reducing_hallucinations'
```

The larger eval-only notebook below already defaults to this `reducing_hallucinations` path.

Run:

```text
stage2_random_heads_lora_control.ipynb
```

This notebook tests the reviewer-requested control:

```text
causal hallucination heads -> layer-matched random 32 heads
```

It keeps the Stage 2 training data, DPO objective, LoRA config, and evaluation split fixed.

For the larger reviewer-facing evaluation after the random adapter is trained, run:

```text
stage2_large_random_head_eval.ipynb
```

This notebook does not retrain. It loads the baseline model, targeted-head adapter, and random-head adapter, then evaluates all three on the same larger split with CHAIR and average caption length.

## Already Included

```text
stage2_random_heads_lora_control.ipynb
stage2_large_random_head_eval.ipynb
results/final_hallucination_heads.json
cache/selected_imgs.json
```

## Still Needed

Add these from your original Drive/Colab project before running:

```text
cache/screening_state.pkl
coco/annotations/instances_val2014.json
coco/annotations/captions_val2014.json
coco/val2014_subset/*.jpg
```

If those files already exist in your Drive under `llava_hallucination_heads`, you can upload this bundle over the existing folder and skip re-uploading COCO.

## Outputs

The notebook writes separate random-head outputs and should not overwrite the targeted Stage 2 adapter:

```text
results/stage2_random_heads32_selection.json
results/stage2_random_heads32_baseline_eval.json
results/stage2_random_heads32_lora_eval.json
results/stage2_random_heads32_lora_adapter/
results/stage2_random_heads32_training_log.json
results/stage2_random_heads32_large_eval_n200.json
```
