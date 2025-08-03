import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" 

from huggingface_hub import snapshot_download

snapshot_download(
    repo_id = "unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF",
    local_dir = "unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/Qwen3-30B-A3B-Thinking-2507-GGUF",
    local_dir = "unsloth/Qwen3-30B-A3B-Thinking-2507-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/Qwen3-235B-A22B-Thinking-2507-GGUF",
    local_dir = "unsloth/Qwen3-235B-A22B-Thinking-2507-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/Qwen3-235B-A22B-Instruct-2507-GGUF",
    local_dir = "unsloth/Qwen3-235B-A22B-Instruct-2507-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF",
    local_dir = "unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/Qwen3-Coder-480B-A35B-Instruct-GGUF",
    local_dir = "unsloth/Qwen3-Coder-480B-A35B-Instruct-GGUF",
    allow_patterns = ["*UD-Q2_K_XL*"],
)

