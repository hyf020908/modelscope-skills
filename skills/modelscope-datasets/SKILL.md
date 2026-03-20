---
name: modelscope-datasets
description: Create, curate, and publish datasets on ModelScope Hub with template-driven validation and SQL-based analysis.
---

# ModelScope Datasets

Use this skill for end-to-end dataset creation, normalization, validation, and publication on ModelScope Hub.

## Operating Mode

- Prefer template-driven structure over ad hoc JSON files.
- Keep splits, schema, and metadata explicit.
- Validate rows before upload instead of relying on downstream training failures.
- Use SQL only for local analysis or transformation after a snapshot exists.

## What This Skill Covers

- Create dataset repositories on ModelScope Hub.
- Validate rows against templates: `chat`, `classification`, `qa`, `tabular`, `completion`, `custom`.
- Append or rewrite split files with consistent JSONL structure.
- Inspect or transform local snapshots with DuckDB.
- Publish processed outputs back to ModelScope.

## Primary Scripts

- `scripts/dataset_manager.py`
  Repository initialization, template setup, row validation, split upload, stats.
- `scripts/sql_manager.py`
  Local SQL query, schema description, export, and optional push-back to Hub.

## Standard Workflow

1. Infer dataset type from current files or user intent.
2. Initialize the target dataset repo.
3. Select the nearest template and validate rows.
4. Upload normalized split files.
5. Run local SQL checks or exports if needed.
6. Publish curated outputs and supporting metadata.

## Quick Commands

```bash
uv run scripts/dataset_manager.py init --repo-id your-name/my-dataset
uv run scripts/dataset_manager.py quick-setup --repo-id your-name/my-dataset --template chat
uv run scripts/dataset_manager.py add-rows \
  --repo-id your-name/my-dataset \
  --template chat \
  --rows-json '[{"messages":[{"role":"user","content":"hello"},{"role":"assistant","content":"hi"}]}]'
uv run scripts/sql_manager.py query \
  --input './data/my-dataset/**/*.parquet' \
  --sql 'SELECT count(*) AS rows FROM data'
```

## AI Execution Contract

When using this skill, the agent should:

1. Detect whether the workspace already contains usable dataset files.
2. Choose the closest supported template and normalize rows toward it.
3. Generate missing repo metadata and split structure when necessary.
4. Validate before upload and repair only straightforward issues automatically.
5. Leave a clean dataset repo or a clean local staging directory if credentials are missing.

## Authentication

Use either:

- `MODELSCOPE_API_TOKEN`
- `modelscope login --token "$MODELSCOPE_API_TOKEN"`

## Validation Expectations

- Required template fields must exist and be non-empty.
- Chat rows must contain valid `role` and `content`.
- Split names should stay conventional unless the user explicitly needs custom names.
- Metadata such as `source`, `license`, and `language` should be preserved when known.

## Output Expectations

Provide:

- Dataset type and chosen template.
- Files created, normalized, or uploaded.
- Validation results and remaining warnings.
- Repository identifier created or reused.
- Upload status or exact next action if blocked.

## Guardrails

- Never log or commit tokens.
- Avoid uploading private, regulated, or unlicensed data.
- Keep raw and processed data separate when both exist.
- For large datasets, upload in chunks and verify resulting files.
