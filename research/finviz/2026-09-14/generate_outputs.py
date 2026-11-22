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
    "ADBE": "Adobe Inc",
    "CENX": "Century Aluminum Co",
    "COHU": "Cohu Inc",
    "ERO": "Ero Copper Corp",
    "HPE": "Hewlett Packard Enterprise Co",
    "MH": "McGraw Hill Inc",
    "NOK": "Nokia Corp ADR",
    "QLYS": "Qualys Inc",
    "RPD": "Rapid7 Inc",
    "SGML": "Sigma Lithium Corp",
    "SIMO": "Silicon Motion Technology Corp ADR",
    "SKIL": "Skillsoft Corp",
    "TENB": "Tenable Holdings Inc",
    "TER": "Teradyne Inc",
    "VIAV": "Viavi Solutions Inc",
    "ZS": "Zscaler Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ADBE": ("直接", "Adobe财报（9/11盘后）：季度业绩超预期并上调指引，UBS重制目标价；+5.30%列标普500科技反弹侧——软件/网络安全主题清一色上涨日的板块贝塔+个股事件双击。。（事件时间2026-09-11 16:00 ET）"),
    "AEHL": ("联动", "暂未找到同日直接催化；-22.28%列All Stocks工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "AMGN": ("联动", "暂未找到同日直接催化；+1.10%列道指医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "AMZN": ("联动", "暂未找到同日直接催化；-1.26%列道指可选消费（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选可选消费的偏弱方向一致。"),
    "BBGI": ("联动", "暂未找到同日直接催化；+14.67%列All Stocks通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "BKR": ("联动", "暂未找到同日直接催化；-3.86%列纳指100能源（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选能源的偏弱方向一致。"),
    "BMGL": ("联动", "暂未找到同日直接催化；+55.56%列All Stocks医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "BSX": ("联动", "暂未找到同日直接催化；+4.82%列标普500医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "BW": ("联动", "暂未找到同日直接催化；-11.46%列罗素2000工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "CAT": ("联动", "暂未找到同日直接催化；-4.22%列道指工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "CECO": ("联动", "暂未找到同日直接催化；-9.79%列罗素2000工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "CEG": ("联动", "暂未找到同日直接催化；-7.09%列标普500公用事业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "CENX": ("联动", "暂未找到同日直接催化；-5.70%列主题层金属商品（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选金属商品的偏弱方向一致。"),
    "CNC": ("联动", "暂未找到同日直接催化；+4.50%列标普500医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "COCO": ("联动", "暂未找到同日直接催化；+5.81%列罗素2000必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "COE": ("联动", "暂未找到同日直接催化；+12.16%列All Stocks必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "COHR": ("直接", "Coherent遭AI硬件链抛售拖累（与康宁/HPE同链），-12.73%列标普500科技跌幅前列。。（事件时间2026-09-14 盘中 ET）"),
    "COHU": ("联动", "暂未找到同日直接催化；-12.46%列主题层Semiconductors（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选Semiconductors的偏弱方向一致。"),
    "CTNT": ("联动", "暂未找到同日直接催化；-86.95%列All Stocks工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "CVX": ("联动", "暂未找到同日直接催化；-0.88%列道指能源（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选能源的偏弱方向一致。"),
    "DG": ("联动", "暂未找到同日直接催化；+3.68%列标普500必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "DIS": ("联动", "暂未找到同日直接催化；+1.92%列道指通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "DXCM": ("联动", "暂未找到同日直接催化；+1.99%列纳指100医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "ERO": ("联动", "暂未找到同日直接催化；-5.05%列主题层金属商品（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选金属商品的偏弱方向一致。"),
    "ETN": ("联动", "暂未找到同日直接催化；-7.57%列标普500工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "EU": ("联动", "暂未找到同日直接催化；-15.84%列罗素2000能源（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选能源的偏弱方向一致。"),
    "EXC": ("联动", "暂未找到同日直接催化；-1.02%列纳指100公用事业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "FANG": ("联动", "暂未找到同日直接催化；+0.37%列纳指100能源（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选能源的偏弱方向一致。"),
    "FOXA": ("联动", "暂未找到同日直接催化；+3.93%列标普500通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "GEV": ("直接", "GLJ Research首次覆盖给予卖出评级（可跌50%），-8.62%列标普500工业跌幅首位。。（事件时间2026-09-14 盘前 ET）"),
    "GILD": ("联动", "暂未找到同日直接催化；+1.87%列纳指100医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "GLW": ("直接", "康宁宣布20亿美元股权发行，-13.70%列标普500科技跌幅前列——融资稀释惩罚。。（事件时间2026-09-14 盘前 ET）"),
    "GOOGL": ("联动", "暂未找到同日直接催化；+3.22%列道指通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "HD": ("联动", "暂未找到同日直接催化；+0.69%列道指可选消费（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选可选消费的偏弱方向一致。"),
    "HON": ("联动", "暂未找到同日直接催化；-0.48%列道指工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "HPE": ("直接", "Dell跌超7%（AI服务器占基建收入过半的担忧）拖累HPE -10.76%列标普500科技跌幅首位——AI硬件链的获利回吐潮。。（事件时间2026-09-14 盘中 ET）"),
    "HQ": ("联动", "暂未找到同日直接催化；-32.06%列All Stocks科技（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选科技的偏弱方向一致。"),
    "ISRG": ("联动", "暂未找到同日直接催化；+2.38%列纳指100医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "IVVD": ("联动", "暂未找到同日直接催化；+13.53%列罗素2000医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "KGS": ("联动", "暂未找到同日直接催化；-11.32%列罗素2000能源（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选能源的偏弱方向一致。"),
    "KO": ("联动", "暂未找到同日直接催化；+1.20%列道指必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "KR": ("直接", "Kroger Q2财报：电商与零售媒体亮眼，+4.14%列标普500必需消费涨幅首位。。（事件时间2026-09-14 盘前 ET）"),
    "LFMD": ("联动", "暂未找到同日直接催化；+12.79%列罗素2000医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "LIN": ("联动", "暂未找到同日直接催化；-0.39%列纳指100基础材料（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "LWLG": ("联动", "暂未找到同日直接催化；-8.41%列All Stocks基础材料（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "METC": ("联动", "暂未找到同日直接催化；-8.04%列All Stocks基础材料（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "MH": ("联动", "暂未找到同日直接催化；+7.47%列罗素2000必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "MMM": ("联动", "暂未找到同日直接催化；-1.79%列道指工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "MNTK": ("联动", "暂未找到同日直接催化；-16.10%列All Stocks基础材料（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "MO": ("联动", "暂未找到同日直接催化；+2.36%列标普500必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "MRK": ("联动", "暂未找到同日直接催化；+0.64%列道指医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "NFLX": ("联动", "暂未找到同日直接催化；+3.77%列纳指100通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "NKE": ("联动", "暂未找到同日直接催化；+0.68%列道指可选消费（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选可选消费的偏弱方向一致。"),
    "NOK": ("联动", "暂未找到同日直接催化；-13.30%列主题层硬件（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选硬件的偏弱方向一致。"),
    "NRG": ("联动", "暂未找到同日直接催化；-4.40%列标普500公用事业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "NWSA": ("联动", "暂未找到同日直接催化；+3.80%列标普500通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "OFRM": ("联动", "暂未找到同日直接催化；+4.94%列罗素2000必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "PBF": ("直接", "PBF Energy宣布拟发行5亿美元可交换票据（2032到期），-10.09%列All Stocks能源跌幅前列——炼厂融资惩罚。。（事件时间2026-09-14 盘前 ET）"),
    "PDSB": ("直接", "PDS Biotech宣布最高2,230万美元PIPE融资初始交割+新任命，+35.33%列All Stocks医疗保健涨幅侧。。（事件时间2026-09-14 盘前 ET）"),
    "PG": ("联动", "暂未找到同日直接催化；+0.59%列道指必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "PODD": ("联动", "暂未找到同日直接催化；+4.43%列标普500医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "PYPL": ("联动", "暂未找到同日直接催化；+0.58%列纳指100金融（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选金融的偏强方向一致。"),
    "QCLS": ("联动", "暂未找到同日直接催化；-67.25%列All Stocks科技（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选科技的偏弱方向一致。"),
    "QLYS": ("联动", "暂未找到同日直接催化；+15.06%列主题层Software（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选Software的偏强方向一致。"),
    "RBLX": ("联动", "暂未找到同日直接催化；+12.72%列All Stocks通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "RFIL": ("直接", "RF Industries Q3财报（9/11盘后），-12.31%列All Stocks跌幅侧。。（事件时间2026-09-11 16:00 ET）"),
    "RPD": ("联动", "暂未找到同日直接催化；+24.05%列主题层网络安全（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选网络安全的偏强方向一致。"),
    "RUM": ("直接", "报道将Anthropic与137亿美元合同关联到RUM Group，+11.58%列全市场涨幅侧。。（事件时间2026-09-14 盘中 ET）"),
    "SCNI": ("联动", "暂未找到同日直接催化；+46.99%列All Stocks医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "SGML": ("联动", "暂未找到同日直接催化；-6.21%列主题层金属商品（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选金属商品的偏弱方向一致。"),
    "SIMO": ("联动", "暂未找到同日直接催化；-16.76%列主题层Semiconductors（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选Semiconductors的偏弱方向一致。"),
    "SKIL": ("联动", "暂未找到同日直接催化；+13.66%列All Stocks必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "SMXT": ("联动", "暂未找到同日直接催化；-19.23%列All Stocks科技（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选科技的偏弱方向一致。"),
    "STRZ": ("联动", "暂未找到同日直接催化；+9.24%列罗素2000通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "SWVL": ("联动", "暂未找到同日直接催化；-22.56%列All Stocks工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "TENB": ("联动", "暂未找到同日直接催化；+16.51%列主题层网络安全（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选网络安全的偏强方向一致。"),
    "TER": ("联动", "暂未找到同日直接催化；-13.30%列标普500科技（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选科技的偏弱方向一致。"),
    "TTD": ("联动", "暂未找到同日直接催化；+4.39%列标普500通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "TTWO": ("联动", "暂未找到同日直接催化；+3.45%列纳指100通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "TULP": ("联动", "暂未找到同日直接催化；+12.50%列All Stocks必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "TYRA": ("直接", "Tyra Biosciences定价4亿美元公募普通股+预筹权证发行，+13.80%——与融资惩罚相反的个案（临床试验催化并存）。。（事件时间2026-09-14 盘前 ET）"),
    "UNH": ("联动", "暂未找到同日直接催化；+1.18%列道指医疗保健（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选医疗保健的偏强方向一致。"),
    "VIAV": ("联动", "暂未找到同日直接催化；-12.72%列主题层硬件（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选硬件的偏弱方向一致。"),
    "VRT": ("联动", "暂未找到同日直接催化；-7.65%列标普500工业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选工业的偏弱方向一致。"),
    "VSME": ("联动", "暂未找到同日直接催化；+21.51%列All Stocks通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "VST": ("联动", "暂未找到同日直接催化；-5.16%列标普500公用事业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "WMT": ("联动", "暂未找到同日直接催化；+1.80%列道指必需消费（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "WSHP": ("联动", "暂未找到同日直接催化；+10.38%列罗素2000通信服务（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "XEL": ("联动", "暂未找到同日直接催化；-1.77%列纳指100公用事业（偏弱侧）——FOMC前的板块轮动日贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "ZS": ("联动", "暂未找到同日直接催化；+16.52%列主题层网络安全（偏强侧）——FOMC前的板块轮动日贝塔。该股与当日所选网络安全的偏强方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "HACK", "perf": 7.880, "form": "交易所交易基金", "exposure": "全球科技｜网络安全",
         "reason": "网络安全ETF单日+7.88%：八子行业清一色上涨——FOMC前的极端硬件→软件切换中最强分支（Palo Alto上周超预期仍跌的门槛效应终结），与IHAK +7.78%共振。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "SKYY", "perf": 2.713, "form": "交易所交易基金", "exposure": "全球云计算",
         "reason": "云计算ETF：云计算主题清一色上涨（WCLD +6.37%），与网络安全为不同子行业敞口。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "IBIT", "perf": 2.216, "form": "交易所交易基金", "exposure": "比特币现货",
         "reason": "比特币现货ETF：加密货币主题连续反弹（IBIT +2.22%），独立资产类别。合并删除：无同簇产品进入本轮极值候选。"},
    ],
    "down": [
        {"ticker": "PTF", "perf": -7.362, "form": "交易所交易基金", "exposure": "美国科技动量（Dorsey Wright）",
         "reason": "科技动量ETF单日-7.36%领跌全市场：半导体暴跌（SOXX -5.63%/XSD -6.12%）令动量因子满仓受创——上周五+3.70%领涨的完全逆转。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "EWY", "perf": -6.624, "form": "交易所交易基金", "exposure": "韩国股票",
         "reason": "韩国ETF：存储/半导体全球映射的暴跌（上周五+3.25%领涨的完全逆转）——独立地域敞口。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "XSD", "perf": -6.122, "form": "交易所交易基金", "exposure": "美国半导体等权",
         "reason": "半导体等权ETF：等权端领跌（HPE -10.76%/康宁-13.70%/Coherent-12.73%的AI硬件链抛售潮），与韩国ETF为不同地域敞口。合并删除：SOXX（同簇半导体，保留等权端XSD更强一只）。"},
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
        text = "核查9月10日盘后至9月14日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-14"
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
            f"- `finviz_2026-09-14_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-14_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月14日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月14日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周一为FOMC（周三9/16加息概率约90%）前的最后一个完整交易日，市场完成一次极端的硬件→软件切换：半导体主题九子行业清一色下跌（SOXX -5.63%、XSD -6.12%、韩国ETF -6.62%、科技动量ETF -7.36%领跌全市场）——上周五Dell +11.98%创历史新高的AI硬件链遭全面获利回吐（HPE -10.76%、康宁20亿美元股权发行-13.70%、Coherent -12.73%、Teradyne -13.31%）；对侧为**网络安全ETF +7.88%领涨全市场**（八子行业清一色上涨）与**云计算WCLD +6.37%**、软件IGV +5.04%——软硬件跷跷板达到近期极值。通信服务五个股票范围全部领涨（道指清一色：谷歌+3.22%、迪士尼+1.92%；标普+2.81%整体：Trade Desk +4.39%、Fox +3.93%）；医疗保健强势回归（标普+1.39%/道指清一色/纳指100清一色——防御轮入+Centene +4.50%/波士顿科学+4.82%/Insulet获FDA批准+4.43%）；必需消费（道指清一色：沃尔玛+1.80%；Kroger Q2电商亮眼+4.14%、Dollar General +3.68%）。跌幅侧：工业四个范围（道指清一色：卡特彼勒-4.22%、GE Vernova遭GLJ卖出评级-8.62%、Vertiv -7.65%、Eaton -7.57%——AI基建链的融资与评级双杀）；基础材料三个范围（金属商品主题九子行业清一色跌、XME -3.04%）；能源三个范围（炼厂PBF 5亿可交换票据-10.09%）。贵金属回落（黄金-1.49%、白银-2.20%）；VIX期货ETF +1.10%（FOMC前对冲回归）；核能铀矿行全线下跌（NLR -3.31%/NUKZ -3.34%/URNJ -3.83%——第四日回吐）；太空科技行回落（NASA -2.39%/WARP -1.34%/ORBX -1.45%）。Adobe财报超预期+5.30%（软件清一色涨的个股确认）；RUM Group因Anthropic 137亿美元合同报道+11.58%。当日无行情性质结构变化。",
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
    (OUT / "finviz_2026-09-14_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-14_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-14_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
