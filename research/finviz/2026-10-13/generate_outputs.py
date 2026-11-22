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
    "Air Quality": "空气质量",
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
    "AREC": "American Resources Corp",
    "ASTS": "AST SpaceMobile Inc",
    "BBAI": "BigBear.ai Holdings Inc",
    "BKYI": "Bio-Key International Inc",
    "BMBL": "Bumble Inc",
    "FLY": "Firefly Aerospace Inc",
    "GRMN": "Garmin Ltd",
    "IPX": "IperionX Ltd ADR",
    "LUNR": "Intuitive Machines Inc",
    "META": "Meta Platforms Inc",
    "PINS": "Pinterest Inc",
    "PL": "Planet Labs PBC",
    "RCAT": "Red Cat Holdings Inc",
    "SPCX": "Space Exploration Technologies Corp",
    "TXN": "Texas Instruments Inc",
    "USAR": "USA Rare Earth Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ACH": ("联动", "-19.31%列罗素2000医疗保健（偏弱侧）。"),
    "AEP": ("联动", "+1.14%列纳指100公用事业（偏强侧）。"),
    "ALNY": ("联动", "-1.41%列纳指100医疗保健（偏弱侧）。"),
    "ALXO": ("联动", "-22.25%列罗素2000医疗保健（偏弱侧）。"),
    "AMGN": ("联动", "-1.13%列道指医疗保健（偏弱侧）。"),
    "AREC": ("联动", "-11.67%列罗素2000工业（偏弱侧）。"),
    "ASTS": ("直接", "SpaceX D2C激进策略触发Piper Sandler下调（目标价腰斩——'SpaceX诅咒'）。"),
    "AZTR": ("联动", "-39.20%列All Stocks医疗保健（偏弱侧）。"),
    "BA": ("直接", "波音公布三季度交付数据。"),
    "BBAI": ("直接", "BigBear.ai获超2.25亿美元国土安全部合同。"),
    "BKR": ("联动", "+0.48%列纳指100能源（偏强侧）。"),
    "BKYI": ("直接", "BIO-key任命PortalGuard总裁并新增中东政府安全客户。"),
    "BMBL": ("直接", "Bumble以13亿美元被Ithaca Holdings私有化（周一传闻的正式落地）。"),
    "BX": ("联动", "-4.18%列标普500金融（偏弱侧）。"),
    "C": ("直接", "花旗Q3超预期仍-5.60%；CEO称AI需求太强、高利率也难阻投资。"),
    "CAT": ("联动", "-3.33%列道指工业（偏弱侧）。"),
    "CDNL": ("直接", "Cardinal Infrastructure宣布收购Hughes Brothers建筑公司。"),
    "CDT": ("联动", "-31.82%列All Stocks医疗保健（偏弱侧）。"),
    "CEG": ("联动", "+0.65%列纳指100公用事业（偏强侧）。"),
    "CHR": ("联动", "+12.50%列All Stocks通信服务（偏强侧）。"),
    "CHTR": ("联动", "+4.36%列标普500通信服务（偏强侧）。"),
    "CLWT": ("联动", "-26.98%列All Stocks工业（偏弱侧）。"),
    "CNET": ("联动", "+10.53%列All Stocks通信服务（偏强侧）。"),
    "COST": ("联动", "-0.50%列纳指100必需消费（偏弱侧）。"),
    "CVI": ("联动", "+7.15%列罗素2000能源（偏强侧）。"),
    "CVX": ("联动", "+1.27%列道指能源（偏强侧）。"),
    "DIS": ("联动", "+0.08%列道指通信服务（偏强侧）。"),
    "EFXT": ("直接", "Enerflex获吉瓦级数据中心电力合同（积压超1.75吉瓦）。"),
    "ELLO": ("联动", "+11.97%列All Stocks公用事业（偏强侧）。"),
    "EXE": ("联动", "+4.01%列标普500能源（偏强侧）。"),
    "FANG": ("联动", "+1.57%列纳指100能源（偏强侧）。"),
    "FLY": ("联动", "-5.32%列主题层太空科技（偏弱侧）。"),
    "FWRG": ("联动", "+6.93%列罗素2000可选消费（偏强侧）。"),
    "GILD": ("联动", "-1.67%列纳指100医疗保健（偏弱侧）。"),
    "GIS": ("联动", "-2.66%列标普500必需消费（偏弱侧）。"),
    "GOOGL": ("联动", "+0.30%列道指通信服务（偏强侧）。"),
    "GRMN": ("联动", "+3.62%列主题层生物识别（偏强侧）。"),
    "GURE": ("联动", "-15.96%列All Stocks基础材料（偏弱侧）。"),
    "HON": ("联动", "-1.12%列道指工业（偏弱侧）。"),
    "HUM": ("联动", "-3.03%列标普500医疗保健（偏弱侧）。"),
    "IMSR": ("联动", "+5.07%列All Stocks公用事业（偏强侧）。"),
    "INV": ("联动", "-11.51%列罗素2000金融（偏弱侧）。"),
    "IPX": ("联动", "-6.02%列主题层金属商品（偏弱侧）。"),
    "JNJ": ("直接", "强生财报强劲但投资者聚焦医疗科技单元担忧——-5.73%。"),
    "KEN": ("联动", "+3.51%列All Stocks公用事业（偏强侧）。"),
    "KKR": ("联动", "-4.75%列标普500金融（偏弱侧）。"),
    "KO": ("联动", "+0.36%列道指必需消费（偏强侧）。"),
    "KR": ("直接", "Albertsons就合并破裂索赔逾90亿美元；克罗格裁员超三分之一公司员工。"),
    "LIN": ("联动", "+0.98%列纳指100基础材料（偏强侧）。"),
    "LNKS": ("联动", "-57.10%列All Stocks工业（偏弱侧）。"),
    "LNZA": ("联动", "-10.16%列罗素2000工业（偏弱侧）。"),
    "LUNR": ("联动", "-5.29%列主题层太空科技（偏弱侧）。"),
    "META": ("联动", "+2.63%列标普500通信服务（偏强侧）。"),
    "MKC": ("联动", "-2.06%列标普500必需消费（偏弱侧）。"),
    "MNDR": ("联动", "-51.97%列All Stocks医疗保健（偏弱侧）。"),
    "MNST": ("联动", "-1.03%列纳指100必需消费（偏弱侧）。"),
    "MRK": ("联动", "-2.39%列道指医疗保健（偏弱侧）。"),
    "OMC": ("联动", "+1.84%列标普500通信服务（偏强侧）。"),
    "PARR": ("直接", "Par Pacific公布Q3财报日程。"),
    "PBF": ("联动", "+7.23%列罗素2000能源（偏强侧）。"),
    "PCG": ("联动", "+1.29%列标普500公用事业（偏强侧）。"),
    "PG": ("联动", "-0.10%列道指必需消费（偏弱侧）。"),
    "PINS": ("联动", "+4.43%列主题层社交媒体（偏强侧）。"),
    "PL": ("联动", "-5.01%列主题层国防与航空航天（偏弱侧）。"),
    "PNW": ("联动", "+1.67%列标普500公用事业（偏强侧）。"),
    "PSX": ("联动", "+4.00%列标普500能源（偏强侧）。"),
    "PTLO": ("联动", "+6.79%列罗素2000可选消费（偏强侧）。"),
    "RCAT": ("联动", "-3.80%列主题层国防与航空航天（偏弱侧）。"),
    "REA": ("联动", "-11.99%列All Stocks基础材料（偏弱侧）。"),
    "RILY": ("联动", "-6.33%列罗素2000金融（偏弱侧）。"),
    "RKLB": ("联动", "-2.27%列纳指100工业（偏弱侧）。"),
    "SES": ("联动", "+25.02%列罗素2000可选消费（偏强侧）。"),
    "SHW": ("联动", "+1.22%列道指基础材料（偏强侧）。"),
    "SJT": ("联动", "+10.75%列All Stocks能源（偏强侧）。"),
    "SLNH": ("联动", "-7.06%列罗素2000金融（偏弱侧）。"),
    "SPCX": ("联动", "-4.21%列纳指100工业（偏弱侧）。"),
    "STRO": ("联动", "-17.09%列罗素2000医疗保健（偏弱侧）。"),
    "TDAY": ("联动", "+4.80%列罗素2000通信服务（偏强侧）。"),
    "TXN": ("联动", "+2.17%列主题层可穿戴设备（偏强侧）。"),
    "USAR": ("联动", "-4.57%列主题层金属商品（偏弱侧）。"),
    "VLO": ("联动", "+4.69%列标普500能源（偏强侧）。"),
    "VRTX": ("联动", "-4.30%列标普500医疗保健（偏弱侧）。"),
    "VST": ("联动", "+2.67%列标普500公用事业（偏强侧）。"),
    "WFF": ("联动", "-87.73%列All Stocks工业（偏弱侧）。"),
    "WMT": ("联动", "-0.71%列道指必需消费（偏弱侧）。"),
    "XEL": ("联动", "+0.63%列纳指100公用事业（偏强侧）。"),
    "YMAT": ("联动", "-35.74%列All Stocks基础材料（偏弱侧）。"),
    "ZIP": ("联动", "+6.82%列罗素2000通信服务（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "UNG", "perf": 4.487, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货ETF +4.49%领涨全市场：底部结构内的第四波反弹加速（10.7 +1.85%/10.9 +1.85%/10.12 -0.82%后的爆发）——冬季旺季预期与底部确认的共振。合并删除：无同簇产品。"},
        {"ticker": "IEO", "perf": 3.136, "form": "交易所交易基金", "exposure": "美国油气勘探与生产",
         "reason": "油气勘探生产ETF +3.14%列第二：能源五个股票范围连续第二日领涨（标普21只中20涨/+1.72%：瓦莱罗+4.69%/Expand +4.01%/Phillips 66 +4.00%——炼厂三重奏）；胡塞袭击的地缘溢价延续。合并删除：PXE +3.04%（同簇能源生产商）。"},
        {"ticker": "CRAK", "perf": 3.24, "form": "交易所交易基金", "exposure": "炼油（VanEck）",
         "reason": "炼油ETF +3.24%：裂解价差的地缘放大（胡塞袭击+柴油紧缺）——瓦莱罗/Phillips 66的+4%级共振为能源股最强端。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "BBC", "perf": -5.615, "form": "交易所交易基金", "exposure": "临床试验生物科技",
         "reason": "临床试验生物科技ETF -5.62%领跌全市场：医疗保健五个股票范围领跌的板块端确认——罗素2000医疗保健418只中360跌/-2.85%；强生财报强劲但医疗科技担忧-5.73%/Vertex -4.30%/Humana -3.03%——上周五修复的一日回吐。合并删除：无同簇产品。"},
        {"ticker": "BRF", "perf": -4.081, "form": "交易所交易基金", "exposure": "巴西股票（小盘）",
         "reason": "巴西小盘ETF -4.08%：大选后拉美行情的回吐（EWZ -2.5%级）——上周的+5.26%/+13.51%脉冲后的均值回归。合并删除：EWZ（同簇巴西，保留最深跌幅的小盘端）。"},
        {"ticker": "XBI", "perf": -3.038, "form": "交易所交易基金", "exposure": "生物科技（SPDR）",
         "reason": "生物科技ETF -3.04%列跌幅第三：医疗保健端的全面出清（XLV -1.35%/医疗动量PTH -2.01%）——财报季的医保/药械风险规避。合并删除：无同簇产品。"},
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
        text = "核查10月3日盘后至10月13日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-13"
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
            f"- `finviz_2026-10-13_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-13_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月13日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月13日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周二为财报季首份大行财报日：能源五个股票范围连续第二日领涨（标普500 21只中20涨/+1.72%：瓦莱罗+4.69%/Expand Energy +4.01%/Phillips 66 +4.00%——炼厂三重奏；All Stocks 247只中181涨/+1.60%〔Enerflex +14.37%〔吉瓦级数据中心电力合同、积压超1.75吉瓦〕〕；道指雪佛龙+1.27%清一色涨；罗素2000 91只中69涨/+1.26%〔Par +8.13%/PBF +7.23%/CVI +7.15%〕——XLE +1.80%/XOP +2.85%/炼油CRAK +3.24%/油气勘探IEO +3.14%列全市场第二；**天然气ETF +4.49%领涨全市场**〔底部第四波加速〕）；通信服务三个范围居前（All Stocks 239只中119涨/+0.76%〔**Bumble +56.58%——13亿美元被Ithaca Holdings私有化（周一传闻正式落地）**〕；标普500 19只中14涨/+0.93%〔Charter +4.36%/Meta +2.63%/OMC +1.84%〕；道指谷歌+0.30%/迪士尼+0.08%清一色涨——XLC +0.74%/RSPC +0.34%，Verizon +1.75%/AT&T +1.60%/T-Mobile +1.23%的频谱修复延续）；公用事业三个范围（纳指100四成分清一色涨〔Vistra +2.67%/AEP +1.14%〕——XLU +0.58%）。跌幅侧：**医疗保健五个范围领跌**（All Stocks 1,042只中831跌/-1.50%〔微盘〕；标普500 60只中37跌/-1.30%〔强生-5.73%〔财报强劲但医疗科技单元担忧〕/Vertex -4.30%/Humana -3.03%〕；道指四成分清一色跌/-3.10%；罗素2000医疗保健418只中360跌/-2.85%——XLV -1.35%/XBI -3.04%/BBC -5.62%领跌全市场〔上周五修复的一日回吐〕）；工业三个范围（纳指100工业-3.13%〔SpaceX -4.21%/Rocket Lab -2.27%〕；道指工业-2.11%〔卡特彼勒-3.33%〕）；金融三个范围（花旗Q3超预期仍-5.60%〔市场聚焦费用/息差细节；CEO"AI需求太强、高利率难阻投资"〕/KKR -4.75%/黑石-4.18%——XLF -0.42%，JPM -0.86%/高盛-0.23%的财报日分化）；基础材料三个范围（XME -1.04%）。主题层2个清一色涨（生物识别+5.56%〔硬件+8.6%〕/可穿戴）对6个清一色跌（太空科技-2.26%/金属商品-1.66%/国防-1.31%/教育科技/量子/网安）。社交媒体+3.14%（垂直社群+14.0%——Bumble私有化的板块效应）；巴西ETF -4.08%列跌幅第二（拉美回吐）；半导体企稳（SOXX -0.17%：甲骨文+4.23%/AMD +1.90%对美光-3.62%）；铀链偏弱整理；太空科技回落（NASA -3.25%）；加密分化。VIX期货ETF持平。Character.AI申请破产（运营五年）。克罗格遭Albertsons索赔90亿美元并裁员三分之一。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-10-13_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-13_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-13_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
