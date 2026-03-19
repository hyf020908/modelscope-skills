#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Create minimum remote-training assets for a low-cost PAI DLC SFT run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def write_if_missing(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def build_train_lines() -> List[str]:
    rows = [
        {
            "instruction": "Explain SFT in one sentence.",
            "input": "",
            "output": "SFT fine-tunes a base model on instruction-response pairs to match target behavior.",
        },
        {
            "instruction": "Rewrite with a formal tone: can you send it today?",
            "input": "",
            "output": "Could you please send it today?",
        },
        {
            "instruction": "Give three tips for maintainable code.",
            "input": "",
            "output": "Use small modules, add tests, and keep naming consistent.",
        },
        {
            "instruction": "Translate to Chinese: We will fix this issue soon.",
            "input": "",
            "output": "我们会尽快修复这个问题。",
        },
    ]
    return [json.dumps(x, ensure_ascii=False) for x in rows]


def build_valid_lines() -> List[str]:
    rows = [
        {
            "instruction": "State one benefit of unit tests.",
            "input": "",
            "output": "Unit tests help detect regressions quickly.",
        }
    ]
    return [json.dumps(x, ensure_ascii=False) for x in rows]


def env_block(data: Dict[str, str]) -> str:
    return "\n".join([f"{k}={v}" for k, v in data.items()]) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap minimal remote training assets")
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--model-id", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    changed: List[str] = []
    kept: List[str] = []

    train_path = root / "data/train.jsonl"
    valid_path = root / "data/valid.jsonl"
    pilot_cfg = root / "configs/pilot.env"
    full_cfg = root / "configs/full.env"
    remote_env = root / "configs/remote.auto.env"

    train_content = "\n".join(build_train_lines()) + "\n"
    valid_content = "\n".join(build_valid_lines()) + "\n"

    pilot_content = env_block(
        {
            "MODEL_ID": args.model_id,
            "TRAIN_TYPE": "lora",
            "MAX_LENGTH": "256",
            "BATCH_SIZE": "1",
            "GRAD_ACC": "2",
            "LEARNING_RATE": "5e-5",
            "EPOCHS": "1",
            "MAX_STEPS": "6",
            "SAVE_STEPS": "3",
            "EVAL_STEPS": "3",
            "LOGGING_STEPS": "2",
            "LORA_RANK": "4",
            "EVAL_DATASET": "AI-ModelScope/alpaca-gpt4-data-zh#100",
            "EXTRA_SWIFT_ARGS": "--bf16 false --fp16 false --torch_dtype float32",
        }
    )
    full_content = env_block(
        {
            "MODEL_ID": args.model_id,
            "TRAIN_TYPE": "lora",
            "MAX_LENGTH": "512",
            "BATCH_SIZE": "1",
            "GRAD_ACC": "4",
            "LEARNING_RATE": "5e-5",
            "EPOCHS": "1",
            "MAX_STEPS": "24",
            "SAVE_STEPS": "12",
            "EVAL_STEPS": "12",
            "LOGGING_STEPS": "4",
            "LORA_RANK": "8",
            "EVAL_DATASET": "AI-ModelScope/alpaca-gpt4-data-zh#120",
            "EXTRA_SWIFT_ARGS": "--bf16 false --fp16 false --torch_dtype float32",
        }
    )
    remote_content = env_block(
        {
            "ALIBABA_CLOUD_ACCESS_KEY_ID": "",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "",
            "ALIBABA_CLOUD_SECURITY_TOKEN": "",
            "PAI_REGION": "cn-shanghai",
            "PAI_WORKSPACE_ID": "",
            "PAI_DLC_IMAGE": "pytorch/pytorch:latest",
            "PAI_DLC_ECS_SPEC": "",
            "PAI_DLC_GPU": "0",
            "PAI_DLC_CPU": "4",
            "PAI_DLC_MEMORY": "16Gi",
            "PAI_DLC_MAX_MINUTES": "180",
            "MODELSCOPE_API_TOKEN": "",
            "MS_REPO_OWNER": "",
            "MS_REPO_BASE": "qwen2p5-1p5b-sft",
        }
    )

    files = {
        train_path: train_content,
        valid_path: valid_content,
        pilot_cfg: pilot_content,
        full_cfg: full_content,
        remote_env: remote_content,
    }
    for p, content in files.items():
        if write_if_missing(p, content, args.force):
            changed.append(str(p))
        else:
            kept.append(str(p))

    result = {
        "root": str(root),
        "changed_files": changed,
        "kept_files": kept,
        "next_commands": [
            ".venv/bin/python scripts/submit_pai_dlc.py --env-file configs/remote.auto.env --mode pilot --wait --retry-once",
            ".venv/bin/python scripts/submit_pai_dlc.py --env-file configs/remote.auto.env --mode full --wait",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
