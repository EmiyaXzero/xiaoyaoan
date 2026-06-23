"""KnowS AI 循证检索客户端.

用于在本地 SQLite 知识库未命中时，检索外部医学证据补充药物相互作用信息。
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from medsafe_core.models import EvidenceItem


KNOWS_API_BASE = "https://api.nullht.com/v1"
DEFAULT_ENDPOINT = "evidences/ai_search_paper_cn"


def _get_api_key() -> str | None:
    return os.environ.get("KNOWS_API_KEY")


def _call_knows(query: str, endpoint: str = DEFAULT_ENDPOINT) -> dict[str, Any]:
    api_key = _get_api_key()
    if not api_key:
        return {}

    url = f"{KNOWS_API_BASE}/{endpoint}"
    data = json.dumps({"query": query}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return {}


def _evidence_to_item(drug_a: str, drug_b: str, item: dict[str, Any]) -> EvidenceItem | None:
    """把 KnowS 返回的单条证据转成 EvidenceItem."""
    title = item.get("title") or item.get("name") or ""
    abstract = item.get("abstract") or item.get("content") or item.get("text") or ""
    source = item.get("source") or item.get("url") or item.get("doi") or "KnowS AI"

    mechanism = title
    if abstract:
        mechanism = f"{title}：{abstract}" if title else abstract

    if not mechanism:
        return None

    return EvidenceItem(
        type="ddi",
        drug_a=drug_a,
        drug_b=drug_b,
        severity="中",
        mechanism=mechanism,
        advice="该证据来自外部文献检索，具体用药请结合临床并咨询医生/药师。",
        source=source,
    )


def search_drug_interaction_evidence(drug_a: str, drug_b: str) -> list[EvidenceItem]:
    """检索 KnowS AI 中关于两种药品相互作用的外部证据.

    未配置 KNOWS_API_KEY 或调用失败时返回空列表，不影响主流程。
    """
    query = f"{drug_a} {drug_b} 药物相互作用 drug interaction"
    result = _call_knows(query)
    items = result.get("evidences") or []

    evidence: list[EvidenceItem] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        ev = _evidence_to_item(drug_a, drug_b, item)
        if ev:
            evidence.append(ev)
    return evidence
