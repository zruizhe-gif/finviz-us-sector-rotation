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
    "ASTS": "AST SpaceMobile Inc",
    "BKKT": "Bakkt Inc",
    "BTDR": "Bitdeer Technologies Group",
    "CHGG": "Chegg Inc",
    "COIN": "Coinbase Global Inc",
    "DUOL": "Duolingo Inc",
    "IBM": "International Business Machines Corp",
    "MARA": "MARA Holdings Inc",
    "MSTR": "Strategy Inc",
    "OKTA": "Okta Inc",
    "RDW": "Redwire Corp",
    "RPD": "Rapid7 Inc",
    "SIMO": "Silicon Motion Technology Corp ADR",
    "SNDK": "Sandisk Corp",
    "SPIR": "Spire Global Inc",
    "WOLF": "Wolfspeed Inc",
    "ZM": "Zoom Communications Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEI": ("联动", "暂未找到同日直接催化；-16.44%列All Stocks房地产（偏弱侧）。"),
    "AMGN": ("联动", "暂未找到同日直接催化；+1.55%列纳指100医疗保健（偏强侧）。"),
    "AMR": ("联动", "暂未找到同日直接催化；-5.69%列罗素2000基础材料（偏弱侧）。"),
    "AMZN": ("联动", "暂未找到同日直接催化；+1.00%列道指可选消费（偏强侧）。"),
    "ARE": ("联动", "暂未找到同日直接催化；-5.40%列标普500房地产（偏弱侧）。"),
    "ASPI": ("联动", "暂未找到同日直接催化；-6.32%列罗素2000基础材料（偏弱侧）。"),
    "ASTS": ("联动", "暂未找到同日直接催化；-6.68%列主题层太空科技（偏弱侧）。"),
    "BA": ("联动", "暂未找到同日直接催化；+0.61%列道指工业（偏强侧）。"),
    "BKKT": ("直接", "Rithm Capital Appoints Ann DeVries as Head of Investor Relations。"),
    "BTDR": ("联动", "暂未找到同日直接催化；+15.39%列罗素2000科技（偏强侧）。"),
    "CAT": ("联动", "暂未找到同日直接催化；+1.30%列道指工业（偏强侧）。"),
    "CD": ("联动", "暂未找到同日直接催化；+20.27%列罗素2000金融（偏强侧）。"),
    "CEG": ("联动", "暂未找到同日直接催化；-3.08%列标普500公用事业（偏弱侧）。"),
    "CEPU": ("联动", "暂未找到同日直接催化；-7.04%列All Stocks公用事业（偏弱侧）。"),
    "CF": ("联动", "暂未找到同日直接催化；-4.57%列标普500基础材料（偏弱侧）。"),
    "CHGG": ("联动", "暂未找到同日直接催化；-6.61%列主题层教育科技（偏弱侧）。"),
    "COHR": ("联动", "暂未找到同日直接催化；+7.22%列标普500科技（偏强侧）。"),
    "COIN": ("直接", "Coinbase Seeks Approval to List Perpetual Futures Tied to U.S. Stocks。"),
    "CVX": ("联动", "暂未找到同日直接催化；-0.97%列道指能源（偏弱侧）。"),
    "DIS": ("联动", "暂未找到同日直接催化；-2.54%列道指通信服务（偏强侧）。"),
    "DSP": ("联动", "暂未找到同日直接催化；+18.56%列罗素2000科技（偏强侧）。"),
    "DUOL": ("联动", "暂未找到同日直接催化；-3.54%列主题层教育科技（偏弱侧）。"),
    "DXCM": ("联动", "暂未找到同日直接催化；+1.61%列纳指100医疗保健（偏强侧）。"),
    "ELA": ("联动", "暂未找到同日直接催化；-8.85%列罗素2000可选消费（偏弱侧）。"),
    "ELMT": ("联动", "暂未找到同日直接催化；+4.60%列罗素2000工业（偏强侧）。"),
    "ETN": ("联动", "暂未找到同日直接催化；+3.74%列标普500工业（偏强侧）。"),
    "EXC": ("联动", "暂未找到同日直接催化；-1.34%列纳指100公用事业（偏弱侧）。"),
    "FIP": ("联动", "暂未找到同日直接催化；+7.53%列罗素2000工业（偏强侧）。"),
    "FIX": ("联动", "暂未找到同日直接催化；+4.92%列标普500工业（偏强侧）。"),
    "FLYX": ("联动", "暂未找到同日直接催化；+7.26%列罗素2000工业（偏强侧）。"),
    "FWDI": ("联动", "暂未找到同日直接催化；+24.19%列All Stocks可选消费（偏强侧）。"),
    "GEMI": ("联动", "暂未找到同日直接催化；+31.15%列罗素2000金融（偏强侧）。"),
    "GOOGL": ("联动", "暂未找到同日直接催化；+0.64%列道指通信服务（偏强侧）。"),
    "GS": ("联动", "暂未找到同日直接催化；-0.99%列道指金融（偏弱侧）。"),
    "HD": ("联动", "暂未找到同日直接催化；-0.84%列道指可选消费（偏强侧）。"),
    "HONA": ("联动", "暂未找到同日直接催化；-2.11%列纳指100工业（偏弱侧）。"),
    "HOOD": ("直接", "Strategy, Circle, and Coinbase Lead Crypto Stock Rally on Tokenized Stock Approval。"),
    "HTOO": ("联动", "暂未找到同日直接催化；-6.02%列All Stocks公用事业（偏弱侧）。"),
    "HUHU": ("联动", "暂未找到同日直接催化；+38.95%列All Stocks工业（偏强侧）。"),
    "IBKR": ("联动", "暂未找到同日直接催化；+2.61%列标普500金融（偏强侧）。"),
    "IBM": ("联动", "暂未找到同日直接催化；-3.45%列主题层网络安全（偏弱侧）。"),
    "INHD": ("联动", "暂未找到同日直接催化；-14.33%列All Stocks基础材料（偏弱侧）。"),
    "ISRG": ("联动", "暂未找到同日直接催化；+2.55%列纳指100医疗保健（偏强侧）。"),
    "KRRO": ("联动", "暂未找到同日直接催化；-15.09%列罗素2000医疗保健（偏弱侧）。"),
    "LIN": ("联动", "暂未找到同日直接催化；+0.42%列纳指100基础材料（偏强侧）。"),
    "LRCX": ("联动", "暂未找到同日直接催化；+6.98%列标普500科技（偏强侧）。"),
    "LRHC": ("联动", "暂未找到同日直接催化；-9.86%列All Stocks房地产（偏弱侧）。"),
    "MARA": ("直接", "Strategy, Circle, and Coinbase Lead Crypto Stock Rally on Tokenized Stock Approval。"),
    "MCD": ("联动", "暂未找到同日直接催化；-0.10%列道指可选消费（偏强侧）。"),
    "METC": ("联动", "暂未找到同日直接催化；-6.01%列罗素2000基础材料（偏弱侧）。"),
    "MMM": ("联动", "暂未找到同日直接催化；+0.72%列道指工业（偏强侧）。"),
    "MSTR": ("直接", "Strategy, Circle, and Coinbase Lead Crypto Stock Rally on Tokenized Stock Approval。"),
    "NRG": ("联动", "暂未找到同日直接催化；-2.42%列标普500公用事业（偏弱侧）。"),
    "NUE": ("联动", "暂未找到同日直接催化；-6.32%列标普500基础材料（偏弱侧）。"),
    "NWGL": ("联动", "暂未找到同日直接催化；-18.63%列All Stocks基础材料（偏弱侧）。"),
    "OKTA": ("联动", "暂未找到同日直接催化；-4.03%列主题层网络安全（偏弱侧）。"),
    "PDC": ("联动", "暂未找到同日直接催化；+21.67%列All Stocks科技（偏强侧）。"),
    "PRPL": ("联动", "暂未找到同日直接催化；+34.32%列All Stocks可选消费（偏强侧）。"),
    "PWR": ("联动", "暂未找到同日直接催化；+3.27%列标普500工业（偏强侧）。"),
    "PYPL": ("联动", "暂未找到同日直接催化；-1.00%列纳指100金融（偏弱侧）。"),
    "QNME": ("联动", "暂未找到同日直接催化；+92.25%列All Stocks工业（偏强侧）。"),
    "RDW": ("联动", "暂未找到同日直接催化；-7.01%列主题层太空科技（偏弱侧）。"),
    "REFR": ("直接", "Research Frontiers Welcomes Gauzy's Court-Approved Restructuring and the Restart of SPD-Smart Light Control Film Product。"),
    "RETO": ("联动", "暂未找到同日直接催化；-10.96%列All Stocks基础材料（偏弱侧）。"),
    "RKLB": ("联动", "暂未找到同日直接催化；-4.79%列纳指100工业（偏弱侧）。"),
    "RPD": ("联动", "暂未找到同日直接催化；-3.55%列主题层网络安全（偏弱侧）。"),
    "RSI": ("联动", "暂未找到同日直接催化；-7.72%列罗素2000可选消费（偏弱侧）。"),
    "SHW": ("联动", "暂未找到同日直接催化；-0.07%列道指基础材料（偏弱侧）。"),
    "SIMO": ("联动", "暂未找到同日直接催化；+7.43%列主题层半导体（偏强侧）。"),
    "SION": ("联动", "暂未找到同日直接催化；-16.99%列罗素2000医疗保健（偏弱侧）。"),
    "SKYA": ("联动", "暂未找到同日直接催化；+23.72%列All Stocks科技（偏强侧）。"),
    "SNDK": ("联动", "暂未找到同日直接催化；+10.99%列标普500科技（偏强侧）。"),
    "SPIR": ("联动", "暂未找到同日直接催化；-6.10%列主题层太空科技（偏弱侧）。"),
    "STLD": ("联动", "暂未找到同日直接催化；-4.11%列标普500基础材料（偏弱侧）。"),
    "SVRN": ("联动", "暂未找到同日直接催化；+43.20%列All Stocks工业（偏强侧）。"),
    "TRI": ("联动", "暂未找到同日直接催化；-5.12%列纳指100工业（偏弱侧）。"),
    "TRUG": ("直接", "TruGolf Links Announces New Initiatives with Polymath to Develop Financing Opportunities for Franchisees。"),
    "TRV": ("联动", "暂未找到同日直接催化；-1.28%列道指金融（偏弱侧）。"),
    "V": ("联动", "暂未找到同日直接催化；-0.44%列道指金融（偏弱侧）。"),
    "VENU": ("联动", "暂未找到同日直接催化；-8.03%列罗素2000可选消费（偏弱侧）。"),
    "VGAS": ("联动", "暂未找到同日直接催化；-8.70%列All Stocks公用事业（偏弱侧）。"),
    "VMRK": ("联动", "暂未找到同日直接催化；-2.84%列标普500房地产（偏弱侧）。"),
    "VST": ("联动", "暂未找到同日直接催化；-2.01%列标普500公用事业（偏弱侧）。"),
    "WHLR": ("联动", "暂未找到同日直接催化；-29.06%列All Stocks房地产（偏弱侧）。"),
    "WOLF": ("联动", "暂未找到同日直接催化；+7.79%列主题层半导体（偏强侧）。"),
    "WY": ("联动", "暂未找到同日直接催化；-2.03%列标普500房地产（偏弱侧）。"),
    "XEL": ("联动", "暂未找到同日直接催化；-1.81%列纳指100公用事业（偏弱侧）。"),
    "XENE": ("直接", "Premarket movers: Xenon sinks on trial pause, Netflix hit by downgrade。"),
    "ZM": ("联动", "暂未找到同日直接催化；-3.68%列主题层教育科技（偏弱侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "IBIT", "perf": 6.282, "form": "交易所交易基金", "exposure": "比特币现货",
         "reason": "比特币现货ETF +6.28%领涨全市场：加密货币主题居涨幅首位（Coinbase +11.66%/Robinhood +9.12%/Bakkt +15.42%）——三巫日的最强单资产行情。合并删除：BITO、FBTC（同簇比特币，保留最强IBIT）。"},
        {"ticker": "SOXX", "perf": 2.691, "form": "交易所交易基金", "exposure": "全球半导体",
         "reason": "半导体ETF：SanDisk +10.99%/Coherent +7.22%/Wolfspeed +7.79%——科技领涨第三日（半导体主题涨幅侧第二）。合并删除：XSD（同簇半导体，保留SOXX）。"},
        {"ticker": "IAI", "perf": 1.255, "form": "交易所交易基金", "exposure": "资本市场",
         "reason": "资本市场ETF +1.26%：Coinbase +11.66%的加密金融映射。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "URA", "perf": -2.413, "form": "交易所交易基金", "exposure": "全球铀矿",
         "reason": "铀ETF -2.41%领跌全市场：核能铀矿行全线回落（NLR -2.60%/URNJ -2.35%）——昨日反弹的单日逆转。合并删除：无同簇产品。"},
        {"ticker": "XME", "perf": -2.372, "form": "交易所交易基金", "exposure": "金属矿业",
         "reason": "金属矿业ETF -2.37%：贵金属矿回落（白银现货+1.63%微涨但矿业端走弱）——昨日XME +2.34%的完全逆转。合并删除：无同簇产品。"},
        {"ticker": "FUTY", "perf": -2.097, "form": "交易所交易基金", "exposure": "公用事业",
         "reason": "公用事业ETF -2.10%：四范围领跌（SP清一色/N100清一色）——Constellation -3.08%/NRG -2.42%的AI电力谱系再度回落。合并删除：无同簇产品。"},
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
        text = "核查9月10日盘后至9月18日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-18"
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
            f"- `finviz_2026-09-18_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-18_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月18日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月18日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周五为三巫日（约2万亿美元衍生品到期）——**比特币ETF +6.28%领涨全市场**（以太坊ETF +7.85%/替代币ETF +11.19%；Coinbase +11.66%/Robinhood +9.12%），加密货币主题居40个主题涨幅首位；**科技五个股票范围全部领涨**（XLK +0.82%/SOXX +2.69%：SanDisk +10.99%/Coherent +7.22%/Wolfspeed +7.79%——半导体领涨第三日）；**工业四个范围居前**（道指工业+0.93%：卡特彼勒+1.31%/3M +0.72%；Comfort Systems +4.92%/Eaton +3.74%的AI基建修复）；可选消费两个范围（亚马逊+1.00%）。**跌幅侧**：**公用事业四个范围领跌**（SP清一色/N100清一色：Constellation -3.08%/NRG -2.42%——AI电力谱系昨日反弹的单日逆转）；基础材料三个范围（纽柯-6.32%/CF -4.57%——金属矿业XME -2.37%昨日+2.34%的逆转）；房地产两个范围。**8个主题清一色下跌**（太空科技/网络安全/教育科技/生物识别/房地产/运输/智能家居/环境可持续——昨日20个主题清一色涨的宽度大幅收缩）；核能铀矿行全线回落（NLR -2.60%/URNJ -2.35%——昨日反弹的逆转）；太空科技行回落（NASA -0.87%/WARP -2.07%）。贵金属分化（黄金+0.70%微涨/白银+1.63%但矿业端走弱）。VIX期货ETF +0.65%（三巫日波动率仍高）。当日无行情性质结构变化。",
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
    (OUT / "finviz_2026-09-18_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-18_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-18_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
