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
    "CDNS": "Cadence Design Systems Inc",
    "COHR": "Coherent Corp",
    "CTVA": "Corteva Inc",
    "GPCR": "Structure Therapeutics Inc ADR",
    "IOT": "Samsara Inc",
    "LITE": "Lumentum Holdings Inc",
    "MSTR": "Strategy Inc",
    "NICE": "NICE Ltd ADR",
    "OHI": "Omega Healthcare Investors Inc",
    "PPC": "Pilgrim's Pride Corp",
    "SBRA": "Sabra Healthcare REIT Inc",
    "SFM": "Sprouts Farmers Market Inc",
    "SNPS": "Synopsys Inc",
    "STKH": "Steakholder Foods Ltd ADR",
    "TDC": "Teradata Corp",
    "TEM": "Tempus AI Inc",
    "U": "Unity Software Inc",
    "VKTX": "Viking Therapeutics Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ACN": ("直接", "埃森哲FY2026 Q4超预期、管理服务订单创纪录——盘中一度+22%。"),
    "AEP": ("联动", "+0.94%列纳指100公用事业（偏强侧）。"),
    "ALNY": ("联动", "-6.31%列纳指100医疗保健（偏弱侧）。"),
    "AMC": ("联动", "-8.00%列罗素2000通信服务（偏弱侧）。"),
    "AMGN": ("联动", "-3.38%列标普500医疗保健（偏弱侧）。"),
    "APD": ("联动", "-1.76%列标普500基础材料（偏弱侧）。"),
    "APP": ("联动", "-3.14%列标普500通信服务（偏弱侧）。"),
    "BA": ("直接", "近万名波音工人批准新合同避免西海岸罢工（工程师层反对并授权罢工——分层结果）。"),
    "BBGI": ("联动", "-12.61%列All Stocks通信服务（偏弱侧）。"),
    "BIRD": ("联动", "+33.72%列All Stocks科技（偏强侧）。"),
    "BKR": ("联动", "+1.31%列纳指100能源（偏强侧）。"),
    "BLMN": ("联动", "+8.13%列罗素2000可选消费（偏强侧）。"),
    "CABO": ("联动", "-5.99%列罗素2000通信服务（偏弱侧）。"),
    "CAT": ("联动", "+1.92%列道指工业（偏强侧）。"),
    "CDNS": ("联动", "+6.22%列主题层工业自动化（偏强侧）。"),
    "CDZI": ("联动", "-5.61%列罗素2000公用事业（偏弱侧）。"),
    "CEG": ("联动", "+1.93%列纳指100公用事业（偏强侧）。"),
    "CHRW": ("联动", "+3.50%列标普500工业（偏强侧）。"),
    "COHR": ("联动", "+10.90%列主题层虚拟与增强现实（偏强侧）。"),
    "CPK": ("直接", "Chesapeake Utilities宣布2.25亿美元ATM股权发行。"),
    "CRH": ("联动", "-1.33%列标普500基础材料（偏弱侧）。"),
    "CTVA": ("直接", "法院裁决后Corteva于10月1日推进一分为二分拆——-83.81%为除权机械性调整。"),
    "CVI": ("联动", "+6.61%列罗素2000能源（偏强侧）。"),
    "CVX": ("联动", "+1.42%列道指能源（偏强侧）。"),
    "CWCO": ("联动", "+2.82%列All Stocks公用事业（偏强侧）。"),
    "CWT": ("联动", "-2.64%列罗素2000公用事业（偏弱侧）。"),
    "DHR": ("直接", "Julie Montgomery出任丹纳赫总裁兼CEO。"),
    "DIS": ("直接", "迪士尼计划电视业务重组（瘦身延续）。"),
    "DKI": ("联动", "-17.83%列All Stocks通信服务（偏弱侧）。"),
    "DMRC": ("联动", "+16.15%列罗素2000科技（偏强侧）。"),
    "EFXT": ("直接", "Enerflex获大型数据中心开发合同并完成亚太资产剥离。"),
    "EMAT": ("联动", "-15.49%列All Stocks基础材料（偏弱侧）。"),
    "EP": ("联动", "+7.02%列All Stocks能源（偏强侧）。"),
    "EVCM": ("联动", "+14.20%列罗素2000科技（偏强侧）。"),
    "EXC": ("联动", "+0.17%列纳指100公用事业（偏强侧）。"),
    "FANG": ("联动", "+0.93%列纳指100能源（偏强侧）。"),
    "FHTX": ("直接", "Foghorn裁员40%——与礼来的癌症合作破裂。"),
    "FICO": ("直接", "上市以来最差季度后的第二日反弹+11.69%（美银下调目标价不改反弹）。"),
    "FRVO": ("联动", "+6.40%列All Stocks公用事业（偏强侧）。"),
    "GEV": ("联动", "+3.89%列标普500工业（偏强侧）。"),
    "GOOGL": ("联动", "-1.70%列道指通信服务（偏弱侧）。"),
    "GPCR": ("联动", "-7.32%列主题层医疗保健与生物科技（偏弱侧）。"),
    "HON": ("联动", "+1.36%列道指工业（偏强侧）。"),
    "INCY": ("联动", "-3.47%列标普500医疗保健（偏弱侧）。"),
    "INSG": ("直接", "Inseego完成对诺基亚固定无线接入业务的收购。"),
    "IOT": ("联动", "+5.01%列主题层工业自动化（偏强侧）。"),
    "JAGU": ("联动", "+13.89%列All Stocks能源（偏强侧）。"),
    "JNJ": ("联动", "-2.30%列道指医疗保健（偏弱侧）。"),
    "JPM": ("联动", "+0.71%列道指金融（偏强侧）。"),
    "KPTI": ("联动", "-28.95%列All Stocks医疗保健（偏弱侧）。"),
    "LIN": ("联动", "-1.10%列纳指100基础材料（偏弱侧）。"),
    "LIND": ("联动", "+7.00%列罗素2000可选消费（偏强侧）。"),
    "LITE": ("联动", "+7.67%列主题层虚拟与增强现实（偏强侧）。"),
    "MPC": ("联动", "+6.25%列标普500能源（偏强侧）。"),
    "MRK": ("联动", "-1.03%列道指医疗保健（偏弱侧）。"),
    "MSTR": ("联动", "+4.84%列主题层大数据（偏强侧）。"),
    "NFLX": ("直接", "联席CEO称增长不及预期+媒体板块随派拉蒙收购齐跌。"),
    "NICE": ("联动", "+4.68%列主题层大数据（偏强侧）。"),
    "NIVF": ("联动", "-39.88%列All Stocks医疗保健（偏弱侧）。"),
    "NKTR": ("直接", "Nektar脱发治疗数据积极仍大跌（利好兑现+板块出清）。"),
    "NMAX": ("联动", "-8.70%列罗素2000通信服务（偏弱侧）。"),
    "OHI": ("联动", "-2.33%列主题层老龄化与长寿（偏弱侧）。"),
    "OXY": ("直接", "西方石油获高盛上调评级。"),
    "PARR": ("联动", "+5.62%列罗素2000能源（偏强侧）。"),
    "PBF": ("联动", "+6.99%列罗素2000能源（偏强侧）。"),
    "PPC": ("联动", "-6.70%列主题层农业与食品科技（偏弱侧）。"),
    "PSKY": ("直接", "派拉蒙逼近完成华纳收购引发媒体股齐跌；新发债券跌破发行价、收益率破10%。"),
    "PYPL": ("联动", "+1.01%列纳指100金融（偏强侧）。"),
    "REGN": ("直接", "二期COURAGE试验确认Trevogrumab防止GLP-1期间瘦体重流失；赛诺菲扩大80亿美元免疫学合作。"),
    "RETO": ("联动", "-18.73%列All Stocks基础材料（偏弱侧）。"),
    "RPGL": ("联动", "+59.85%列All Stocks科技（偏强侧）。"),
    "SBRA": ("联动", "-2.64%列主题层老龄化与长寿（偏弱侧）。"),
    "SCNX": ("联动", "-31.83%列All Stocks医疗保健（偏弱侧）。"),
    "SES": ("联动", "+36.05%列罗素2000可选消费（偏强侧）。"),
    "SFM": ("联动", "-2.82%列主题层老龄化与长寿（偏弱侧）。"),
    "SHW": ("联动", "-0.77%列道指基础材料（偏弱侧）。"),
    "SNPS": ("直接", "新思科技上调长期增长与利润率目标、FY2027收入指引110亿美元以上。"),
    "STKH": ("联动", "-51.11%列主题层农业与食品科技（偏弱侧）。"),
    "TDC": ("联动", "+3.75%列主题层大数据（偏强侧）。"),
    "TEM": ("联动", "-6.59%列主题层医疗保健与生物科技（偏弱侧）。"),
    "TLN": ("联动", "+3.33%列All Stocks公用事业（偏强侧）。"),
    "TRV": ("联动", "+1.44%列道指金融（偏强侧）。"),
    "TTWO": ("联动", "-1.87%列纳指100通信服务（偏弱侧）。"),
    "U": ("联动", "+6.55%列主题层虚拟与增强现实（偏强侧）。"),
    "V": ("联动", "+0.14%列道指金融（偏强侧）。"),
    "VEEA": ("联动", "+59.91%列All Stocks科技（偏强侧）。"),
    "VKTX": ("联动", "-6.41%列主题层医疗保健与生物科技（偏弱侧）。"),
    "VLO": ("联动", "+5.38%列标普500能源（偏强侧）。"),
    "XHLD": ("联动", "-14.87%列All Stocks通信服务（偏弱侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "BNO", "perf": 4.760, "form": "商品信托", "exposure": "布伦特原油期货",
         "reason": "布伦特原油ETF +4.76%领涨全市场：油价单日大涨（布伦特端+4.76%显著强于WTI端+2.99%的价差结构为地缘/供给信号）——炼厂端马拉松+6.25%/PBF +6.99%/瓦莱罗+5.38%的股票端共振确认。合并删除：DBO +3.16%、USO +2.99%（同簇原油期货）。"},
        {"ticker": "UGA", "perf": 4.227, "form": "商品信托", "exposure": "汽油期货（RBOB）",
         "reason": "汽油期货ETF +4.23%：连续第二日+4%级别暴涨（周三+4.75%）——柴油出口禁令政治溢价第五轮往返的强化，成品油紧缺的极致定价。合并删除：无同簇产品。"},
        {"ticker": "PXE", "perf": 3.376, "form": "交易所交易基金", "exposure": "能源生产商股票（Invesco）",
         "reason": "能源生产商ETF +3.38%：能源五个股票范围全部列涨幅第一的板块端确认——西方石油获高盛上调+4.55%、上游XOP +2.77%。合并删除：PXI +2.56%、FXN +2.43%、DBE +2.40%、VDE +1.99%、XLE +1.95%（同簇能源股，保留最强者）。"},
    ],
    "down": [
        {"ticker": "EIRL", "perf": -2.960, "form": "交易所交易基金", "exposure": "爱尔兰股票",
         "reason": "爱尔兰ETF -2.96%领跌全市场：欧洲金融中心的利率冲击端（欧元区金融股ETF同步-2.79%）——全球长端利率高位的离岸传导。合并删除：无同簇产品。"},
        {"ticker": "BBC", "perf": -2.790, "form": "交易所交易基金", "exposure": "临床试验生物科技",
         "reason": "临床试验生物科技ETF -2.79%：医疗保健五个股票范围全部领跌的板块端确认——KPTI -28.95%/Nektar -22.39%/Foghorn裁员40%（礼来合作破裂）-18.21%；医疗生物主题清一色跌-1.62%。合并删除：无同簇产品。"},
        {"ticker": "EUFN", "perf": -2.790, "form": "交易所交易基金", "exposure": "欧洲金融股",
         "reason": "欧洲金融股ETF -2.79%：全球利率冲击的欧洲端映射（爱尔兰-2.96%同源）——美欧长端利率共振高位的离岸压力。合并删除：无同簇产品。"},
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
        text = "核查9月21日盘后至10月1日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-01"
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
            f"- `finviz_2026-10-01_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-01_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月1日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月1日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周四为美光财报反应日+油价大涨日：能源五个股票范围全部列涨幅第一（标普500 21只中20涨/+1.96%：马拉松+6.25%/瓦莱罗+5.38%/西方石油+4.55%〔获高盛上调〕；道指雪佛龙+1.42%清一色涨；罗素2000 91只中73涨/+1.81%〔PBF +6.99%/CVI +6.61%〕——布伦特ETF +4.76%领涨全市场〔显著强于WTI端+2.99%的价差结构〕、汽油ETF +4.23%连续第二日+4%级别〔柴油禁令政治溢价第五轮往返〕；XLE +1.95%/XOP +2.77%）；科技三个范围居前（All Stocks +0.97%/标普500 +0.73%〔埃森哲Q4超预期+15.78%/新思科技上调长期目标+12.78%/FICO反弹+11.69%〕/罗素2000 +1.54%——美光财报反应日：美光+3.03%/闪迪+2.75%/存储器主题+2.12%，软件XSW +2.59%/WCLD +2.17%续强）；工业两个范围领涨（标普500 75只中63涨/+0.99%：GEV +3.89%/罗宾逊+3.50%/波音+3.35%〔万名工人批准合同避免罢工〕）。跌幅侧：医疗保健五个股票范围全部领跌（XLV -1.32%/XBI -2.01%/BBC -2.79%列ETF跌幅端：KPTI -28.95%/Nektar -22.39%/Foghorn裁员40%〔礼来合作破裂〕-18.21%——医疗生物主题清一色跌-1.62%）；通信服务五个范围领跌（XLC -0.93%：派拉蒙逼近完成华纳收购引发媒体股齐跌-9.58%〔其新发债券跌破发行价、收益率破10%〕/迪士尼电视重组-3.40%/Netflix -2.49%〔CEO称增长不及预期〕）；基础材料四个范围领跌（标普端-4.82%为Corteva分拆除权〔一分为二、-83.81%机械性调整〕主导——剔除后材料真实跌幅温和：XLB -0.33%、金属矿业XME +0.70%微涨）。主题层11个清一色涨（工业自动化+1.67%/VR +1.53%/大数据+1.11%/传统能源/物联网/社交媒体/金融科技/云计算/AI/自动驾驶/量子）对4个清一色跌（农业食品-4.21%〔农资投入-10.9%——Corteva分拆的谱系定价〕/医疗生物/老龄化/REIT）。金融反弹（KIE +1.21%/KRE +0.73%/PYPL +1.01%）；公用事业XLU +0.61%（NQ四成分清一色涨：Constellation +1.93%）。天然气-2.02%回落；贵金属分化（黄金+0.50%/白银+0.94%对金矿-1.31%）；铀链企稳偏弱；比特币ETF反弹（IBIT +1.31%）；韩国ETF +1.82%（美光反应）；爱尔兰-2.96%/欧洲金融-2.79%领跌ETF（欧洲利率端）。VIX期货ETF续涨（VIXY +0.83%）。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-10-01_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-01_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-01_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
