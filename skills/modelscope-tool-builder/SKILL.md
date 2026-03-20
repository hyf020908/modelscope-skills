---
name: modelscope-tool-builder
description: Build reusable automation scripts for ModelScope Hub API workflows.
---

# ModelScope Tool Builder

Use this skill when a repetitive ModelScope workflow should become a reusable script or small utility instead of a one-off shell command.

## Operating Mode

- Build tools with explicit inputs, outputs, and failure modes.
- Prefer official ModelScope CLI or SDK behavior over scraping or undocumented endpoints.
- Keep tools composable so they can be used by agents, CI, or local operators.
- Emit structured output whenever possible.

## What To Build

- Data collection tools for models or datasets.
- Metadata normalization and enrichment pipelines.
- Reporting scripts.
- Upload, sync, or export utilities for curated artifacts.

## Reference Templates

- `references/baseline_modelscope_api.py`
- `references/baseline_modelscope_api.sh`
- `references/baseline_modelscope_api.tsx`
- `references/modelscope_enrich_models.sh`
- `references/modelscope_model_card_frontmatter.sh`
- `references/modelscope_model_papers_auth.sh`

## AI Execution Contract

When using this skill, the agent should:

1. Identify the repeatable part of the workflow.
2. Turn it into a documented script with stable flags.
3. Validate inputs early and emit actionable errors.
4. Provide example usage and an output schema.
5. Test the lightest meaningful path locally when possible.

## Standards

- Prefer explicit CLI flags over hardcoded constants.
- Include idempotent behavior and clear exit codes.
- Emit JSON output for downstream automation when appropriate.
- Keep token handling external through environment variables.

## Delivery Checklist

- The script has `--help` and at least one usage example.
- Output schema is documented or obvious from structured output.
- Failure modes include actionable messages.
- Network calls include timeout and retry behavior when relevant.
