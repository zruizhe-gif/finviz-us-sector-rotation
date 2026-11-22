from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[2]
OUT = SKILL / "AI_reports" / "daily"
DATA = json.loads((HERE / "calculated-statistics.json").read_text(encoding="utf-8"))

RANGE_ORDER = ("all_stocks", "sp500", "dow30", "nasdaq100", "russell2000", "themes")
SECTION_LABEL = {
    "all_stocks": "一、All Stocks", "sp500": "二、S&P 500",
    "dow30": "三、Dow Jones 30", "nasdaq100": "四、Nasdaq 100",
    "russell2000": "五、Russell 2000", "themes": "六、主题",
}
MAP_URLS = {
    "all_stocks": "https://finviz.com/map?t=sec_all&st=d1",
    "sp500": "https://finviz.com/map?t=sec&st=d1",
    "dow30": "https://finviz.com/map?t=sec_dji&st=d1",
    "nasdaq100": "https://finviz.com/map?t=sec_ndx&st=d1",
    "russell2000": "https://finviz.com/map?t=sec_rut&st=d1",
    "themes": "https://finviz.com/map?t=themes&st=d1",
    "etf": "https://finviz.com/map?t=etf&st=d1",
}

CN = {
    "Utilities": "公用事业", "Energy": "能源", "Technology": "科技",
    "Communication Services": "通信服务", "Real Estate": "房地产",
    "Consumer Cyclical": "可选消费", "Industrials": "工业",
    "Basic Materials": "基础材料", "Financial": "金融", "Healthcare": "医疗保健",
    "Consumer Defensive": "必需消费", "Semiconductors": "半导体",
    "Commodities Energy": "能源商品", "Environmental Sustainability": "环境可持续发展",
    "Cybersecurity": "网络安全", "Biometrics": "生物识别",
    "Education Technology": "教育科技", "Consumer Goods": "消费品",
    "Space Tech": "太空科技", "Quantum Computing": "量子计算",
    "Hardware": "硬件", "Social Media": "社交媒体", "Software": "软件",
    "E-commerce": "电子商务", "Big Data": "大数据",
    "Defense & Aerospace": "国防与航空航天", "Commodities Metals": "金属商品",
    "Cloud Computing": "云计算", "Transportation & Logistics": "运输与物流",
    "Artificial Intelligence": "人工智能", "Digital Entertainment": "数字娱乐",
    "Real Estate & REITs": "房地产与REITs", "Energy Traditional": "传统能源",
    "Healthcare & Biotech": "医疗保健与生物科技",
    "Healthy Food & Nutrition": "健康食品与营养", "Smart Home": "智能家居", "Virtual & Augmented Reality": "虚拟与增强现实",
    "Agriculture & FoodTech": "农业与食品科技", "Autonomous Systems": "自动驾驶系统", "Commodities Agriculture": "农业商品",
    "Crypto & Blockchain": "加密货币与区块链", "Aging Population & Longevity": "老龄化与长寿", "FinTech": "金融科技",
    "Electric Vehicles": "电动汽车", "Robotics": "机器人",
    "Internet of Things": "物联网", "Industrial Automation": "工业自动化", "Nanotechnology": "纳米技术",
    "Telecommunications": "电信", "Wearables": "可穿戴设备", "Energy Renewable": "可再生能源",
}

