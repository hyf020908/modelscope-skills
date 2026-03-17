---
name: modelscope-jobs
description: Execute reproducible ML workflows and publish outputs to ModelScope repositories using UV scripts and token-authenticated uploads.
---

# ModelScope Jobs

Use this skill for script-based workflow execution where outputs must be versioned on ModelScope Hub.

## Scope

- Batch data generation and transformation.
- Large-scale inference scripts.
- Dataset statistics and reporting pipelines.
- Uploading produced artifacts to model or dataset repos.

## Included Script Templates

- `scripts/generate-responses.py`
- `scripts/cot-self-instruct.py`
- `scripts/finepdfs-stats.py`

These scripts are intended to run with `uv run` and push results using `HubApi`.

## Runtime Patterns

### Local / single node

```bash
uv run scripts/generate-responses.py \
  --source-dataset your-org/prompts \
  --output-dataset your-org/generated-responses \
  --model Qwen/Qwen2.5-7B-Instruct
```

### Multi-GPU node

```bash
torchrun --nproc_per_node=4 scripts/generate-responses.py \
  --source-dataset your-org/prompts \
  --output-dataset your-org/generated-responses \
  --model Qwen/Qwen2.5-14B-Instruct
```

### Scheduled environment

Use your own scheduler (for example cron, Airflow, Argo, Slurm, or CI runners) and keep script entrypoints unchanged.

## Authentication

```bash
export MODELSCOPE_API_TOKEN=<token>
modelscope login --token "$MODELSCOPE_API_TOKEN"
```

In Python:

```python
from modelscope.hub.api import HubApi

api = HubApi()
api.login("<token>")
```

## Artifact Persistence

Use explicit repository targets and stable output paths:

- `data/` for machine-readable artifacts
- `reports/` for markdown/json summaries
- `checkpoints/` for training or adapter snapshots

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

## Operational Checklist

- Confirm token is available before runtime.
- Validate input schemas before launching heavy workloads.
- Persist intermediate artifacts for reproducibility.
- Emit structured logs (JSON lines preferred).
- Include commit messages with timestamp + purpose.

## Guardrails

- Never embed tokens in source code.
- Never publish private raw data by default.
- Do not assume a specific cloud job provider in scripts.
- Keep script interfaces stable (`--help` must stay accurate).
