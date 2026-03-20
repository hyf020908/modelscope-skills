---
name: modelscope-jobs
description: Execute reproducible ML workflows and publish outputs to ModelScope repositories using UV scripts and token-authenticated uploads.
---

# ModelScope Jobs

Use this skill for reproducible script-based ML workflows whose outputs should be persisted on ModelScope Hub.

## Operating Mode

- Local machine is the control plane for packaging, validation, and submission.
- Lightweight checks can run locally.
- Heavy inference, data generation, or reporting pipelines should be submitted to PAI DLC when the workload is non-trivial.
- Outputs should be written to stable local paths and then published to ModelScope repos.

## Credential Gate

Before any real PAI DLC submission, generate `configs/pai.required.env` if the required PAI fields are missing or not yet confirmed. That file must contain exactly these editable placeholders:

```bash
ALIBABA_CLOUD_ACCESS_KEY_ID=
ALIBABA_CLOUD_ACCESS_KEY_SECRET=
PAI_REGION=
PAI_WORKSPACE_ID=
```

After generating the file:

1. Ask the user to fill those four fields.
2. Tell the user to reply with exactly `continue`.
3. Do not attempt the real remote submission until the user continues.

`MODELSCOPE_API_TOKEN` remains optional at this pause point, but it is required later when local assets must be uploaded to ModelScope or outputs must be published automatically.

## Scope

- Batch data generation and transformation.
- Large-scale inference scripts.
- Dataset statistics and reporting pipelines.
- Publishing produced artifacts to model or dataset repositories.

## Included Scripts

- `scripts/generate-responses.py`
- `scripts/cot-self-instruct.py`
- `scripts/finepdfs-stats.py`
- `scripts/submit_pai_dlc.py`

The included data-generation scripts can run directly with `uv run`. The submitter is the remote execution bridge for PAI DLC.

## Local Runtime Patterns

```bash
uv run scripts/generate-responses.py \
  --source-dataset your-org/prompts \
  --output-dataset your-org/generated-responses \
  --model Qwen/Qwen2.5-7B-Instruct
```

```bash
torchrun --nproc_per_node=4 scripts/generate-responses.py \
  --source-dataset your-org/prompts \
  --output-dataset your-org/generated-responses \
  --model Qwen/Qwen2.5-14B-Instruct
```

## Remote Execution Pattern

When local scripts or local inputs must be visible inside PAI DLC, set:

- `REMOTE_ASSET_PATHS`
- `REMOTE_ASSET_REPO` or `MS_REPO_OWNER` + `MS_REPO_BASE`
- `REMOTE_BOOTSTRAP_COMMAND`
- `USER_COMMAND`
- `MODELSCOPE_API_TOKEN` when private assets or publishing are involved

Then submit with:

```bash
uv run scripts/submit_pai_dlc.py --env-file configs/remote.auto.env --mode full --wait
```

## Authentication

```bash
export MODELSCOPE_API_TOKEN=<token>
modelscope login --token "$MODELSCOPE_API_TOKEN"
```

Python alternative:

```python
from modelscope.hub.api import HubApi

api = HubApi()
api.login("<token>")
```

## Artifact Persistence

Use stable output paths:

- `data/` for machine-readable artifacts
- `reports/` for markdown or JSON summaries
- `checkpoints/` for model outputs

Upload pattern:

```python
from modelscope.hub.api import HubApi

api = HubApi()
api.upload_folder(
    repo_id="your-org/your-dataset",
    folder_path="./outputs",
    path_in_repo="data",
    repo_type="dataset",
    token="<token>",
)
```

## AI Execution Contract

When using this skill, the agent should:

1. Infer the intended job shape from the workspace or user request.
2. Create `configs/pai.required.env` and wait for `continue` before the first real remote submission when the four required PAI fields are not yet ready.
3. Keep command-line interfaces stable and explicit.
4. Package missing assets before remote submission instead of assuming they are already accessible.
5. Publish outputs when credentials allow, or leave exact publish commands if blocked.
6. Save a machine-readable execution summary.

## Guardrails

- Never embed tokens in source code.
- Never publish private raw data by default.
- Do not assume a cloud scheduler other than the one explicitly configured.
- Keep script `--help` accurate when adding or changing flags.
