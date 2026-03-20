---
name: transformers-js
description: Build JavaScript/TypeScript inference workflows with Transformers.js, using ModelScope-hosted assets through local downloads.
---

# Transformers.js for ModelScope Workflows

Use this skill when users need browser or Node.js inference and want to source model artifacts from ModelScope repositories.

## Operating Mode

- Prefer a minimal runnable JS or TS project over framework-heavy scaffolding.
- Download model assets explicitly so local paths are deterministic.
- Reuse the existing frontend or Node project structure when present.
- Keep install, run, and asset-loading steps visible to the user and to downstream agents.

## Important Note

Transformers.js is distributed as the npm package `@huggingface/transformers`. The package name is upstream-defined and must remain unchanged.

## Standard Workflow

1. Decide whether the project should run in Node.js, the browser, or both.
2. Download the required model files from ModelScope.
3. Load tokenizer and model from a local path.
4. Add a minimal example input/output flow.
5. Leave concise install and run instructions.

## Install

```bash
npm install @huggingface/transformers
```

## Local Model Loading Example

```ts
import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline('text-classification', './models/qwen-local');
const out = await classifier('ModelScope integration with Transformers.js');
console.log(out);
```

## Model Preparation

Use `modelscope download` first:

```bash
modelscope download --model your-org/your-model --local_dir ./models/qwen-local
```

## AI Execution Contract

When using this skill, the agent should:

1. Infer the smallest useful JS or TS runtime shape for the task.
2. Keep asset paths explicit and local.
3. Add lightweight validation and error handling.
4. Keep the project runnable without requiring hidden manual steps.

## Guardrails

- Prefer local model paths for deterministic deployments.
- Pin package versions in production code.
- Cache model artifacts between runs when possible.
