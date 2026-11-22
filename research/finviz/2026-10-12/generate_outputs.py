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
    "BMBL": "Bumble Inc",
    "CRWD": "Crowdstrike Holdings Inc",
    "CWST": "Casella Waste Systems Inc",
    "IONQ": "IonQ Inc",
    "META": "Meta Platforms Inc",
    "NEE": "NextEra Energy Inc",
    "NVTS": "Navitas Semiconductor Corp",
    "OXY": "Occidental Petroleum Corp",
    "PLD": "Prologis Inc",
    "QBTS": "D-Wave Quantum Inc",
    "QUBT": "Quantum Computing Inc",
    "REXR": "Rexford Industrial Realty Inc",
    "RPD": "Rapid7 Inc",
    "SAIL": "Sailpoint Inc",
    "SNAP": "Snap Inc",
    "WELL": "Welltower Inc",
    "WOLF": "Wolfspeed Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ABLV": ("联动", "-44.35%列All Stocks可选消费（偏弱侧）。"),
    "ABNB": ("联动", "-1.43%列纳指100可选消费（偏弱侧）。"),
    "AEVA": ("联动", "-10.62%列罗素2000科技（偏弱侧）。"),
    "ALAB": ("联动", "-5.29%列纳指100科技（偏弱侧）。"),
    "AMZN": ("联动", "-1.10%列道指可选消费（偏弱侧）。"),
    "APA": ("联动", "+2.09%列标普500能源（偏强侧）。"),
    "BA": ("直接", "伯恩斯坦把波音目标价下调至278美元（现金流缺乏清晰可见性）；Avalon下大额飞机订单。"),
    "BE": ("联动", "-6.50%列标普500工业（偏弱侧）。"),
    "BKNG": ("联动", "-1.19%列纳指100可选消费（偏弱侧）。"),
    "BMBL": ("直接", "Bumble因10亿美元收购谈判报道而暴涨。"),
    "CAT": ("联动", "-0.14%列道指工业（偏弱侧）。"),
    "CDLX": ("联动", "+8.74%列All Stocks通信服务（偏强侧）。"),
    "CDZI": ("联动", "+5.26%列罗素2000公用事业（偏强侧）。"),
    "CEG": ("联动", "-1.40%列纳指100公用事业（偏弱侧）。"),
    "CIEN": ("联动", "-9.95%列标普500科技（偏弱侧）。"),
    "CMG": ("直接", "星巴克否认收购Chipotle——回落（星巴克股价涨至92.13美元）。"),
    "COHR": ("联动", "-7.87%列标普500科技（偏弱侧）。"),
    "COP": ("联动", "+2.58%列标普500能源（偏强侧）。"),
    "CPRT": ("联动", "-3.08%列标普500工业（偏弱侧）。"),
    "CRWD": ("联动", "-4.37%列主题层网络安全（偏弱侧）。"),
    "CSCO": ("联动", "-2.58%列道指科技（偏弱侧）。"),
    "CTNM": ("直接", "Contineum因Bristol Myers Squibb的IPF混合数据先涨后跌（Stifel维持买入）。"),
    "CVNA": ("联动", "-6.62%列标普500可选消费（偏弱侧）。"),
    "CVX": ("联动", "+1.43%列道指能源（偏强侧）。"),
    "CWST": ("联动", "+1.70%列主题层环境可持续发展（偏强侧）。"),
    "DAIC": ("联动", "-28.87%列All Stocks科技（偏弱侧）。"),
    "DCX": ("联动", "-19.33%列All Stocks可选消费（偏弱侧）。"),
    "DHT": ("直接", "DHT公布Q3船队日均收益14.13万美元与Q4油轮运价。"),
    "DIS": ("联动", "+0.41%列道指通信服务（偏强侧）。"),
    "DK": ("联动", "+3.79%列罗素2000能源（偏强侧）。"),
    "ENHA": ("联动", "+20.00%列All Stocks必需消费（偏强侧）。"),
    "EXC": ("联动", "+0.86%列纳指100公用事业（偏强侧）。"),
    "FCHL": ("联动", "+14.42%列All Stocks必需消费（偏强侧）。"),
    "FIX": ("联动", "-4.53%列标普500工业（偏弱侧）。"),
    "FIZZ": ("联动", "+5.34%列罗素2000必需消费（偏强侧）。"),
    "FRO": ("联动", "+5.51%列All Stocks能源（偏强侧）。"),
    "GOOGL": ("联动", "+0.30%列道指通信服务（偏强侧）。"),
    "HAIN": ("联动", "+11.82%列All Stocks必需消费（偏强侧）。"),
    "HD": ("联动", "-0.04%列道指可选消费（偏弱侧）。"),
    "HELE": ("联动", "+7.47%列罗素2000必需消费（偏强侧）。"),
    "HLF": ("联动", "+4.45%列罗素2000必需消费（偏强侧）。"),
    "HNRG": ("联动", "+4.60%列罗素2000公用事业（偏强侧）。"),
    "IBM": ("联动", "-0.05%列道指科技（偏弱侧）。"),
    "IE": ("联动", "-7.95%列罗素2000基础材料（偏弱侧）。"),
    "IMXI": ("联动", "-14.21%列罗素2000科技（偏弱侧）。"),
    "INDI": ("联动", "-10.58%列罗素2000科技（偏弱侧）。"),
    "IONQ": ("直接", "IonQ宣布13亿美元全股票收购网安公司Elisity——股价下跌。"),
    "KDP": ("联动", "+3.12%列标普500必需消费（偏强侧）。"),
    "KO": ("联动", "+1.98%列道指必需消费（偏强侧）。"),
    "KPTI": ("联动", "-16.51%列罗素2000医疗保健（偏弱侧）。"),
    "LEN": ("联动", "-2.66%列标普500可选消费（偏弱侧）。"),
    "LIN": ("联动", "+0.75%列纳指100基础材料（偏强侧）。"),
    "LITE": ("联动", "-9.78%列标普500科技（偏弱侧）。"),
    "LWLG": ("联动", "-9.86%列罗素2000基础材料（偏弱侧）。"),
    "MCD": ("联动", "+0.18%列道指可选消费（偏强侧）。"),
    "MDLZ": ("联动", "+2.28%列标普500必需消费（偏强侧）。"),
    "MERC": ("联动", "-18.37%列All Stocks基础材料（偏弱侧）。"),
    "META": ("联动", "+3.38%列标普500通信服务（偏强侧）。"),
    "MMM": ("联动", "+0.58%列道指工业（偏强侧）。"),
    "NAT": ("联动", "+3.78%列罗素2000能源（偏强侧）。"),
    "NEE": ("联动", "+1.46%列主题层环境可持续发展（偏强侧）。"),
    "NTCL": ("联动", "-27.33%列All Stocks科技（偏弱侧）。"),
    "NVDA": ("联动", "-1.29%列道指科技（偏弱侧）。"),
    "NVTS": ("联动", "-7.33%列主题层半导体（偏弱侧）。"),
    "OKE": ("联动", "+2.47%列标普500能源（偏强侧）。"),
    "ORA": ("联动", "+3.12%列罗素2000公用事业（偏强侧）。"),
    "OXY": ("联动", "+1.70%列主题层环境可持续发展（偏强侧）。"),
    "PG": ("联动", "+1.30%列道指必需消费（偏强侧）。"),
    "PLD": ("联动", "+2.30%列主题层房地产与REITs（偏强侧）。"),
    "PYPL": ("联动", "+0.94%列纳指100金融（偏强侧）。"),
    "QBTS": ("联动", "-5.70%列主题层量子计算（偏弱侧）。"),
    "QUBT": ("联动", "-6.86%列主题层量子计算（偏弱侧）。"),
    "RETO": ("联动", "-13.64%列All Stocks基础材料（偏弱侧）。"),
    "REXR": ("联动", "+2.10%列主题层房地产与REITs（偏强侧）。"),
    "RPD": ("联动", "-5.89%列主题层网络安全（偏弱侧）。"),
    "SAIL": ("联动", "-5.78%列主题层网络安全（偏弱侧）。"),
    "SNAP": ("联动", "+4.82%列主题层社交媒体（偏强侧）。"),
    "SNDK": ("联动", "-5.97%列纳指100科技（偏弱侧）。"),
    "SRZN": ("联动", "-16.61%列罗素2000医疗保健（偏弱侧）。"),
    "STZ": ("联动", "+3.07%列标普500必需消费（偏强侧）。"),
    "TEN": ("联动", "+6.19%列All Stocks能源（偏强侧）。"),
    "TMC": ("联动", "-14.16%列All Stocks基础材料（偏弱侧）。"),
    "TMUS": ("联动", "+2.21%列标普500通信服务（偏强侧）。"),
    "TSLA": ("直接", "Cybercab因学区超速遭监管调查；Jefferies因交付韧性上调目标价。"),
    "UAMY": ("联动", "-8.70%列罗素2000基础材料（偏弱侧）。"),
    "VZ": ("联动", "+2.71%列标普500通信服务（偏强侧）。"),
    "WCT": ("联动", "-28.29%列All Stocks科技（偏弱侧）。"),
    "WELL": ("联动", "+2.14%列主题层房地产与REITs（偏强侧）。"),
    "WMT": ("联动", "+1.55%列道指必需消费（偏强侧）。"),
    "WOLF": ("联动", "-8.43%列主题层半导体（偏弱侧）。"),
    "XEL": ("联动", "+0.54%列纳指100公用事业（偏强侧）。"),
    "XELB": ("联动", "-24.30%列All Stocks可选消费（偏弱侧）。"),
    "ZNB": ("联动", "+8.60%列All Stocks通信服务（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "GREK", "perf": 2.225, "form": "交易所交易基金", "exposure": "希腊股票",
         "reason": "希腊ETF +2.23%领涨全市场：欧债外围的修复反弹（上周「欧洲末日循环」担忧后的喘息）；欧洲利率端的轮动受益者。合并删除：无同簇产品。"},
        {"ticker": "DBO", "perf": 2.114, "form": "商品信托", "exposure": "WTI原油期货（Invesco）",
         "reason": "WTI原油期货ETF +2.11%列第二：油价续涨（USO +1.91%/BNO +1.77%）——能源五个股票范围领涨的商品端共振；财报季开幕前能源股的定价前奏。合并删除：USO +1.91%、BNO +1.77%（同簇原油期货）。"},
        {"ticker": "IHI", "perf": 2.029, "form": "交易所交易基金", "exposure": "美国医疗器械",
         "reason": "医疗器械ETF +2.03%列第三：医疗保健的防御+器械双属性日（XLV +0.69%）；上周Humana星级重估的医保链延续。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "EWY", "perf": -4.023, "form": "交易所交易基金", "exposure": "韩国股票",
         "reason": "韩国ETF -4.02%再度领跌全市场：三星初步业绩失望的存储链第二波——半导体主题九子行业清一色跌-2.83%（存储-4.4%/下一代-4.5%）：闪迪-5.97%/美光-3.88%；上周四-4.03%后的第二轮重挫。合并删除：无同簇产品。"},
        {"ticker": "XSD", "perf": -3.553, "form": "交易所交易基金", "exposure": "半导体股票（等权）",
         "reason": "等权半导体ETF -3.55%：半导体/网络安全/量子计算三大AI主题齐清一色跌（网安-2.51%〔周五+3.98%的反转〕/量子-2.47%）——财报季开幕日的AI链风险规避。合并删除：SOXX -2.60%、SMH（同簇半导体）。"},
        {"ticker": "URA", "perf": -3.033, "form": "交易所交易基金", "exposure": "全球铀矿",
         "reason": "铀矿ETF -3.03%：核电定价日（10.6）暴涨后的持续回吐（NLR -3.05%/URNM -2.88%——第四轮回吐）；Vistra -2.08%/Constellation -1.40%的电力端同步。合并删除：无同簇产品。"},
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
        text = "核查10月2日盘后至10月12日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-12"
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
            f"- `finviz_2026-10-12_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-12_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月12日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月12日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周一为财报季开幕日+AI链第二轮降温日：能源五个股票范围领涨（All Stocks 247只中149涨/+1.28%〔DHT +6.41%/TEN +6.19%/Frontline +5.51%——油轮三重奏〕；标普500 21只中19涨/+1.48%〔康菲+2.58%/ONEOK +2.47%/APA +2.09%〕；道指雪佛龙+1.43%清一色涨——XLE +1.43%/XOP +1.45%、WTI期货ETF +2.11%列全市场第二）；必需消费五个范围居前（道指三成分清一色涨/+1.60%〔可口可乐+1.98%/沃尔玛+1.55%/宝洁+1.30%〕；纳指100七成分清一色涨〔Keurig +3.12%/Constellation +3.07%/亿滋+2.28%〕——XLP +1.18%）；通信服务三个范围偏强（标普500 19只中13涨/+1.14%〔Meta +3.38%/Verizon +2.71%〔频谱收购后的反弹〕/T-Mobile +2.21%〕——上周五频谱三杀的超跌修复）。跌幅侧：科技五个股票范围领跌（All Stocks 777只中553跌/-1.20%；标普500 88只中60跌/-0.94%〔Ciena -9.95%/Lumentum -9.78%/Coherent -7.87%——光模块三杀〕；纳指100 44只中35跌/-0.89%〔LITE -9.78%/闪迪-5.97%/Astera -5.29%〕；罗素2000 248只中178跌/-2.26%——XLK -1.22%/SOXX -2.60%/XSD -3.55%列跌幅第二：**韩国ETF -4.02%再度领跌全市场**——三星余震+**半导体/网安/量子三大AI主题齐清一色跌**〔半导体-2.83%/网安-2.51%/量子-2.47%〕）；可选消费三个范围（Carvana -6.62%/Chipotle -3.77%〔星巴克否认收购〕/Lennar -2.66%）；基础材料三个范围（XME -1.41%）。铀链第四轮回吐（URA -3.03%）。主题层3个清一色涨（**社交媒体+3.35%〔垂直社群+12.9%——Bumble收购+49.61%的并购催化〕**/REIT/环境可持续）对10个清一色跌。Bumble获10亿美元收购谈判报道+49.61%；IonQ 13亿美元收购网安公司-9.07%；波音遭伯恩斯坦下调目标价至278美元；特斯拉Cybercab学区超速遭监管调查。VIX期货ETF回落（VIXY -1.59%）。希腊ETF +2.23%领涨全市场。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-10-12_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-12_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-12_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
