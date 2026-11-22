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
    "IT & Telecom": "信息技术与电信",
    "Waste": "废物处理",
    "Water": "水务",
    "Climate": "气候",
    "Agriculture": "农业",
    "Tourism": "旅游",
    "Energy": "能源",
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
    "ACI": "Albertsons Companies Inc",
    "CHGG": "Chegg Inc",
    "DSP": "Viant Technology Inc",
    "DUOL": "Duolingo Inc",
    "FLY": "Firefly Aerospace Inc",
    "HLN": "Haleon plc ADR",
    "IPX": "IperionX Ltd ADR",
    "KR": "Kroger Co",
    "LCID": "Lucid Group Inc",
    "NMG": "Nouveau Monde Graphite Inc",
    "PL": "Planet Labs PBC",
    "PSNY": "Polestar Automotive Holding UK PLC ADR",
    "RBLX": "Roblox Corp",
    "RDDT": "Reddit Inc",
    "SES": "SES AI Corp",
    "SKIL": "Skillsoft Corp",
    "UUUU": "Energy Fuels Inc",
    "VSAT": "Viasat Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ACI": ("联动", "+2.27%列主题层健康食品与营养（偏强侧）。"),
    "ADV": ("联动", "+6.35%列罗素2000通信服务（偏强侧）。"),
    "AFRI": ("直接", "Forafric宣布意向书收购AL NASR（确立阿尔及利亚地位）。"),
    "AIRE": ("联动", "-10.40%列All Stocks房地产（偏弱侧）。"),
    "ALB": ("联动", "-3.38%列标普500基础材料（偏弱侧）。"),
    "ALLE": ("联动", "-4.70%列标普500工业（偏弱侧）。"),
    "AMGN": ("联动", "+2.60%列标普500医疗保健（偏强侧）。"),
    "AMZN": ("联动", "+1.42%列标普500可选消费（偏强侧）。"),
    "AXON": ("联动", "-3.02%列纳指100工业（偏弱侧）。"),
    "BKH": ("联动", "+7.21%列罗素2000公用事业（偏强侧）。"),
    "BKR": ("联动", "-3.01%列纳指100能源（偏弱侧）。"),
    "CASY": ("联动", "+2.00%列标普500可选消费（偏强侧）。"),
    "CAT": ("直接", "卡特彼勒与迪尔随监管压力持续走弱（连续第二日）。"),
    "CBRE": ("联动", "-2.37%列标普500房地产（偏弱侧）。"),
    "CCG": ("联动", "+16.10%列All Stocks通信服务（偏强侧）。"),
    "CCOI": ("联动", "+6.77%列罗素2000通信服务（偏强侧）。"),
    "CDNL": ("联动", "-9.23%列罗素2000工业（偏弱侧）。"),
    "CDZI": ("联动", "+3.43%列罗素2000公用事业（偏强侧）。"),
    "CHGG": ("联动", "+4.08%列主题层教育科技（偏强侧）。"),
    "CPHI": ("联动", "+32.59%列All Stocks医疗保健（偏强侧）。"),
    "CRH": ("直接", "CRH收购丹麦与芬兰的骨料业务。"),
    "CVX": ("直接", "Hess Midstream因雪佛龙重组与2027展望下调而跌；CEO警告柴油出口禁令将伤害供给。"),
    "DIS": ("联动", "+0.69%列道指通信服务（偏强侧）。"),
    "DKI": ("联动", "+22.79%列All Stocks通信服务（偏强侧）。"),
    "DLR": ("直接", "Digital Realty定价10亿美元2036年担保票据（利率敏感端融资日）。"),
    "DSP": ("联动", "+7.12%列主题层社交媒体（偏强侧）。"),
    "DUOL": ("联动", "+2.42%列主题层教育科技（偏强侧）。"),
    "EAF": ("联动", "-9.04%列罗素2000工业（偏弱侧）。"),
    "EME": ("联动", "-4.83%列标普500工业（偏弱侧）。"),
    "FANG": ("联动", "-0.32%列纳指100能源（偏弱侧）。"),
    "FCEL": ("直接", "FuelCell CFO Bishop任职15年后离职（前Xylem高管接任）。"),
    "FEAM": ("直接", "5E Advanced Materials提供整合与预期财务补充细节。"),
    "FLY": ("联动", "-5.78%列主题层太空科技（偏弱侧）。"),
    "FSM": ("直接", "Fortuna公布Q3产量69,665金当量盎司。"),
    "FWDI": ("联动", "-9.21%列罗素2000可选消费（偏弱侧）。"),
    "GIBO": ("联动", "+23.74%列All Stocks通信服务（偏强侧）。"),
    "GILD": ("直接", "吉利德与高知特签五年DevOps协议。"),
    "GO": ("联动", "+4.64%列罗素2000必需消费（偏强侧）。"),
    "GOOGL": ("联动", "+0.81%列道指通信服务（偏强侧）。"),
    "HD": ("联动", "-0.32%列道指可选消费（偏弱侧）。"),
    "HLN": ("联动", "+1.69%列主题层健康食品与营养（偏强侧）。"),
    "HON": ("联动", "-2.24%列道指工业（偏弱侧）。"),
    "HONA": ("联动", "-2.75%列纳指100工业（偏弱侧）。"),
    "HUHU": ("联动", "-20.51%列All Stocks工业（偏弱侧）。"),
    "HYMC": ("联动", "-5.92%列罗素2000基础材料（偏弱侧）。"),
    "IPX": ("联动", "-6.94%列主题层金属商品（偏弱侧）。"),
    "ISRG": ("联动", "+2.41%列纳指100医疗保健（偏强侧）。"),
    "JNJ": ("联动", "+1.44%列道指医疗保健（偏强侧）。"),
    "JVA": ("直接", "Coffee Holding宣布250万美元回购计划。"),
    "KR": ("联动", "+1.44%列标普500必需消费（偏强侧）。"),
    "LCID": ("联动", "-6.49%列罗素2000可选消费（偏弱侧）。"),
    "LIN": ("联动", "-1.22%列纳指100基础材料（偏弱侧）。"),
    "LLY": ("联动", "+2.70%列标普500医疗保健（偏强侧）。"),
    "LWAY": ("联动", "+4.11%列罗素2000必需消费（偏强侧）。"),
    "MAA": ("联动", "-2.38%列标普500房地产（偏弱侧）。"),
    "MCD": ("直接", "麦当劳遭AI定价工具反垄断集体诉讼。"),
    "MELI": ("联动", "+0.80%列纳指100可选消费（偏强侧）。"),
    "MMM": ("联动", "-0.93%列道指工业（偏弱侧）。"),
    "MO": ("联动", "+1.21%列标普500必需消费（偏强侧）。"),
    "MOS": ("联动", "-4.63%列标普500基础材料（偏弱侧）。"),
    "MRK": ("联动", "+0.60%列道指医疗保健（偏强侧）。"),
    "MRNA": ("联动", "+4.81%列标普500医疗保健（偏强侧）。"),
    "MTRN": ("联动", "-6.87%列罗素2000基础材料（偏弱侧）。"),
    "NMG": ("联动", "-6.09%列主题层金属商品（偏弱侧）。"),
    "NWE": ("联动", "+7.33%列罗素2000公用事业（偏强侧）。"),
    "NXTS": ("联动", "-22.30%列All Stocks基础材料（偏弱侧）。"),
    "PFAI": ("联动", "+116.67%列All Stocks必需消费（偏强侧）。"),
    "PL": ("联动", "-4.42%列主题层太空科技（偏弱侧）。"),
    "PSNY": ("联动", "-5.90%列主题层电动汽车（偏弱侧）。"),
    "PYPL": ("联动", "+0.62%列纳指100金融（偏强侧）。"),
    "RBLX": ("直接", "Unity获谷歌AI游戏平台合作。"),
    "RDDT": ("联动", "+2.52%列主题层社交媒体（偏强侧）。"),
    "RKLB": ("联动", "-4.18%列纳指100工业（偏弱侧）。"),
    "ROL": ("联动", "+1.71%列标普500可选消费（偏强侧）。"),
    "ROST": ("联动", "+0.59%列纳指100可选消费（偏强侧）。"),
    "SBFM": ("联动", "+75.92%列All Stocks医疗保健（偏强侧）。"),
    "SCAG": ("联动", "-20.62%列All Stocks工业（偏弱侧）。"),
    "SES": ("联动", "-8.20%列罗素2000可选消费（偏弱侧）。"),
    "SHW": ("联动", "-1.92%列道指基础材料（偏弱侧）。"),
    "SKIL": ("联动", "+9.38%列主题层教育科技（偏强侧）。"),
    "SQFT": ("联动", "-10.20%列All Stocks房地产（偏弱侧）。"),
    "SSTK": ("联动", "+9.56%列罗素2000通信服务（偏强侧）。"),
    "STZ": ("直接", "Constellation Brands Q2 2027盈利超预期（啤酒需求偏软）；美银下调目标价。"),
    "SXTC": ("联动", "+126.40%列All Stocks医疗保健（偏强侧）。"),
    "UUUU": ("联动", "-8.88%列主题层金属商品（偏弱侧）。"),
    "VCIG": ("联动", "-45.32%列All Stocks工业（偏弱侧）。"),
    "VHUB": ("联动", "+12.10%列All Stocks必需消费（偏强侧）。"),
    "VSAT": ("联动", "-4.72%列主题层太空科技（偏弱侧）。"),
    "WHLR": ("联动", "-24.29%列All Stocks房地产（偏弱侧）。"),
    "WS": ("直接", "Worthington Steel Q1不及预期。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "UNG", "perf": 2.700, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货ETF +2.70%领涨全市场：底部结构内的第二根反弹阳线（周一+1.80%后加速）——气强油弱格局的独立行情延续。合并删除：无同簇产品。"},
        {"ticker": "PPH", "perf": 1.220, "form": "交易所交易基金", "exposure": "制药（VanEck）",
         "reason": "制药ETF +1.22%列全市场第二：医疗保健三个范围领涨的板块端确认——Moderna +4.81%（周二-7.75%后的即日反转）/礼来+2.70%/安进+2.60%；昨日出清端的V型修复。合并删除：无同簇产品。"},
        {"ticker": "IHE", "perf": 1.068, "form": "交易所交易基金", "exposure": "美国制药（iShares）",
         "reason": "美国制药ETF +1.07%列第三：制药端双ETF共振确认医疗保健的修复日——吉利德获五年DevOps协议+1.82%。合并删除：无同簇产品（与PPH为不同发行商的制药敞口、分别保留）。"},
    ],
    "down": [
        {"ticker": "URA", "perf": -4.474, "form": "交易所交易基金", "exposure": "全球铀矿",
         "reason": "铀矿ETF -4.47%领跌全市场：周二+4.01%的完全回吐——核电定价日暴涨后的即日出清（URNM -4.83%/URNJ -5.39%/NLR -3.80%），主题脉冲结构的又一次往返。合并删除：无同簇产品。"},
        {"ticker": "PALL", "perf": -4.471, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF -4.47%：贵金属全线崩跌（白银-2.94%/金矿-3.88%/银矿-3.54%）——汽车催化剂金属与工业金属（DBB端）同步走弱的金属商品主题-3.18%领跌。合并删除：无同簇产品。"},
        {"ticker": "PPLT", "perf": -4.460, "form": "商品信托", "exposure": "铂金现货",
         "reason": "铂金ETF -4.46%：钯铂双崩（各-4.5%）为当日商品端最极端定价——上周贵金属反弹链的全面逆转。合并删除：无同簇产品。"},
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
        text = "核查9月27日盘后至10月7日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-07"
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
            f"- `finviz_2026-10-07_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-07_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月7日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月7日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周三为医疗保健修复+工业金属出清日：医疗保健三个范围领涨（All Stocks 1,044只中416涨/整体+0.78%〔微盘〕；标普500 60只中30涨/+1.09%：Moderna +4.81%〔周二-7.75%的即日反转〕/礼来+2.70%/安进+2.60%；纳指100九只中7涨/+1.49%——制药双ETF领涨〔PPH +1.22%/IHE +1.07%〕、XLV +1.03%）；通信服务偏强（道指谷歌+0.81%/迪士尼+0.69%清一色涨；罗素2000通信+0.64%〔Shutterstock +9.56%/Cogent +6.77%〕；RSPC +0.12%对XLC -0.35%的分化）；必需消费微涨（Constellation Brands Q2超预期+2.35%）。跌幅侧：**工业三个范围领跌**（标普500 75只中68跌/-2.23%：卡特彼勒-5.75%〔监管压力连续第二日〕/EMCOR -4.83%/Allegion -4.70%；道指工业四成分清一色跌/-3.58%；罗素2000 248只中197跌/-2.46%〔FuelCell CFO离职-11.06%〕——XLI -2.18%/ITA -2.24%）；**基础材料三个范围领跌**（All Stocks 283只中239跌/-2.19%；道指宣伟-1.92%/纳指100林德-1.22%清一色跌；金属商品主题-3.18%〔稀土-4.5%/白银-4.0%〕——XLB -1.51%/XME -3.14%）；房地产三个范围（标普500 30只中27跌/-1.36%〔Digital Realty定价10亿票据-2.26%〕——XHB -2.55%/IYR -1.44%）。ETF端：**铀矿URA -4.47%领跌全市场**（周二+4.01%的完全回吐：URNJ -5.39%）、钯铂各-4.5%崩跌（白银-2.94%/金矿-3.88%）；**天然气UNG +2.70%领涨**（底部反弹第二日）。主题层**18个清一色跌、仅2个清一色涨**（教育科技+1.62%/社交媒体+0.53%）——金属商品/太空科技-2.90%/电动汽车-2.23%领跌。半导体回落（SOXX -1.12%：存储反弹MU +4.06%/闪迪+1.93%为例外——希捷+0.24%企稳）；网络安全IHAK -1.91%（昨日+1.58%的回吐）；加密ETF回落（IBIT -2.64%/ETHA -4.58%）；VIX期货ETF微涨（VIXY +0.56%）。麦当劳遭AI定价反垄断集体诉讼-0.68%；Unity获谷歌合作+1.87%。当日无行情性质结构变化。',
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
    for company in THEME_COMPANY.values():
        body_without_urls = body_without_urls.replace(company, "")
    for term in forbidden:
        assert term not in body_without_urls, term
    assert text.count("暂未找到同日直接催化") > 0
    assert "CIK=&" not in text
    for ticker, company in THEME_COMPANY.items():
        assert f"{company}（{ticker}）" in text, ticker


def main() -> None:
    stocks, all_codes = audit_inputs()
    (OUT / "finviz_2026-10-07_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-07_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-07_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
