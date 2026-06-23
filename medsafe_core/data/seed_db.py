"""将样本数据写入 SQLite 知识库."""

from __future__ import annotations

from medsafe_core.db import get_connection, init_db, reset_db
from medsafe_core.data.sample_data import (
    DRUGS,
    ALIASES,
    DDI_PAIRS,
    FOOD_DRUG_PAIRS,
    ELDERLY_RISK_RULES,
)


def seed_drugs(conn) -> dict[str, int]:
    """插入药品主表，返回 name_cn -> id 映射."""
    drug_ids: dict[str, int] = {}
    for drug in DRUGS:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO drugs (name_cn, name_en, atc_code, category)
            VALUES (?, ?, ?, ?)
            """,
            (drug["name_cn"], drug.get("name_en"), drug.get("atc_code"), drug.get("category")),
        )
        # 重新查询获取 id
        row = conn.execute(
            "SELECT id FROM drugs WHERE name_cn = ?", (drug["name_cn"],)
        ).fetchone()
        if row:
            drug_ids[drug["name_cn"]] = row["id"]
    return drug_ids


def seed_aliases(conn, drug_ids: dict[str, int]) -> None:
    for canonical, alias_list in ALIASES.items():
        drug_id = drug_ids.get(canonical)
        if drug_id is None:
            continue
        for alias in alias_list:
            conn.execute(
                "INSERT OR IGNORE INTO drug_aliases (drug_id, alias) VALUES (?, ?)",
                (drug_id, alias),
            )


def seed_ddi_pairs(conn, drug_ids: dict[str, int]) -> None:
    for pair in DDI_PAIRS:
        a_id = drug_ids.get(pair["drug_a"])
        b_id = drug_ids.get(pair["drug_b"])
        if a_id is None or b_id is None:
            continue
        conn.execute(
            """
            INSERT OR IGNORE INTO ddi_pairs
            (drug_a_id, drug_b_id, severity, mechanism, advice, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                a_id,
                b_id,
                pair["severity"],
                pair.get("mechanism", ""),
                pair.get("advice", ""),
                pair.get("source", ""),
            ),
        )
        # 双向存储，方便查询
        conn.execute(
            """
            INSERT OR IGNORE INTO ddi_pairs
            (drug_a_id, drug_b_id, severity, mechanism, advice, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                b_id,
                a_id,
                pair["severity"],
                pair.get("mechanism", ""),
                pair.get("advice", ""),
                pair.get("source", ""),
            ),
        )


def seed_food_drug_pairs(conn, drug_ids: dict[str, int]) -> None:
    for item in FOOD_DRUG_PAIRS:
        drug_id = drug_ids.get(item["drug"])
        if drug_id is None:
            continue
        conn.execute(
            """
            INSERT OR IGNORE INTO food_drug_pairs
            (drug_id, food, effect, advice, source)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                drug_id,
                item["food"],
                item.get("effect", ""),
                item.get("advice", ""),
                item.get("source", ""),
            ),
        )


def seed_elderly_risk_rules(conn, drug_ids: dict[str, int]) -> None:
    for rule in ELDERLY_RISK_RULES:
        drug_id = drug_ids.get(rule["drug"])
        if drug_id is None:
            continue
        conn.execute(
            """
            INSERT OR IGNORE INTO elderly_risk_rules
            (drug_id, risk_type, reason, recommendation, source)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                drug_id,
                rule["risk_type"],
                rule.get("reason", ""),
                rule.get("recommendation", ""),
                rule.get("source", ""),
            ),
        )


def seed_all(reset: bool = True) -> None:
    """初始化数据库并填充样本数据."""
    if reset:
        reset_db()
    else:
        init_db()
    with get_connection() as conn:
        drug_ids = seed_drugs(conn)
        seed_aliases(conn, drug_ids)
        seed_ddi_pairs(conn, drug_ids)
        seed_food_drug_pairs(conn, drug_ids)
        seed_elderly_risk_rules(conn, drug_ids)
        conn.commit()


if __name__ == "__main__":
    seed_all(reset=True)
    print("数据库种子完成。")