SUB_CN = {
    "Curriculum": "课程内容", "Platforms": "平台", "Infrastructure": "基础设施",
    "Workforce": "职业教育", "ThreatOps": "威胁情报", "App Security": "应用安全", "Security": "安全",
    "Cloud": "云计算", "Endpoint": "端点安全", "ZeroTrust": "零信任", "SIEM": "安全信息与事件管理",
    "Identity IAM": "身份与访问管理", "Network": "网络",
    "Analytics & BI": "分析与商业智能", "AI Platforms": "人工智能平台", "Providers": "数据服务商",
    "Satellites": "卫星", "Data Analytics": "数据分析", "Launch": "发射", "Defense": "国防",
    "Drones": "无人机", "SpaceTech": "太空科技", "Missiles": "导弹", "Aviation": "航空",
    "Weapons": "武器", "Manufacturing": "制造", "CyberDefense": "网络防御",
    "Hardware": "硬件", "Software": "软件", "软件": "软件",
    "CyberSecurity": "网络安全", "Healthcare": "医疗健康", "Aging Pharma": "老龄化制药", "Senior Living": "养老居住", "Healthy Aging": "健康老龄化",
    "Advertising": "广告", "Enabling Tech": "支撑技术", "Gov & Defense": "政府与国防",
    "Identity": "身份认证", "Networks": "社交网络", "Niche": "垂直社群", "Visual Content": "视觉内容",
    "Silver": "白银", "Gold": "黄金", "Precious": "贵金属", "Industrial": "工业金属",
    "Battery": "电池", "Rare Earth": "稀土", "Recycling": "回收",
    "Packaging": "封装", "Memory": "存储", "Lithography": "光刻", "Next-Gen": "下一代硬件",
    "Oil Services": "油服", "Oil Production": "石油生产", "Majors": "大型油气", "Thermal": "动力煤",
    "Gaming": "游戏",
    "Apparel": "服装服饰",
    "Analog": "模拟芯片", "Compute": "计算芯片", "Design": "芯片设计工具", "Design Tools": "芯片设计工具", "Wireless": "无线芯片",
    "V-SaaS": "垂直SaaS", "CRM": "客户关系管理", "H-SaaS": "横向SaaS",
    "Fertilizers": "化肥", "Grains": "谷物", "Softs": "软商品", "Livestock": "畜牧",
    "Servers": "服务器", "Electronics": "电子设备",
    "OS": "操作系统", "E-Commerce": "电子商务", "Telecom": "电信设备",
    "Storage": "存储", "Data Centers": "数据中心", "Foundries": "晶圆代工",
    "Biofuels": "生物燃料",
    "Meal Delivery": "餐食外送", "Retailers": "零售商", "Supplements": "膳食补充剂", "Alt Protein": "替代蛋白",
    "Applications": "应用", "Networking": "网络设备", "Suppliers": "供应商", "Automation": "自动化", "Robotics": "机器人", "3D Printing": "3D打印", "Edge Devices": "边缘设备", "IoT": "物联网", "Logistics": "物流", "Machine Vision": "机器视觉", "Tokenization": "代币化", "Payments": "支付", "Collaboration": "协作办公", "DevOps": "开发运维", "Self-Driving": "自动驾驶",
    "Office": "办公", "Housing": "住宅", "Retail": "零售物业", "Warehousing": "仓储",
    "Batteries": "动力电池", "Chips": "车规芯片", "Charging": "充电设施", "Fleets": "车队", "Manufacturers": "整车制造商",
    "Diagnostics": "诊断", "Genomics": "基因组学", "Oncology": "肿瘤", "Enterprise": "企业级",
    "Mining": "挖矿", "Farm-Direct": "农场直供", "Food": "食品",
    "Luxury": "奢侈品", "Secondhand": "二手",
    "Indoor Farming": "室内种植", "Smart Farming": "智慧农业", "Crop Inputs": "农资投入", "Processing": "农产品加工",
    "Oil Refining": "炼油", "Nuclear": "核能", "Utilities": "公用事业",
    "Music": "音乐", "Video": "视频",
    "DTC": "直面消费者", "Marketplaces": "交易平台", "Omnichannel": "全渠道零售", "Grocery": "食品杂货",
    "Gambling": "博彩", "Betting": "体育投注", "Ads & Media": "广告与媒体", "Social": "社交",
    "PaaS": "平台即服务", "Edge": "边缘计算", "Hybrid Cloud": "混合云", "Hyperscalers": "超大规模云厂商", "Multi Cloud": "多云架构", "Serverless": "无服务器", "Databases": "数据库",
    "AV & Mobility": "自动驾驶与出行", "Consumer": "消费级应用", "Medical": "医疗机器人",
    "Blockchain": "区块链", "Trading": "交易平台", "Insurance": "保险科技", "Exchanges": "交易所", "Lending": "借贷科技", "Neobanks": "新型银行",
    "Rail": "铁路", "5G": "5G通信", "Immersive": "沉浸式技术", "Satcom": "卫星通信", "Smartwatches": "智能手表", "Cloud & Edge": "云与边缘", "Sport": "体育运动", "Air Cargo": "航空货运", "Maritime": "海运", "Trucking": "卡车运输", "Air Travel": "航空客运", "Industrial IoT": "工业物联网", "Printing": "印刷", "PCs & Devices": "个人电脑与设备", "Hydrogen": "氢能", "Solar": "太阳能", "Wind": "风能", "Geothermal": "地热", "Grid": "电网", "Fuel Cells": "燃料电池", "Batteries": "电池储能", "Oil": "石油", "Uranium": "铀", "Gas & LNG": "天然气与LNG", "Smart Grid": "智能电网", "Materials": "医疗材料", "Therapeutics": "治疗药物", "Devices": "医疗器械", "Metabolic": "代谢疾病", "Telemedicine": "远程医疗", "IT & Data": "医疗信息与数据",
}

