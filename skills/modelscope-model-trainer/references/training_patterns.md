# Training Patterns

## Pattern A: Single-stage SFT

- Prepare cleaned dataset
- Train one adapter
- Evaluate and publish best checkpoint

## Pattern B: SFT -> DPO

- Build preference pairs from SFT outputs
- Continue from SFT checkpoint
- Compare alignment metrics before publishing

## Pattern C: Long-running GRPO

- Start from validated SFT/DPO checkpoint
- Use strict checkpoint cadence
- Track rollback point every N steps
