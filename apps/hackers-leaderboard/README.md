# Contributor Leaderboard

This app ranks owners by publicly visible ModelScope repository activity (models + datasets).

## Collect Data

```bash
uv run collect_points.py --owners Qwen AI-ModelScope iic --output-dir ./data
```

Publish to dataset repo:

```bash
uv run collect_points.py \
  --owners Qwen AI-ModelScope iic \
  --push-to modelscope-skills/hackers-leaderboard
```

## Run App

```bash
uv run app.py
```
