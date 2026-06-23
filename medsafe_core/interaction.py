"""药物相互作用（DDI）查询."""

from __future__ import annotations

from itertools import combinations

from medsafe_core.db import get_connection
from medsafe_core.models import InteractionResult, EvidenceItem, aggregate_severity
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


def check_drug_interactions(drugs: list[str]) -> InteractionResult:
    """查询多种药物之间的相互作用."""
    if not drugs or len(drugs) < 2:
        return InteractionResult(
            risk_level="无",
            summary="请至少提供两种药品进行相互作用查询。",
        )

    normalized: dict[str, str | None] = {}
    for d in drugs:
        normalized[d] = normalize_drug_name(d)

    not_found = [orig for orig, canon in normalized.items() if canon is None]
    canonicals = [canon for canon in normalized.values() if canon is not None]

    if not canonicals:
        return InteractionResult(
            risk_level="无",
            summary="未识别到任何已知药品，请检查药品名称。",
            not_found=not_found,
        )

    evidence: list[EvidenceItem] = []
    with get_connection() as conn:
        ids = {name: _get_drug_id(conn, name) for name in canonicals}
        for a, b in combinations(canonicals, 2):
            a_id, b_id = ids.get(a), ids.get(b)
            if a_id is None or b_id is None:
                continue
            evidence.extend(_query_ddi(conn, a_id, b_id))

    if evidence:
        risk_level = aggregate_severity([e.severity for e in evidence])
        summary = f"在 {len(canonicals)} 种药品中识别到 {len(evidence)} 条相互作用，最高风险等级为「{risk_level}」。"
    else:
        risk_level = "无"
        summary = f"在 {len(canonicals)} 种药品中未检索到已知的相互作用，但用药仍需遵医嘱。"

    return InteractionResult(
        risk_level=risk_level,
        summary=summary,
        evidence=evidence,
        not_found=not_found,
    )
