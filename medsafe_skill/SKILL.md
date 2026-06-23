# medsafe-helper Skill 定义

## 基本信息

- **name**: `medsafe-helper`
- **description**: 用药安全科普助手：查询药物相互作用、食物-药物冲突、解读药品说明书、筛查老年用药风险。所有结果仅供参考，不构成诊疗建议。
- **version**: `0.1.0`
- **author**: MedSafe Team
- **license**: Apache-2.0

## 能力说明

本 Skill 暴露 4 个脚本工具，供 ms-agent 等宿主按自然语言触发后调用：

| 脚本 | 功能 |
|------|------|
| `scripts/check_interaction.py` | 查询多种药品之间的相互作用 |
| `scripts/check_food_drug.py` | 查询食物/饮品与药品的冲突 |
| `scripts/explain_label.py` | 药品说明书大白话解读 |
| `scripts/screen_elderly.py` | 老年用药清单批量风险筛查 |

## 输入/输出约定

- 脚本从 **stdin** 读取 JSON 参数。
- 脚本向 **stdout** 输出 JSON 结果。
- 统一返回结构包含 `risk_level`、`summary`、`evidence`、`disclaimer` 字段。

## 输入示例

### check_interaction

```json
{
  "drugs": ["阿司匹林", "华法林"]
}
```

### check_food_drug

```json
{
  "drug": "甲硝唑",
  "food": "酒"
}
```

### explain_label

```json
{
  "drug": "阿司匹林",
  "section": "注意事项"
}
```

### screen_elderly

```json
{
  "medications": ["阿司匹林", "华法林", "阿普唑仑"]
}
```

## 输出示例

```json
{
  "risk_level": "高",
  "summary": "阿司匹林与华法林联用可能增加出血风险，需密切监测。",
  "evidence": [
    {
      "type": "ddi",
      "drug_a": "阿司匹林",
      "drug_b": "华法林",
      "severity": "高",
      "mechanism": "抗血小板与抗凝作用叠加",
      "source": "DrugBank"
    }
  ],
  "disclaimer": "本结果仅供参考，具体用药请遵医嘱。"
}
```

## 使用提示

- 触发词示例："查一下阿司匹林和华法林能不能一起吃"、"甲硝唑能喝酒吗"、"阿司匹林说明书注意事项"、"帮我筛查这些药对老人有没有风险"。
- 当药品名归一化失败时，结果中会包含 `not_found` 字段，提示用户检查药品名称。
- 本 Skill 不替代医生或药师的专业判断。
