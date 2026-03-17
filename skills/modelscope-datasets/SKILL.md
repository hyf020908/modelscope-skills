---
name: modelscope-datasets
description: Create, curate, and publish datasets on ModelScope Hub with template-driven validation and SQL-based analysis.
---

# ModelScope Datasets

Use this skill for end-to-end dataset workflows on ModelScope Hub.

## What This Skill Covers

- Create dataset repositories on ModelScope Hub.
- Validate rows against dataset templates (`chat`, `classification`, `qa`, `tabular`, `completion`, `custom`).
- Append or rewrite split files with consistent JSONL format.
- Run local DuckDB SQL over downloaded parquet files.
- Publish processed artifacts back to ModelScope.

## Primary Scripts

- `scripts/dataset_manager.py`: repository lifecycle + JSONL content operations.
- `scripts/sql_manager.py`: SQL analysis and transform/export pipeline.

## Standard Workflow

1. Initialize repository.
2. Validate and append rows.
3. Inspect stats and schema.
4. Run SQL transforms.
5. Upload curated outputs.

## Quick Commands

```bash
# 1) Initialize dataset repository
uv run scripts/dataset_manager.py init --repo-id your-name/my-dataset

# 2) Quick template setup
uv run scripts/dataset_manager.py quick-setup --repo-id your-name/my-dataset --template chat

# 3) Add rows
uv run scripts/dataset_manager.py add-rows \
  --repo-id your-name/my-dataset \
  --template chat \
  --rows-json '[{"messages":[{"role":"user","content":"hello"},{"role":"assistant","content":"hi"}]}]'

# 4) SQL profile on local files
uv run scripts/sql_manager.py query \
  --input './data/my-dataset/**/*.parquet' \
  --sql 'SELECT count(*) AS rows FROM data'
```

## Authentication

Use one of these patterns:

- `MODELSCOPE_API_TOKEN` environment variable.
- `modelscope login --token "$MODELSCOPE_API_TOKEN"` before running scripts.

## Validation Expectations

- Keep row schema aligned with selected template.
- Ensure required fields exist and content is non-empty.
- Reject malformed chat turns (`role` + `content` required).
- Include metadata fields when available (`source`, `license`, `language`).

## Publishing Rules

- Use clear commit messages for data updates.
- Separate raw and processed outputs (`raw/`, `processed/`).
- Include a concise dataset README and license metadata.

## Safety

- Never log or commit secrets.
- Avoid uploading private or regulated data.
- For large datasets, upload in folder batches and verify checksums.
