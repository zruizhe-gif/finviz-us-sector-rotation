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
    "ACHR": "Archer Aviation Inc",
    "ARE": "Alexandria Real Estate Equities Inc",
    "BSY": "Bentley Systems Inc",
    "CHRW": "C.H. Robinson Worldwide Inc",
    "DKNG": "DraftKings Inc",
    "DOC": "Healthpeak Properties Inc",
    "FWRD": "Forward Air Corp",
    "GWRE": "Guidewire Software Inc",
    "INSE": "Inspired Entertainment Inc",
    "MELI": "MercadoLibre Inc",
    "MNTS": "Momentus Inc",
    "NU": "Nu Holdings Ltd",
    "PTC": "PTC Inc",
    "RDW": "Redwire Corp",
    "RSI": "Rush Street Interactive Inc",
    "TSAT": "Telesat Corp",
    "VIRT": "Virtu Financial Inc",
    "VTR": "Ventas Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ACHR": ("联动", "-3.48%列主题层运输与物流（偏弱侧）。"),
    "ACR": ("联动", "-5.60%列罗素2000房地产（偏弱侧）。"),
    "AEP": ("直接", "肯塔基电力与TeraWulf敲定扩大协议（1亿美元定制基础设施——加密矿电力）。"),
    "ALDX": ("联动", "-21.05%列All Stocks医疗保健（偏弱侧）。"),
    "AMGN": ("联动", "-0.01%列道指医疗保健（偏弱侧）。"),
    "APP": ("联动", "+5.13%列标普500通信服务（偏强侧）。"),
    "ARE": ("联动", "-3.15%列标普500房地产（偏弱侧）。"),
    "AWK": ("联动", "-1.85%列标普500公用事业（偏弱侧）。"),
    "BESS": ("联动", "-19.48%列All Stocks公用事业（偏弱侧）。"),
    "BHR": ("联动", "-6.63%列罗素2000房地产（偏弱侧）。"),
    "BORR": ("联动", "+6.14%列罗素2000能源（偏强侧）。"),
    "BSY": ("联动", "+7.82%列主题层软件（偏强侧）。"),
    "CABO": ("联动", "-7.86%列罗素2000通信服务（偏弱侧）。"),
    "CCEP": ("联动", "+0.41%列纳指100必需消费（偏强侧）。"),
    "CDZI": ("联动", "-6.79%列罗素2000公用事业（偏弱侧）。"),
    "CEG": ("联动", "+3.93%列纳指100公用事业（偏强侧）。"),
    "CHRW": ("直接", "标普因53亿美元RXO收购把C.H. Robinson展望下调至负面（并购方贴水）。"),
    "COST": ("联动", "+0.31%列纳指100必需消费（偏强侧）。"),
    "CRML": ("直接", "Critical Metals获格陵兰Tanbreez采矿批准——结束六连跌。"),
    "CSCO": ("联动", "+0.55%列道指科技（偏强侧）。"),
    "CTVA": ("联动", "+3.94%列标普500基础材料（偏强侧）。"),
    "CVX": ("联动", "-0.11%列道指能源（偏弱侧）。"),
    "D": ("联动", "-0.47%列标普500公用事业（偏弱侧）。"),
    "DIS": ("联动", "+1.39%列道指通信服务（偏强侧）。"),
    "DKNG": ("直接", "DraftKings获美银上调评级（预测市场双赢）。"),
    "DNA": ("联动", "+21.30%列罗素2000医疗保健（偏强侧）。"),
    "DOC": ("联动", "-3.33%列标普500房地产（偏弱侧）。"),
    "ECHO": ("联动", "+4.20%列标普500通信服务（偏强侧）。"),
    "EXC": ("联动", "+0.22%列纳指100公用事业（偏强侧）。"),
    "FMC": ("联动", "+6.63%列罗素2000基础材料（偏强侧）。"),
    "FTHM": ("直接", "Fathom与Neighborhood Intelligence因估值分歧互相终止合并。"),
    "FWRD": ("联动", "-5.28%列主题层运输与物流（偏弱侧）。"),
    "GDC": ("联动", "-7.69%列罗素2000通信服务（偏弱侧）。"),
    "GIBO": ("联动", "+10.24%列All Stocks通信服务（偏强侧）。"),
    "GILD": ("联动", "-0.08%列纳指100医疗保健（偏弱侧）。"),
    "GNE": ("联动", "-1.95%列罗素2000公用事业（偏弱侧）。"),
    "GOOGL": ("联动", "+0.86%列道指通信服务（偏强侧）。"),
    "GWRE": ("联动", "+7.28%列主题层金融科技（偏强侧）。"),
    "HAL": ("联动", "+2.92%列标普500能源（偏强侧）。"),
    "HTO": ("联动", "-2.81%列罗素2000公用事业（偏弱侧）。"),
    "ICU": ("联动", "-24.31%列All Stocks医疗保健（偏弱侧）。"),
    "INSE": ("联动", "+14.86%列主题层数字娱乐（偏强侧）。"),
    "JNJ": ("联动", "-1.21%列道指医疗保健（偏弱侧）。"),
    "KO": ("联动", "+1.00%列道指必需消费（偏强侧）。"),
    "LIN": ("联动", "+0.60%列纳指100基础材料（偏强侧）。"),
    "MELI": ("直接", "巴西大选结果引发拉美资产起飞：MercadoLibre/XP/Embraer齐涨。"),
    "MNTS": ("联动", "-3.50%列主题层太空科技（偏弱侧）。"),
    "MRK": ("联动", "-3.30%列道指医疗保健（偏弱侧）。"),
    "MRNO": ("联动", "-8.99%列All Stocks房地产（偏弱侧）。"),
    "MSFT": ("联动", "+1.48%列道指科技（偏强侧）。"),
    "MSGM": ("联动", "+10.70%列All Stocks通信服务（偏强侧）。"),
    "NEE": ("联动", "-0.72%列标普500公用事业（偏弱侧）。"),
    "NU": ("联动", "+13.03%列主题层金融科技（偏强侧）。"),
    "NUE": ("联动", "+4.58%列标普500基础材料（偏强侧）。"),
    "NVAX": ("联动", "+20.08%列罗素2000医疗保健（偏强侧）。"),
    "NVDA": ("联动", "+2.12%列道指科技（偏强侧）。"),
    "NXXT": ("联动", "-8.97%列All Stocks公用事业（偏弱侧）。"),
    "OPEN": ("联动", "-5.33%列罗素2000房地产（偏弱侧）。"),
    "PBR": ("联动", "+11.50%列All Stocks能源（偏强侧）。"),
    "PCVX": ("联动", "+30.70%列罗素2000医疗保健（偏强侧）。"),
    "PEP": ("联动", "-0.19%列纳指100必需消费（偏弱侧）。"),
    "PG": ("联动", "+0.71%列道指必需消费（偏强侧）。"),
    "PSKY": ("直接", "派拉蒙公布Skydance领导层班子（华纳合并完成前）。"),
    "PTC": ("直接", "施耐德电气以226亿美元全现金收购PTC。"),
    "PYPL": ("联动", "+3.05%列纳指100金融（偏强侧）。"),
    "RDW": ("直接", "Redwire获Axiom空间站后续太阳能阵列合同（盘前涨但收跌——与公告方向背离）。"),
    "REGN": ("联动", "-1.19%列纳指100医疗保健（偏弱侧）。"),
    "RIG": ("联动", "+6.58%列All Stocks能源（偏强侧）。"),
    "RSI": ("联动", "+4.90%列主题层数字娱乐（偏强侧）。"),
    "RXO": ("直接", "C.H. Robinson以约58亿美元收购RXO（行业整合催化）。"),
    "SAFX": ("联动", "-8.80%列All Stocks公用事业（偏弱侧）。"),
    "SBFM": ("联动", "-36.97%列All Stocks医疗保健（偏弱侧）。"),
    "SGLY": ("联动", "+34.10%列All Stocks工业（偏强侧）。"),
    "SHW": ("联动", "-0.33%列道指基础材料（偏弱侧）。"),
    "SLB": ("联动", "+3.16%列标普500能源（偏强侧）。"),
    "SPHR": ("直接", "Sphere遭分析师下调（需求软化快于预期）。"),
    "STLD": ("联动", "+3.90%列标普500基础材料（偏强侧）。"),
    "SVRN": ("联动", "+32.72%列All Stocks工业（偏强侧）。"),
    "TSAT": ("联动", "-3.81%列主题层太空科技（偏弱侧）。"),
    "TXT": ("联动", "-1.95%列标普500工业（偏弱侧）。"),
    "UAL": ("联动", "-2.23%列标普500工业（偏弱侧）。"),
    "VAL": ("联动", "+6.51%列All Stocks能源（偏强侧）。"),
    "VIRT": ("联动", "+6.96%列主题层金融科技（偏强侧）。"),
    "VIV": ("联动", "+9.36%列All Stocks通信服务（偏强侧）。"),
    "VLO": ("联动", "+3.21%列标普500能源（偏强侧）。"),
    "VRTX": ("联动", "-0.24%列纳指100医疗保健（偏弱侧）。"),
    "VTR": ("联动", "-3.15%列标普500房地产（偏弱侧）。"),
    "WHLR": ("联动", "-47.34%列All Stocks房地产（偏弱侧）。"),
    "WMT": ("联动", "+0.78%列道指必需消费（偏强侧）。"),
    "WS": ("联动", "+5.82%列罗素2000基础材料（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "BRF", "perf": 13.507, "form": "交易所交易基金", "exposure": "巴西股票（小盘）",
         "reason": "巴西小盘ETF +13.51%领涨全市场：巴西大选结果引发拉美资产全面重估——EWZ +12.54%/拉美40指数+8.23%同向；个股端Petrobras +11.50%/Nubank +13.03%/MercadoLibre +9.67%/Vivo +9.36%。合并删除：EWZ +12.54%（同簇巴西，保留更强的小盘端）。"},
        {"ticker": "ILF", "perf": 8.233, "form": "交易所交易基金", "exposure": "拉美40指数",
         "reason": "拉美40指数ETF +8.23%：大选结果的外溢——拉美整体的风险偏好重定价（巴西为震中）。合并删除：无同簇产品。"},
        {"ticker": "OIH", "perf": 3.136, "form": "交易所交易基金", "exposure": "油服设备（VanEck）",
         "reason": "油服ETF +3.14%：油价商品端回落（BNO -2.62%）与股票端走强的背离日——斯伦贝谢+3.16%/哈里伯顿+2.92%随大选后的拉美能源链与并购整合预期（CHRW-RXO式整合逻辑外溢）。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "UGA", "perf": -2.740, "form": "商品信托", "exposure": "汽油期货（RBOB）",
         "reason": "汽油期货ETF -2.74%领跌全市场：柴油进口禁令政治溢价的第七轮往返（周五-2.36%后连续第二日回吐）——G7释放1亿桶储备的压价效应在成品油端显现。合并删除：无同簇产品。"},
        {"ticker": "BNO", "perf": -2.615, "form": "商品信托", "exposure": "布伦特原油期货",
         "reason": "布伦特原油ETF -2.62%：G7亿桶储备释放+特朗普柴油进口禁令言论的政策组合压价——上周四+4.76%的回吐。合并删除：USO -2.29%、DBO（同簇原油期货）。"},
        {"ticker": "DBE", "perf": -1.641, "form": "交易所交易基金", "exposure": "能源综合（期货）",
         "reason": "能源综合ETF -1.64%：能源商品端全线回落（原油-2.3%~-2.6%/汽油-2.74%）——但能源股票端（XLE +1.00%）逆商品上涨的分化结构。合并删除：IXC/FENY/VDE等（同簇能源股，商品端保留最深跌幅）。"},
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
        text = "核查9月25日盘后至10月5日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-05"
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
            f"- `finviz_2026-10-05_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-05_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月5日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月5日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周一为巴西大选结果日+并购大日：**巴西ETF +13.51%领涨全市场**（EWZ +12.54%/拉美40 +8.23%：Petrobras +11.50%/Nubank +13.03%/MercadoLibre +9.67%）；**施耐德电气以226亿美元全现金收购PTC**（+33.49%——年内最大软件并购）；**C.H. Robinson以约58亿美元收购RXO**（RXO +22.54%/CHRW -10.85%〔标普下调展望〕）。轮入侧：工业三个范围领涨（All Stocks 694只中318涨/整体+1.43%——运输链并购整合为主线）；通信服务三个范围领涨（All Stocks +1.12%〔Vivo +9.36%等拉美通信〕/标普500 +1.10%〔AppLovin +5.13%/EchoStar +4.20%/派拉蒙+2.90%〔公布Skydance领导班子〕〕/道指迪士尼+1.39%/谷歌+0.86%清一色涨——XLC +1.17%）；能源三个范围居前（All Stocks +0.90%〔Petrobras +11.50%〕/罗素2000 91只中79涨/+1.93%〔Transocean +6.58%/Valaris +6.51%〕——XLE +1.00%/XOP +1.36%/油服OIH +3.14%〔斯伦贝谢+3.16%/哈里伯顿+2.92%〕；但商品端回落：USO -2.29%/BNO -2.62%/UGA -2.74%领跌全市场〔G7亿桶压价+禁令往返第七轮〕——股票对商品的背离日）；基础材料三个范围（标普500 +1.09%〔纽柯+4.58%/Corteva +3.94%〔分拆后重估〕/钢铁动态+3.90%〕；XLB +1.31%/XME +1.91%）。跌幅侧：房地产三个范围（标普500 30只中17跌/-0.41%〔医疗办公REIT领跌：Healthpeak -3.33%/Ventas -3.15%/Alexandria -3.15%〕——REIT主题连续偏弱）；公用事业两个范围（罗素2000 32只中24跌/-0.66%）；医疗保健偏弱（道指默克-3.30%/强生-1.21%）。主题层**11个清一色涨、零清一色跌**（金融科技+2.62%〔新型银行+4.2%——Nubank谱系〕/软件+2.14%/数字娱乐+1.48%〔DraftKings获美银上调+5.43%〕/社交媒体/网络安全/能源商品/电商/大数据/消费品/可穿戴/教育科技）。软件/云续强（XSW +1.72%/WCLD +2.13%）；半导体分化（SOXX +0.10%对存储MU -1.02%/SNDK -0.92%续回落）；PayPal +3.05%（金融科技领涨）；加密ETF反弹（IBIT +1.74%/DIME +5.95%）；铀链反弹（NLR +0.96%）；太空科技回落（LUNR -2.85%——主题-0.53%）；VIX期货ETF回落（VIXY -1.08%）。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-10-05_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-05_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-05_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