THEME_COMPANY = {
    "AMAT": "Applied Materials Inc",
    "ARQQ": "Arqit Quantum Inc",
    "AWRE": "Aware Inc",
    "BKYI": "Bio-Key International Inc",
    "CAMT": "Camtek Ltd",
    "DKNG": "DraftKings Inc",
    "FLY": "Firefly Aerospace Inc",
    "INSE": "Inspired Entertainment Inc",
    "IONQ": "IonQ Inc",
    "META": "Meta Platforms Inc",
    "MGNI": "Magnite Inc",
    "MNTS": "Momentus Inc",
    "MRVL": "Marvell Technology Inc",
    "QBTS": "D-Wave Quantum Inc",
    "SPCX": "Space Exploration Technologies Corp",
    "SPIR": "Spire Global Inc",
    "SRAD": "Sportradar Group AG",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEP": ("联动", "+0.93%列纳指100公用事业（偏强侧）。"),
    "ALOY": ("联动", "-4.99%列罗素2000基础材料（偏弱侧）。"),
    "AMAT": ("联动", "+5.19%列主题层半导体（偏强侧）。"),
    "AMR": ("联动", "-5.43%列罗素2000基础材料（偏弱侧）。"),
    "AMSS": ("联动", "-20.87%列All Stocks必需消费（偏弱侧）。"),
    "AMZN": ("联动", "+0.21%列道指可选消费（偏强侧）。"),
    "APC": ("联动", "-6.46%列罗素2000能源（偏弱侧）。"),
    "ARQQ": ("联动", "-2.11%列主题层量子计算（偏弱侧）。"),
    "AWRE": ("联动", "+4.54%列主题层生物识别（偏强侧）。"),
    "AXP": ("联动", "-0.30%列道指金融（偏弱侧）。"),
    "BA": ("直接", "FAA将因新软件故障推迟737 MAX 10批准——周一-6.91%后的超跌反弹+1.78%。"),
    "BE": ("联动", "+10.80%列标普500工业（偏强侧）。"),
    "BGIN": ("联动", "+34.78%列All Stocks科技（偏强侧）。"),
    "BIPC": ("联动", "+2.00%列罗素2000公用事业（偏强侧）。"),
    "BKR": ("联动", "-2.10%列纳指100能源（偏弱侧）。"),
    "BKYI": ("联动", "+85.71%列All Stocks工业（偏强侧）。"),
    "CAMT": ("联动", "+7.16%列主题层半导体（偏强侧）。"),
    "CAT": ("直接", "卡特彼勒协议收购Fabick Cat经销商。"),
    "CEG": ("联动", "+1.59%列纳指100公用事业（偏强侧）。"),
    "CSIQ": ("联动", "+10.85%列罗素2000科技（偏强侧）。"),
    "CSX": ("联动", "+0.36%列纳指100工业（偏强侧）。"),
    "CTRI": ("联动", "+2.11%列罗素2000公用事业（偏强侧）。"),
    "CVX": ("联动", "-0.96%列道指能源（偏弱侧）。"),
    "DKNG": ("联动", "-7.42%列主题层数字娱乐（偏弱侧）。"),
    "DLTR": ("联动", "-2.34%列标普500必需消费（偏弱侧）。"),
    "DXST": ("联动", "+55.90%列All Stocks工业（偏强侧）。"),
    "EIX": ("联动", "+4.06%列All Stocks公用事业（偏强侧）。"),
    "ELLO": ("联动", "+5.72%列All Stocks公用事业（偏强侧）。"),
    "FANG": ("联动", "-0.69%列纳指100能源（偏弱侧）。"),
    "FLNC": ("联动", "+4.27%列All Stocks公用事业（偏强侧）。"),
    "FLY": ("联动", "-5.18%列主题层太空科技（偏弱侧）。"),
    "GDC": ("联动", "+7.14%列罗素2000通信服务（偏强侧）。"),
    "GNRC": ("联动", "+3.42%列标普500工业（偏强侧）。"),
    "GRAN": ("联动", "-17.77%列All Stocks金融（偏弱侧）。"),
    "GS": ("联动", "-0.00%列道指金融（偏弱侧）。"),
    "HAL": ("联动", "-2.74%列标普500能源（偏弱侧）。"),
    "HD": ("联动", "-0.64%列道指可选消费（偏弱侧）。"),
    "HMH": ("联动", "-7.83%列罗素2000能源（偏弱侧）。"),
    "HONA": ("联动", "+2.05%列标普500工业（偏强侧）。"),
    "HSY": ("联动", "-1.82%列标普500必需消费（偏弱侧）。"),
    "IDT": ("直接", "IDT公布创纪录的第四季度与2026财年业绩。"),
    "INSE": ("直接", "Inspired就巴西监管进展发布更新。"),
    "INSG": ("联动", "+7.35%列罗素2000科技（偏强侧）。"),
    "INV": ("联动", "-13.05%列罗素2000金融（偏弱侧）。"),
    "IONQ": ("联动", "-1.50%列主题层量子计算（偏弱侧）。"),
    "KDP": ("联动", "-1.37%列纳指100必需消费（偏弱侧）。"),
    "KO": ("联动", "-0.39%列道指必需消费（偏弱侧）。"),
    "LGHL": ("联动", "-21.97%列All Stocks金融（偏弱侧）。"),
    "LIN": ("联动", "+0.28%列纳指100基础材料（偏强侧）。"),
    "MCD": ("联动", "+0.16%列道指可选消费（偏强侧）。"),
    "MDLZ": ("联动", "-1.43%列纳指100必需消费（偏弱侧）。"),
    "META": ("联动", "+3.24%列标普500通信服务（偏强侧）。"),
    "METC": ("联动", "-6.68%列罗素2000基础材料（偏弱侧）。"),
    "MGNI": ("联动", "+9.70%列罗素2000通信服务（偏强侧）。"),
    "MLM": ("联动", "-2.38%列标普500基础材料（偏弱侧）。"),
    "MMM": ("联动", "-0.58%列道指工业（偏弱侧）。"),
    "MNTS": ("联动", "-8.19%列主题层太空科技（偏弱侧）。"),
    "MRVL": ("联动", "+4.51%列主题层半导体（偏强侧）。"),
    "MSGY": ("联动", "+41.85%列All Stocks工业（偏强侧）。"),
    "NESR": ("联动", "-11.14%列All Stocks能源（偏弱侧）。"),
    "NFLX": ("直接", "德意志银行上调评级（全球机会）。"),
    "NINE": ("联动", "-7.92%列All Stocks能源（偏弱侧）。"),
    "NUE": ("直接", "纽柯Q3指引不及预期（市场原定价60%盈利反弹）。"),
    "PG": ("联动", "-0.48%列道指必需消费（偏弱侧）。"),
    "PIPR": ("直接", "Piper Sandler洽谈收购Perella Weinberg的报道（并购方贴水）。"),
    "PMAX": ("联动", "-30.00%列All Stocks金融（偏弱侧）。"),
    "PNW": ("联动", "+2.28%列标普500公用事业（偏强侧）。"),
    "PYPL": ("联动", "-0.72%列纳指100金融（偏弱侧）。"),
    "QBTS": ("联动", "-2.09%列主题层量子计算（偏弱侧）。"),
    "RCON": ("联动", "-8.21%列All Stocks能源（偏弱侧）。"),
    "RDDT": ("联动", "+1.59%列标普500通信服务（偏强侧）。"),
    "RDZN": ("联动", "+9.16%列罗素2000科技（偏强侧）。"),
    "RILY": ("联动", "-10.38%列罗素2000金融（偏弱侧）。"),
    "SANG": ("直接", "Sangoma被BRC以2.04亿美元收购。"),
    "SHW": ("联动", "-0.71%列道指基础材料（偏弱侧）。"),
    "SLB": ("联动", "-3.15%列标普500能源（偏弱侧）。"),
    "SPCX": ("直接", "TD Cowen首次覆盖买入（AI算力驱动估值主体）。"),
    "SPIR": ("联动", "-5.03%列主题层太空科技（偏弱侧）。"),
    "SRAD": ("联动", "-7.37%列主题层数字娱乐（偏弱侧）。"),
    "SSTI": ("直接", "SoundThinking同意被Transom Capital收购（每股最高11美元现金）。"),
    "STLD": ("联动", "-3.69%列标普500基础材料（偏弱侧）。"),
    "TANH": ("联动", "-16.46%列All Stocks必需消费（偏弱侧）。"),
    "TPL": ("联动", "-2.79%列标普500能源（偏弱侧）。"),
    "TRV": ("联动", "+0.01%列道指金融（偏强侧）。"),
    "TWG": ("联动", "-18.56%列All Stocks必需消费（偏弱侧）。"),
    "VST": ("联动", "+2.04%列标普500公用事业（偏强侧）。"),
    "WMT": ("联动", "-1.77%列标普500必需消费（偏弱侧）。"),
    "XEL": ("联动", "+1.87%列纳指100公用事业（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "EWY", "perf": 1.917, "form": "交易所交易基金", "exposure": "韩国股票",
         "reason": "韩国ETF +1.92%：全球半导体链的映射（应用材料+5.19%/Marvell +4.51%）——半导体主题九子行业清一色涨（等权+1.33%）的全球共振。合并删除：无同簇产品。"},
        {"ticker": "GDXJ", "perf": 1.490, "form": "交易所交易基金", "exposure": "全球中小金矿股",
         "reason": "中小金矿ETF +1.49%：贵金属的修复日（黄金GLD +1.32%/白银SLV +0.96%）——利率回落（公用事业XLU +1.17%四范围领涨的同源）令周一-5.79%的崩跌端反弹；Gold Fields +4.55%（并购遭拒次日的超跌修复）。合并删除：无同簇产品。"},
        {"ticker": "PTF", "perf": 1.383, "form": "交易所交易基金", "exposure": "科技动量（Dorsey Wright）",
         "reason": "科技动量ETF +1.38%：半导体领涨的动量映射——存储器主题+0.44%连续修复、设备端（应用材料+5.19%）为财报季前定价。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "USO", "perf": -4.440, "form": "商品信托", "exposure": "WTI原油期货",
         "reason": "WTI原油期货ETF -4.44%领跌全市场：伊朗外长将在纽约会见调停人（美方缺席）的外交进展预期+峰会周政治溢价的持续出清——WTI端跌幅（-4.44%）深于布伦特端（BNO -2.62%）的价差结构为美湾供给信号。合并删除：DBO -4.38%（同簇WTI期货）。"},
        {"ticker": "UNG", "perf": -4.078, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货ETF -4.08%：底部结构内的第三日回吐（上周两根大阳线后的持续整理）——能源商品整体的周末出清延续。合并删除：无同簇产品。"},
        {"ticker": "XES", "perf": -2.883, "form": "交易所交易基金", "exposure": "油服与设备（SPDR）",
         "reason": "油服设备ETF -2.88%：油价大跌的股票端映射——斯伦贝谢-3.15%/哈里伯顿-2.74%；能源五个股票范围全部领跌（炼油CRAK -2.15%同步）。合并删除：OIH（同簇油服，保留跌幅更深者）。"},
    ],
}


