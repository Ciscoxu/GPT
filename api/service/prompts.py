# service/prompts.py
from typing import Dict
from api.models import GenerationRequest

# —— 风格提示 —— #
_STYLE_HINTS: Dict[str, Dict[str, str]] = {
    "zh": {
        "persuasive": "风格要求：内容要具有说服力，激发读者兴趣并引导他们采取行动。",
        "educational": "风格要求：内容要有条理、易于理解，具备教育意义。",
        "casual": "风格要求：语言自然、轻松、贴近生活，适合社交平台。",
        "authoritative": "风格要求：展现专业性和可信度，语气坚定且可靠。"
    },
    "en": {
        "persuasive": "Style: Persuasive. The content should be convincing, engaging, and motivate action.",
        "educational": "Style: Educational. The content should be informative, structured, and easy to understand.",
        "casual": "Style: Casual. The tone should be friendly, relaxed, and conversational.",
        "authoritative": "Style: Authoritative. The tone should reflect expertise, professionalism, and trust."
    },
    "es": {
        "persuasive": "Estilo: Persuasivo. El contenido debe ser convincente y motivar a la acción.",
        "educational": "Estilo: Educativo. El contenido debe ser claro y didáctico.",
        "casual": "Estilo: Informal. El tono debe ser amigable y relajado.",
        "authoritative": "Estilo: Autoritario. El tono debe reflejar autoridad y profesionalismo."
    },
}

_LANG_PREFIX = {
    "zh": "【输出要求】请使用简体中文回答。\n\n",
    "en": "【Output】Please respond in English.\n\n",
    "es": "【Salida】Por favor responde en español.\n\n",
}

# —— Prompt 模板 —— #
_PROMPT_TEMPLATES: Dict[str, Dict[str, str]] = {
    "product": {
        "zh": "{style_hint}\n请根据以下产品信息，撰写一段中文推广文案…\n【产品信息】\n{content}\n\n【推广文案】：",
        "en": "{style_hint}\nBased on the product information below…\n[Product Info]\n{content}\n\n[Promotional Copy]:",
        "es": "{style_hint}\nCon base en la siguiente información…\n[Información del producto]\n{content}\n\n[Texto promocional]:",
    },
    "store": {
        "zh": "{style_hint}\n请根据以下门店信息，撰写一段中文推广文案…\n【门店信息】\n{content}\n\n【推广文案】：",
        "en": "{style_hint}\nBased on the following store information…\n[Store Info]\n{content}\n\n[Promotional Copy]:",
        "es": "{style_hint}\nCon base en la siguiente información sobre la tienda…\n[Información de la tienda]\n{content}\n\n[Texto promocional]:",
    },
    "video_script": {
        "zh": "{style_hint}\n请你生成一段适合短视频平台的中文文案…\n【主题信息】\n{content}\n\n【脚本】：",
        "en": "{style_hint}\nWrite a compelling short video script…\n[Topic Info]\n{content}\n\n[Video Script]:",
        "es": "{style_hint}\nRedacta un guion atractivo…\n[Tema]\n{content}\n\n[Guion]:",
    },
    "chat": {
        "zh": "{style_hint}\n你是一个{style}风格的中文AI助手…\n{content}",
        "en": "{style_hint}\nYou are an AI assistant with a {style} style…\n{content}",
        "es": "{style_hint}\nEres un asistente de IA con un estilo {style}…\n{content}",
    },
}

def _style_hint(lang: str, style: str) -> str:
    return _STYLE_HINTS.get(lang, {}).get(style, "")

def build_prompt(request: GenerationRequest, content_type: str) -> str:
    """根据语言 & 内容类型拼接 prompt 字符串。"""
    lang = request.language.value
    style = request.style.value
    style_hint = _style_hint(lang, style)
    content = request.prompt

    if content_type not in _PROMPT_TEMPLATES:
        content_type = "chat"

    tmpl = _PROMPT_TEMPLATES[content_type].get(lang) or _PROMPT_TEMPLATES[content_type]["en"]
    lang_prefix = _LANG_PREFIX.get(lang, "")

    return lang_prefix + tmpl.format(content=content, style=style, style_hint=style_hint)
