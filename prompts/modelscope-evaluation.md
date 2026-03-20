$modelscope-evaluation

You are running inside local codex-cli.
Use this skill to collect, normalize, organize, and publish benchmark or evaluation results for a ModelScope model repository.

Hard requirements:
1. Do not stop because evaluation files are messy or incomplete.
2. Reuse existing logs, tables, README content, and result artifacts when possible.
3. If metrics are scattered, consolidate them into a clean evaluation summary.
4. Normalize score names, formats, and benchmark metadata.
5. Generate missing evaluation documentation if needed.
6. Prefer reproducible summaries over hand-written one-off edits.
7. If publishing is blocked by credentials, still prepare all files for immediate upload.
8. Heavy or long-running evaluation should run remotely on PAI DLC instead of on local macOS.
9. When remote execution needs local files, upload them first through `REMOTE_ASSET_PATHS` plus a ModelScope asset repo before submitting to PAI.
10. Keep all process narration and progress updates in Chinese.

Please do the following:
A. Scan the workspace and current repo for evaluation outputs, logs, README sections, and metric files.
B. Extract the benchmark names, task types, score values, and any model/version metadata.
C. Decide whether the task is metadata-only or requires actual evaluation execution.
D. Normalize the results into a consistent structure.
E. If execution is required, package scripts/configs for remote use and submit the job to PAI DLC.
F. Generate or update evaluation summary files and README sections.
G. If appropriate, prepare Hub-ready metadata for publishing the evaluation results.
H. Upload or stage the outputs for ModelScope publication.

Output only:
1. Benchmarks detected
2. Metrics normalized
3. Files generated or updated
4. Remote execution status
5. Publication status
6. Any single blocking issue
