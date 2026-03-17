#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Generate a recommended `swift grpo` command."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Print an ms-swift GRPO command template")
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output", default="./outputs/grpo")
    args = parser.parse_args()

    cmd = (
        "swift grpo "
        f"--model {args.model} "
        f"--dataset {args.dataset} "
        f"--output_dir {args.output}"
    )
    print(cmd)


if __name__ == "__main__":
    main()
