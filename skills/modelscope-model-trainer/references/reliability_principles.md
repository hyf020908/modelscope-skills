# Reliability Principles

- Reproducibility first: seed, config, and data revision must be pinned.
- Fail fast: run smoke tests before full epochs.
- Observable runs: capture training + validation metrics each checkpoint.
- Safe publishing: push only validated checkpoints.
