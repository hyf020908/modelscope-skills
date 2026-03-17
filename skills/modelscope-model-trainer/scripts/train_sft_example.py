#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Generate a recommended `swift sft` command for ModelScope workflows."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Print an ms-swift SFT command template")
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output", default="./outputs/sft")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    cmd = (
        "swift sft "
        f"--model {args.model} "
        f"--dataset {args.dataset} "
        f"--output_dir {args.output} "
        f"--num_train_epochs {args.epochs}"
    )
    print(cmd)


if __name__ == "__main__":
    main()
