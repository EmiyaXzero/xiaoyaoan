"""食物-药物冲突查询."""

from __future__ import annotations

from medsafe_core.db import get_connection
from medsafe_core.llm_client import BASE_SYSTEM_PROMPT, call_llm
from medsafe_core.models import InteractionResult, EvidenceItem
from medsafe_core.normalizer import normalize_drug_name


_FOOD_DRUG_SYSTEM_PROMPT = (
    BASE_SYSTEM_PROMPT
    + "\n任务：判断用户给出的药品与食物/饮品之间是否存在已知冲突。"
    "如有冲突，说明机制、风险和注意事项；如没有明确冲突，回答'未检索到明确冲突'。"
    "不要给出停药、换药或剂量调整建议。"
)


def _llm_food_drug_evidence(drug: str, food: str) -> list[EvidenceItem]:
    """本地未命中时，调用 LLM 评估食物-药物冲突."""
    user_prompt = (
        f"药品：{drug}\n"
        f"食物/饮品：{food}\n\n"
        "请判断二者是否存在已知冲突，并给出简要说明。"
    )
    content = call_llm(_FOOD_DRUG_SYSTEM_PROMPT, user_prompt, temperature=0.3, max_tokens=512)
    if not content or "未检索到明确冲突" in content:
        return []

    return [
        EvidenceItem(
            type="food_drug",
            drug_a=drug,
            food=food,
            severity="中",
            mechanism=content,
            advice="该结果由大模型基于公开资料生成，仅供参考，具体用药请咨询医生或药师。",
            source="LLM 辅助检索",
        )
    ]


def check_food_drug_interaction(drug: str, food: str) -> InteractionResult:
    """查询特定药品与食物/饮品之间的冲突."""
    canonical = normalize_drug_name(drug)
    if canonical is None:
        return InteractionResult(
            risk_level="无",
            summary=f"未找到药品「{drug}」，请检查名称。",
            not_found=[drug],
        )

    food_input = food.strip()
    if not food_input:
        return InteractionResult(
            risk_level="无",
            summary="请输入食物或饮品名称。",
        )

    evidence: list[EvidenceItem] = []
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM drugs WHERE name_cn = ?", (canonical,)
        ).fetchone()
        if row is None:
            return InteractionResult(
                risk_level="无",
                summary=f"未找到药品「{drug}」的详细记录。",
                not_found=[drug],
            )
        drug_id = row["id"]
        rows = conn.execute(
            """
            SELECT d.name_cn AS drug_a, f.food, f.effect, f.advice, f.source
            FROM food_drug_pairs f
            JOIN drugs d ON f.drug_id = d.id
            WHERE f.drug_id = ?
            """,
            (drug_id,),
        ).fetchall()

        for r in rows:
            # 简单匹配：食物名包含或等于输入
            if food_input.lower() in r["food"].lower() or r["food"].lower() in food_input.lower():
                evidence.append(
                    EvidenceItem(
                        type="food_drug",
                        drug_a=r["drug_a"],
                        food=r["food"],
                        severity="中",
                        mechanism=r["effect"] or "",
                        advice=r["advice"] or "",
                        source=r["source"] or "",
                    )
                )

    # 本地未命中时，尝试 LLM 辅助检索
    if not evidence:
        evidence.extend(_llm_food_drug_evidence(canonical, food_input))

    if evidence:
        summary = f"{canonical} 与 {food_input} 存在 {len(evidence)} 条冲突提示。"
        risk_level = max((e.severity for e in evidence), key=lambda s: ["无", "低", "中", "高", "禁忌"].index(s))
    else:
        summary = f"未检索到 {canonical} 与 {food_input} 的已知冲突，但仍建议遵医嘱。"
        risk_level = "无"

    return InteractionResult(
        risk_level=risk_level,
        summary=summary,
        evidence=evidence,
    )
