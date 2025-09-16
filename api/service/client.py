# service/client.py
import os
import json
from typing import Optional, List
import yaml
from fastapi import HTTPException
from vllm import LLM, SamplingParams

from api.models import (
    VLLMConfig,
    GenerationRequest,
    GenerationResponse,
)

from .prompts import build_prompt

DEFAULT_CONFIG_PATH = os.getenv("VLLM_CONFIG_PATH", "configs/vllm.yaml")

class VLLMService:
    """封装 vLLM 的本地嵌入式推理客户端。"""

    def __init__(self, config_path: Optional[str] = None):
        self.llm: Optional[LLM] = None
        self.config: Optional[VLLMConfig] = None
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._load_config()
        self._init_model()

    # ---------------- internal ---------------- #
    def _load_config(self):
        if not os.path.exists(self.config_path):
            # fallback to defaults
            self.config = VLLMConfig()
            print(f"[vLLM] Config not found at {self.config_path}, using defaults: {self.config}")
            return

        try:
            if self.config_path.endswith((".yaml", ".yml")):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            else:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            self.config = VLLMConfig(**data)
            print(f"[vLLM] Loaded config from {self.config_path}: {self.config}")
        except Exception as e:
            raise RuntimeError(f"Failed to load config {self.config_path}: {e}")

    def _init_model(self):
        assert self.config is not None, "Config must be loaded before model init."
        try:
            self.llm = LLM(
                model=self.config.model_name,
                tensor_parallel_size=self.config.tensor_parallel_size,
                gpu_memory_utilization=self.config.gpu_memory_utilization,
                max_model_len=self.config.max_model_len,
                trust_remote_code=self.config.trust_remote_code,
            )
            print(f"[vLLM] Initialized model: {self.config.model_name}")
        except Exception as e:
            print(f"[vLLM] Init failed: {e}")
            raise

    # ---------------- API surface ---------------- #
    async def generate(self, request: GenerationRequest, content_type: str = "chat") -> GenerationResponse:
        if self.llm is None:
            raise HTTPException(status_code=500, detail="Model is not initialized.")

        try:
            formatted_prompt = build_prompt(request, content_type)

            tokenizer = self.llm.get_tokenizer()
            sys_msg = {
                "zh": "你是一个专业的中文内容创作者。无论用户输入什么语言，都必须使用简体中文回答。",
                "en": "You are a helpful assistant specialized in short-form scripts, must use english to respond.",
                "es": "Eres un asistente experto en escribir guiones cortos y efectivos, debes usar español para responder.",
            }.get(request.language.value, "You are a helpful assistant.")

            messages = [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": formatted_prompt},
            ]
            templated_prompt = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )

            # collect stop ids
            stop_token_ids: List[int] = []
            try:
                eot_id = tokenizer.convert_tokens_to_ids("<|eot_id|>")
                if isinstance(eot_id, int) and eot_id >= 0:
                    stop_token_ids.append(eot_id)
            except Exception:
                pass
            if getattr(tokenizer, "eos_token_id", None) is not None:
                stop_token_ids.append(tokenizer.eos_token_id)

            sampling_params = SamplingParams(
                temperature=request.temperature,
                top_p=request.top_p,
                max_tokens=request.max_tokens,
                stop_token_ids=stop_token_ids or None,
                repetition_penalty=1.2,
            )

            outputs = self.llm.generate([templated_prompt], sampling_params)
            if not outputs:
                raise RuntimeError("No output generated")

            output = outputs[0]
            text = output.outputs[0].text if output.outputs else ""
            tokens_used = len(output.outputs[0].token_ids) if output.outputs else 0

            return GenerationResponse(
                generated_text=text.strip(),
                tokens_used=tokens_used,
                model_name=self.config.model_name if self.config else "unknown",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Content generation failed: {e}")
