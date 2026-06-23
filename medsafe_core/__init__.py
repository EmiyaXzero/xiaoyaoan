"""小药安 / MedSafe-Helper 统一领域内核.

提供用药安全相关的核心能力：
- 药品名称归一化
- 药物相互作用（DDI）查询
- 食物-药物冲突查询
- 药品说明书大白话解读
- 老年用药清单批量筛查
"""

from medsafe_core.models import InteractionResult, ExplanationResult, ScreeningResult
from medsafe_core.normalizer import normalize_drug_name
from medsafe_core.interaction import check_drug_interactions
from medsafe_core.food_drug import check_food_drug_interaction
from medsafe_core.label_explainer import explain_drug_label
from medsafe_core.elderly_screen import screen_elderly_medications
from medsafe_core.db import init_db, get_db_path

__all__ = [
    "InteractionResult",
    "ExplanationResult",
    "ScreeningResult",
    "normalize_drug_name",
    "check_drug_interactions",
    "check_food_drug_interaction",
    "explain_drug_label",
    "screen_elderly_medications",
    "init_db",
    "get_db_path",
]
