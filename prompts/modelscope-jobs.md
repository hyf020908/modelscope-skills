$modelscope-jobs

You are running inside local codex-cli.
Treat the local machine as a control plane only.
Use this skill to package and run a reproducible ML workflow as a ModelScope-oriented job, then publish outputs to ModelScope repositories.

Hard requirements:
1. Do not use the local machine for long-running training or heavy execution if remote or job-based execution is more appropriate.
2. Package the workflow into reproducible scripts and job-ready assets.
3. If the workspace is incomplete, generate the minimal missing files and continue.
4. Prefer UV-based reproducible execution where suitable.
5. Publish resulting artifacts to ModelScope Hub when credentials allow.
6. If remote execution is blocked, still prepare the complete job package and submission commands.
7. Prefer PAI DLC for heavy execution and treat the local machine as the orchestration plane only.
8. When remote execution needs local scripts or local inputs, upload them first through `REMOTE_ASSET_PATHS` and a ModelScope dataset repo before submitting.
9. Keep all process narration and progress updates in Chinese.

Please do the following:
A. Scan the workspace and infer the intended workflow.
B. Organize code, configs, inputs, and outputs into a reproducible job structure.
C. Generate missing scripts and job entrypoints as needed.
D. Prepare the workflow for execution with sensible defaults.
E. Run only lightweight validation locally when necessary.
F. Submit the real workload to PAI DLC when it is non-trivial.
G. Publish outputs or prepare them for ModelScope upload.
H. Save a job manifest and execution summary.

Output only:
1. Job type inferred
2. Scripts and configs generated
3. Execution method used
4. Artifacts produced
5. Publication status
6. Any single blocking issue
