#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式聊天客户端：
- 默认调用 /v1/generate （content_type="chat"）
- 支持 --type=chat|product|store|video 切换端点
- 支持将多轮历史拼接进 prompt（简单合并）
- 可配置语言/风格/温度等
"""
import os
import sys
import argparse
import requests
from typing import List, Dict

DEFAULT_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ENDPOINTS = {
    "chat": "/v1/generate",
    "product": "/v1/generate/product",
    "store": "/v1/generate/store",
    "video": "/v1/generate/video",
}

def build_prompt_with_history(history: List[Dict[str, str]], user_input: str, max_turns: int = 6) -> str:
    """
    非严格 chat 格式，仅把最近若干轮拼接成人类可读的上下文。
    你的服务端会再用 tokenizer.apply_chat_template 包装。
    """
    recent = history[-max_turns:]
    lines = []
    for h in recent:
        role = "你" if h["role"] == "user" else "助理"
        lines.append(f"{role}: {h['content']}")
    lines.append(f"你: {user_input}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API 基地址，如 http://localhost:8000")
    ap.add_argument("--type", default="chat", choices=list(ENDPOINTS.keys()), help="生成类型（选择不同端点）")
    ap.add_argument("--lang", default="zh", choices=["zh", "en", "es"], help="输出语言")
    ap.add_argument("--style", default="casual", choices=["persuasive","educational","casual","authoritative"], help="风格")
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=0.9)
    ap.add_argument("--no-history", action="store_true", help="不拼接对话历史")
    ap.add_argument("--timeout", type=int, default=120, help="HTTP 超时秒数")
    args = ap.parse_args()

    url = args.base_url.rstrip("/") + ENDPOINTS[args.type]
    print(f"[chatagent] endpoint => {url}\n输入你的内容，输入 /exit 退出。\n")

    history: List[Dict[str, str]] = []

    while True:
        try:
            user_in = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_in:
            continue
        if user_in.lower() in ("/exit", "/quit"):
            break

        if args.no_history:
            prompt = user_in
        else:
            prompt = build_prompt_with_history(history, user_in)

        payload = {
            "prompt": prompt,
            "language": args.lang,
            "style": args.style,
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "stop_sequences": []
        }

        try:
            resp = requests.post(url, json=payload, timeout=args.timeout)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[错误] 请求失败：{e}")
            continue

        text = data.get("generated_text", "").strip()
        print(f"\n助理> {text}\n")

        # 记录历史
        history.append({"role": "user", "content": user_in})
        history.append({"role": "assistant", "content": text})

    print("已退出。")

if __name__ == "__main__":
    main()
