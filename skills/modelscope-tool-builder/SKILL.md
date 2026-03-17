---
name: modelscope-tool-builder
description: Build reusable automation scripts for ModelScope Hub API workflows.
---

# ModelScope Tool Builder

Use this skill when users need repeatable scripts that query, filter, enrich, or publish ModelScope model/dataset metadata.

## What To Build

- Data collection tools for models/datasets.
- Metadata normalization pipelines.
- Daily/weekly reporting scripts.
- Upload or sync utilities for curated artifacts.

## Reference Templates

- `references/baseline_modelscope_api.py`
- `references/baseline_modelscope_api.sh`
- `references/baseline_modelscope_api.tsx`
- `references/modelscope_enrich_models.sh`
- `references/modelscope_model_card_frontmatter.sh`
- `references/modelscope_model_papers_auth.sh`

## Standards

- Prefer explicit CLI flags over hardcoded constants.
- Include idempotent behavior and clear exit codes.
- Emit JSON output for downstream automation.
- Keep token handling external (`MODELSCOPE_API_TOKEN`).

## Delivery Checklist

- Script has `--help` and usage examples.
- Output schema is documented.
- Failure modes include actionable error messages.
- Network calls include timeout and retry policy.
