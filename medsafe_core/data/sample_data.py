"""样本用药知识数据.

数据为演示用途，覆盖常见慢病用药与部分相互作用示例。
实际生产环境应替换为 NMPA、DrugBank、Beers Criteria 等权威来源。
"""

from __future__ import annotations

DRUGS: list[dict] = [
    # 心血管
    {"name_cn": "阿司匹林", "name_en": "Aspirin", "atc_code": "B01AC06", "category": "抗血小板药"},
    {"name_cn": "华法林", "name_en": "Warfarin", "atc_code": "B01AA03", "category": "口服抗凝药"},
    {"name_cn": "氯吡格雷", "name_en": "Clopidogrel", "atc_code": "B01AC04", "category": "抗血小板药"},
    {"name_cn": "阿托伐他汀", "name_en": "Atorvastatin", "atc_code": "C10AA05", "category": "调脂药"},
    {"name_cn": "辛伐他汀", "name_en": "Simvastatin", "atc_code": "C10AA01", "category": "调脂药"},
    {"name_cn": "瑞舒伐他汀", "name_en": "Rosuvastatin", "atc_code": "C10AA07", "category": "调脂药"},
    {"name_cn": "氨氯地平", "name_en": "Amlodipine", "atc_code": "C08CA01", "category": "降压药"},
    {"name_cn": "硝苯地平", "name_en": "Nifedipine", "atc_code": "C08CA05", "category": "降压药"},
    {"name_cn": "缬沙坦", "name_en": "Valsartan", "atc_code": "C09CA03", "category": "降压药"},
    {"name_cn": "厄贝沙坦", "name_en": "Irbesartan", "atc_code": "C09CA04", "category": "降压药"},
    {"name_cn": "美托洛尔", "name_en": "Metoprolol", "atc_code": "C07AB02", "category": "β受体阻滞剂"},
    {"name_cn": "比索洛尔", "name_en": "Bisoprolol", "atc_code": "C07AB07", "category": "β受体阻滞剂"},
    # 降糖
    {"name_cn": "二甲双胍", "name_en": "Metformin", "atc_code": "A10BA02", "category": "降糖药"},
    {"name_cn": "格列美脲", "name_en": "Glimepiride", "atc_code": "A10BB12", "category": "磺脲类降糖药"},
    {"name_cn": "阿卡波糖", "name_en": "Acarbose", "atc_code": "A10BF01", "category": "α-糖苷酶抑制剂"},
    {"name_cn": "西格列汀", "name_en": "Sitagliptin", "atc_code": "A10BH01", "category": "DPP-4抑制剂"},
    {"name_cn": "胰岛素", "name_en": "Insulin", "atc_code": "A10A", "category": "胰岛素"},
    # 抗感染/消炎
    {"name_cn": "阿莫西林", "name_en": "Amoxicillin", "atc_code": "J01CA04", "category": "抗生素"},
    {"name_cn": "头孢呋辛", "name_en": "Cefuroxime", "atc_code": "J01DC02", "category": "抗生素"},
    {"name_cn": "左氧氟沙星", "name_en": "Levofloxacin", "atc_code": "J01MA12", "category": "喹诺酮类抗生素"},
    {"name_cn": "甲硝唑", "name_en": "Metronidazole", "atc_code": "P01AB01", "category": "抗原虫/厌氧菌"},
    {"name_cn": "布洛芬", "name_en": "Ibuprofen", "atc_code": "M01AE01", "category": "NSAIDs"},
    {"name_cn": "对乙酰氨基酚", "name_en": "Paracetamol", "atc_code": "N02BE01", "category": "解热镇痛药"},
    # 精神神经
    {"name_cn": "阿普唑仑", "name_en": "Alprazolam", "atc_code": "N05BA12", "category": "苯二氮䓬类"},
    {"name_cn": "艾司唑仑", "name_en": "Estazolam", "atc_code": "N05BA04", "category": "苯二氮䓬类"},
    {"name_cn": "舍曲林", "name_en": "Sertraline", "atc_code": "N06AB06", "category": "SSRI抗抑郁药"},
    {"name_cn": "帕罗西汀", "name_en": "Paroxetine", "atc_code": "N06AB05", "category": "SSRI抗抑郁药"},
    # 消化
    {"name_cn": "奥美拉唑", "name_en": "Omeprazole", "atc_code": "A02BC01", "category": "质子泵抑制剂"},
    {"name_cn": "雷贝拉唑", "name_en": "Rabeprazole", "atc_code": "A02BC04", "category": "质子泵抑制剂"},
    {"name_cn": "莫沙必利", "name_en": "Mosapride", "atc_code": "A03FA09", "category": "促胃肠动力药"},
    # 其他常见
    {"name_cn": "呋塞米", "name_en": "Furosemide", "atc_code": "C03CA01", "category": "利尿剂"},
    {"name_cn": "氢氯噻嗪", "name_en": "Hydrochlorothiazide", "atc_code": "C03AA03", "category": "利尿剂"},
    {"name_cn": "螺内酯", "name_en": "Spironolactone", "atc_code": "C03DA01", "category": "保钾利尿剂"},
    {"name_cn": "华法林钠", "name_en": "Warfarin Sodium", "atc_code": "B01AA03", "category": "口服抗凝药"},
]

