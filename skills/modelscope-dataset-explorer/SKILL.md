---
name: modelscope-dataset-explorer
description: Explore ModelScope datasets using Hub metadata APIs, local snapshot downloads, and SQL analysis with DuckDB.
---

# ModelScope Dataset Explorer

Use this skill when users need to inspect dataset structure, sample rows, or run ad-hoc analysis before training or evaluation.

## Workflow

1. Inspect dataset metadata from ModelScope Hub.
2. Download required files or split subsets to local workspace.
3. Run SQL or pandas exploration on local parquet/json/csv files.
4. Summarize quality issues and recommended transformations.

## Metadata Discovery

Use Python for reliable discovery:

```python
from modelscope.hub.api import HubApi

api = HubApi()
# owner_or_group can be a username or organization
result = api.list_datasets(owner_or_group="AI-ModelScope", page_number=1, page_size=20)
print(result)
```

## Snapshot Download

```bash
# Full dataset snapshot
modelscope download --dataset your-org/your-dataset --local_dir ./data/your-dataset

# Selective download by pattern
modelscope download --dataset your-org/your-dataset --include "*.parquet" --local_dir ./data/your-dataset
```

Python alternative:

```python
from modelscope.hub.snapshot_download import dataset_snapshot_download

local_dir = dataset_snapshot_download("your-org/your-dataset", local_dir="./data/your-dataset")
print(local_dir)
```

## Query With DuckDB

```bash
duckdb -c "SELECT count(*) FROM read_parquet('./data/your-dataset/**/*.parquet');"
```

Use this pattern for lightweight profiling:

```sql
SELECT
  count(*) AS rows,
  approx_count_distinct(label) AS distinct_labels,
  avg(length(text)) AS avg_text_len
FROM read_parquet('./data/your-dataset/**/*.parquet');
```

## Publishing Curated Data Back To Hub

```bash
# Create dataset repository once
modelscope create your-name/cleaned-dataset --repo_type dataset --visibility public

# Upload processed files
modelscope upload your-name/cleaned-dataset ./outputs data --repo-type dataset
```

## Output Expectations

Provide:

- Dataset schema summary (columns and inferred types).
- Split statistics and missing-value profile.
- At least 3 representative samples.
- Concrete transformation recommendations for downstream training.

## Guardrails

- Do not assume a public remote SQL endpoint exists.
- Do not expose private data in logs or markdown snippets.
- Keep downloaded data inside project-scoped directories.
