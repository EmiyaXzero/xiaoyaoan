#!/usr/bin/env python3
"""魔搭创空间入口文件.

本文件位于项目根目录，供 ModelScope Studio 直接启动。
实际 UI 逻辑在 studio/app.py 中实现。
"""

import logging

from studio.app import main

if __name__ == "__main__":
    # 开启 medsafe_core 模块的 INFO 日志，方便在创空间日志里查看 LLM 调用情况
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()