ALIASES: dict[str, list[str]] = {
    "阿司匹林": ["阿司匹林肠溶片", "拜阿司匹灵", "Aspirin", "aspirin", "ASA"],
    "华法林": ["华法林钠", "华法林片", "Warfarin", "warfarin"],
    "氯吡格雷": ["波立维", "Plavix", "Clopidogrel"],
    "阿托伐他汀": ["立普妥", "Lipitor", "Atorvastatin"],
    "辛伐他汀": ["舒降之", "Zocor", "Simvastatin"],
    "瑞舒伐他汀": ["可定", "Crestor", "Rosuvastatin"],
    "氨氯地平": ["络活喜", "Norvasc", "Amlodipine"],
    "硝苯地平": ["拜新同", "Adalat", "Nifedipine"],
    "缬沙坦": ["代文", "Diovan", "Valsartan"],
    "厄贝沙坦": ["安博维", "Avapro", "Irbesartan"],
    "美托洛尔": ["倍他乐克", "Betaloc", "Metoprolol"],
    "比索洛尔": ["康忻", "Bisoprolol", "Concor"],
    "二甲双胍": ["格华止", "Glucophage", "Metformin"],
    "格列美脲": ["亚莫利", "Amaryl", "Glimepiride"],
    "阿卡波糖": ["拜糖苹", "Glucobay", "Acarbose"],
    "西格列汀": ["捷诺维", "Januvia", "Sitagliptin"],
    "阿莫西林": ["阿莫仙", "Amoxil", "Amoxicillin"],
    "头孢呋辛": ["西力欣", "Zinnat", "Cefuroxime"],
    "左氧氟沙星": ["可乐必妥", "Cravit", "Levofloxacin"],
    "甲硝唑": ["灭滴灵", "Metronidazole"],
    "布洛芬": ["芬必得", "Ibuprofen", "Advil"],
    "对乙酰氨基酚": ["扑热息痛", "泰诺", "Paracetamol", "Acetaminophen", "Tylenol"],
    "阿普唑仑": ["佳静安定", "Alprazolam", "Xanax"],
    "艾司唑仑": ["舒乐安定", "Estazolam"],
    "舍曲林": ["左洛复", "Zoloft", "Sertraline"],
    "帕罗西汀": ["赛乐特", "Paxil", "Paroxetine"],
    "奥美拉唑": ["洛赛克", "Losec", "Omeprazole"],
    "雷贝拉唑": ["波利特", "Pariet", "Rabeprazole"],
    "莫沙必利": ["加斯清", "Mosapride"],
    "呋塞米": ["速尿", "Lasix", "Furosemide"],
    "氢氯噻嗪": ["双克", "Hydrochlorothiazide", "HCTZ"],
    "螺内酯": ["安体舒通", "Spironolactone", "Aldactone"],
}

