#!/usr/bin/env python3
"""小药安 / MedSafe-Helper Studio (Gradio)."""

from __future__ import annotations

import io
from pathlib import Path

import gradio as gr
import pandas as pd

import sys

# 确保能导入项目根目录下的 medsafe_core
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from medsafe_core import (
    check_drug_interactions,
    check_food_drug_interaction,
    explain_drug_label,
    screen_elderly_medications,
)
from medsafe_core.label_explainer import DEFAULT_SECTIONS


DISCLAIMER = (
    "⚠️ 免责声明：本工具仅用于用药安全科普，查询结果仅供参考，"
    "不构成诊断、处方或用药调整建议。具体用药请务必咨询医生或药师。"
)

RISK_COLORS = {
    "禁忌": "#DC2626",
    "高": "#EA580C",
    "中": "#CA8A04",
    "低": "#2563EB",
    "无": "#16A34A",
}

CSS = """
:root {
    --primary: #0D9488;
    --primary-dark: #134E4A;
    --bg-light: #F0FDFA;
}

.gradio-container {
    background: linear-gradient(180deg, #F0FDFA 0%, #FFFFFF 100%);
}

#disclaimer-banner {
    background: #FEF3C7;
    border-left: 5px solid #F59E0B;
    color: #92400E;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 14px;
    line-height: 1.5;
}

.header-title {
    color: var(--primary-dark);
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 4px;
}

.header-subtitle {
    color: #475569;
    font-size: 16px;
    margin-bottom: 20px;
}

.risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    color: white;
    font-weight: 600;
    font-size: 14px;
    margin-right: 8px;
}

.evidence-card {
    background: white;
    border-left: 4px solid var(--primary);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
"""


def _risk_badge(level: str) -> str:
    color = RISK_COLORS.get(level, "#6B7280")
    return f'<span class="risk-badge" style="background:{color}">{level}</span>'


def _format_evidence(evidence: list[dict]) -> str:
    if not evidence:
        return "<p>未检索到具体证据条目。</p>"
    parts = []
    for i, e in enumerate(evidence, 1):
        title = ""
        if e.get("type") == "ddi":
            title = f"{e.get('drug_a')} + {e.get('drug_b')}"
        elif e.get("type") == "food_drug":
            title = f"{e.get('drug_a')} + {e.get('food')}"
        elif e.get("type") == "elderly_risk":
            title = f"{e.get('drug_a')}（老年风险）"
        else:
            title = "风险提示"

        severity = e.get("severity", "无")
        badge = _risk_badge(severity)
        mechanism = e.get("mechanism", "")
        advice = e.get("advice", "")
        source = e.get("source", "")

        lines = [f"<div class='evidence-card' style='border-left-color:{RISK_COLORS.get(severity, '#6B7280')}'>"]
        lines.append(f"<strong>{i}. {title}</strong> {badge}")
        if mechanism:
            lines.append(f"<p><strong>机制/说明：</strong>{mechanism}</p>")
        if advice:
            lines.append(f"<p><strong>建议：</strong>{advice}</p>")
        if source:
            lines.append(f"<p style='color:#64748B;font-size:12px'><strong>来源：</strong>{source}</p>")
        lines.append("</div>")
        parts.append("\n".join(lines))
    return "\n".join(parts)


def _format_interaction_result(result: dict) -> str:
    lines = [
        f"<h3>{_risk_badge(result['risk_level'])} {result['summary']}</h3>",
        _format_evidence(result.get("evidence", [])),
    ]
    if result.get("not_found"):
        lines.append(
            f"<p style='color:#DC2626'>⚠️ 未识别以下药品：{', '.join(result['not_found'])}，请检查名称。</p>"
        )
    lines.append(
        f"<p style='color:#64748B;font-size:13px;margin-top:16px;border-top:1px solid #E2E8F0;padding-top:8px'>"
        f"{result['disclaimer']}</p>"
    )
    return "\n".join(lines)


def _format_screening_result(result: dict) -> str:
    lines = [f"<h3>{_risk_badge(result['risk_level'])} {result['summary']}</h3>"]

    interactions = result.get("interactions", [])
    elderly_risks = result.get("elderly_risks", [])

    if interactions:
        lines.append("<h4>🔁 药物相互作用</h4>")
        lines.append(_format_evidence(interactions))

    if elderly_risks:
        lines.append("<h4>👴 老年用药风险</h4>")
        lines.append(_format_evidence(elderly_risks))

    if result.get("not_found"):
        lines.append(
            f"<p style='color:#DC2626'>⚠️ 未识别以下药品：{', '.join(result['not_found'])}，请检查名称。</p>"
        )

    lines.append(
        f"<p style='color:#64748B;font-size:13px;margin-top:16px;border-top:1px solid #E2E8F0;padding-top:8px'>"
        f"{result['disclaimer']}</p>"
    )
    return "\n".join(lines)


