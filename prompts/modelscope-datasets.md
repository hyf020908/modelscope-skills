$modelscope-datasets

You are running inside local codex-cli.
Use this skill to create, curate, validate, and publish a dataset to ModelScope Hub.

Hard requirements:
1. Do not stop because the current directory lacks a finished dataset.
2. If no dataset exists yet, automatically create a minimal but valid starter dataset.
3. Prefer clean, publishable structure over ad hoc files.
4. Validate format, splits, metadata, and basic quality before publishing.
5. Generate all missing files needed for a usable dataset repository.
6. Keep the dataset small and practical if the project is empty.
7. Publish to ModelScope Hub if credentials allow; otherwise prepare everything for immediate publish.

Please do the following:
A. Scan the workspace for existing data files and infer the intended dataset type.
B. If no dataset is present, create a minimal starter dataset with train/valid splits.
C. Normalize file structure, field names, and metadata.
D. Validate the dataset and fix straightforward issues automatically.
E. Generate a clean dataset card / README and supporting files.
F. Create or reuse the target dataset repository on ModelScope Hub.
G. Upload the dataset if credentials are available.

Output only:
1. Dataset type and structure
2. Files created or normalized
3. Validation results
4. Hub repository created or reused
5. Upload result
6. Any single blocking issue