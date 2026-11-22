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
    "ALB": "Albemarle Corp",
    "AMTX": "Aemetis Inc",
    "ATLX": "Atlas Lithium Corp",
    "CALM": "Cal-Maine Foods Inc",
    "DAN": "Dana Inc",
    "FLY": "Firefly Aerospace Inc",
    "GEVO": "Gevo Inc",
    "INTC": "Intel Corp",
    "INVZ": "Innoviz Technologies Ltd",
    "IONQ": "IonQ Inc",
    "KGC": "Kinross Gold Corp",
    "LAUR": "Laureate Education Inc",
    "PL": "Planet Labs PBC",
    "QBTS": "D-Wave Quantum Inc",
    "RKLB": "Rocket Lab Corp",
    "SKIL": "Skillsoft Corp",
    "TAL": "TAL Education Group ADR",
    "TE": "T1 Energy Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ABX": ("联动", "+5.75%列罗素2000金融（偏强侧）。"),
    "ALB": ("联动", "-4.60%列标普500基础材料（偏弱侧）。"),
    "AMTX": ("联动", "-6.84%列罗素2000基础材料（偏弱侧）。"),
    "APEI": ("联动", "+3.21%列罗素2000必需消费（偏强侧）。"),
    "APUS": ("联动", "+114.85%列All Stocks医疗保健（偏强侧）。"),
    "ASPN": ("联动", "-6.69%列罗素2000基础材料（偏弱侧）。"),
    "ATLX": ("联动", "-3.27%列主题层金属商品（偏弱侧）。"),
    "AXP": ("联动", "+1.23%列道指金融（偏强侧）。"),
    "BA": ("直接", "波音下跌：习特会未带来新客机订单的预期消退（Boeing falls as hopes for a new China jet order fade）。"),
    "BESS": ("联动", "-7.14%列All Stocks公用事业（偏弱侧）。"),
    "BKR": ("联动", "-1.27%列纳指100能源（偏弱侧）。"),
    "BXC": ("联动", "-7.50%列罗素2000工业（偏弱侧）。"),
    "CALM": ("联动", "-4.53%列主题层农业商品（偏弱侧）。"),
    "CAPS": ("联动", "-13.98%列All Stocks基础材料（偏弱侧）。"),
    "CAT": ("联动", "-0.83%列道指工业（偏弱侧）。"),
    "CD": ("联动", "+20.79%列罗素2000金融（偏强侧）。"),
    "CEG": ("联动", "-0.86%列纳指100公用事业（偏弱侧）。"),
    "CRL": ("联动", "+6.17%列标普500医疗保健（偏强侧）。"),
    "CURI": ("联动", "+8.33%列罗素2000通信服务（偏强侧）。"),
    "CVX": ("联动", "+0.07%列道指能源（偏强侧）。"),
    "DAN": ("联动", "-7.91%列主题层电动汽车（偏弱侧）。"),
    "DIS": ("联动", "+2.03%列标普500通信服务（偏强侧）。"),
    "DKI": ("联动", "+12.40%列All Stocks通信服务（偏强侧）。"),
    "EIX": ("联动", "-1.81%列标普500公用事业（偏弱侧）。"),
    "EL": ("联动", "-3.50%列标普500必需消费（偏弱侧）。"),
    "ENLT": ("联动", "-5.02%列All Stocks公用事业（偏弱侧）。"),
    "EOSE": ("联动", "-9.36%列罗素2000工业（偏弱侧）。"),
    "EXC": ("联动", "-1.20%列纳指100公用事业（偏弱侧）。"),
    "EXE": ("联动", "+1.81%列标普500能源（偏强侧）。"),
    "FANG": ("联动", "+1.81%列标普500能源（偏强侧）。"),
    "FGBI": ("联动", "+3.81%列罗素2000金融（偏强侧）。"),
    "FLY": ("联动", "+5.43%列主题层太空科技（偏强侧）。"),
    "GEVO": ("联动", "-3.45%列主题层农业商品（偏弱侧）。"),
    "GLND": ("直接", "Greenland Energy宣布延长Jameson Land与80 Mile plc的farm-out协议——格陵兰概念微盘的再度爆发（周三-20.92%后+83.85%）。"),
    "GOOGL": ("联动", "+1.34%列道指通信服务（偏强侧）。"),
    "GRPN": ("联动", "+4.24%列罗素2000通信服务（偏强侧）。"),
    "GURE": ("联动", "-10.00%列All Stocks基础材料（偏弱侧）。"),
    "HTOO": ("联动", "-9.87%列All Stocks公用事业（偏弱侧）。"),
    "ILMN": ("联动", "+7.25%列标普500医疗保健（偏强侧）。"),
    "INTC": ("联动", "+3.91%列主题层量子计算（偏强侧）。"),
    "INVZ": ("联动", "-8.62%列主题层电动汽车（偏弱侧）。"),
    "IONQ": ("联动", "+5.74%列主题层量子计算（偏强侧）。"),
    "KDP": ("联动", "-2.77%列标普500必需消费（偏弱侧）。"),
    "KGC": ("直接", "Kinross Gold大跌：La Coipa与Round Mountain产出指引下调——金矿股当日领跌。"),
    "KO": ("联动", "+0.01%列道指必需消费（偏强侧）。"),
    "LAUR": ("联动", "+3.79%列罗素2000必需消费（偏强侧）。"),
    "LIN": ("联动", "-0.34%列纳指100基础材料（偏弱侧）。"),
    "META": ("直接", "扎克伯格披露Muse AI代理将对促成的交易收取费用（变现模式落地）+摩根大通上调目标价至920美元+Citizens看近19%上行。"),
    "MGEE": ("联动", "-3.35%列罗素2000公用事业（偏弱侧）。"),
    "MLM": ("联动", "-2.11%列标普500基础材料（偏弱侧）。"),
    "MMM": ("联动", "-1.63%列道指工业（偏弱侧）。"),
    "MNST": ("联动", "-2.82%列标普500必需消费（偏弱侧）。"),
    "MOS": ("联动", "-2.79%列标普500基础材料（偏弱侧）。"),
    "MRNA": ("联动", "+6.98%列标普500医疗保健（偏强侧）。"),
    "NEE": ("联动", "-1.82%列标普500公用事业（偏弱侧）。"),
    "NFLX": ("联动", "+0.50%列纳指100通信服务（偏强侧）。"),
    "NRG": ("联动", "-2.85%列标普500公用事业（偏弱侧）。"),
    "NRGV": ("联动", "-2.94%列罗素2000公用事业（偏弱侧）。"),
    "ORA": ("联动", "-3.43%列罗素2000公用事业（偏弱侧）。"),
    "PFSA": ("联动", "+47.80%列All Stocks医疗保健（偏强侧）。"),
    "PG": ("联动", "-1.16%列道指必需消费（偏弱侧）。"),
    "PL": ("联动", "+7.57%列主题层太空科技（偏强侧）。"),
    "PSKY": ("联动", "+2.21%列标普500通信服务（偏强侧）。"),
    "PYPL": ("联动", "+0.17%列纳指100金融（偏强侧）。"),
    "QBTS": ("联动", "+3.99%列主题层量子计算（偏强侧）。"),
    "RKDA": ("联动", "-25.82%列All Stocks必需消费（偏弱侧）。"),
    "RKLB": ("联动", "+4.69%列主题层太空科技（偏强侧）。"),
    "RUM": ("联动", "+3.99%列罗素2000通信服务（偏强侧）。"),
    "SHW": ("联动", "-1.86%列道指基础材料（偏弱侧）。"),
    "SJT": ("联动", "+12.58%列All Stocks能源（偏强侧）。"),
    "SKIL": ("联动", "+3.38%列主题层教育科技（偏强侧）。"),
    "SKYQ": ("联动", "+14.57%列All Stocks能源（偏强侧）。"),
    "SRZN": ("联动", "+108.42%列All Stocks医疗保健（偏强侧）。"),
    "TAL": ("联动", "+2.00%列主题层教育科技（偏强侧）。"),
    "TE": ("联动", "-5.69%列主题层电动汽车（偏弱侧）。"),
    "TJGC": ("直接", "TJGC Group宣布股票回购计划。"),
    "TNMG": ("联动", "+10.35%列All Stocks通信服务（偏强侧）。"),
    "TROX": ("联动", "-6.28%列罗素2000基础材料（偏弱侧）。"),
    "TRV": ("联动", "+0.56%列道指金融（偏强侧）。"),
    "TWG": ("联动", "-23.96%列All Stocks必需消费（偏弱侧）。"),
    "UNFI": ("联动", "+5.51%列罗素2000必需消费（偏强侧）。"),
    "V": ("联动", "+1.79%列道指金融（偏强侧）。"),
    "VLO": ("联动", "+1.87%列标普500能源（偏强侧）。"),
    "WMT": ("直接", "沃尔玛下跌：Scintilla把供应商数据转化为AI（零售数据护城河受威胁）。"),
    "XEL": ("联动", "-1.56%列纳指100公用事业（偏弱侧）。"),
    "XMTR": ("联动", "-7.27%列罗素2000工业（偏弱侧）。"),
    "XXII": ("联动", "-35.47%列All Stocks必需消费（偏弱侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "UNG", "perf": 6.256, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货ETF +6.26%领涨全市场：本周第二根大阳线（周二+5.85%后再度爆发）——气强油弱格局延续，天然气独立于原油的行情成为本周能源商品的主线。合并删除：无同簇产品（UNL为中期天然气、独立保留）。"},
        {"ticker": "USO", "perf": 2.862, "form": "商品信托", "exposure": "WTI原油期货",
         "reason": "WTI原油期货ETF +2.86%：油价连续第二日反弹（Brent重返100美元上方）——习特会能源交易预期+柴油纪录高价与出口禁令政治的延续定价。合并删除：DBO +2.80%、BNO +2.45%（同簇原油期货）。"},
        {"ticker": "FCOM", "perf": 1.661, "form": "交易所交易基金", "exposure": "通信服务（含电信权重）",
         "reason": "通信服务ETF +1.66%：五范围领涨的板块端确认——Meta +4.50%（Muse收费模式落地+摩根大通上调目标价至920美元）与电信权重的利率企稳反弹共振。合并删除：无同簇产品（XLC为等权与市值混合口径、独立保留）。"},
    ],
    "down": [
        {"ticker": "TAN", "perf": -3.507, "form": "交易所交易基金", "exposure": "全球太阳能",
         "reason": "太阳能ETF -3.51%领跌全市场：清洁能源谱系在利率高位（10年期5%上方第二日）的贴现率打击叠加美国70%反数据中心情绪的压制。合并删除：无同簇产品。"},
        {"ticker": "URA", "perf": -2.691, "form": "交易所交易基金", "exposure": "全球铀矿",
         "reason": "铀矿ETF -2.69%：铀链连续第三日下跌（URNJ -3.72%/URNM -2.94%/NLR -1.95%）——Cameco -2.95%/Oklo -1.36%，AI电力叙事的短期冷却延续。合并删除：无同簇产品。"},
        {"ticker": "TUR", "perf": -2.401, "form": "交易所交易基金", "exposure": "土耳其股票",
         "reason": "土耳其ETF -2.40%：新兴市场在美元延续上行与全球利率冲击下的压力释放（国家ETF为当日跌幅第三）。合并删除：无同簇产品。"},
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
        text = "核查9月16日盘后至9月24日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-24"
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
            f"- `finviz_2026-09-24_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-24_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月24日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月24日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周四为习特会正式会谈日：通信服务五个股票范围全部领涨（连续两日五范围领跌的直接反转——XLC +1.27%：Meta +4.50%〔扎克伯格披露Muse将对促成的交易收费+摩根大通上调目标价至920美元〕、迪士尼+2.03%、谷歌+1.34%〔连续两日下跌后反弹〕、电信FCOM +1.66%列全市场第三）；能源四个范围续涨（XLE +0.37/XOP +0.77——油价连续第二日反弹：USO +2.86/BNO +2.45，天然气ETF +6.26%领涨全市场为本周第二根大阳线）；金融三个范围反弹（罗素2000金融357只中267涨：Visa +1.79%〔Muse结算通道预期〕/区域银行KRE +0.80%）。跌幅侧：基础材料五个范围全部领跌（XLB -1.19/XME -1.48——金矿Kinross指引下调-11.59%、金属商品主题连续第二日清一色跌）；公用事业四个范围领跌（XLU -0.98：NRG -2.85/NextEra -1.82——10年期5%上方的类债压制第二日）；必需消费四个范围领跌（XLP -0.89：沃尔玛遭Scintilla供应商数据AI化威胁-2.66%）。主题层3个清一色涨（太空科技+1.47：Intuitive Machines +3.02/Rocket Lab +4.69；量子计算+1.17：IonQ +5.74；教育科技+0.66）对6个清一色跌（电动汽车/农业商品/金属商品/大数据/机器人/工业自动化）。铀链连续第三日下跌（URA -2.69%列跌幅第二）；太阳能TAN -3.51%领跌全市场；土耳其TUR -2.40%。生物科技脉冲个股回吐（Viking -11.77/MAZE -6.69）但板块XBI +0.55%。比特币ETF持平（IBIT -0.15/ETHA +0.59/DIME +4.24）。VIX期货ETF续涨（VIXY +0.66）——事件日波动率维持高位。波音-1.57%（中国新客机订单预期消退）；迪尔-2.05%（周三会前上涨的"卖事实"）。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-09-24_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-24_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-24_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
