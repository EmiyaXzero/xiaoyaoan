"""老年人用药清单批量风险筛查."""

from __future__ import annotations

from itertools import combinations

from medsafe_core.db import get_connection
from medsafe_core.models import ScreeningResult, EvidenceItem, aggregate_severity
from medsafe_core.normalizer import normalize_drug_name


def _get_drug_id(conn, name: str) -> int | None:
    row = conn.execute("SELECT id FROM drugs WHERE name_cn = ?", (name,)).fetchone()
    return row["id"] if row else None


def _query_ddi(conn, a_id: int, b_id: int) -> list[EvidenceItem]:
    rows = conn.execute(
        """
        SELECT d1.name_cn AS drug_a, d2.name_cn AS drug_b,
               p.severity, p.mechanism, p.advice, p.source
        FROM ddi_pairs p
        JOIN drugs d1 ON p.drug_a_id = d1.id
        JOIN drugs d2 ON p.drug_b_id = d2.id
        WHERE p.drug_a_id = ? AND p.drug_b_id = ?
        """,
        (a_id, b_id),
    ).fetchall()
    return [
        EvidenceItem(
            type="ddi",
            drug_a=row["drug_a"],
            drug_b=row["drug_b"],
            severity=row["severity"],
            mechanism=row["mechanism"] or "",
            advice=row["advice"] or "",
            source=row["source"] or "",
        )
        for row in rows
    ]


def _query_elderly_risks(conn, drug_id: int) -> list[EvidenceItem]:
    rows = conn.execute(
        """
        SELECT d.name_cn AS drug_a, r.risk_type, r.reason, r.recommendation, r.source
        FROM elderly_risk_rules r
        JOIN drugs d ON r.drug_id = d.id
        WHERE r.drug_id = ?
        """,
        (drug_id,),
    ).fetchall()
    return [
        EvidenceItem(
            type="elderly_risk",
            drug_a=row["drug_a"],
            severity="高",
            mechanism=row["risk_type"] or "",
            advice=f"{row['reason']}；建议：{row['recommendation']}",
            source=row["source"] or "",
        )
        for row in rows
    ]


def screen_elderly_medications(meds: list[str]) -> ScreeningResult:
    """对老年人用药清单进行批量风险筛查."""
    if not meds:
        return ScreeningResult(
            risk_level="无",
            summary="用药清单为空，请输入至少一种药品。",
        )

    normalized: dict[str, str | None] = {}
    for m in meds:
        normalized[m] = normalize_drug_name(m)

    not_found = [orig for orig, canon in normalized.items() if canon is None]
    canonicals = [canon for canon in normalized.values() if canon is not None]

    if not canonicals:
        return ScreeningResult(
            risk_level="无",
            summary="未识别到任何已知药品，请检查药品名称。",
            not_found=not_found,
        )

    interactions: list[EvidenceItem] = []
    elderly_risks: list[EvidenceItem] = []

    with get_connection() as conn:
        ids = {name: _get_drug_id(conn, name) for name in canonicals}

        # 两两组合查询 DDI
        for a, b in combinations(canonicals, 2):
            a_id, b_id = ids.get(a), ids.get(b)
            if a_id is None or b_id is None:
                continue
            interactions.extend(_query_ddi(conn, a_id, b_id))

        # 单药老年风险
        for name in canonicals:
            drug_id = ids.get(name)
            if drug_id is None:
                continue
            elderly_risks.extend(_query_elderly_risks(conn, drug_id))

    all_severities = [e.severity for e in interactions + elderly_risks]
    risk_level = aggregate_severity(all_severities)

    if interactions or elderly_risks:
        summary = (
            f"在 {len(canonicals)} 种药品中，"
            f"发现 {len(interactions)} 条药物相互作用、"
            f"{len(elderly_risks)} 条老年用药风险提示，"
            f"综合风险等级为「{risk_level}」。建议携带清单咨询医生或药师。"
        )
    else:
        summary = (
            f"在 {len(canonicals)} 种药品中未检索到已知的相互作用或老年高风险提示，"
            f"但仍需遵医嘱定期评估用药方案。"
        )

    return ScreeningResult(
        risk_level=risk_level,
        summary=summary,
        interactions=interactions,
        elderly_risks=elderly_risks,
        not_found=not_found,
    )
