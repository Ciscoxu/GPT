# api/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 路由
from api.service.router import router as vllm_router

app = FastAPI(title="vLLM Content API", version="1.0.0")

# ——— CORS（前端本地或线上可访问）———
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ——— 挂载路由 ———
app.include_router(vllm_router)

# ——— 健康检查 ———
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"service": "vLLM API", "docs": "/docs"}