DDI_PAIRS: list[dict] = [
    # 心血管
    {"drug_a": "阿司匹林", "drug_b": "华法林", "severity": "高", "mechanism": "抗血小板与抗凝作用叠加，显著增加出血风险", "advice": "联用需严密监测凝血功能与出血征象，请遵医嘱调整", "source": "DrugBank / NMPA说明书"},
    {"drug_a": "阿司匹林", "drug_b": "氯吡格雷", "severity": "高", "mechanism": "双重抗血小板作用，出血风险增加", "advice": "仅在明确适应证（如急性冠脉综合征术后）下由医生决定是否联用", "source": "DrugBank"},
    {"drug_a": "华法林", "drug_b": "阿莫西林", "severity": "中", "mechanism": "抗生素可能改变肠道菌群，影响维生素K合成，增强华法林作用", "advice": "联用期间加强 INR 监测", "source": "Lexicomp"},
    {"drug_a": "华法林", "drug_b": "甲硝唑", "severity": "高", "mechanism": "甲硝唑抑制华法林代谢，增加出血风险", "advice": "避免自行联用，需医生评估并监测 INR", "source": "DrugBank"},
    {"drug_a": "阿托伐他汀", "drug_b": "克拉霉素", "severity": "中", "mechanism": "CYP3A4 强抑制剂显著升高他汀血药浓度，肌病/横纹肌溶解风险增加", "advice": "避免联用或换用不经 CYP3A4 代谢的他汀", "source": "FDA / DrugBank"},
    {"drug_a": "辛伐他汀", "drug_b": "克拉霉素", "severity": "高", "mechanism": "CYP3A4 强抑制剂显著升高辛伐他汀血药浓度", "advice": "禁忌或严格限制剂量，需医生评估", "source": "FDA说明书"},
    {"drug_a": "氨氯地平", "drug_b": "辛伐他汀", "severity": "中", "mechanism": "氨氯地平抑制辛伐他汀代谢，升高肌病风险", "advice": "辛伐他汀日剂量不超过 20 mg", "source": "FDA说明书"},
    {"drug_a": "美托洛尔", "drug_b": "氨氯地平", "severity": "低", "mechanism": "联用可增强降压效果，也可能增加心动过缓风险", "advice": "监测血压与心率", "source": "临床用药须知"},
    # 降糖
    {"drug_a": "二甲双胍", "drug_b": "碘造影剂", "severity": "中", "mechanism": "造影剂可能诱发肾功能不全，增加乳酸酸中毒风险", "advice": "造影检查前后遵医嘱暂停二甲双胍", "source": "NMPA说明书"},
    {"drug_a": "格列美脲", "drug_b": "阿司匹林", "severity": "中", "mechanism": "阿司匹林可能增强降糖作用，增加低血糖风险", "advice": "监测血糖，尤其是初始联用时", "source": "DrugBank"},
    {"drug_a": "胰岛素", "drug_b": "β受体阻滞剂", "severity": "中", "mechanism": "β受体阻滞剂可能掩盖低血糖心悸症状，延迟低血糖恢复", "advice": "密切监测血糖，选择高选择性β受体阻滞剂", "source": "临床用药须知"},
    # NSAIDs
    {"drug_a": "布洛芬", "drug_b": "阿司匹林", "severity": "中", "mechanism": "布洛芬可能竞争性抑制阿司匹林对血小板的不可逆抑制", "advice": "如需长期联用请间隔服用或咨询医生/药师", "source": "FDA消费者指南"},
    {"drug_a": "布洛芬", "drug_b": "华法林", "severity": "高", "mechanism": "NSAIDs 胃肠道损伤与抗凝叠加，出血风险显著增加", "advice": "避免自行联用，需医生评估", "source": "DrugBank"},
    # 精神神经
    {"drug_a": "舍曲林", "drug_b": "华法林", "severity": "中", "mechanism": "SSRIs 可能影响血小板功能，与华法林联用出血风险增加", "advice": "监测 INR 与出血征象", "source": "Lexicomp"},
    {"drug_a": "帕罗西汀", "drug_b": "阿司匹林", "severity": "中", "mechanism": "SSRIs 与 NSAIDs/抗血小板药联用增加出血风险", "advice": "关注消化道出血征象", "source": "DrugBank"},
    {"drug_a": "阿普唑仑", "drug_b": "艾司唑仑", "severity": "高", "mechanism": "同属苯二氮䓬类，中枢抑制作用叠加，嗜睡、呼吸抑制风险增加", "advice": "避免同类药物叠加使用", "source": "Beers Criteria"},
    # 消化
    {"drug_a": "奥美拉唑", "drug_b": "氯吡格雷", "severity": "中", "mechanism": "奥美拉唑抑制 CYP2C19，可能减弱氯吡格雷抗血小板活性", "advice": "如需联用 PPI，可优先考虑雷贝拉唑或泮托拉唑", "source": "FDA / 临床指南"},
    {"drug_a": "莫沙必利", "drug_b": "红霉素", "severity": "中", "mechanism": "两者均延长 QT 间期，联用增加心律失常风险", "advice": "避免联用或监测心电图", "source": "DrugBank"},
    # 利尿与降压
    {"drug_a": "氢氯噻嗪", "drug_b": "螺内酯", "severity": "低", "mechanism": "排钾与保钾利尿剂联用可减少电解质紊乱，但仍需监测血钾", "advice": "定期监测电解质与肾功能", "source": "临床用药须知"},
    {"drug_a": "呋塞米", "drug_b": "氨基糖苷类抗生素", "severity": "高", "mechanism": "袢利尿剂与氨基糖苷类均有耳肾毒性，联用加重损害", "advice": "避免联用或严密监测听力/肾功能", "source": "DrugBank"},
]

