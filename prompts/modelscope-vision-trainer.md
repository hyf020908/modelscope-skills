$modelscope-vision-trainer

You are running inside local codex-cli.
Treat the local machine as a control plane only.
Automatically prepare a reproducible vision-training workflow and submit the actual training job to a remote cloud environment instead of training locally.

Hard requirements:
1. Never run heavy vision training on local macOS.
2. Local work is limited to dataset inspection, config generation, packaging, submission, status polling, and result collection.
3. Prefer a lightweight pilot run before a full remote training run.
4. If no dataset is present, automatically choose or create a minimal viable vision dataset setup.
5. If configs or scripts are missing, generate the smallest reproducible training pipeline and continue.
6. Use the most suitable vision training approach for the task inferred from the workspace.
7. Publish checkpoints to ModelScope Hub when possible.
8. If remote credentials or execution access are missing, still prepare all assets and exact submission steps.
9. If the workspace does not contain a real runnable training entrypoint for the inferred vision task, do not pretend training can run; scaffold the missing entrypoint or stop at a remote-ready package with exact next steps.
10. When local scripts or local configs must be visible in PAI DLC, upload them first through `REMOTE_ASSET_PATHS` and a ModelScope asset repo.
11. Keep all process narration and progress updates in Chinese.

Please do the following:
A. Infer the vision task from the workspace, such as classification, detection, or segmentation.
B. Reuse any existing data and configs; otherwise create a minimal viable setup.
C. Confirm whether a runnable training entrypoint already exists; scaffold one if missing and feasible.
D. Generate a reproducible remote-ready training configuration.
E. Submit a pilot training run remotely when the entrypoint is real and runnable.
F. Fix one common failure automatically if possible, then continue.
G. Launch the full run, monitor it, collect outputs, and identify the best checkpoint.
H. Publish the final artifacts to ModelScope Hub.

Output only:
1. Vision task inferred
2. Files generated
3. Remote environment used
4. Pilot result
5. Full training result
6. Best checkpoint path
7. Hub publication result
8. The single blocking issue if interrupted
