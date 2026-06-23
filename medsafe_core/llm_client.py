"""共享 LLM 调用客户端."""

from __future__ import annotations

import logging
import os
from typing import Any


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.INFO)
    _handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(_handler)


BASE_SYSTEM_PROMPT = (
    "你是一位用药安全科普助手。所有输出仅用于用药安全科普，"
    "不构成诊断、处方、剂量调整、停药或换药建议。"
    "不要承诺疗效，不要使用'治愈''根治'等绝对化表述。"
    "回答需客观、简洁，并提示具体用药请咨询医生或药师。"
)


def _get_api_key() -> str | None:
    return (
        os.environ.get("MODELSCOPE_ACCESS_TOKEN")
        or os.environ.get("DASHSCOPE_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
    )


def call_llm(system_prompt: str, user_prompt: str, **kwargs: Any) -> str | None:
    """调用 LLM，返回文本内容；未配置 Key 或调用失败时返回 None."""
    api_key = _get_api_key()
    if not api_key:
        logger.info("未配置 LLM API Key，跳过 LLM 调用")
        return None

    try:
        from openai import OpenAI
    except ImportError:
        logger.warning("未安装 openai SDK，无法调用 LLM")
        return None

    model = os.environ.get("MEDSAFE_LLM_MODEL", "stepfun-ai/Step-3.7-Flash")
    base_url = os.environ.get(
        "MEDSAFE_LLM_BASE_URL", "https://api-inference.modelscope.cn/v1/"
    )

    logger.info(f"正在调用 LLM：model={model}")
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=kwargs.get("temperature", 0.5),
            max_tokens=kwargs.get("max_tokens", 1024),
        )
        content = response.choices[0].message.content
        logger.info("LLM 调用成功")
        return content
    except Exception as exc:
        logger.warning(f"LLM 调用失败：{exc}")
        return None