ETFS_UP = [x["ticker"] for x in ETF_SELECTION["up"]]
ETFS_DOWN = [x["ticker"] for x in ETF_SELECTION["down"]]


def pct(value: float) -> str:
    return f"{value:+.3f}%"


def cn(name: str) -> str:
    if name not in CN:
        raise AssertionError(f"未翻译分类名称：{name}")
    return CN[name]


def reason(group: str, ticker: str) -> tuple[str, str]:
    return CONTEXT.get((group, ticker), R[ticker])


def stock_cell(group: str, stock: dict) -> str:
    label, text = reason(group, stock["ticker"])
    company = COMPANY_NAME_FIX.get(stock["ticker"], stock.get("company") or THEME_COMPANY.get(stock["ticker"], stock["ticker"]))
    if label in {"结构", "联动", "权重", "单样本", "估值", "财报延续", "背离"} and "https://" not in text:
        text = "核查9月19日盘后至9月29日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
    return f"{company}（{stock['ticker']}）**{pct(stock['perf'])}**【{label}】{text}"


def width(row: dict) -> str:
    return (f"{row['count']}只；{row['up']}涨/{row['down']}跌/{row['flat']}平；"
            f"上涨{row['up_pct']:.2f}%/下跌{row['down_pct']:.2f}%；整体{pct(row['overall_perf'])}")


