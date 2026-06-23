"""SQLite 知识库连接与初始化."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "medsafe_kg.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_cn TEXT NOT NULL UNIQUE,
    name_en TEXT,
    atc_code TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS drug_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_id INTEGER NOT NULL,
    alias TEXT NOT NULL UNIQUE,
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
);

CREATE TABLE IF NOT EXISTS ddi_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_a_id INTEGER NOT NULL,
    drug_b_id INTEGER NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('禁忌','高','中','低','无')),
    mechanism TEXT,
    advice TEXT,
    source TEXT,
    FOREIGN KEY (drug_a_id) REFERENCES drugs(id),
    FOREIGN KEY (drug_b_id) REFERENCES drugs(id)
);

CREATE TABLE IF NOT EXISTS food_drug_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_id INTEGER NOT NULL,
    food TEXT NOT NULL,
    effect TEXT,
    advice TEXT,
    source TEXT,
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
);

CREATE TABLE IF NOT EXISTS elderly_risk_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_id INTEGER NOT NULL,
    risk_type TEXT NOT NULL,
    reason TEXT,
    recommendation TEXT,
    source TEXT,
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
);
"""


def get_db_path() -> Path:
    return DB_PATH


def ensure_data_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """创建表结构（若不存在）."""
    ensure_data_dir()
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def reset_db() -> None:
    """删除并重建数据库（慎用）."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
