#!/usr/bin/env python3
"""Skill 脚本：查询食物-药物冲突."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from medsafe_core import check_food_drug_interaction


def main() -> None:
    try:
        params = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"输入不是合法 JSON: {e}"}, ensure_ascii=False))
        sys.exit(1)

    drug = params.get("drug", "")
    food = params.get("food", "")
    if not drug or not food:
        print(json.dumps({"error": "请提供 drug 与 food 参数"}, ensure_ascii=False))
        sys.exit(1)

    result = check_food_drug_interaction(drug, food)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
