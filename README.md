# local_llm_server

An illustration how to setup a local LLM server with OpenWEB UI interface. Run 30B, 235B, and 480B parameter models locally on you workstation!

## Hardware Configuration 
* Intel/AMD system with at least 24 cores
* 256 GB DDR5
* NVIDIA 5090 w/ 32GB VRAM
* 1.5TB free storage space for models

## Prerequisites 

System setup with:
* kernel drivers for NVIDIA GPU
* docker with NVIDIA-Runtime support
* Python environment
 
## Steps for setup and execution

1. Download ~1.5TB of LLM models:
```bash
$ pip install -r requirements.txt
$ python ./download_models.py 
```

2. Run LLM server
```bash
$ docker compose up -d
```

3. Connect to web UI at http://localhost:3000 (a control panel for llama-swap will be at http://localhost:8080)

## References
* https://openwebui.com
* https://github.com/mostlygeek/llama-swap
* https://docs.unsloth.ai/basics/qwen3-coder-how-to-run-locally
* https://docs.unsloth.ai/basics/gpt-oss-how-to-run-and-fine-tune
* https://docs.unsloth.ai/models/grok-2
* https://chat.z.ai
