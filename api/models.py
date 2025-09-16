from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel

# —— 枚举 ——
class LanguageEnum(str, Enum):
    zh = "zh"
    en = "en"
    es = "es"

class StyleEnum(str, Enum):
    persuasive = "persuasive"
    educational = "educational"
    casual = "casual"
    authoritative = "authoritative"

# —— 生成请求/响应 ——
class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 2500
    language: LanguageEnum
    style: StyleEnum
    temperature: float = 0.5
    top_p: float = 0.85
    stop_sequences: List[str] = []

class GenerationResponse(BaseModel):
    generated_text: str
    tokens_used: int
    model_name: str
    lora_adapter: Optional[str] = None

# —— vLLM 配置（与 configs/vllm.yaml 对应） ——
class VLLMConfig(BaseModel):
    model_name: str = "LLM-Research/Meta-Llama-3-8B-Instruct"
    tensor_parallel_size: int = 1
    gpu_memory_utilization: float = 0.8
    max_model_len: int = 32768
    enable_lora: bool = True
    max_lora_rank: int = 64

    trust_remote_code: Optional[bool] = None
    dtype: Optional[str] = None
    quantization: Optional[Any] = None
    seed: Optional[int] = None
    # …需要时再逐步补充

# —— 预留的扩展配置（先保留，暂不在主流程使用） ——
class DecodingConfig(BaseModel):
    guided_decoding_backend: Optional[str] = None

class ObservabilityConfig(BaseModel):
    otlp_traces_endpoint: Optional[str] = None
    collect_model_forward_time: Optional[bool] = None
    collect_model_execute_time: Optional[bool] = None

class ModelConfig(BaseModel):
    model: str
    tokenizer: Optional[str] = None
    tokenizer_mode: Optional[str] = None
    revision: Optional[str] = None
    code_revision: Optional[str] = None
    rope_scaling: Optional[Any] = None
    rope_theta: Optional[Any] = None
    tokenizer_revision: Optional[str] = None
    max_model_len: Optional[int] = None
    quantization: Optional[Any] = None
    quantization_param_path: Optional[str] = None
    enforce_eager: Optional[bool] = None
    max_context_len_to_capture: Optional[int] = None
    max_seq_len_to_capture: Optional[int] = None
    max_logprobs: Optional[int] = None
    disable_sliding_window: Optional[bool] = None
    skip_tokenizer_init: Optional[bool] = None
    served_model_name: Optional[str] = None
    multimodal_config: Optional[Dict[str, Any]] = None
    limit_mm_per_prompt: Optional[int] = None
    use_async_output_proc: Optional[bool] = None
    mm_processor_kwargs: Optional[Dict[str, Any]] = None
    override_neuron_config: Optional[Dict[str, Any]] = None
    config_format: Optional[str] = None
    hf_overrides: Optional[Dict[str, Any]] = None
