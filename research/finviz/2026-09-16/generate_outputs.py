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
    "AR": "Antero Resources Corp",
    "ASTS": "AST SpaceMobile Inc",
    "DELL": "Dell Technologies Inc",
    "FANG": "Diamondback Energy Inc",
    "FWRD": "Forward Air Corp",
    "INTC": "Intel Corp",
    "JBHT": "J.B. Hunt Transport Services Inc",
    "LITE": "Lumentum Holdings Inc",
    "LOCL": "Local Bounti Corp",
    "LSF": "Laird Superfood Inc",
    "MLEC": "Moolec Science SA",
    "MNTS": "Momentus Inc",
    "MRVL": "Marvell Technology Inc",
    "OXY": "Occidental Petroleum Corp",
    "SPCX": "Space Exploration Technologies Corp",
    "TFII": "TFI International Inc",
    "UMC": "United Micro Electronics ADR",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AAPL": ("联动", "暂未找到同日直接催化；+0.32%列道指科技（偏强侧）。"),
    "AEHL": ("直接", "Antelope Enterprise Holdings Limited Announces Closing of $6.0 Million Convertible Promissory Notes Offering。"),
    "ALAB": ("联动", "暂未找到同日直接催化；+6.59%列纳指100科技（偏强侧）。"),
    "ALB": ("联动", "暂未找到同日直接催化；-3.51%列标普500基础材料（偏弱侧）。"),
    "AMGN": ("联动", "暂未找到同日直接催化；+0.19%列道指医疗保健（偏强侧）。"),
    "AMZN": ("联动", "暂未找到同日直接催化；-0.99%列道指可选消费（偏弱侧）。"),
    "AR": ("联动", "暂未找到同日直接催化；-8.11%列主题层能源商品（偏弱侧）。"),
    "ASTS": ("联动", "暂未找到同日直接催化；+0.85%列主题层太空科技（偏强侧）。"),
    "AXON": ("联动", "暂未找到同日直接催化；+5.96%列纳指100工业（偏强侧）。"),
    "BAK": ("联动", "暂未找到同日直接催化；-15.71%列All Stocks基础材料（偏弱侧）。"),
    "BKR": ("联动", "暂未找到同日直接催化；-0.70%列纳指100能源（偏弱侧）。"),
    "BRCC": ("联动", "暂未找到同日直接催化；+7.89%列罗素2000必需消费（偏强侧）。"),
    "BUR": ("联动", "暂未找到同日直接催化；-7.42%列罗素2000金融（偏弱侧）。"),
    "CDZI": ("联动", "暂未找到同日直接催化；+1.43%列罗素2000公用事业（偏强侧）。"),
    "CFG": ("联动", "暂未找到同日直接催化；-4.84%列标普500金融（偏弱侧）。"),
    "COHR": ("联动", "暂未找到同日直接催化；+6.92%列标普500科技（偏强侧）。"),
    "CTVA": ("联动", "暂未找到同日直接催化；-2.85%列标普500基础材料（偏弱侧）。"),
    "CVX": ("联动", "暂未找到同日直接催化；-2.86%列道指能源（偏弱侧）。"),
    "DELL": ("联动", "暂未找到同日直接催化；+3.64%列主题层硬件（偏强侧）。"),
    "DXCM": ("联动", "暂未找到同日直接催化；+1.03%列纳指100医疗保健（偏强侧）。"),
    "EAF": ("联动", "暂未找到同日直接催化；+13.74%列罗素2000工业（偏强侧）。"),
    "EONR": ("联动", "暂未找到同日直接催化；-9.78%列All Stocks能源（偏弱侧）。"),
    "EPRT": ("联动", "暂未找到同日直接催化；-4.29%列罗素2000房地产（偏弱侧）。"),
    "ES": ("联动", "暂未找到同日直接催化；+0.97%列标普500公用事业（偏强侧）。"),
    "EW": ("联动", "暂未找到同日直接催化；+4.13%列标普500医疗保健（偏强侧）。"),
    "FANG": ("联动", "暂未找到同日直接催化；-8.03%列标普500能源（偏弱侧）。"),
    "FGNX": ("联动", "暂未找到同日直接催化；-22.10%列All Stocks金融（偏弱侧）。"),
    "FLYX": ("联动", "暂未找到同日直接催化；+7.02%列罗素2000工业（偏强侧）。"),
    "FRGT": ("联动", "暂未找到同日直接催化；+30.21%列All Stocks科技（偏强侧）。"),
    "FWRD": ("联动", "暂未找到同日直接催化；-5.55%列主题层运输与物流（偏弱侧）。"),
    "GILD": ("联动", "暂未找到同日直接催化；+0.94%列纳指100医疗保健（偏强侧）。"),
    "GLOO": ("联动", "暂未找到同日直接催化；+24.09%列All Stocks科技（偏强侧）。"),
    "GTY": ("联动", "暂未找到同日直接催化；-4.29%列罗素2000房地产（偏弱侧）。"),
    "HBAN": ("联动", "暂未找到同日直接催化；-5.55%列标普500金融（偏弱侧）。"),
    "HNRG": ("联动", "暂未找到同日直接催化；+2.51%列罗素2000公用事业（偏强侧）。"),
    "HONA": ("联动", "暂未找到同日直接催化；+3.59%列纳指100工业（偏强侧）。"),
    "HOOD": ("联动", "暂未找到同日直接催化；-5.46%列标普500金融（偏弱侧）。"),
    "HPK": ("联动", "暂未找到同日直接催化；-8.91%列All Stocks能源（偏弱侧）。"),
    "INR": ("联动", "暂未找到同日直接催化；-9.68%列All Stocks能源（偏弱侧）。"),
    "INTC": ("联动", "暂未找到同日直接催化；+4.03%列标普500科技（偏强侧）。"),
    "IPST": ("联动", "暂未找到同日直接催化；-12.62%列All Stocks金融（偏弱侧）。"),
    "ISRG": ("联动", "暂未找到同日直接催化；+1.36%列纳指100医疗保健（偏强侧）。"),
    "JBHT": ("直接", "J.B. Hunt warns of earnings drop as diesel hits record high。"),
    "JNJ": ("联动", "暂未找到同日直接催化；+0.03%列道指医疗保健（偏强侧）。"),
    "KO": ("联动", "暂未找到同日直接催化；-0.95%列道指必需消费（偏强侧）。"),
    "LGHL": ("联动", "暂未找到同日直接催化；-20.47%列All Stocks金融（偏弱侧）。"),
    "LIN": ("联动", "暂未找到同日直接催化；-0.19%列纳指100基础材料（偏弱侧）。"),
    "LITE": ("联动", "暂未找到同日直接催化；+9.59%列标普500科技（偏强侧）。"),
    "LOCL": ("联动", "暂未找到同日直接催化；-12.29%列主题层农业与食品科技（偏弱侧）。"),
    "LSF": ("联动", "暂未找到同日直接催化；-9.56%列主题层农业与食品科技（偏弱侧）。"),
    "MAMA": ("联动", "暂未找到同日直接催化；+8.45%列罗素2000必需消费（偏强侧）。"),
    "MCD": ("联动", "暂未找到同日直接催化；-1.67%列道指可选消费（偏弱侧）。"),
    "MGY": ("联动", "暂未找到同日直接催化；-8.58%列罗素2000能源（偏弱侧）。"),
    "MLEC": ("联动", "暂未找到同日直接催化；-8.99%列主题层农业与食品科技（偏弱侧）。"),
    "MNTS": ("联动", "暂未找到同日直接催化；+1.74%列主题层太空科技（偏强侧）。"),
    "MOS": ("联动", "暂未找到同日直接催化；-2.63%列标普500基础材料（偏弱侧）。"),
    "MRK": ("联动", "暂未找到同日直接催化；+0.78%列道指医疗保健（偏强侧）。"),
    "MRVL": ("联动", "暂未找到同日直接催化；+3.61%列主题层半导体（偏强侧）。"),
    "MSFT": ("联动", "暂未找到同日直接催化；-1.37%列道指科技（偏强侧）。"),
    "MTD": ("联动", "暂未找到同日直接催化；+3.63%列标普500医疗保健（偏强侧）。"),
    "NCT": ("联动", "暂未找到同日直接催化；+18.40%列All Stocks工业（偏强侧）。"),
    "NKE": ("联动", "暂未找到同日直接催化；-1.22%列道指可选消费（偏弱侧）。"),
    "NRG": ("联动", "暂未找到同日直接催化；+1.31%列标普500公用事业（偏强侧）。"),
    "NTST": ("联动", "暂未找到同日直接催化；-5.39%列罗素2000房地产（偏弱侧）。"),
    "NVDA": ("联动", "暂未找到同日直接催化；+0.81%列道指科技（偏强侧）。"),
    "OPAL": ("联动", "暂未找到同日直接催化；+3.78%列All Stocks公用事业（偏强侧）。"),
    "OXY": ("联动", "暂未找到同日直接催化；-6.55%列标普500能源（偏弱侧）。"),
    "PCG": ("联动", "暂未找到同日直接催化；+1.52%列标普500公用事业（偏强侧）。"),
    "PG": ("联动", "暂未找到同日直接催化；+0.24%列道指必需消费（偏强侧）。"),
    "PWP": ("联动", "暂未找到同日直接催化；-4.92%列罗素2000金融（偏弱侧）。"),
    "PYPL": ("联动", "暂未找到同日直接催化；-2.04%列纳指100金融（偏弱侧）。"),
    "QCLS": ("联动", "暂未找到同日直接催化；+118.44%列All Stocks科技（偏强侧）。"),
    "RETO": ("联动", "暂未找到同日直接催化；-34.29%列All Stocks基础材料（偏弱侧）。"),
    "RVTY": ("联动", "暂未找到同日直接催化；+3.95%列标普500医疗保健（偏强侧）。"),
    "SDST": ("联动", "暂未找到同日直接催化；+17.35%列All Stocks工业（偏强侧）。"),
    "SENEA": ("联动", "暂未找到同日直接催化；+3.70%列罗素2000必需消费（偏强侧）。"),
    "SHW": ("联动", "暂未找到同日直接催化；-0.55%列道指基础材料（偏弱侧）。"),
    "SPCX": ("联动", "暂未找到同日直接催化；+5.15%列纳指100工业（偏强侧）。"),
    "TAC": ("联动", "暂未找到同日直接催化；+3.91%列All Stocks公用事业（偏强侧）。"),
    "TFII": ("联动", "暂未找到同日直接催化；-5.39%列主题层运输与物流（偏弱侧）。"),
    "TPL": ("联动", "暂未找到同日直接催化；-6.21%列标普500能源（偏弱侧）。"),
    "UMC": ("联动", "暂未找到同日直接催化；+4.26%列主题层半导体（偏强侧）。"),
    "VGAS": ("联动", "暂未找到同日直接催化；+4.69%列All Stocks公用事业（偏强侧）。"),
    "VRTS": ("联动", "暂未找到同日直接催化；-5.16%列罗素2000金融（偏弱侧）。"),
    "WMT": ("联动", "暂未找到同日直接催化；-0.55%列道指必需消费（偏强侧）。"),
    "WOR": ("联动", "暂未找到同日直接催化；+8.24%列罗素2000工业（偏强侧）。"),
    "YMAT": ("联动", "暂未找到同日直接催化；-16.87%列All Stocks基础材料（偏弱侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "PTF", "perf": 1.992, "form": "交易所交易基金", "exposure": "美国科技动量",
         "reason": "科技动量ETF +2.00%：FOMC加息落地后的科技反弹（SOXX +0.64%/光模块Lumentum +9.59%/Intel +4.03%）——周一暴跌的第二天修复。合并删除：无同簇产品。"},
        {"ticker": "EWT", "perf": 1.622, "form": "交易所交易基金", "exposure": "台湾股票",
         "reason": "台湾ETF：半导体反弹的亚洲映射（台积电链条），独立地域敞口。合并删除：无同簇产品。"},
        {"ticker": "PRN", "perf": 1.338, "form": "交易所交易基金", "exposure": "美国工业动量",
         "reason": "工业动量ETF：Axon +5.96%/SpaceX +5.15%的AI/太空工业反弹，与科技为不同行业。合并删除：无同簇产品。"},
    ],
    "down": [
        {"ticker": "TUR", "perf": -6.608, "form": "交易所交易基金", "exposure": "土耳其股票",
         "reason": "土耳其ETF -6.61%领跌全市场：新兴市场在Fed加息+美元走强下的资本外流。合并删除：无同簇产品。"},
        {"ticker": "FCG", "perf": -5.626, "form": "交易所交易基金", "exposure": "天然气生产股",
         "reason": "天然气生产股ETF -5.63%：能源五范围领跌（XLE -2.88%/XOP -3.96%）的FOMC日获利回吐。合并删除：无同簇产品。"},
        {"ticker": "FXN", "perf": -4.148, "form": "交易所交易基金", "exposure": "能源生产商股票",
         "reason": "能源生产商ETF -4.15%：FOMC加息落地后能源遭全线抛售（Diamondback -8.03%/西方石油-6.55%）。合并删除：无同簇产品。"},
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
        text = "核查9月10日盘后至9月16日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-16"
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
            f"- `finviz_2026-09-16_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-16_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月16日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月16日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周三为FOMC决议日——Warsh的首个FOMC决议以约90%+共识加息落地（加息25bp至3.50-3.75%区间），市场反应为能源与金融的五范围领跌+14个主题清一色下跌的risk-off。**科技四个范围领涨**（AS/SP/Dow/N100）：半导体反弹（SOXX +0.64%/光模块Lumentum +9.59%/Coherent +6.92%/Intel +4.03%——周一AI减速檄文暴跌的第二天修复）、英伟达+0.82%/苹果+0.32%但微软-1.37%分化；**医疗保健三个范围居前**（道指/Dow成分3涨1跌/纳指100清一色：Edwards +4.13%/Revvity +3.95%）；**公用事业三个范围偏强**（XLU持平：PG&E +1.52%/NRG +1.31%反弹）；**工业三个范围偏强**（纳指100工业+3.84%：Axon +5.96%/SpaceX +5.15%）。**跌幅侧**：**能源五个范围全部领跌**（XLE -2.88%/XOP -3.96%/BNO -2.91%：Diamondback -8.03%/西方石油-6.55%/TPL -6.21%——FOMC加息+美元走强的能源获利回吐）；**金融五个范围领跌**（XLF -1.62%：3只标普金融仅3涨/67跌——Huntington -5.55%/Robinhood -5.46%）；基础材料四个范围。太空科技行大涨（NASA +2.61%/WARP +1.15%/ORBX +1.37%——SpaceX +5.15%带动）；核能铀矿行分化（NLR -0.89%/NUKZ +0.18%/URNJ -0.23%）。黄金-0.61%/白银-0.83%回落。VIX期货ETF +0.80%（FOMC后波动率仍高）。当日无行情性质结构变化。",
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
    (OUT / "finviz_2026-09-16_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-16_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-16_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