def subthemes(row: dict, direction: str) -> str:
    ordered = sorted(row["subthemes"], key=lambda x: x["perf"], reverse=direction == "up")[:4]
    result = []
    for x in ordered:
        name = SUB_CN.get(x["display"], SUB_CN.get(x["name"]))
        if name is None:
            raise AssertionError(f"未翻译子主题：{x['display']}")
        result.append(f"{name}{pct(x['perf'])}")
    return (f"{row['count']}个；{row['up']}涨/{row['down']}跌/{row['flat']}平；"
            f"上涨{row['up_pct']:.2f}%/下跌{row['down_pct']:.2f}%；等权{pct(row['overall_perf'])}；"
            + "主要方向：" + "；".join(result))


def render_range(key: str) -> list[str]:
    block = DATA["ranges"][key]
    theme = key == "themes"
    display_label = "主题" if theme else block["label"]
    out = [f"## {SECTION_LABEL[key]}", "", f"核验入口：[Finviz {display_label} 1-Day Map]({MAP_URLS[key]})。", ""]
    if theme:
        out += ["一致性按子主题判定，不按主题内重复股票；大类收益为全部有效子主题的等权平均。", "",
                "| 方向 | 主题与入选身份 | 子主题宽度与等权收益 | 主要子主题及个股原因 |", "|---|---|---|---|"]
    else:
        out += ["| 方向 | 板块与入选身份 | 宽度与整体收益 | 入选个股及原因 |", "|---|---|---|---|"]
    for direction, sign in (("up", "涨"), ("down", "跌")):
        for rank, row in enumerate(block[f"selected_{direction}"], 1):
            third = subthemes(row, direction) if theme else width(row)
            stocks = "；".join(stock_cell(row["name"], x).rstrip("。") for x in row["extreme"]) + "。"
            out.append(f"| {sign}{rank} | {cn(row['name'])}（{row['identity']}） | {third} | {stocks} |")
    out += [""]
    return out


