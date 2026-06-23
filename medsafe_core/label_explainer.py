"""药品说明书大白话解读."""

from __future__ import annotations

import os

from medsafe_core.db import get_connection
from medsafe_core.models import ExplanationResult
from medsafe_core.normalizer import normalize_drug_name

DEFAULT_SECTIONS = ["适应症", "用法用量", "常见不良反应", "禁忌", "注意事项"]


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


def explain_drug_label(drug: str, section: str | None = None) -> ExplanationResult:
    """将药品说明书专业文本解读为通俗语言."""
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

    # 3. 如配置了 LLM API Key，可进一步润色（可选增强）
    api_key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if api_key and selected_section in label_data:
        # 保留扩展点：未来可调用 LLM 对 content 进行大白话润色
        pass

    return ExplanationResult(
        drug=canonical,
        section=selected_section,
        content=content,
    )
