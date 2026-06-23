"""药品名称归一化."""

from __future__ import annotations

from rapidfuzz import process, fuzz

from medsafe_core.db import get_connection

FUZZY_THRESHOLD = 75


def _load_drug_names() -> list[tuple[str, str]]:
    """加载所有药品标准名与别名，返回 (alias, canonical) 列表."""
    items: list[tuple[str, str]] = []
    with get_connection() as conn:
        # 标准名本身也是有效输入
        for row in conn.execute("SELECT name_cn FROM drugs"):
            canonical = row["name_cn"]
            items.append((canonical, canonical))
        # 别名
        for row in conn.execute(
            """
            SELECT a.alias, d.name_cn AS canonical
            FROM drug_aliases a
            JOIN drugs d ON a.drug_id = d.id
            """
        ):
            items.append((row["alias"], row["canonical"]))
    return items


_normalize_cache: dict[str, str | None] | None = None


def normalize_drug_name(name: str) -> str | None:
    """将用户输入的药品名归一化为标准名.

    优先精确匹配，未命中时使用 rapidfuzz 模糊匹配，阈值 0.75。
    """
    global _normalize_cache
    name = name.strip()
    if not name:
        return None

    if _normalize_cache is None:
        _normalize_cache = {}
        for alias, canonical in _load_drug_names():
            _normalize_cache[alias] = canonical

    # 精确匹配（大小写不敏感）
    lower = name.lower()
    for alias, canonical in _normalize_cache.items():
        if alias.lower() == lower:
            return canonical

    # 模糊匹配
    aliases = list(_normalize_cache.keys())
    if not aliases:
        return None
    match = process.extractOne(name, aliases, scorer=fuzz.WRatio)
    if match and match[1] >= FUZZY_THRESHOLD:
        return _normalize_cache[match[0]]
    return None


def invalidate_cache() -> None:
    """数据更新后调用，清空归一化缓存."""
    global _normalize_cache
    _normalize_cache = None