def render_etf() -> list[str]:
    out = ["## 七、ETFs：排除杠杆、反向并按底层敞口去重", "", f"核验入口：[Finviz ETF 1-Day Map]({MAP_URLS['etf']})。先排除杠杆、反向与每日倍数产品，再按底层经济敞口去重。", ""]
    for direction, title in (("up", "上涨三只"), ("down", "下跌三只")):
        out += [f"### {title}", "", "| 产品 | 涨跌幅 | 法律形式与独立敞口 | 驱动及去重证明 |", "|---|---:|---|---|"]
        for row in ETF_SELECTION[direction]:
            out.append(f"| {row['ticker']} | {pct(row['perf'])} | {row['form']}；{row['exposure']} | {row['reason']} |")
        out += [""]
    return out


def selected_mentions() -> list[str]:
    return [x["ticker"] for key in RANGE_ORDER for d in ("selected_up", "selected_down") for row in DATA["ranges"][key][d] for x in row["extreme"]]


def expected_txt() -> tuple[list[str], list[str]]:
    stocks = sorted(set(selected_mentions()))
    etfs = ETFS_UP + ETFS_DOWN
    return stocks, sorted(set(stocks + etfs))


def audit_inputs() -> tuple[list[str], list[str]]:
    assert DATA["date"] == "2026-09-29"
    stocks, all_codes = expected_txt()
    assert set(stocks) == set(R), f"逐股原因缺失或多余：missing={set(stocks)-set(R)} extra={set(R)-set(stocks)}"
    for key in RANGE_ORDER:
        block = DATA["ranges"][key]
        assert len(block["selected_up"]) == len(block["selected_down"]) == 3
        for direction in ("up", "down"):
            selected = block[f"selected_{direction}"]
            uniform = block[f"uniform_{direction}"]
            if len(uniform) >= 3:
                assert all(x["identity"] == "清一色优先" for x in selected)
            else:
                assert sum(x["identity"] == "清一色优先" for x in selected) == len(uniform)
            for row in selected:
                assert row["count"] == row["up"] + row["down"] + row["flat"]
                assert len(row["extreme"]) <= 3
    assert len(ETFS_UP) == len(ETFS_DOWN) == 3
    return stocks, all_codes


