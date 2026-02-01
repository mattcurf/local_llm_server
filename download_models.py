import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1" 

from huggingface_hub import snapshot_download

snapshot_download(
    repo_id = "unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF",
    local_dir = "unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

