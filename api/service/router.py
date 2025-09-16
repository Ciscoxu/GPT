# service/router.py
from fastapi import APIRouter
from api.models import GenerationRequest, GenerationResponse
from .client import VLLMService

router = APIRouter(prefix="/v1", tags=["vllm"])
_service = VLLMService()  # 简单的单例；若要懒加载可改成依赖注入

@router.post("/generate", response_model=GenerationResponse)
async def generate_generic(req: GenerationRequest) -> GenerationResponse:
    """默认对话/通用生成。"""
    return await _service.generate(req, content_type="chat")

@router.post("/generate/product", response_model=GenerationResponse)
async def generate_product(req: GenerationRequest) -> GenerationResponse:
    return await _service.generate(req, content_type="product")

@router.post("/generate/store", response_model=GenerationResponse)
async def generate_store(req: GenerationRequest) -> GenerationResponse:
    return await _service.generate(req, content_type="store")

@router.post("/generate/video", response_model=GenerationResponse)
async def generate_video(req: GenerationRequest) -> GenerationResponse:
    return await _service.generate(req, content_type="video_script")
