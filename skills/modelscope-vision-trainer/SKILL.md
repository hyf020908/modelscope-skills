---
name: modelscope-vision-trainer
description: Train and fine-tune vision models with reproducible data pipelines and publish checkpoints to ModelScope Hub.
---

# ModelScope Vision Trainer

Use this skill for object detection, image classification, and segmentation fine-tuning workflows.

## Scope

- Dataset sanity checks (label schema, class balance, file integrity).
- Training command generation for classification/detection/segmentation.
- Runtime sizing and cost estimation.
- Uploading checkpoints and reports to ModelScope repos.

## Included Scripts

- `scripts/dataset_inspector.py`
- `scripts/estimate_cost.py`
- `scripts/image_classification_training.py`
- `scripts/object_detection_training.py`
- `scripts/sam_segmentation_training.py`

## Recommended Flow

1. Run `dataset_inspector.py` before training.
2. Start with a small pilot subset.
3. Scale epochs, augmentations, and batch size after validation.
4. Save best checkpoints and evaluation metrics.
5. Publish artifacts to ModelScope model repo.

## Publish Pattern

```bash
modelscope create your-name/vision-model --repo_type model --visibility public
modelscope upload your-name/vision-model ./outputs checkpoints --repo-type model
```

## Guardrails

- Do not skip label integrity checks.
- Keep train/val/test splits disjoint.
- Track both aggregate metrics and per-class metrics.
