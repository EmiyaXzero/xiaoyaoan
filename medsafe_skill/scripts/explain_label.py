#!/usr/bin/env python3
"""Skill 脚本：药品说明书大白话解读."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from medsafe_core import explain_drug_label


def main() -> None:
    try:
        params = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"输入不是合法 JSON: {e}"}, ensure_ascii=False))
        sys.exit(1)

    drug = params.get("drug", "")
    section = params.get("section") or None
    if not drug:
        print(json.dumps({"error": "请提供 drug 参数"}, ensure_ascii=False))
        sys.exit(1)

    result = explain_drug_label(drug, section)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
