from huggingface_hub import snapshot_download

# 指定模型 ID（示例：Meta LLaMA 3 8B Instruct）
model_id = "LLM-Research/Meta-Llama-3-8B-Instruct"

# 下载到项目的 model/ 目录
snapshot_download(
    repo_id=model_id,
    local_dir="./model/LLM-Research/Meta-Llama-3-8B-Instruct",
    local_dir_use_symlinks=False
)

print("模型下载到 ./model/LLM-Research/Meta-Llama-3-8B-Instruct")
