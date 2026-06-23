"""测试配置：确保数据库已初始化."""

from medsafe_core.data.seed_db import seed_all

# 每次测试会话前重新播种数据库
seed_all(reset=True)
