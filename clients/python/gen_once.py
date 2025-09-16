#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一次性生成脚本：
- 支持从 --text 或 --infile 读取输入
- --type=chat|product|store|video 选择端点
- 可将结果保存到 --outfile
"""
import os
import sys
import argparse
import requests

DEFAULT_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ENDPOINTS = {
    "chat": "/v1/generate",
    "product": "/v1/generate/product",
    "store": "/v1/generate/store",
    "video": "/v1/generate/video",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--type", default="chat", choices=list(ENDPOINTS.keys()))
    ap.add_argument("--lang", default="zh", choices=["zh", "en", "es"])
    ap.add_argument("--style", default="casual", choices=["persuasive","educational","casual","authoritative"])
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=0.9)

    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="直接提供文本")
    g.add_argument("--infile", help="从文件读取文本")

    ap.add_argument("--outfile", help="把结果写入文件")
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()

    if args.infile:
        with open(args.infile, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = args.text

    payload = {
        "prompt": content,
        "language": args.lang,
        "style": args.style,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "stop_sequences": []
    }

    url = args.base_url.rstrip("/") + ENDPOINTS[args.type]
    try:
        r = requests.post(url, json=payload, timeout=args.timeout)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[错误] 请求失败：{e}", file=sys.stderr)
        sys.exit(2)

    text = data.get("generated_text", "").strip()
    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[gen_once] 已写入 {args.outfile}")
    else:
        print(text)

if __name__ == "__main__":
    main()
