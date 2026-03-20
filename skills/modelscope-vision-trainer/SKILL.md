---
name: modelscope-vision-trainer
description: Train and fine-tune vision models with reproducible data pipelines and publish checkpoints to ModelScope Hub.
---

# ModelScope Vision Trainer

Use this skill for image classification, object detection, and segmentation fine-tuning workflows.

## Operating Mode

- Local machine is the control plane only for inspection, packaging, config generation, and submission.
- Heavy training should run remotely on PAI DLC.
- The included scripts cover dataset inspection, cost estimation, and command generation.
- If the actual training entrypoint is not already present in the workspace, the agent must scaffold it explicitly or stop at a remote-ready package instead of pretending training can run.

## Credential Gate

Before any real PAI DLC submission, generate `configs/pai.required.env` if the required PAI fields are missing or not yet confirmed. The file must contain:

```bash
ALIBABA_CLOUD_ACCESS_KEY_ID=
ALIBABA_CLOUD_ACCESS_KEY_SECRET=
PAI_REGION=
PAI_WORKSPACE_ID=
```

After generating that file:

1. Tell the user to fill the four fields.
2. Tell the user to reply with exactly `continue`.
3. Do not proceed to real remote submission until the user continues.

`MODELSCOPE_API_TOKEN` can still be requested later when remote asset upload or automatic publication is needed.

## Scope

- Dataset sanity checks such as label schema, class balance, and basic file integrity.
- Training command generation for classification, detection, and segmentation.
- Runtime sizing and cost estimation.
- Remote submission to PAI DLC when a real training entrypoint is available.
- Uploading checkpoints and reports to ModelScope repos.

## Included Scripts

- `scripts/dataset_inspector.py`
- `scripts/estimate_cost.py`
- `scripts/image_classification_training.py`
- `scripts/object_detection_training.py`
- `scripts/sam_segmentation_training.py`
- `scripts/submit_pai_dlc.py`

## Recommended Flow

1. Inspect the dataset first.
2. Infer the vision task from file layout and annotations.
3. Generate `configs/pai.required.env` and wait for `continue` if the four required PAI fields are not ready.
4. Confirm that a runnable training entrypoint exists or scaffold one explicitly.
5. Start with a pilot run before full training.
6. Save best checkpoints and evaluation metrics.
7. Publish artifacts to ModelScope model repo.

## Remote Submission Rule

When local scripts or configs are required inside PAI DLC, upload them first via:

- `REMOTE_ASSET_PATHS`
- `REMOTE_ASSET_REPO` or `MS_REPO_OWNER` + `MS_REPO_BASE`
- `MODELSCOPE_API_TOKEN`

Then submit with `scripts/submit_pai_dlc.py`.

## Publish Pattern

```bash
modelscope create your-name/vision-model --repo_type model --visibility public
modelscope upload your-name/vision-model ./outputs checkpoints --repo-type model
```

## Guardrails

- Do not skip label integrity checks.
- Keep train/val/test splits disjoint.
- Track both aggregate metrics and per-class metrics.
- Do not claim built-in training support for a task unless an actual runnable entrypoint exists.
