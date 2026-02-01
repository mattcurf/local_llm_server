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

1. Run the server:
```bash
docker compose up -d
```

Models are downloaded automatically from HuggingFace on first run and cached in `./models/`.

2. Connect to Open WebUI at http://localhost:3000

The vLLM OpenAI-compatible API is available at http://localhost:8080/v1

## References
* https://docs.vllm.ai
* https://openwebui.com
* https://docs.unsloth.ai/basics/qwen3-coder-how-to-run-locally