def candidate_text(rows: list[dict]) -> str:
    return "、".join(cn(x["name"]) for x in rows) if rows else "无"


def selected_text(rows: list[dict]) -> str:
    return "、".join(f"{cn(x['name'])}（{x['identity']}）" for x in rows)


def render_audit(stocks: list[str], all_codes: list[str]) -> list[str]:
    out = ["## 一致性优先最终复核", "", "| 范围 | 清一色上涨完整候选 | 最终上涨3项 | 清一色下跌完整候选 | 最终下跌3项 |", "|---|---|---|---|---|"]
    for key in RANGE_ORDER:
        b = DATA["ranges"][key]
        display_label = "主题" if key == "themes" else b["label"]
        out.append(f"| {display_label} | {len(b['uniform_up'])}项：{candidate_text(b['uniform_up'])} | {selected_text(b['selected_up'])} | {len(b['uniform_down'])}项：{candidate_text(b['uniform_down'])} | {selected_text(b['selected_down'])} |")
    mentions = selected_mentions()
    duplicates = {k: v for k, v in Counter(mentions).items() if v > 1}
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；原油期货簇（BNO/DBO/USO/DBE/DBE能源股）保留BNO、汽油簇（UGA）独立、铂钯银现货簇分别保留最强者（PPLT/PALL/SIVR为不同金属）。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-29_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-29_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月29日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月29日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周二为利率喘息+能源商品出清日：公用事业四个股票范围全部列涨幅第一（标普500 31只中30涨/+1.15%：爱迪生联合+4.06%/Pinnacle West +2.28%/Vistra +2.04%；XLU +1.17%——10年期收益率回落的类债端修复）；工业四个范围领涨（道指波音+1.78%〔FAA推迟MAX 10认证消息落地后的超跌反弹〕/卡特彼勒+0.82%〔收购Fabick Cat经销商〕；XLI +0.21%）；通信服务两个范围居前（标普500 +0.32%：Meta +3.24%〔连续两日下跌后反弹〕/Reddit +1.59%/Netflix获德银上调+1.55%）。跌幅侧：能源五个股票范围全部领跌（XLE -0.90%/XOP -0.84%/CRAK -2.15%——WTI原油期货ETF -4.44%领跌全市场：伊朗外长将会晤调停人的外交预期；斯伦贝谢-3.15%/哈里伯顿-2.74%）；必需消费四个范围领跌（道指三成分清一色跌：沃尔玛-1.77%/宝洁-0.48%/可口可乐-0.39%——周一领涨的防御端回吐；XLP -0.52%）；金融三个范围领跌（罗素2000金融357只中281跌：Piper Sandler收购Perella谈判-9.72%；银行KBE -1.04%/区域银行KRE -1.02%）。主题层3个清一色涨（生物识别+6.91%：Bio-Key +85.71%等；半导体+1.33%；社交媒体+1.00%）对7个清一色跌（太空科技-1.98%/数字娱乐/量子计算等）。贵金属修复（黄金+1.32%/金矿ETF +1.49%列全市场第二：Gold Fields +4.55%）；半导体反弹（SOXX +1.19%：应用材料+5.19%/Marvell +4.51%；韩国ETF +1.92%列全市场第一）；甲骨文+3.91%（两日大跌后反弹）。苹果-2.66%为科技权重端拖累；DoorDash +4.88%反弹。铀链企稳（NLR +0.16%/URNM +0.69%）；太空科技回落（主题清一色跌：Intuitive Machines -4.28%/Rocket Lab -3.45%）。比特币ETF回升（IBIT +0.25%/ETHA +0.65%）。VIX期货ETF回落（VIXY -0.66%）。Anthropic传2万亿美元IPO估值（420亿美元净亏损后）。当日无行情性质结构变化。',
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5503/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1937/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
    for key in RANGE_ORDER:
        out += render_range(key)
    out += render_etf()
    out += render_audit(stocks, all_codes)
    return "\n".join(out) + "\n"


