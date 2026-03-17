---
name: transformers-js
description: Build JavaScript/TypeScript inference workflows with Transformers.js, using ModelScope-hosted assets through local downloads.
---

# Transformers.js for ModelScope Workflows

Use this skill when users need browser or Node.js inference and want to source model artifacts from ModelScope repositories.

## Important Note

Transformers.js is distributed as the npm package `@huggingface/transformers`. The package name is upstream-defined and must remain unchanged.

## Workflow

1. Download model files from ModelScope to local directory.
2. Load model/tokenizer from local path in Transformers.js.
3. Run inference in Node.js or browser.

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

Use `modelscope download` to collect assets first:

```bash
modelscope download --model your-org/your-model --local_dir ./models/qwen-local
```

## Guardrails

- Prefer local model paths for deterministic deployments.
- Pin package version in production apps.
- Cache model artifacts between runs.
