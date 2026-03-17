# Troubleshooting

## OOM During Training

- Reduce sequence length.
- Reduce micro-batch size.
- Increase gradient accumulation.

## Diverging Loss

- Lower learning rate.
- Check dataset formatting and label leakage.
- Validate tokenizer and special tokens.

## Upload Failures

- Confirm token scope and namespace.
- Retry with smaller upload folders.
