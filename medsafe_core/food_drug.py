"""食物-药物冲突查询."""

from __future__ import annotations

from medsafe_core.db import get_connection
from medsafe_core.models import InteractionResult, EvidenceItem
from medsafe_core.normalizer import normalize_drug_name


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

    if evidence:
        summary = f"{canonical} 与 {food_input} 存在 {len(evidence)} 条已知冲突提示。"
        risk_level = max((e.severity for e in evidence), key=lambda s: ["无", "低", "中", "高", "禁忌"].index(s))
    else:
        summary = f"未检索到 {canonical} 与 {food_input} 的已知冲突，但仍建议遵医嘱。"
        risk_level = "无"

    return InteractionResult(
        risk_level=risk_level,
        summary=summary,
        evidence=evidence,
    )
