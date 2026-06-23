"""药品说明书大白话解读."""

from __future__ import annotations

import logging

from medsafe_core.db import get_connection
from medsafe_core.llm_client import BASE_SYSTEM_PROMPT, call_llm
from medsafe_core.models import ExplanationResult
from medsafe_core.normalizer import normalize_drug_name


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.INFO)
    _handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(_handler)

DEFAULT_SECTIONS = ["适应症", "用法用量", "常见不良反应", "禁忌", "注意事项"]

_LABEL_SYSTEM_PROMPT = (
    BASE_SYSTEM_PROMPT
    + "\n任务：把药品说明书的专业段落改写成通俗易懂的大白话，让患者和家属能看懂。"
    "要求：\n"
    "1. 只解释原文内容，不补充原文没有的信息；\n"
    "2. 结尾必须提示'具体用药请遵医嘱'。"
)


def _generate_plain_explanation(drug: str, section: str, raw: str) -> str:
    """基于模板将说明书段落转为大白话."""
    templates = {
        "适应症": f"「{drug}」主要用于治疗或预防以下情况：{raw}",
        "用法用量": f"「{drug}」一般这样吃：{raw} 请记住，剂量因人而异，必须按医生或药师的建议服用。",
        "常见不良反应": f"吃「{drug}」后，部分人可能会出现：{raw} 如果症状严重或持续，请及时就医。",
        "禁忌": f"以下人群不适合使用「{drug}」：{raw}",
        "注意事项": f"服用「{drug}」时需要注意：{raw}",
    }
    return templates.get(section, f"关于「{drug}」的{section}：{raw}")


def _rewrite_with_llm(drug: str, section: str, raw: str) -> str | None:
    """使用 LLM 润色说明书内容，失败时返回 None."""
    logger.info(f"正在调用 LLM 润色说明书：drug={drug}, section={section}")
    return call_llm(
        _LABEL_SYSTEM_PROMPT,
        f"药品：{drug}\n章节：{section}\n原文：{raw}",
        temperature=0.5,
        max_tokens=1024,
    )


def explain_drug_label(drug: str, section: str | None = None) -> ExplanationResult:
    """将药品说明书专业文本解读为通俗语言."""
    logger.info(f"收到说明书解读请求：drug={drug}, section={section}")
    canonical = normalize_drug_name(drug)
    if canonical is None:
        return ExplanationResult(
            drug=drug,
            section=section or "",
            content=f"未找到药品「{drug}」，请检查名称。",
            not_found=True,
        )

    selected_section = section or "适应症"

    # 1. 尝试从内置样本数据获取
    from medsafe_core.data.sample_data import DRUG_LABELS

    label_data = DRUG_LABELS.get(canonical, {})
    raw = label_data.get(selected_section)

    # 2. 样本数据没有时，尝试从数据库获取（未来可接入 RAG/LLM）
    if raw is None:
        with get_connection() as conn:
            # 目前数据库无说明书全文表，预留扩展
            row = conn.execute(
                "SELECT name_cn, category FROM drugs WHERE name_cn = ?", (canonical,)
            ).fetchone()
            if row is None:
                return ExplanationResult(
                    drug=canonical,
                    section=selected_section,
                    content=f"暂无「{canonical}」的说明书信息。",
                    not_found=True,
                )
            raw = f"暂无该药品「{selected_section}」的详细说明书内容。该药品属于「{row['category']}」。"

    content = _generate_plain_explanation(canonical, selected_section, raw)

    # 3. 如配置了 LLM API Key 且样本数据命中，则调用 LLM 进一步润色
    if selected_section in label_data:
        llm_content = _rewrite_with_llm(canonical, selected_section, raw)
        if llm_content:
            content = llm_content

    return ExplanationResult(
        drug=canonical,
        section=selected_section,
        content=content,
    )