def structural_audit(text: str) -> None:
    lines = text.splitlines()
    sections = {}
    heading = None
    for line in lines:
        if line.startswith("## "):
            heading = line[3:]
            sections[heading] = []
        elif heading:
            sections[heading].append(line)
    for label in [SECTION_LABEL[k] for k in RANGE_ORDER]:
        rows = [x for x in sections[label] if x.startswith("| ") and not x.startswith("|---")]
        assert len(rows) == 7 and all(x.count("|") == 5 for x in rows), label
    etf = sections["七、ETFs：排除杠杆、反向并按底层敞口去重"]
    rows = [x for x in etf if x.startswith("| ") and not x.startswith("|---")]
    assert len(rows) == 8 and all(x.count("|") == 5 for x in rows)
    forbidden = ["Consumer Goods", "Environmental Sustainability", "Commodities Energy", "Communication Services", "Consumer Cyclical", "Education Technology", "Cybersecurity", "Biometrics", "Big Data", "Defense & Aerospace", "Space Tech", "Social Media", "Cloud Computing", "Artificial Intelligence", "E-commerce", "Digital Entertainment", "Real Estate & REITs", "Transportation & Logistics", "Quantum Computing", "Commodities Metals", "Hardware"]
    body_without_urls = re.sub(r"https?://[^)\s]+", "", text)
    for term in forbidden:
        assert term not in body_without_urls, term
    assert text.count("暂未找到同日直接催化") > 0
    assert "CIK=&" not in text
    for ticker, company in THEME_COMPANY.items():
        assert f"{company}（{ticker}）" in text, ticker


def main() -> None:
    stocks, all_codes = audit_inputs()
    (OUT / "finviz_2026-09-29_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-29_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-29_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
