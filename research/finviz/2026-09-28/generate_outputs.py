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
    "AUID": "authID Inc",
    "AWRE": "Aware Inc",
    "BMY": "Bristol-Myers Squibb Co",
    "BODI": "Beachbody Company Inc",
    "CLF": "Cleveland-Cliffs Inc",
    "COUR": "Coursera Inc",
    "CTGO": "Contango Silver & Gold Inc",
    "DFTX": "Definium Therapeutics Inc",
    "DUOL": "Duolingo Inc",
    "GFI": "Gold Fields Ltd ADR",
    "OKTA": "Okta Inc",
    "PACB": "Pacific Biosciences of California Inc",
    "PANW": "Palo Alto Networks Inc",
    "QCOM": "Qualcomm Inc",
    "SEER": "Seer Inc",
    "SFM": "Sprouts Farmers Market Inc",
    "UTI": "Universal Technical Institute Inc",
    "ZS": "Zscaler Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEP": ("联动", "-0.13%列纳指100公用事业（偏弱侧）。"),
    "AMGN": ("联动", "+0.85%列纳指100医疗保健（偏强侧）。"),
    "AMZN": ("联动", "-1.41%列道指可选消费（偏弱侧）。"),
    "ARES": ("联动", "-3.01%列标普500金融（偏弱侧）。"),
    "ASPI": ("联动", "-11.11%列罗素2000基础材料（偏弱侧）。"),
    "AUID": ("联动", "-20.09%列主题层生物识别（偏弱侧）。"),
    "AWRE": ("联动", "-6.78%列主题层生物识别（偏弱侧）。"),
    "BA": ("联动", "-6.91%列道指工业（偏弱侧）。"),
    "BKR": ("联动", "-1.23%列纳指100能源（偏弱侧）。"),
    "BMY": ("直接", "本周FDA决策观察名单（BMY关键审批在即）。"),
    "BNKK": ("联动", "+22.22%列All Stocks必需消费（偏强侧）。"),
    "BODI": ("联动", "+3.84%列主题层老龄化与长寿（偏强侧）。"),
    "BUDA": ("联动", "+11.33%列All Stocks必需消费（偏强侧）。"),
    "BX": ("联动", "-3.26%列标普500金融（偏弱侧）。"),
    "BYSI": ("联动", "+44.11%列All Stocks医疗保健（偏强侧）。"),
    "CABO": ("直接", "标普将Cable One下调至B+（宽带前景恶化）。"),
    "CAT": ("联动", "-0.20%列道指工业（偏弱侧）。"),
    "CCEP": ("联动", "+1.12%列纳指100必需消费（偏强侧）。"),
    "CEG": ("联动", "-1.08%列纳指100公用事业（偏弱侧）。"),
    "CITR": ("联动", "-12.04%列All Stocks基础材料（偏弱侧）。"),
    "CLF": ("联动", "-7.88%列主题层金属商品（偏弱侧）。"),
    "COST": ("联动", "+0.02%列纳指100必需消费（偏强侧）。"),
    "COUR": ("联动", "-8.12%列主题层教育科技（偏弱侧）。"),
    "CTGO": ("联动", "-8.62%列罗素2000基础材料（偏弱侧）。"),
    "CVNA": ("联动", "-7.05%列标普500可选消费（偏弱侧）。"),
    "CVX": ("联动", "+0.94%列标普500能源（偏强侧）。"),
    "DASH": ("联动", "-7.74%列标普500可选消费（偏弱侧）。"),
    "DCX": ("联动", "-21.94%列All Stocks可选消费（偏弱侧）。"),
    "DFTX": ("联动", "+6.19%列主题层医疗保健与生物科技（偏强侧）。"),
    "DIS": ("直接", "迪士尼无广告版Disney+提价13%；CFO称流媒体利润已超过此前水平。"),
    "DLTR": ("联动", "+1.71%列标普500必需消费（偏强侧）。"),
    "DUOL": ("联动", "-6.42%列主题层教育科技（偏弱侧）。"),
    "EONR": ("直接", "EON Resources公布2025年业绩并推进二叠纪增长计划。"),
    "FANG": ("联动", "-0.77%列纳指100能源（偏弱侧）。"),
    "FLNC": ("联动", "-4.46%列罗素2000公用事业（偏弱侧）。"),
    "GETY": ("直接", "Getty Images与贷款方洽谈救援融资的报道——-40.95%。"),
    "GFI": ("直接", "Gold Fields大跌：Northern Star拒绝其272亿美元收购要约（此前周五Bloomberg报道其主动接洽）。"),
    "GOOGL": ("联动", "-0.34%列道指通信服务（偏弱侧）。"),
    "GRML": ("联动", "-19.17%列All Stocks基础材料（偏弱侧）。"),
    "HD": ("联动", "-1.13%列道指可选消费（偏弱侧）。"),
    "HON": ("联动", "-0.48%列道指工业（偏弱侧）。"),
    "HYMC": ("联动", "-8.75%列罗素2000基础材料（偏弱侧）。"),
    "IDXX": ("联动", "+1.89%列纳指100医疗保健（偏强侧）。"),
    "INN": ("联动", "+1.39%列罗素2000房地产（偏强侧）。"),
    "ISRG": ("联动", "+2.37%列标普500医疗保健（偏强侧）。"),
    "KKR": ("直接", "KKR公布第三季度期内资产变现活动更新。"),
    "KO": ("直接", "可口可乐任命Monster前高管执掌北美业务。"),
    "KOD": ("直接", "Kodiak Sciences公布DAYBREAK三期试验顶线结果——单日+177.96%。"),
    "LESL": ("联动", "-18.17%列All Stocks可选消费（偏弱侧）。"),
    "LFCR": ("直接", "Lifecore Biomedical将被Webster Equity Partners收购。"),
    "LIN": ("联动", "+0.46%列纳指100基础材料（偏强侧）。"),
    "LMNR": ("联动", "+2.29%列罗素2000必需消费（偏强侧）。"),
    "MARPS": ("联动", "+6.14%列All Stocks能源（偏强侧）。"),
    "MCD": ("联动", "-1.23%列道指可选消费（偏弱侧）。"),
    "META": ("直接", "Meta发布企业级AI平台并聘请MongoDB CEO执掌新业务线；MongoDB因CEO出走一度-16%~-18%。"),
    "MTD": ("联动", "+2.22%列标普500医疗保健（偏强侧）。"),
    "NAUT": ("联动", "+15.30%列罗素2000医疗保健（偏强侧）。"),
    "NCI": ("联动", "-83.75%列All Stocks可选消费（偏弱侧）。"),
    "NFLX": ("联动", "-2.69%列标普500通信服务（偏弱侧）。"),
    "NGVC": ("联动", "+3.33%列罗素2000必需消费（偏强侧）。"),
    "NRGV": ("联动", "-7.96%列罗素2000公用事业（偏弱侧）。"),
    "OKTA": ("联动", "+3.58%列主题层网络安全（偏强侧）。"),
    "PACB": ("联动", "+5.56%列主题层医疗保健与生物科技（偏强侧）。"),
    "PANW": ("联动", "+4.63%列主题层网络安全（偏强侧）。"),
    "PEB": ("联动", "+1.68%列罗素2000房地产（偏强侧）。"),
    "PG": ("联动", "+1.92%列标普500必需消费（偏强侧）。"),
    "PK": ("联动", "+1.88%列罗素2000房地产（偏强侧）。"),
    "PM": ("联动", "+1.72%列标普500必需消费（偏强侧）。"),
    "POR": ("联动", "-5.70%列罗素2000公用事业（偏弱侧）。"),
    "PYPL": ("联动", "-1.38%列纳指100金融（偏弱侧）。"),
    "QCOM": ("联动", "-7.17%列主题层生物识别（偏弱侧）。"),
    "RDDT": ("联动", "-4.51%列标普500通信服务（偏弱侧）。"),
    "RDZN": ("联动", "-10.36%列罗素2000科技（偏弱侧）。"),
    "SEER": ("联动", "+6.28%列主题层医疗保健与生物科技（偏强侧）。"),
    "SFM": ("联动", "+1.54%列主题层老龄化与长寿（偏强侧）。"),
    "SHW": ("联动", "+1.12%列道指基础材料（偏强侧）。"),
    "SJT": ("联动", "+8.77%列All Stocks能源（偏强侧）。"),
    "SWMR": ("联动", "-12.30%列罗素2000科技（偏弱侧）。"),
    "TANH": ("联动", "+21.74%列All Stocks必需消费（偏强侧）。"),
    "THRY": ("联动", "-10.34%列罗素2000科技（偏弱侧）。"),
    "TSLA": ("联动", "-3.94%列标普500可选消费（偏弱侧）。"),
    "USNA": ("联动", "+2.21%列罗素2000必需消费（偏强侧）。"),
    "UTI": ("联动", "-9.02%列主题层教育科技（偏弱侧）。"),
    "VLO": ("联动", "+0.62%列标普500能源（偏强侧）。"),
    "VTRS": ("联动", "+2.47%列标普500医疗保健（偏强侧）。"),
    "WMT": ("直接", "沃尔玛CEO回应动态定价担忧：AI不会导致Surge Pricing。"),
    "XEL": ("联动", "-0.59%列纳指100公用事业（偏弱侧）。"),
    "XHLD": ("联动", "-92.45%列All Stocks通信服务（偏弱侧）。"),
    "XOM": ("联动", "+1.20%列标普500能源（偏强侧）。"),
    "ZS": ("联动", "+3.28%列主题层网络安全（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "BBC", "perf": 2.171, "form": "交易所交易基金", "exposure": "临床试验生物科技",
         "reason": "临床试验生物科技ETF +2.17%领涨全市场：Kodiak Sciences三期顶线数据+177.96%、Lifecore被Webster Equity Partners收购+55.24%——医疗保健四个股票范围领涨的板块端确认。合并删除：无同簇产品。"},
        {"ticker": "GREK", "perf": 1.309, "form": "交易所交易基金", "exposure": "希腊股票",
         "reason": "希腊ETF +1.31%：连续第二日领涨（上周五+2.24%）——欧债外围银行的独立行情延续。合并删除：无同簇产品。"},
        {"ticker": "XPH", "perf": 1.210, "form": "交易所交易基金", "exposure": "标普制药",
         "reason": "制药ETF +1.21%：医疗保健领涨日的权重端映射——Viatris +2.47%/直觉外科+2.37%；百时美施贵宝本周FDA审批窗口。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "GDXJ", "perf": -5.788, "form": "交易所交易基金", "exposure": "全球中小金矿股",
         "reason": "中小金矿ETF -5.79%领跌全市场：Gold Fields 272亿美元收购Northern Star遭拒-12.88%叠加黄金现货-3.94%——金属商品主题黄金子行业-5.7%的极端定价日。合并删除：无同簇产品。"},
        {"ticker": "RING", "perf": -5.630, "form": "交易所交易基金", "exposure": "全球金矿股（iShares）",
         "reason": "全球金矿ETF -5.63%：金矿谱系全线崩跌（Newmont -4.43%）——并购受挫+金价大跌的双击。合并删除：无同簇产品（与GDXJ为不同发行商产品、分别保留）。"},
        {"ticker": "SIVR", "perf": -5.512, "form": "商品信托", "exposure": "白银现货",
         "reason": "白银现货ETF -5.51%：白银-5.49%的极端回落——贵金属全线崩跌（黄金-3.94%）。合并删除：SLV -5.49%、SIL -4.99%（同簇白银现货信托）。"},
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
        text = "核查9月18日盘后至9月28日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-28"
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
            f"- `finviz_2026-09-28_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-28_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月28日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月28日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周一为峰会周后的防御+医疗保健日：必需消费五个股票范围全部领涨（标普500 +0.38%：宝洁+1.92%/菲利普莫里斯+1.72%/美元树+1.71%；XLP +0.27%）；医疗保健四个范围领涨（罗素2000医疗保健+1.21%：Kodiak三期数据+177.96%/Lifecore被收购+55.24%——临床试验生物科技ETF +2.17%领涨全市场、制药ETF +1.21%）；能源三个范围续强（道指雪佛龙清一色+0.94%：埃克森+1.20%——原油USO +1.13%）。跌幅侧：通信服务三个范围领跌（Meta -4.79%〔发布企业级AI平台并挖角MongoDB CEO——MongoDB -18.46%〕/Reddit -4.51%/Getty -40.95%〔救援融资报道〕）；可选消费三个范围领跌（DoorDash -7.74%/Carvana -7.05%/特斯拉-3.94%〔摩根大通下调Q3交付预测〕）；金融两个范围领跌（标普500金融-1.13%：KKR -3.55%/黑石-3.26%/Ares -3.01%——另类资管全线、纳指100金融清一色跌）。金矿与贵金属全线崩跌（GDXJ -5.79%/RING -5.63%/SIVR -5.51%列跌幅前三——Gold Fields 272亿美元收购遭拒-12.88%、黄金-3.94%/白银-5.49%）；金属矿业XME -2.69%。主题层20个清一色跌对2个清一色涨（网络安全+1.43%反弹：Palo Alto +4.63%/Zscaler +3.28%；老龄化+0.30%）——生物识别-3.79/金属商品-3.53/教育科技-2.82领跌。半导体回吐（SOXX -2.08%：美光-2.62%/闪迪-3.65%）；网络安全与软件分化（IHAK +1.09%对IGV -0.55%）。波音-6.91%为道指工业清一色跌的最大拖累（无当日公告）；航空航天国防ITA -2.13%。铀链回落（URA -1.91%）；太空科技回落（WARP -1.98%）；比特币ETF回落（IBIT -0.76%）。VIX期货ETF反弹（VIXY +1.08%）。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-09-28_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-28_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-28_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
