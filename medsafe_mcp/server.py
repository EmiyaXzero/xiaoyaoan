#!/usr/bin/env python3
"""MedSafe-Helper MCP Server.

暴露 4 个工具：
- check_drug_interactions
- check_food_drug_interaction
- explain_drug_label
- screen_elderly_medication_list

运行方式：
    python -m medsafe_mcp.server          # stdio（默认）
    python -m medsafe_mcp.server --sse    # SSE 模式
"""

from __future__ import annotations

import argparse

from mcp.server.fastmcp import FastMCP

from medsafe_core import (
    check_drug_interactions,
    check_food_drug_interaction,
    explain_drug_label,
    screen_elderly_medications,
)

mcp = FastMCP("medsafe-helper")


@mcp.tool()
def check_drug_interactions_tool(drugs: list[str]) -> dict:
    """查询多种药物之间的相互作用.

    Args:
        drugs: 药品名称列表，例如 ["阿司匹林", "华法林"]

    Returns:
        包含 risk_level、summary、evidence、disclaimer 的字典
    """
    return check_drug_interactions(drugs).to_dict()


@mcp.tool()
def check_food_drug_interaction_tool(drug: str, food: str) -> dict:
    """查询食物/饮品与药物的冲突.

    Args:
        drug: 药品名称，例如 "甲硝唑"
        food: 食物或饮品名称，例如 "酒"

    Returns:
        包含 risk_level、summary、evidence、disclaimer 的字典
    """
    return check_food_drug_interaction(drug, food).to_dict()


@mcp.tool()
def explain_drug_label_tool(drug: str, section: str | None = None) -> dict:
    """药品说明书大白话解读.

    Args:
        drug: 药品名称，例如 "阿司匹林"
        section: 说明书章节，例如 "注意事项"，默认 "适应症"

    Returns:
        包含 drug、section、content、disclaimer 的字典
    """
    return explain_drug_label(drug, section).to_dict()


@mcp.tool()
def screen_elderly_medication_list_tool(medications: list[str]) -> dict:
    """老年人用药清单批量风险筛查.

    Args:
        medications: 用药清单，例如 ["阿司匹林", "华法林", "阿普唑仑"]

    Returns:
        包含 risk_level、summary、interactions、elderly_risks、disclaimer 的字典
    """
    return screen_elderly_medications(medications).to_dict()


def main() -> None:
    parser = argparse.ArgumentParser(description="MedSafe-Helper MCP Server")
    parser.add_argument("--sse", action="store_true", help="以 SSE 模式运行")
    parser.add_argument("--port", type=int, default=8000, help="SSE 模式端口")
    args = parser.parse_args()

    if args.sse:
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
