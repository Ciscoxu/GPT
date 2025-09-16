# GPT vLLM Service

## 简介
这是一个基于 **FastAPI + vLLM** 的推理服务，支持加载本地大语言模型（如 LLaMA 3），并通过 REST API 提供以下功能：

- 通用对话（Chat）
- 商品推广文案（Product）
- 门店推广文案（Store）
- 短视频脚本（Video Script）

支持多语言（中文、英文、西班牙语）和多种风格（说服型、教育型、休闲型、权威型）。

---

## 项目结构
```
GPT/
├── api/
│   ├── main.py              # FastAPI 启动入口
│   ├── models.py            # Pydantic 数据模型
│   └── service/
│       ├── client.py        # vLLMService 封装
│       ├── prompts.py       # Prompt 模板
│       ├── router.py        # API 路由
│       └── deps.py          # 依赖注入
├── clients/
│   └── python/
│       ├── chatagent.py     # 交互式对话客户端
│       └── gen_once.py      # 一次性调用客户端
├── configs/
│   └── vllm.yaml            # vLLM 配置文件
├── requirements.txt
└── README.md
```

---

## 安装依赖
```bash
pip install -r requirements.txt
```

### requirements.txt
```txt
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pyyaml>=6.0
requests>=2.31.0
vllm>=0.4.2
```

---

## 配置
配置文件路径：`configs/vllm.yaml`  

下载模型：
```bash
huggingface-cli login
python download_model.py
```

示例：
```yaml
model_name: ./model/LLM-Research/Meta-Llama-3-8B-Instruct
tensor_parallel_size: 1
gpu_memory_utilization: 0.9
max_model_len: 8192
enable_lora: true
max_lora_rank: 64
trust_remote_code: true
```

### 配置路径指定
程序会优先读取环境变量：
```bash
export VLLM_CONFIG_PATH= ../GPT/configs/vllm.yaml
```
若未设置，则默认使用 `configs/vllm.yaml`。

---

## 启动服务
在项目根目录运行：
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

访问：
- 健康检查: [http://localhost:8000/healthz](http://localhost:8000/healthz)  
- API 文档: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API 调用示例

### 通用生成
```bash
curl -X POST http://localhost:8000/v1/generate   -H "Content-Type: application/json"   -d '{
    "prompt": "介绍一下凤梨酥礼盒。",
    "language": "zh",
    "style": "persuasive",
    "max_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.9,
    "stop_sequences": []
  }'
```

### 商品推广文案
```bash
curl -X POST http://localhost:8000/v1/generate/product   -H "Content-Type: application/json"   -d '{"prompt":"新品奶茶联名礼盒","language":"zh","style":"casual","max_tokens":150,"temperature":0.7,"top_p":0.9,"stop_sequences":[]}'
```

---

## 💻 客户端脚本

### 1. 交互式对话
```bash
python clients/python/chatagent.py --lang zh --style persuasive --type chat
```
输入 `/exit` 可退出。

### 2. 一次性生成
直接输入文本：
```bash
python clients/python/gen_once.py --type product --lang zh --style authoritative   --text "这是一家主营台湾凤梨酥的店铺，推出了联名奶茶礼盒。"
```
或

```bash
python clients/python/gen_once.py --type product --lang en --style authoritative --text "This is a Taiwanese pastry shop specializing in pineapple cakes, now launching a co-branded bubble tea gift box."
```
或

```bash
python clients/python/gen_once.py --type product --lang es --style authoritative --text "Esta es una pastelería taiwanesa especializada en pasteles de piña, que ahora lanza una caja de regalo en colaboración con té de burbujas."
```


从文件读取：
```bash
python clients/python/gen_once.py --type video --lang zh --style casual   --infile ./samples/topic.txt   --outfile ./out/video.txt
```

## 📜 License
MIT License