FOOD_DRUG_PAIRS: list[dict] = [
    {"drug": "华法林", "food": "葡萄柚", "effect": "葡萄柚抑制 CYP3A4 与 P-gp，可能升高华法林血药浓度，增加出血风险", "advice": "服药期间避免大量食用葡萄柚及其制品", "source": "FDA消费者指南"},
    {"drug": "阿托伐他汀", "food": "葡萄柚", "effect": "葡萄柚显著升高他汀血药浓度，增加肌病风险", "advice": "服药期间避免食用葡萄柚", "source": "FDA消费者指南"},
    {"drug": "辛伐他汀", "food": "葡萄柚", "effect": "葡萄柚显著升高辛伐他汀血药浓度", "advice": "服药期间避免食用葡萄柚", "source": "FDA消费者指南"},
    {"drug": "二甲双胍", "food": "酒精", "effect": "酒精增加乳酸酸中毒与低血糖风险", "advice": "服药期间避免大量饮酒", "source": "NMPA说明书"},
    {"drug": "格列美脲", "food": "酒精", "effect": "酒精可能诱发双硫仑样反应或严重低血糖", "advice": "服药期间避免饮酒", "source": "NMPA说明书"},
    {"drug": "甲硝唑", "food": "酒精", "effect": "双硫仑样反应：面红、心悸、呕吐、低血压", "advice": "用药期间及停药后至少3天内禁酒", "source": "NMPA说明书"},
    {"drug": "头孢呋辛", "food": "酒精", "effect": "部分头孢菌素可能引起双硫仑样反应", "advice": "用药期间及停药后7天内避免饮酒", "source": "NMPA说明书"},
    {"drug": "左氧氟沙星", "food": "含钙食物/奶制品", "effect": "钙、镁、铝等多价阳离子螯合喹诺酮，降低吸收", "advice": "服药前后2小时避免大量奶制品、钙片、抗酸药", "source": "NMPA说明书"},
    {"drug": "阿莫西林", "food": "益生菌/酸奶", "effect": "抗生素可能杀灭益生菌，降低酸奶中益生菌作用", "advice": "间隔2小时以上服用", "source": "临床用药须知"},
    {"drug": "阿司匹林", "food": "空腹/刺激性食物", "effect": "阿司匹林对胃黏膜有刺激，空腹服用增加胃痛/出血风险", "advice": "肠溶片建议餐前服用，普通片建议餐后服用，具体遵医嘱", "source": "NMPA说明书"},
    {"drug": "布洛芬", "food": "空腹", "effect": "空腹服用增加胃肠道刺激", "advice": "建议随餐或餐后服用", "source": "NMPA说明书"},
    {"drug": "对乙酰氨基酚", "food": "酒精", "effect": "饮酒增加肝损伤风险", "advice": "服药期间避免饮酒", "source": "FDA消费者指南"},
    {"drug": "氨氯地平", "food": "葡萄柚", "effect": "葡萄柚可能轻度升高氨氯地平血药浓度", "advice": "建议避免大量食用葡萄柚", "source": "FDA消费者指南"},
]

