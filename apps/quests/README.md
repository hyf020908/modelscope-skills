---
title: Quests
emoji: 🧭
colorFrom: yellow
colorTo: gray
sdk: static
pinned: false
---

# ModelScope Skills Quest Series

<img src="https://github.com/hyf020908/modelscope-skills/raw/main/assets/banner.png" alt="ModelScope Skills Quests" width="100%">

This quest series helps contributors ship practical, reusable assets for ModelScope workflows in this independent community repository.

## What You Will Build

Over four guided quests, contributors work across the full model lifecycle:

- **Quest 1**: Evaluate Hub models and publish structured benchmark metadata.
- **Quest 2**: Create and publish high-quality datasets.
- **Quest 3**: Fine-tune language models and release reproducible checkpoints.
- **Quest 4**: Improve tooling, reporting, and leaderboard automation.

## Quest Index

| Quest | Focus | Link |
|------|-------|------|
| Quest 1 | Evaluate a Hub model | [02_evaluate-hub-model.md](02_evaluate-hub-model.md) |
| Quest 2 | Publish a Hub dataset | [03_publish-hub-dataset.md](03_publish-hub-dataset.md) |
| Quest 3 | Supervised fine-tuning | [04_sft-finetune-hub.md](04_sft-finetune-hub.md) |

## Getting Started

### 1. Join the Organization

Join the `modelscope-skills` community organization on ModelScope so contributions can be tracked centrally.

### 2. Set Up an Agent

Use any coding agent that can read markdown instructions and run shell/Python commands:

- Claude Code
- Codex CLI
- Gemini CLI
- Cursor / Windsurf
- Other terminal-first coding agents

Install skills from this repository using the main [README](../../README.md).

### 3. Authenticate with ModelScope

Create an access token on ModelScope, then login:

```bash
# Interactive login
modelscope login

# Or token-based login in CI/headless environments
modelscope login --token "$MODELSCOPE_API_TOKEN"
```

### 4. Clone the Repository

```bash
git clone https://github.com/hyf020908/modelscope-skills.git
cd modelscope-skills
```

## Leaderboards

Leaderboard apps live in this repository:

- Evaluation leaderboard: `apps/evals-leaderboard/`
- Contributor leaderboard: `apps/hackers-leaderboard/`

Run locally:

```bash
uv run apps/hackers-leaderboard/collect_points.py --owners Qwen AI-ModelScope iic --output-dir ./apps/hackers-leaderboard/data
python apps/hackers-leaderboard/app.py
```

## Contribution Rules

- Use repository skills and scripts where possible.
- Submit clean, reproducible outputs.
- Keep metadata complete and verifiable.
- Document methods clearly in PR descriptions.

## Help

- [ModelScope Discord](https://discord.com/channels/879548962464493619/1442881667986624554)
- [ModelScope livestreams](https://www.youtube.com/@ModelScope/streams)
- [GitHub issues](https://github.com/hyf020908/modelscope-skills/issues)

Start with Quest 1 and build momentum across the series.
