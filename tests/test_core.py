"""核心功能单元测试."""

from medsafe_core import (
    normalize_drug_name,
    check_drug_interactions,
    check_food_drug_interaction,
    explain_drug_label,
    screen_elderly_medications,
)


def test_normalize_exact():
    assert normalize_drug_name("阿司匹林") == "阿司匹林"


def test_normalize_alias():
    assert normalize_drug_name("拜阿司匹灵") == "阿司匹林"
    assert normalize_drug_name("Aspirin") == "阿司匹林"


def test_normalize_unknown():
    assert normalize_drug_name("不存在的药") is None


def test_check_drug_interactions():
    result = check_drug_interactions(["阿司匹林", "华法林"])
    assert result.risk_level == "高"
    assert len(result.evidence) >= 1
    assert result.evidence[0].type == "ddi"


def test_check_drug_interactions_not_found():
    result = check_drug_interactions(["阿司匹林", "未知药品"])
    assert "未知药品" in result.not_found


def test_check_food_drug_interaction():
    result = check_food_drug_interaction("甲硝唑", "酒")
    assert result.risk_level == "中"
    assert any("酒精" in (e.food or "") for e in result.evidence)


def test_explain_drug_label():
    result = explain_drug_label("阿司匹林", "注意事项")
    assert result.drug == "阿司匹林"
    assert "阿司匹林" in result.content
    assert not result.not_found


def test_explain_drug_label_not_found():
    result = explain_drug_label("未知药品")
    assert result.not_found


def test_screen_elderly_medications():
    result = screen_elderly_medications(["阿司匹林", "华法林", "阿普唑仑"])
    assert result.risk_level == "高"
    assert len(result.interactions) >= 1
    assert len(result.elderly_risks) >= 1