def _format_explanation_result(result: dict) -> str:
    if result.get("not_found"):
        return (
            f"<p style='color:#DC2626'>{result['content']}</p>"
            f"<p style='color:#64748B;font-size:13px'>{result['disclaimer']}</p>"
        )
    return (
        f"<h3>「{result['drug']}」— {result['section']}</h3>"
        f"<div class='evidence-card'>{result['content']}</div>"
        f"<p style='color:#64748B;font-size:13px;margin-top:16px'>{result['disclaimer']}</p>"
    )


def _parse_drug_list(text: str) -> list[str]:
    if not text:
        return []
    # 支持换行、逗号、顿号、分号分隔
    separators = ["\n", ",", "，", "、", ";", "；"]
    items = [text]
    for sep in separators:
        new_items = []
        for item in items:
            new_items.extend([s.strip() for s in item.split(sep) if s.strip()])
        items = new_items
    return list(dict.fromkeys(items))  # 去重保持顺序


def on_check_interactions(drug_text: str) -> str:
    drugs = _parse_drug_list(drug_text)
    result = check_drug_interactions(drugs).to_dict()
    return _format_interaction_result(result)


def on_check_food_drug(drug: str, food: str) -> str:
    result = check_food_drug_interaction(drug, food).to_dict()
    return _format_interaction_result(result)


def on_explain_label(drug: str, section: str) -> str:
    result = explain_drug_label(drug, section).to_dict()
    return _format_explanation_result(result)


def on_screen_elderly(manual_text: str, file) -> str:
    meds = _parse_drug_list(manual_text)
    if file is not None:
        try:
            if isinstance(file, str):
                df = pd.read_csv(file)
            else:
                df = pd.read_csv(io.BytesIO(file))
            # 自动识别药品名所在列
            drug_col = None
            for col in df.columns:
                if "药" in col or col.lower() in ("drug", "medication", "name", "药品"):
                    drug_col = col
                    break
            if drug_col is None:
                drug_col = df.columns[0]
            file_meds = [str(x).strip() for x in df[drug_col].dropna() if str(x).strip()]
            meds = list(dict.fromkeys(meds + file_meds))
        except Exception as e:
            return f"<p style='color:#DC2626'>CSV 解析失败：{e}</p>"

    result = screen_elderly_medications(meds).to_dict()
    return _format_screening_result(result)


def build_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.HTML(
            f"""
            <div class="header-title">小药安 MedSafe-Helper</div>
            <div class="header-subtitle">用药安全科普助手 · 药物相互作用 · 食物-药物冲突 · 说明书解读 · 老年用药筛查</div>
            <div id="disclaimer-banner">{DISCLAIMER}</div>
            """
        )

        with gr.Tabs():
            with gr.Tab("药物相互作用"):
                gr.Markdown("输入 2~10 个药品名，查询是否存在已知的相互作用。")
                drug_input = gr.Textbox(
                    label="药品列表",
                    placeholder="例如：阿司匹林、华法林、氯吡格雷（可用换行、逗号、顿号分隔）",
                    lines=3,
                )
                check_btn = gr.Button("查询相互作用", variant="primary")
                interaction_output = gr.HTML(label="结果")
                check_btn.click(
                    fn=on_check_interactions,
                    inputs=drug_input,
                    outputs=interaction_output,
                )

            with gr.Tab("食物-药物冲突"):
                gr.Markdown("输入药品和食物/饮品，查询是否存在冲突。")
                with gr.Row():
                    fd_drug = gr.Textbox(label="药品", placeholder="例如：甲硝唑")
                    fd_food = gr.Textbox(label="食物/饮品", placeholder="例如：酒、葡萄柚")
                fd_btn = gr.Button("查询冲突", variant="primary")
                fd_output = gr.HTML(label="结果")
                fd_btn.click(
                    fn=on_check_food_drug,
                    inputs=[fd_drug, fd_food],
                    outputs=fd_output,
                )

            with gr.Tab("说明书解读"):
                gr.Markdown("选择药品和章节，获取大白话版说明书解读。")
                with gr.Row():
                    label_drug = gr.Textbox(label="药品", placeholder="例如：阿司匹林")
                    label_section = gr.Dropdown(
                        label="章节",
                        choices=DEFAULT_SECTIONS,
                        value="适应症",
                    )
                label_btn = gr.Button("解读", variant="primary")
                label_output = gr.HTML(label="解读结果")
                label_btn.click(
                    fn=on_explain_label,
                    inputs=[label_drug, label_section],
                    outputs=label_output,
                )

            with gr.Tab("老年清单筛查"):
                gr.Markdown("手动输入用药清单，或上传 CSV 文件，批量筛查老年用药风险。")
                elderly_input = gr.Textbox(
                    label="用药清单",
                    placeholder="例如：阿司匹林、华法林、阿普唑仑（可用换行、逗号分隔）",
                    lines=5,
                )
                elderly_file = gr.File(
                    label="上传 CSV（可选）",
                    file_types=[".csv"],
                )
                elderly_btn = gr.Button("开始筛查", variant="primary")
                elderly_output = gr.HTML(label="筛查报告")
                elderly_btn.click(
                    fn=on_screen_elderly,
                    inputs=[elderly_input, elderly_file],
                    outputs=elderly_output,
                )

    return demo


def main() -> None:
    demo = build_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        css=CSS,
    )


if __name__ == "__main__":
    main()
