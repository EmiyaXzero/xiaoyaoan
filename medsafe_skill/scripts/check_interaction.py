#!/usr/bin/env python3
"""Skill 脚本：查询药物相互作用."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# 将项目根目录加入路径，确保能导入 medsafe_core
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from medsafe_core import check_drug_interactions


def main() -> None:
    try:
        params = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"输入不是合法 JSON: {e}"}, ensure_ascii=False))
        sys.exit(1)

    drugs = params.get("drugs", [])
    if not isinstance(drugs, list):
        print(json.dumps({"error": "参数 drugs 应为列表"}, ensure_ascii=False))
        sys.exit(1)

    result = check_drug_interactions(drugs)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
