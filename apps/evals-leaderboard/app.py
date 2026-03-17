#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["gradio>=5.50.0", "requests>=2.32.0"]
# ///

"""Evaluation leaderboard viewer."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import gradio as gr
import requests

TABLE_HEADERS = ["Model", "Benchmark", "Score", "Source"]
TABLE_DATATYPES = ["markdown", "text", "number", "markdown"]

DEFAULT_DATASET_REPO = "modelscope-skills/evals-leaderboard"
LEADERBOARD_URL = os.getenv(
    "LEADERBOARD_JSONL_URL",
    f"https://www.modelscope.cn/datasets/{DEFAULT_DATASET_REPO}/resolve/master/data/leaderboard.jsonl",
)
METADATA_URL = os.getenv(
    "LEADERBOARD_METADATA_URL",
    f"https://www.modelscope.cn/datasets/{DEFAULT_DATASET_REPO}/resolve/master/data/metadata.json",
)

LOCAL_LEADERBOARD = Path("./data/leaderboard.jsonl")
LOCAL_METADATA = Path("./data/metadata.json")


def format_model_link(model_id: str) -> str:
    return f"[{model_id}](https://www.modelscope.cn/models/{model_id}/summary)"


def format_source_link(source_type: str, contributor: str, source_url: str) -> str:
    return f"{source_type} by [{contributor}]({source_url})"


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


def fetch_leaderboard() -> tuple[list[dict], dict]:
    try:
        return fetch_remote()
    except Exception:
        if LOCAL_LEADERBOARD.exists():
            return fetch_local()
        raise


def refresh_handler() -> tuple[str, list[list]]:
    try:
        leaderboard, metadata = fetch_leaderboard()
        rows = [
            [
                format_model_link(entry["model_id"]),
                entry["benchmark"],
                entry["score"],
                format_source_link(entry.get("source_type", "source"), entry.get("contributor", "unknown"), entry.get("source_url", "#")),
            ]
            for entry in leaderboard
        ]
        status = "\n".join(
            [
                f"**Last updated:** {metadata.get('generated_at', 'unknown')}",
                f"**Models with scores:** {metadata.get('models_with_scores', 'unknown')}",
                f"**Total entries:** {metadata.get('total_entries', len(leaderboard))}",
            ]
        )
        return status, rows
    except Exception as exc:
        return f"Failed to load leaderboard: {exc}", []


def build_app() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("# ModelScope Evaluation Leaderboard")
        status_box = gr.Markdown("Loading leaderboard...")
        leaderboard_table = gr.Dataframe(headers=TABLE_HEADERS, datatype=TABLE_DATATYPES, interactive=False, wrap=True)
        demo.load(refresh_handler, outputs=[status_box, leaderboard_table])
    return demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ModelScope evaluation leaderboard web app.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the Gradio server.")
    parser.add_argument("--port", type=int, default=7860, help="Port to bind the Gradio server.")
    parser.add_argument("--share", action="store_true", help="Enable Gradio share link.")
    args = parser.parse_args()

    demo = build_app()
    demo.launch(server_name=args.host, server_port=args.port, share=args.share)


if __name__ == "__main__":
    main()
