#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Generate a reference command for object detection fine-tuning."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Print object detection training command")
    parser.add_argument("--model", required=True)
    parser.add_argument("--train-annotations", required=True)
    parser.add_argument("--val-annotations", required=True)
    parser.add_argument("--images-root", required=True)
    parser.add_argument("--output", default="./outputs/det")
    args = parser.parse_args()

    cmd = (
        "python train_object_detection.py "
        f"--model {args.model} "
        f"--train_annotations {args.train_annotations} "
        f"--val_annotations {args.val_annotations} "
        f"--images_root {args.images_root} "
        f"--output_dir {args.output}"
    )
    print(cmd)


if __name__ == "__main__":
    main()