ELDERLY_RISK_RULES: list[dict] = [
    {"drug": "阿普唑仑", "risk_type": "中枢神经系统抑制/跌倒风险", "reason": "苯二氮䓬类在老年人中增加镇静、认知障碍、跌倒与骨折风险", "recommendation": "尽量避免长期使用，如确需使用应选择最低有效剂量并定期评估", "source": "Beers Criteria"},
    {"drug": "艾司唑仑", "risk_type": "中枢神经系统抑制/跌倒风险", "reason": "苯二氮䓬类在老年人中增加镇静、跌倒与骨折风险", "recommendation": "避免作为失眠首选，优先考虑非药物治疗", "source": "Beers Criteria"},
    {"drug": "阿米替林", "risk_type": "抗胆碱能作用", "reason": "三环类抗抑郁药抗胆碱能强，老年人易出现尿潴留、便秘、认知障碍", "recommendation": "避免使用", "source": "Beers Criteria"},
    {"drug": "苯海索", "risk_type": "抗胆碱能作用", "reason": "抗胆碱能药物在老年人中禁忌或慎用", "recommendation": "避免用于帕金森病以外的适应证", "source": "Beers Criteria"},
    {"drug": "布洛芬", "risk_type": "胃肠道/肾脏/心血管风险", "reason": "NSAIDs 长期使用增加消化道出血、肾功能损害、心血管事件风险", "recommendation": "长期使用需加用胃黏膜保护剂并监测肾功能", "source": "Beers Criteria"},
    {"drug": "吲哚美辛", "risk_type": "胃肠道/肾脏/心血管风险", "reason": "NSAIDs 中风险较高", "recommendation": "避免长期使用", "source": "Beers Criteria"},
    {"drug": "哌替啶", "risk_type": "中枢神经毒性", "reason": "代谢产物去甲哌替啶在老年人中易蓄积，导致癫痫样发作", "recommendation": "避免使用", "source": "Beers Criteria"},
    {"drug": "氯苯那敏", "risk_type": "抗胆碱能/认知障碍", "reason": "第一代抗组胺药具有较强的抗胆碱能作用", "recommendation": "避免使用", "source": "Beers Criteria"},
    {"drug": "异丙嗪", "risk_type": "抗胆碱能/跌倒", "reason": "吩噻嗪类抗组胺药在老年人中风险高", "recommendation": "避免使用", "source": "Beers Criteria"},
    {"drug": "华法林", "risk_type": "出血风险", "reason": "老年人对华法林更敏感，出血风险增加", "recommendation": "严格监测 INR，评估出血与栓塞风险", "source": "Beers Criteria / NMPA说明书"},
    {"drug": "格列美脲", "risk_type": "低血糖风险", "reason": "长效磺脲类在老年人中低血糖风险高", "recommendation": "优先选择低血糖风险更小的降糖药", "source": "Beers Criteria"},
    {"drug": "格列本脲", "risk_type": "低血糖风险", "reason": "长效且代谢产物有活性，老年人低血糖风险高", "recommendation": "避免使用", "source": "Beers Criteria"},
    {"drug": "呋塞米", "risk_type": "电解质紊乱/脱水", "reason": "老年人对利尿剂敏感，易出现低钾、脱水、体位性低血压", "recommendation": "从小剂量开始，定期监测电解质与肾功能", "source": "NMPA说明书"},
    {"drug": "氢氯噻嗪", "risk_type": "电解质紊乱/跌倒", "reason": "长期使用可导致低钠、低钾、体位性低血压", "recommendation": "定期监测电解质，注意跌倒预防", "source": "NMPA说明书"},
    {"drug": "美托洛尔", "risk_type": "心动过缓/跌倒", "reason": "老年人心脏传导系统退行性变，更易出现心动过缓", "recommendation": "监测心率血压，避免突然停药", "source": "NMPA说明书"},
    {"drug": "地高辛", "risk_type": "中毒风险", "reason": "老年人肾功能下降，地高辛清除减慢，治疗窗窄", "recommendation": "低剂量起始，监测血药浓度与心电图", "source": "Beers Criteria"},
]

