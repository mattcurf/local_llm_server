import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1" 

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

# GLM
snapshot_download(
    repo_id = "unsloth/GLM-4-32B-0414-GGUF",
    local_dir = "unsloth/GLM-4-32B-0414-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/GLM-4.5-Air-GGUF",
    local_dir = "unsloth/GLM-4.5-Air-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/GLM-4.5-GGUF",
    local_dir = "unsloth/GLM-4.5-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

# GPT-oss
snapshot_download(
    repo_id = "unsloth/gpt-oss-20b-GGUF",
    local_dir = "unsloth/gpt-oss-20b-GGUF",
    allow_patterns = ["*Q8_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/gpt-oss-120b-GGUF",
    local_dir = "unsloth/gpt-oss-120b-GGUF",
    allow_patterns = ["*Q8_K_XL*"],
)

# DeepSeek-V3.1
snapshot_download(
    repo_id = "unsloth/DeepSeek-V3.1-GGUF",
    local_dir = "unsloth/DeepSeek-V3.1-GGUF",
    allow_patterns = ["*UD-TQ1_0*"], 
)

snapshot_download(
    repo_id = "unsloth/DeepSeek-V3.1-GGUF",
    local_dir = "unsloth/DeepSeek-V3.1-GGUF",
    allow_patterns = ["*UD-Q2_K_XL*"],
)

snapshot_download(
    repo_id = "unsloth/grok-2-GGUF",
    local_dir = "unsloth/grok-2-GGUF",
    allow_patterns = ["*Q4_K_XL*"],
)

