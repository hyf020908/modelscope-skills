# Training Methods

## SFT

Use when you have instruction-response pairs and need baseline adaptation.

## DPO

Use when you have preference pairs (`chosen`/`rejected`) and want alignment without reward model training.

## GRPO

Use when reinforcement-style optimization is needed with group-relative rewards.

## Selection Rule

- Start with SFT.
- Add DPO for preference alignment.
- Use GRPO only when reward signals justify extra complexity.
