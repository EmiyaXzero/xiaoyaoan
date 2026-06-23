"""统一返回数据模型."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


DISCLAIMER = "本工具仅用于用药安全科普，查询结果仅供参考，不构成诊断、处方或用药调整建议。具体用药请务必咨询医生或药师。"


SEVERITY_ORDER = ["禁忌", "高", "中", "低", "无"]


def aggregate_severity(severities: list[str]) -> str:
    """从多个风险等级中聚合出最高等级."""
    if not severities:
        return "无"
    best_index = min(
        (SEVERITY_ORDER.index(s) for s in severities if s in SEVERITY_ORDER),
        default=SEVERITY_ORDER.index("无"),
    )
    return SEVERITY_ORDER[best_index]


@dataclass
class EvidenceItem:
    """单条证据."""

    type: str
    drug_a: str | None = None
    drug_b: str | None = None
    food: str | None = None
    severity: str = "无"
    mechanism: str = ""
    advice: str = ""
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InteractionResult:
    """相互作用查询结果."""

    risk_level: str = "无"
    summary: str = ""
    evidence: list[EvidenceItem] = field(default_factory=list)
    disclaimer: str = DISCLAIMER
    not_found: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "summary": self.summary,
            "evidence": [e.to_dict() for e in self.evidence],
            "disclaimer": self.disclaimer,
            "not_found": self.not_found,
        }


@dataclass
class ExplanationResult:
    """说明书解读结果."""

    drug: str = ""
    section: str = ""
    content: str = ""
    disclaimer: str = DISCLAIMER
    not_found: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScreeningResult:
    """老年用药清单批量筛查结果."""

    risk_level: str = "无"
    summary: str = ""
    interactions: list[EvidenceItem] = field(default_factory=list)
    elderly_risks: list[EvidenceItem] = field(default_factory=list)
    disclaimer: str = DISCLAIMER
    not_found: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "summary": self.summary,
            "interactions": [e.to_dict() for e in self.interactions],
            "elderly_risks": [e.to_dict() for e in self.elderly_risks],
            "disclaimer": self.disclaimer,
            "not_found": self.not_found,
        }
