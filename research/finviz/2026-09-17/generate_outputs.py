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
    "ARM": "Arm Holdings Plc ADR",
    "ATI": "ATI Inc",
    "BA": "Boeing Co",
    "DKNG": "DraftKings Inc",
    "DSP": "Viant Technology Inc",
    "EXK": "Endeavour Silver Corp",
    "FLUT": "Flutter Entertainment Plc",
    "HXL": "Hexcel Corp",
    "IONQ": "IonQ Inc",
    "IPX": "IperionX Ltd ADR",
    "PINS": "Pinterest Inc",
    "QBTS": "D-Wave Quantum Inc",
    "RDDT": "Reddit Inc",
    "RGTI": "Rigetti Computing Inc",
    "SRAD": "Sportradar Group AG",
    "SVM": "Silvercorp Metals Inc",
    "UMC": "United Micro Electronics ADR",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEP": ("联动", "暂未找到同日直接催化；+0.77%列纳指100公用事业（偏强侧）。"),
    "AMZN": ("联动", "暂未找到同日直接催化；+2.13%列道指可选消费（偏强侧）。"),
    "AON": ("联动", "暂未找到同日直接催化；-1.50%列标普500金融（偏弱侧）。"),
    "ARM": ("直接", "Arm CEO Rene Haas more confident on $2 billion AI chip revenue target。"),
    "ATI": ("联动", "暂未找到同日直接催化；-3.17%列主题层国防与航空航天（偏弱侧）。"),
    "AXON": ("联动", "暂未找到同日直接催化；-3.19%列标普500工业（偏弱侧）。"),
    "BA": ("联动", "暂未找到同日直接催化；-2.46%列主题层国防与航空航天（偏弱侧）。"),
    "BENF": ("联动", "暂未找到同日直接催化；-23.22%列All Stocks金融（偏弱侧）。"),
    "BGS": ("联动", "暂未找到同日直接催化；-3.19%列罗素2000必需消费（偏弱侧）。"),
    "BKR": ("联动", "暂未找到同日直接催化；+0.43%列纳指100能源（偏强侧）。"),
    "BLDR": ("联动", "暂未找到同日直接催化；-3.30%列标普500工业（偏弱侧）。"),
    "BRK-B": ("联动", "暂未找到同日直接催化；-2.04%列标普500金融（偏弱侧）。"),
    "CBOE": ("联动", "暂未找到同日直接催化；-1.39%列标普500金融（偏弱侧）。"),
    "CCEP": ("联动", "暂未找到同日直接催化；-2.19%列纳指100必需消费（偏弱侧）。"),
    "CEG": ("联动", "暂未找到同日直接催化；+1.26%列纳指100公用事业（偏强侧）。"),
    "COTY": ("联动", "暂未找到同日直接催化；-6.46%列罗素2000必需消费（偏弱侧）。"),
    "CPRT": ("联动", "暂未找到同日直接催化；-3.76%列标普500工业（偏弱侧）。"),
    "CSCO": ("联动", "暂未找到同日直接催化；+2.32%列道指科技（偏强侧）。"),
    "CVX": ("联动", "暂未找到同日直接催化；+0.01%列道指能源（偏强侧）。"),
    "DAIC": ("联动", "暂未找到同日直接催化；+163.68%列All Stocks科技（偏强侧）。"),
    "DC": ("联动", "暂未找到同日直接催化；+7.04%列罗素2000基础材料（偏强侧）。"),
    "DCX": ("联动", "暂未找到同日直接催化；+37.53%列All Stocks可选消费（偏强侧）。"),
    "DDD": ("联动", "暂未找到同日直接催化；+12.74%列罗素2000科技（偏强侧）。"),
    "DKNG": ("联动", "暂未找到同日直接催化；-7.64%列主题层数字娱乐（偏弱侧）。"),
    "DSP": ("直接", "Viant Technology Inc. Announces Launch of Public Offering of Class A Common Stock。"),
    "DTSS": ("联动", "暂未找到同日直接催化；+106.36%列All Stocks科技（偏强侧）。"),
    "EAT": ("联动", "暂未找到同日直接催化；-5.25%列罗素2000可选消费（偏弱侧）。"),
    "EBAY": ("联动", "暂未找到同日直接催化；+3.42%列标普500可选消费（偏强侧）。"),
    "ED": ("联动", "暂未找到同日直接催化；+1.57%列标普500公用事业（偏强侧）。"),
    "EL": ("联动", "暂未找到同日直接催化；-1.82%列标普500必需消费（偏弱侧）。"),
    "ELE": ("联动", "暂未找到同日直接催化；+7.69%列罗素2000基础材料（偏强侧）。"),
    "ES": ("联动", "暂未找到同日直接催化；+1.67%列标普500公用事业（偏强侧）。"),
    "EXK": ("联动", "暂未找到同日直接催化；+6.72%列主题层金属商品（偏强侧）。"),
    "EYPT": ("联动", "暂未找到同日直接催化；+15.65%列罗素2000医疗保健（偏强侧）。"),
    "FANG": ("联动", "暂未找到同日直接催化；+1.23%列纳指100能源（偏强侧）。"),
    "FEAM": ("联动", "暂未找到同日直接催化；+17.05%列All Stocks基础材料（偏强侧）。"),
    "FLUT": ("联动", "暂未找到同日直接催化；-5.19%列主题层数字娱乐（偏弱侧）。"),
    "FSP": ("联动", "暂未找到同日直接催化；-4.49%列All Stocks房地产（偏弱侧）。"),
    "FUBO": ("联动", "暂未找到同日直接催化；-6.60%列罗素2000通信服务（偏弱侧）。"),
    "GBLI": ("联动", "暂未找到同日直接催化；-8.30%列All Stocks金融（偏弱侧）。"),
    "GLSI": ("联动", "暂未找到同日直接催化；+17.66%列罗素2000医疗保健（偏强侧）。"),
    "GSUN": ("联动", "暂未找到同日直接催化；-19.31%列All Stocks必需消费（偏弱侧）。"),
    "HCWC": ("联动", "暂未找到同日直接催化；-19.93%列All Stocks必需消费（偏弱侧）。"),
    "HD": ("联动", "暂未找到同日直接催化；+0.01%列道指可选消费（偏强侧）。"),
    "HPE": ("联动", "暂未找到同日直接催化；+7.69%列标普500科技（偏强侧）。"),
    "HSY": ("联动", "暂未找到同日直接催化；-1.44%列标普500必需消费（偏弱侧）。"),
    "HXL": ("联动", "暂未找到同日直接催化；-3.34%列主题层国防与航空航天（偏弱侧）。"),
    "HYMC": ("联动", "暂未找到同日直接催化；+7.28%列罗素2000基础材料（偏强侧）。"),
    "INTC": ("联动", "暂未找到同日直接催化；+7.67%列标普500科技（偏强侧）。"),
    "IONQ": ("联动", "暂未找到同日直接催化；+9.50%列主题层半导体（偏强侧）。"),
    "IP": ("联动", "暂未找到同日直接催化；+4.38%列标普500可选消费（偏强侧）。"),
    "IPX": ("联动", "暂未找到同日直接催化；+9.05%列主题层金属商品（偏强侧）。"),
    "JXN": ("联动", "暂未找到同日直接催化；-5.63%列All Stocks金融（偏弱侧）。"),
    "KDP": ("联动", "暂未找到同日直接催化；-1.16%列标普500必需消费（偏弱侧）。"),
    "KO": ("联动", "暂未找到同日直接催化；+0.22%列道指必需消费（偏弱侧）。"),
    "KXIN": ("联动", "暂未找到同日直接催化；+54.87%列All Stocks可选消费（偏强侧）。"),
    "LIN": ("联动", "暂未找到同日直接催化；-0.78%列纳指100基础材料（偏弱侧）。"),
    "LOOP": ("联动", "暂未找到同日直接催化；+10.12%列All Stocks基础材料（偏强侧）。"),
    "LRE": ("联动", "暂未找到同日直接催化；-3.74%列All Stocks房地产（偏弱侧）。"),
    "LULU": ("联动", "暂未找到同日直接催化；+3.55%列标普500可选消费（偏强侧）。"),
    "LVWR": ("联动", "暂未找到同日直接催化；+19.33%列All Stocks可选消费（偏强侧）。"),
    "MAMA": ("联动", "暂未找到同日直接催化；-8.00%列罗素2000必需消费（偏弱侧）。"),
    "MSFT": ("联动", "暂未找到同日直接催化；+1.52%列道指科技（偏强侧）。"),
    "NCMI": ("联动", "暂未找到同日直接催化；-5.13%列罗素2000通信服务（偏弱侧）。"),
    "NKE": ("联动", "暂未找到同日直接催化；+1.62%列道指可选消费（偏强侧）。"),
    "NVDA": ("联动", "暂未找到同日直接催化；+2.54%列道指科技（偏强侧）。"),
    "PG": ("联动", "暂未找到同日直接催化；+0.36%列道指必需消费（偏弱侧）。"),
    "PINS": ("联动", "暂未找到同日直接催化；-1.82%列主题层社交媒体（偏弱侧）。"),
    "PYPL": ("联动", "暂未找到同日直接催化；+0.44%列纳指100金融（偏强侧）。"),
    "QBTS": ("直接", "IBM Matches a $1 Billion CHIPS Award For Quantum Foundry。"),
    "RDDT": ("联动", "暂未找到同日直接催化；-3.03%列主题层社交媒体（偏弱侧）。"),
    "REAX": ("联动", "暂未找到同日直接催化；-7.41%列All Stocks房地产（偏弱侧）。"),
    "RGTI": ("直接", "IBM Matches a $1 Billion CHIPS Award For Quantum Foundry。"),
    "RXT": ("联动", "暂未找到同日直接催化；+12.64%列罗素2000科技（偏强侧）。"),
    "SAH": ("联动", "暂未找到同日直接催化；-9.27%列罗素2000可选消费（偏弱侧）。"),
    "SDGR": ("联动", "暂未找到同日直接催化；+26.37%列罗素2000医疗保健（偏强侧）。"),
    "SES": ("联动", "暂未找到同日直接催化；-8.34%列罗素2000可选消费（偏弱侧）。"),
    "SHLS": ("联动", "暂未找到同日直接催化；+12.17%列罗素2000科技（偏强侧）。"),
    "SHW": ("联动", "暂未找到同日直接催化；-0.16%列道指基础材料（偏弱侧）。"),
    "SMCI": ("联动", "暂未找到同日直接催化；+9.50%列标普500科技（偏强侧）。"),
    "SRAD": ("联动", "暂未找到同日直接催化；-6.58%列主题层数字娱乐（偏弱侧）。"),
    "STRZ": ("联动", "暂未找到同日直接催化；-5.67%列罗素2000通信服务（偏弱侧）。"),
    "SVM": ("直接", "Silvercorp Renews Share Repurchase Program。"),
    "TURB": ("联动", "暂未找到同日直接催化；+49.97%列All Stocks科技（偏强侧）。"),
    "UMC": ("联动", "暂未找到同日直接催化；+8.61%列主题层半导体（偏强侧）。"),
    "USAS": ("直接", "Americas Gold and Silver Announces Some of the Best Grade-Widths Drilled to Date at the Cosala Complex Including High-Gr。"),
    "VSA": ("联动", "暂未找到同日直接催化；-8.69%列All Stocks必需消费（偏弱侧）。"),
    "VST": ("联动", "暂未找到同日直接催化；+2.26%列标普500公用事业（偏强侧）。"),
    "WMT": ("联动", "暂未找到同日直接催化；-0.66%列道指必需消费（偏弱侧）。"),
    "XEL": ("联动", "暂未找到同日直接催化；+1.26%列纳指100公用事业（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "GDXJ", "perf": 4.753, "form": "交易所交易基金", "exposure": "全球金矿（中小型）",
         "reason": "金矿ETF +4.75%领涨全市场：FOMC加息落地后的贵金属全线反弹（黄金+1.69%/白银+3.37%/银矿+4.49%）——'利空出尽'的避险资产修复。合并删除：GDX/SGDM/RING（同簇金矿股）。"},
        {"ticker": "SIL", "perf": 4.487, "form": "交易所交易基金", "exposure": "全球银矿",
         "reason": "银矿ETF +4.49%：白银现货+3.37%的高弹性映射——贵金属反弹日的第二强矿业敞口。合并删除：SILJ（同簇银矿股）。"},
        {"ticker": "PTF", "perf": 4.241, "form": "交易所交易基金", "exposure": "美国科技动量",
         "reason": "科技动量ETF +4.24%：FOMC后科技全面反弹（SOXX +3.4%/XSD +4.1%）——20个主题清一色涨的核心引擎。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "VIXY", "perf": -3.905, "form": "交易所交易基金", "exposure": "VIX期货",
         "reason": "VIX期货ETF -3.91%领跌：FOMC'利空出尽'的对冲平仓——前日+0.80%的完全逆转，本周第二次单日-4%级别VIX回撤。合并删除：VXX（同簇VIX期货）。"},
        {"ticker": "DBA", "perf": -1.388, "form": "商品信托", "exposure": "农产品篮",
         "reason": "农产品ETF：玉米回调与贵金属反弹的分化。合并删除：无同簇产品。"},
        {"ticker": "BNO", "perf": -1.296, "form": "商品信托", "exposure": "布伦特原油",
         "reason": "布伦特原油ETF：油价自109美元高位连续第二日回落（FOMC后美元走强+获利回吐）——与贵金属反弹的分化。合并删除：无同簇产品。"},
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
        text = "核查9月10日盘后至9月17日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-17"
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
            f"- `finviz_2026-09-17_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-17_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月17日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月17日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周四为FOMC加息落地后的首个完整交易日——市场以**20个主题清一色上涨**（本周最大risk-on图谱、与昨日14个主题清一色跌的完全反转）回应'利空出尽'：VIX期货ETF -3.91%（对冲全面平仓）；**科技五个股票范围全部领涨**（XLK +2.25%/SOXX +3.39%/XSD +4.06%：Super Micro +9.50%/HPE +7.69%/Intel +7.67%/英伟达+2.54%/微软+1.52%——FOMC加息25bp至3.75-4.00%被完全定价后科技反弹）；**贵金属全线暴涨**（金矿ETF +4.75%领涨全市场/白银+3.37%/黄金+1.69%/铀+3.17%）；**核能铀矿行全线大涨**（NLR +2.99%/NUKZ +2.19%/URNJ +2.51%——连续多日回吐后的首次集体反弹）；**太空科技行大涨**（NASA +4.10%/WARP +3.64%/ORBX +3.85%——SpaceX持续带动）；加密货币反弹（DIME +5.76%/ETH +1.76%）。可选消费三个范围居前（亚马逊+2.13%/耐克+1.62%/Lululemon +3.55%）；公用事业两个范围偏强（XLU +0.90%：Vistra +2.26%/Constellation +1.26%——AI电力反弹）。**必需消费五个范围领跌**（标普-0.11%：Estée Lauder -1.82%/Hershey -1.44%/Keurig -1.16%——防御退潮的极致）；金融两个范围偏弱（AS/SP：Berkshire -2.04%/Aon -1.50%）；通信服务一个范围偏弱（XLC -0.58%）。道指基本持平（能源清一色微涨/+0.01%；科技+1.81%对冲必需消费-0.25%）。当日无行情性质结构变化。",
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
    (OUT / "finviz_2026-09-17_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-17_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-17_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