DRUG_LABELS: dict[str, dict[str, str]] = {
    "阿司匹林": {
        "适应症": "用于预防和治疗缺血性心脑血管疾病，如冠心病、脑梗死等。",
        "用法用量": "通常每日一次，每次 75~100 mg，肠溶片建议餐前服用。具体剂量请遵医嘱。",
        "常见不良反应": "胃肠道不适、胃痛、恶心，少数患者可能出现出血（如牙龈出血、黑便）。",
        "禁忌": "对阿司匹林过敏、活动性消化道出血、严重肝肾功能不全、血友病等患者禁用。",
        "注意事项": "手术前应告知医生正在服用；饮酒会增加胃出血风险；不要自行停药。",
    },
    "二甲双胍": {
        "适应症": "用于 2 型糖尿病，尤其适合超重或肥胖患者。",
        "用法用量": "通常从小剂量开始，随餐或餐后服用，逐渐加量以减少胃肠不适。",
        "常见不良反应": "恶心、腹泻、腹胀、食欲减退，多可随用药时间延长而缓解。",
        "禁忌": "严重肾功能不全、酸中毒、严重感染、酗酒者禁用。",
        "注意事项": "用药期间避免大量饮酒；造影检查前后可能需要暂停，遵医嘱。",
    },
    "华法林": {
        "适应症": "用于预防和治疗血栓栓塞性疾病，如房颤、深静脉血栓、心脏瓣膜置换术后。",
        "用法用量": "个体化剂量，需根据 INR 监测结果调整，通常每日一次，固定时间服用。",
        "常见不良反应": "出血（鼻出血、牙龈出血、黑便、瘀斑），严重时可危及生命。",
        "禁忌": "活动性出血、严重高血压、近期手术、妊娠早期等禁用。",
        "注意事项": "需定期监测 INR；很多药物和食物会影响疗效，新增或停用任何药物请先咨询医生/药师。",
    },
    "阿托伐他汀": {
        "适应症": "用于高胆固醇血症、冠心病等心血管疾病的二级预防。",
        "用法用量": "通常每晚一次，常用剂量 10~20 mg，具体遵医嘱。",
        "常见不良反应": "肌肉酸痛、乏力、肝功能异常，极少数出现横纹肌溶解。",
        "禁忌": "活动性肝病、妊娠期及哺乳期禁用。",
        "注意事项": "用药期间避免大量饮用葡萄柚汁；出现不明原因肌肉疼痛及时就医。",
    },
    "氨氯地平": {
        "适应症": "用于高血压和慢性稳定型心绞痛。",
        "用法用量": "通常每日一次，每次 5~10 mg，晨起服用。",
        "常见不良反应": "踝部水肿、头痛、面部潮红、心悸、疲劳。",
        "禁忌": "严重低血压、对氨氯地平过敏者禁用。",
        "注意事项": "不要突然停药；肝功能不全者慎用；避免大量食用葡萄柚。",
    },
    "布洛芬": {
        "适应症": "用于缓解轻至中度疼痛（如头痛、牙痛、关节痛）和退热。",
        "用法用量": "成人每次 0.2~0.4 g，每 4~6 小时一次，每日不超过 1.2 g（OTC）或遵医嘱。",
        "常见不良反应": "胃痛、恶心、消化不良，长期大量使用可伤肾、升高血压。",
        "禁忌": "活动性消化道溃疡、严重心肾功能不全、阿司匹林哮喘禁用。",
        "注意事项": "饭后服用可减少胃刺激；避免与阿司匹林长期联用；孕妇慎用。",
    },
    "甲硝唑": {
        "适应症": "用于治疗厌氧菌感染及某些原虫感染。",
        "用法用量": "成人通常每次 0.2~0.4 g，每日 3 次，疗程遵医嘱。",
        "常见不良反应": "恶心、金属味、食欲减退、头痛，尿液可能变深。",
        "禁忌": "妊娠早期、哺乳期、对本品过敏者禁用。",
        "注意事项": "用药期间及停药后 3 天内禁止饮酒；可引起双硫仑样反应。",
    },
    "舍曲林": {
        "适应症": "用于治疗抑郁症、强迫症、惊恐障碍等。",
        "用法用量": "通常每日一次，早晨或晚上服用，剂量遵医嘱逐渐调整。",
        "常见不良反应": "恶心、腹泻、头痛、失眠或嗜睡、性功能障碍。",
        "禁忌": "正在服用单胺氧化酶抑制剂（MAOI）者禁用。",
        "注意事项": "起效需 2~4 周；不要突然停药；出现自杀意念需立即就医。",
    },
}
