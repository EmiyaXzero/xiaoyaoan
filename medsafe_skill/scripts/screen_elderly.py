#!/usr/bin/env python3
"""Skill 脚本：老年用药清单批量筛查."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from medsafe_core import screen_elderly_medications


def main() -> None:
    try:
        params = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"输入不是合法 JSON: {e}"}, ensure_ascii=False))
        sys.exit(1)

    medications = params.get("medications", [])
    if not isinstance(medications, list):
        print(json.dumps({"error": "参数 medications 应为列表"}, ensure_ascii=False))
        sys.exit(1)

    result = screen_elderly_medications(medications)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
