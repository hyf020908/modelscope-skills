---
name: modelscope-cli
description: Use the official `modelscope` CLI for ModelScope Hub authentication, repository creation, download, and upload workflows.
---

# ModelScope CLI

Use this skill when a task involves ModelScope Hub operations that should run from the command line.

## When To Use

- Login or token-based authentication for ModelScope Hub.
- Create model or dataset repositories.
- Download model or dataset snapshots (full or filtered).
- Upload files or folders to an existing repository.
- Check and clean local ModelScope cache.

## Core Commands

### Authentication

```bash
modelscope login --token "$MODELSCOPE_API_TOKEN"
```

For one-off commands, you can also pass `--token` directly.

### Create Repository

```bash
# Model repository
modelscope create your-name/your-model --repo_type model --visibility public

# Dataset repository
modelscope create your-name/your-dataset --repo_type dataset --visibility private
```

### Download

```bash
# Download a whole model repo
modelscope download --model Qwen/Qwen2.5-7B-Instruct --local_dir ./artifacts

# Download selected files
modelscope download --model Qwen/Qwen2.5-7B-Instruct tokenizer.json config.json --local_dir ./artifacts

# Download a dataset repo
modelscope download --dataset your-name/your-dataset --local_dir ./dataset
```

### Upload

```bash
# Upload one file to model repo
modelscope upload your-name/your-model ./README.md README.md --repo-type model

# Upload a folder to dataset repo
modelscope upload your-name/your-dataset ./data data --repo-type dataset
```

## Python SDK Equivalents

Use these when CLI is not ideal:

```python
from modelscope.hub.api import HubApi
from modelscope.hub.snapshot_download import snapshot_download, dataset_snapshot_download

api = HubApi()
api.login("<token>")
api.create_repo("your-name/your-model", repo_type="model", exist_ok=True)

snapshot_download(repo_id="Qwen/Qwen2.5-7B-Instruct", local_dir="./artifacts")
dataset_snapshot_download("your-name/your-dataset", local_dir="./dataset")
```

## Safety And Quality

- Never hardcode tokens in scripts or docs.
- Prefer `--local_dir` for deterministic outputs.
- Use include/exclude patterns for large repositories.
- For automation, include clear commit messages on upload operations.

## Troubleshooting

- Unauthorized errors: verify token scope and owner namespace.
- Empty downloads: confirm repo type (`model` vs `dataset`) and revision.
- Partial uploads: re-run with `--include`/`--exclude` reviewed for glob mistakes.
