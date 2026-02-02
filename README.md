# local_llm_server

A local LLM server using vLLM with Open WebUI interface. Run Qwen3-Coder-30B locally on your workstation!

## Hardware Configuration 
* Intel/AMD system with at least 24 cores
* 64 GB DDR5
* NVIDIA 5090 w/ 32GB VRAM

## Prerequisites 

* NVIDIA GPU drivers installed
* Docker with NVIDIA Container Toolkit

## Setup and Execution

1. Set your OpenRouter API key (for cloud model fallback):
```bash
export OPENROUTER_API_KEY=your-key-here
```

2. Run the server:
```bash
docker compose up -d
```

Models are downloaded automatically from HuggingFace on first run and cached in `./models/`.

3. Connect to Open WebUI at http://localhost:3000

The vLLM OpenAI-compatible API is available at http://localhost:8080/v1

## Claude Code CLI Configuration

To use Claude Code CLI with the local claude-code-router:

```bash
export ANTHROPIC_BASE_URL=http://localhost:3456
export ANTHROPIC_API_KEY=your-secret-key-here
```

Replace `localhost` with your server's IP for remote access.

## References
* https://docs.vllm.ai
* https://openwebui.com
* https://docs.unsloth.ai/basics/qwen3-coder-how-to-run-locally
