#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["gradio>=5.50.0", "requests>=2.32.0"]
# ///

"""Contributor leaderboard viewer."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import gradio as gr
import requests

TABLE_HEADERS = ["Rank", "Owner", "Points", "Models", "Datasets"]
TABLE_DATATYPES = ["number", "text", "number", "number", "number"]

DEFAULT_DATASET_REPO = "modelscope-skills/hackers-leaderboard"
LEADERBOARD_URL = os.getenv(
    "HACKERS_LEADERBOARD_JSONL_URL",
    f"https://www.modelscope.cn/datasets/{DEFAULT_DATASET_REPO}/resolve/master/data/leaderboard.jsonl",
)
METADATA_URL = os.getenv(
    "HACKERS_LEADERBOARD_METADATA_URL",
    f"https://www.modelscope.cn/datasets/{DEFAULT_DATASET_REPO}/resolve/master/data/metadata.json",
)

LOCAL_LEADERBOARD = Path("./data/leaderboard.jsonl")
LOCAL_METADATA = Path("./data/metadata.json")


def fetch_remote() -> tuple[list[dict], dict]:
    r1 = requests.get(LEADERBOARD_URL, timeout=20)
    r1.raise_for_status()
    rows = [json.loads(line) for line in r1.text.splitlines() if line.strip()]

    r2 = requests.get(METADATA_URL, timeout=20)
    r2.raise_for_status()
    meta = r2.json()
    return rows, meta


def fetch_local() -> tuple[list[dict], dict]:
    rows = [json.loads(line) for line in LOCAL_LEADERBOARD.read_text(encoding="utf-8").splitlines() if line.strip()]
    meta = json.loads(LOCAL_METADATA.read_text(encoding="utf-8")) if LOCAL_METADATA.exists() else {}
    return rows, meta


def fetch() -> tuple[list[dict], dict]:
    try:
        return fetch_remote()
    except Exception:
        if LOCAL_LEADERBOARD.exists():
            return fetch_local()
        raise


def refresh_handler() -> tuple[str, list[list]]:
    try:
        rows, meta = fetch()
        table = [
            [idx + 1, row["username"], row["total_points"], row.get("models", 0), row.get("datasets", 0)]
            for idx, row in enumerate(rows)
        ]
        status = "\n".join(
            [
                f"**Last updated:** {meta.get('generated_at', 'unknown')}",
                f"**Participants:** {meta.get('total_participants', len(rows))}",
                f"**Total points:** {meta.get('total_points', sum(r['total_points'] for r in rows))}",
            ]
        )
        return status, table
    except Exception as exc:
        return f"Failed to load leaderboard: {exc}", []


def build_app() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("# ModelScope Contributor Leaderboard")
        status = gr.Markdown("Loading leaderboard...")
        table = gr.Dataframe(headers=TABLE_HEADERS, datatype=TABLE_DATATYPES, interactive=False)
        demo.load(refresh_handler, outputs=[status, table])
    return demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ModelScope contributor leaderboard web app.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the Gradio server.")
    parser.add_argument("--port", type=int, default=7861, help="Port to bind the Gradio server.")
    parser.add_argument("--share", action="store_true", help="Enable Gradio share link.")
    args = parser.parse_args()

    demo = build_app()
    demo.launch(server_name=args.host, server_port=args.port, share=args.share)


if __name__ == "__main__":
    main()
