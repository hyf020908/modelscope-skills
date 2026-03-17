# Quest 2: Publish a Hub Dataset

Create and release production-grade datasets on ModelScope Hub with clear schema, licensing, and provenance.

## Why This Matters

Open, high-quality datasets directly improve downstream model quality and reproducibility.

## Skill To Use

Use `skills/modelscope-datasets/`.

Core capabilities:

- Initialize dataset repositories with clean structure.
- Validate rows against task templates.
- Append data in JSONL split format.
- Run SQL analysis and upload transformed outputs.

## Quick Start

```bash
uv run skills/modelscope-datasets/scripts/dataset_manager.py quick-setup \
  --repo-id "your-username/your-dataset" \
  --template chat
```

## XP Tiers

### Starter (50 XP)

Upload a small, clean dataset with a complete dataset card.

```bash
uv run skills/modelscope-datasets/scripts/dataset_manager.py init \
  --repo-id "modelscope-skills/your-dataset"

uv run skills/modelscope-datasets/scripts/dataset_manager.py add-rows \
  --repo-id "modelscope-skills/your-dataset" \
  --template classification \
  --rows-json "$(cat your_data.json)"
```

### Standard (100 XP)

Publish a conversational dataset with strong documentation and validated schema.

### Advanced (200 XP)

Release a multilingual or transformed variant of an existing public dataset and document the transformation pipeline.

## Quality Checklist

- Clear license in README frontmatter.
- Explicit train/validation/test split policy.
- Provenance notes for source and cleaning steps.
- Schema-valid rows for the selected template.

## Resources

- [Skill guide](../../skills/modelscope-datasets/SKILL.md)
- [Dataset templates](../../skills/modelscope-datasets/templates/)
- [Examples](../../skills/modelscope-datasets/examples/)

---

Next: [Quest 3 - Supervised Fine-Tuning](04_sft-finetune-hub.md)
