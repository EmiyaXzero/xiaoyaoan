# 小药安 / MedSafe-Helper

> 面向大众与家庭照护者的用药安全科普工具。
> 支持药物-药物相互作用、食物-药物冲突、药品说明书大白话解读、老年人用药清单批量风险筛查。

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## ⚠️ 重要免责声明

**本工具仅用于用药安全科普，所有查询结果仅供参考，不构成诊断、处方、剂量调整、停药或换药建议。**

- 具体用药方案必须由具备资质的医生或药师根据患者实际情况制定。
- 本工具不提供紧急医疗建议。如用药后出现不适，请立即就医。
- 本工具演示数据为常见药品样本，不代表完整权威数据库，实际生产环境应接入 NMPA、DrugBank、Beers Criteria 等权威来源。

---

## 功能特性

| 功能 | 说明 |
|------|------|
| **药物相互作用查询** | 输入 2~10 个药品名，返回风险等级、作用机制、建议与来源 |
| **食物-药物冲突** | 输入药品 + 食物/饮品，返回已知冲突说明 |
| **说明书大白话解读** | 选择章节，将专业说明书内容转译为通俗语言 |
| **老年用药清单筛查** | 手动输入或上传 CSV，批量筛查药物相互作用与老年高风险规则 |

### 风险分级

| 等级 | 颜色 | 含义 |
|------|------|------|
| 禁忌 | 🔴 红 | 强烈建议立即咨询医生/药师 |
| 高 | 🟠 橙 | 存在明确风险，需在专业指导下用药 |
| 中 | 🟡 黄 | 可能需要注意，建议进一步确认 |
| 低 | 🔵 蓝 | 一般性提示 |
| 无 | 🟢 绿 | 未检索到已知相互作用，仍需遵医嘱 |

---

## 技术架构

采用「统一领域内核 + 多形态封装」：

```
交互层
├── ModelScope Studio (Gradio)  ← 普通用户网页 Demo
├── MCP Client (Cursor/Cherry Studio/Claude)  ← Agent/IDE 工具
└── ms-agent / Skill 宿主        ← ModelScope Skills 中心
        ↓
统一内核 medsafe_core（Python 包）
├── 药品名称归一化
├── 药物相互作用（DDI）查询
├── 食物-药物冲突查询
├── 说明书大白话生成
└── 老年清单批量筛查
        ↓
数据层：SQLite 用药知识库 + 预留 RAG/LLM 扩展接口
```

---

## 快速开始

### 1. 克隆仓库并安装依赖

```bash
git clone https://github.com/your-org/medsafe-helper.git
cd medsafe-helper
pip install -r requirements.txt
```

### 2. 初始化知识库

```bash
python -m medsafe_core.data.seed_db
```

### 3. 启动 Studio

```bash
python studio/app.py
```

浏览器访问 `http://localhost:7860`。

### 4. 使用 Skill

进入 `medsafe_skill/` 目录，脚本从 stdin 读取 JSON：

```bash
echo '{"drugs":["阿司匹林","华法林"]}' | python medsafe_skill/scripts/check_interaction.py
```

### 5. 启动 MCP Server

STDIO 模式（供本地 IDE/Agent 使用）：

```bash
python -m medsafe_mcp.server
```

SSE 模式：

```bash
python -m medsafe_mcp.server --sse --port 8000
```

---

## 目录结构

```
medsafe-helper/
├── .trae/documents/         # PRD 与技术架构文档
├── medsafe_core/            # 统一领域内核
│   ├── data/                # 样本数据与种子脚本
│   ├── db.py                # SQLite 连接
│   ├── normalizer.py        # 药品名称归一化
│   ├── interaction.py       # DDI 查询
│   ├── food_drug.py         # 食物-药物冲突
│   ├── label_explainer.py   # 说明书解读
│   └── elderly_screen.py    # 老年筛查
├── medsafe_skill/           # Skill 形态
│   ├── SKILL.md
│   └── scripts/
├── medsafe_mcp/             # MCP Server 形态
│   └── server.py
├── studio/                  # Gradio Studio
│   └── app.py
├── data/                    # SQLite 数据库（运行种子后生成）
├── tests/                   # 单元测试
├── README.md
├── requirements.txt
├── pyproject.toml
└── ms_deploy.json           # ModelScope 创空间部署配置
```

---

## 数据来源

本 MVP 使用合成样本数据覆盖常见慢病用药，来源参考：

- NMPA 已批准药品说明书公开文本
- DrugBank Open Data
- FDA 消费者用药指南
- Beers Criteria（老年用药风险）
- 临床用药须知

生产环境建议接入：

- **KnowS API**（循证检索）
- **Sealos FastGPT**（RAG 知识库）
- 权威 DDI 数据库与 NMPA 完整说明书

---

## 合规与局限

- 不做诊断承诺：输出仅描述风险/证据，不输出「可治疗/可治愈」。
- 不做处方建议：不输出剂量调整、停药、换药、联合用药指导。
- 不使用真实患者数据：Demo 仅使用合成示例 CSV。
- 明确局限性：每次输出附带免责声明，README 专门写局限性章节。
- 药品覆盖有限：MVP 聚焦 200+ 常见药别名，匹配失败会明确提示。

---

## 提交入口

- Skill 提交：`https://modelscope.cn/skills/create?template=custom`
- MCP 提交：`https://modelscope.cn/mcp/servers/create`
- Studio 提交：`https://modelscope.cn/studios/create`

---

## 团队与许可证

- 项目团队：MedSafe Team
- 许可证：[Apache-2.0](LICENSE)

---

**安全用药，从了解开始。**
