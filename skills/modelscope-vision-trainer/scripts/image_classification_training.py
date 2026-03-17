#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Generate a reference command for image classification fine-tuning."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Print classification training command")
    parser.add_argument("--model", required=True)
    parser.add_argument("--train-dir", required=True)
    parser.add_argument("--val-dir", required=True)
    parser.add_argument("--output", default="./outputs/cls")
    args = parser.parse_args()

    cmd = (
        "python train_image_classification.py "
        f"--model {args.model} "
        f"--train_dir {args.train_dir} "
        f"--val_dir {args.val_dir} "
        f"--output_dir {args.output}"
    )
    print(cmd)


if __name__ == "__main__":
    main()
