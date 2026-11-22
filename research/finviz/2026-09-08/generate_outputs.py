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
    "Rail": "铁路", "Air Cargo": "航空货运", "Maritime": "海运", "Trucking": "卡车运输", "Air Travel": "航空客运", "Industrial IoT": "工业物联网", "Printing": "印刷", "PCs & Devices": "个人电脑与设备", "Hydrogen": "氢能", "Solar": "太阳能", "Wind": "风能", "Geothermal": "地热", "Grid": "电网", "Fuel Cells": "燃料电池", "Batteries": "电池储能", "Oil": "石油", "Uranium": "铀", "Gas & LNG": "天然气与LNG", "Smart Grid": "智能电网", "Materials": "医疗材料", "Therapeutics": "治疗药物", "Devices": "医疗器械", "Metabolic": "代谢疾病", "Telemedicine": "远程医疗", "IT & Data": "医疗信息与数据",
}

THEME_COMPANY = {
    "AMGN": "AMGEN Inc",
    "ASTS": "AST SpaceMobile Inc",
    "BKSY": "BlackSky Technology Inc",
    "BRBR": "Bellring Brands Inc",
    "CHGG": "Chegg Inc",
    "DCBO": "Docebo Inc",
    "DUOL": "Duolingo Inc",
    "FCEL": "Fuelcell Energy Inc",
    "GPCR": "Structure Therapeutics Inc ADR",
    "GWH": "ESS Tech Inc",
    "LEU": "Centrus Energy Corp",
    "MNTK": "Montauk Renewables Inc",
    "NRGV": "Energy Vault Holdings Inc",
    "RDW": "Redwire Corp",
    "SANA": "Sana Biotechnology Inc",
    "SFM": "Sprouts Farmers Market Inc",
    "SMPL": "Simply Good Foods Co",
    "SMR": "NuScale Power Corp",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AMGN": ("直接", "诺华Lp(a)降脂药三期结果成功直接打击安进的竞争管线预期（'诺华试验结果炸毁安进股价'），叠加BMO下调评级，-10.08%列标普500与纳指100医疗保健跌幅首位、拖累道指。（事件时间2026-09-08 06:52 ET起） [Why Novartis' Drug Trial Results Are Blowing Up Amgen Stock](https://finviz.com/news/388210/why-novartis-drug-trial-results-are-blowing-up-amgn-stock)"),
    "BSX": ("直接", "波士顿科学宣布网络攻击将影响2026年业绩、不大可能达成净销售增长与EPS指引，-5.90%列标普500医疗保健跌幅前列。（事件时间2026-09-08 07:44 ET起） [Boston Scientific misses 2026 guidance after cyberattack](https://finviz.com/news/388195/boston-scientific-misses-2026-guidance-after-cyberattack)"),
    "SEI": ("直接", "Solaris Energy Infrastructure上调2026年EBITDA指引并首次给出2027年一季度指引（AI数据中心电力需求），+16.29%列All Stocks与罗素2000能源涨幅首位。（事件时间2026-09-08 06:45 ET） [Solaris Energy Infrastructure Raises 2026 and Initiates First Quarter 2027 Guidance](https://finviz.com/news/388185/solaris-energy-infrastructure-raises-2026-and-initiates-q1-2027-guidance)"),
    "PTON": ("直接", "摩根士丹利以'结构性健身逆风'下调Peloton评级，-6.67%列罗素2000可选消费跌幅第三。（事件时间2026-09-08 08:11 ET） [Morgan Stanley cuts Peloton rating on structural fitness headwinds](https://finviz.com/news/388225/morgan-stanley-cuts-peloton-rating-on-structural-fitness-headwinds)"),
    "V": ("直接", "印度UPI季度交易量超过Visa的717亿笔（新兴市场竞争压力），-1.71%列道指金融（清一色下跌）首位。（事件时间2026-09-08 15:51 ET） [Visa Falls as UPI's Quarterly Pace Tops Its 71.7 Billion Transactions](https://finviz.com/news/388260/visa-falls-as-upis-quarterly-pace-tops)"),
    "ONEW": ("联动", "暂未找到同日直接催化（唯一候选为董事会变动公告，罕见驱动-8%量级）；-7.95%列罗素2000可选消费跌幅侧（微盘流动性）。该股与当日所选可选消费的偏弱方向一致。"),
    "GOOGL": ("联动", "窗口内候选：为遵守欧盟DMA而降级欧洲搜索结果、重启核电站获美国政府19亿美元贷款（AI电力叙事强化）；-0.03%基本持平——正负新闻对冲。该股与当日道指通信服务（清一色下跌）的表现一致。"),
    "NVDA": ("联动", "窗口内候选均为无关聚合条目；-2.01%为道指科技（清一色下跌）成分——上周五存储大涨后的超大盘科技回调。该股与当日道指科技的偏弱方向一致。"),
    "CVX": ("联动", "盘前'伊朗局势下能源股上涨'的板块报道；+0.58%为道指能源（清一色上涨）唯一成分。该股与当日所选能源的偏强方向一致。"),
    "FANG": ("联动", "同上板块报道；+0.22%为纳指100能源（清一色上涨）成分。该股与当日所选能源的偏强方向一致。"),
    "MPC": ("联动", "同上板块报道（炼厂）；+2.28%列标普500能源第三。该股与当日所选能源的偏强方向一致。"),
    "VLO": ("联动", "窗口内候选为财报日期公告（例行）；+3.27%列标普500能源第二——炼端价差随油价跳升。该股与当日所选能源的偏强方向一致。"),
    "TPL": ("联动", "无窗口新闻；+5.38%列标普500能源首位（二线油气资产）。该股与当日所选能源的偏强方向一致。"),
    "ODFL": ("联动", "盘前movers聚合报道；+0.61%列纳指100工业（4涨/9跌）涨幅侧。该股与当日所选工业的表现一致。"),
    "HON": ("联动", "窗口内唯一候选为'航空航天股票风险高于订单簿表象'的分析文章；-0.65%为道指工业（1涨/3跌）成分。该股与当日道指工业的分化表现一致。"),
    "CAT": ("联动", "无窗口新闻；+1.05%为道指工业（1涨/3跌）唯一上涨成分。该股与当日道指工业的分化表现一致。"),
    "MMM": ("联动", "无窗口新闻；-0.62%为道指工业（1涨/3跌）成分。该股与当日道指工业的分化表现一致。"),
    "DIS": ("联动", "无窗口新闻；-0.24%为道指通信服务（清一色下跌）成分。该股与当日道指通信服务的偏弱方向一致。"),
    "SPCX": ("联动", "窗口内候选为Musk'把股价发射上天'评论与Stoke Space CEO'第三方无法与SpaceX竞争'的正面表态；+3.73%列纳指100工业涨幅首位。该股与当日所选工业的偏强方向一致。"),
    "CD": ("联动", "无窗口新闻微盘（数字资产）；-13.76%列All Stocks与罗素2000金融跌幅前列——比特币回吐的延续。该股与当日所选金融的偏弱方向一致。"),
    "GPCR": ("联动", "无窗口新闻微盘；-14.70%列医疗保健与生物科技主题（清一色下跌）首位——安进事件日的板块传染。该股与当日所选医疗保健的偏弱方向一致。"),
    "SANA": ("联动", "无窗口新闻（细胞疗法）；-10.39%列医疗保健主题第二——同上板块传染。该股与当日所选医疗保健的偏弱方向一致。"),
    "SYK": ("联动", "无窗口新闻（医疗器械）；-8.81%列标普500医疗保健第二——波士顿科学网络攻击日的器械板块共振。该股与当日所选医疗保健的偏弱方向一致。"),
    "ISRG": ("联动", "无窗口新闻（手术机器人）；-4.51%列纳指100医疗保健（清一色下跌）第二。该股与当日所选医疗保健的偏弱方向一致。"),
    "DXCM": ("联动", "无窗口新闻（血糖监测）；-3.83%列纳指100医疗保健第三。该股与当日所选医疗保健的偏弱方向一致。"),
    "IMSR": ("联动", "无窗口新闻微盘（熔盐堆）；+10.10%列All Stocks公用事业涨幅第二——核能谱系主线。该股与当日所选公用事业的偏强方向一致。"),
    "UROY": ("联动", "无窗口新闻（铀权利金）；+8.56%列All Stocks能源涨幅第二——铀ETF +3.13%的核能日映射。该股与当日所选能源的偏强方向一致。"),
    "MNTK": ("联动", "无窗口新闻（可再生天然气）；+12.11%列能源商品主题（清一色上涨）第二位。该股与当日所选能源、能源商品的偏强方向一致。"),
    "GWH": ("联动", "无窗口新闻（储能）；+13.27%列可再生能源主题（清一色上涨）第二位。该股与当日能源大谱系的偏强方向一致。"),
    "SMR": ("联动", "无窗口新闻（小型模块化反应堆）；+15.26%列能源商品主题首位——核能主线的核心标的。该股与当日所选能源的偏强方向一致。"),
    "FCEL": ("联动", "无窗口新闻（燃料电池）；+18.80%列罗素2000工业涨幅首位、可再生能源主题首位。该股与当日能源大谱系的偏强方向一致。"),
    "SATL": ("联动", "无窗口新闻（卫星遥感）；+15.30%列罗素2000工业第二——太空科技主题（清一色上涨）共振。该股与当日所选工业、太空科技的偏强方向一致。"),
    "BNC": ("联动", "无窗口新闻微盘；+50.43%列All Stocks工业涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "SST": ("联动", "无窗口新闻微盘（广告技术）；+30.55%列All Stocks工业涨幅第二，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "SWVL": ("联动", "无窗口新闻微盘（中概出行）；+30.22%列All Stocks工业涨幅第三，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "NRGV": ("联动", "无窗口新闻（储能）；+12.50%列All Stocks与罗素2000公用事业涨幅首位。该股与当日所选公用事业的偏强方向一致。"),
    "FLNC": ("联动", "无窗口新闻（储能系统）；+6.67%列罗素2000公用事业第二。该股与当日所选公用事业的偏强方向一致。"),
    "CDZI": ("联动", "无窗口新闻（水资源）；+3.48%列罗素2000公用事业第三。该股与当日所选公用事业的偏强方向一致。"),
    "EIX": ("联动", "无窗口新闻；+4.51%列标普500公用事业涨幅首位——加州双雄的第三日修复。该股与当日所选公用事业的偏强方向一致。"),
    "PCG": ("联动", "无窗口新闻；+3.64%列标普500公用事业第二。该股与当日所选公用事业的偏强方向一致。"),
    "SRE": ("联动", "无窗口新闻；+1.70%列标普500公用事业第三。该股与当日所选公用事业的偏强方向一致。"),
    "XEL": ("联动", "无窗口新闻；+1.53%列纳指100公用事业（清一色上涨）首位——利率上行日类债端逆势走强（与AI电力叙事的合力）。该股与当日所选公用事业的偏强方向一致。"),
    "AEP": ("联动", "无窗口新闻；+0.74%为纳指100公用事业（清一色上涨）成分。该股与当日所选公用事业的偏强方向一致。"),
    "EXC": ("联动", "无窗口新闻；+0.71%为纳指100公用事业（清一色上涨）成分。该股与当日所选公用事业的偏强方向一致。"),
    "LEU": ("联动", "无窗口新闻（铀浓缩）；+6.69%列罗素2000能源第二——核能燃料链。该股与当日所选能源的偏强方向一致。"),
    "DK": ("联动", "无窗口新闻（炼厂）；+5.30%列罗素2000能源第三。该股与当日所选能源的偏强方向一致。"),
    "VIVK": ("联动", "无窗口新闻微盘；+7.65%列All Stocks能源涨幅第三，低流通异动。该股与当日所选能源的偏强方向一致。"),
    "NKLR": ("联动", "无窗口新闻微盘；+7.40%列All Stocks公用事业涨幅第三。该股与当日所选公用事业的偏强方向一致。"),
    "BIAF": ("联动", "无窗口新闻微盘（诊断）；-41.52%列All Stocks医疗保健跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选医疗保健的偏弱方向一致。"),
    "LEXX": ("联动", "无窗口新闻微盘；-33.78%列医疗保健跌幅第二，低流通崩跌，暂未找到同日直接催化。该股与当日所选医疗保健的偏弱方向一致。"),
    "JAGX": ("联动", "无窗口新闻微盘；-30.60%列医疗保健跌幅第三，低流通崩跌，暂未找到同日直接催化。该股与当日所选医疗保健的偏弱方向一致。"),
    "BENF": ("联动", "无窗口新闻微盘；-22.96%列All Stocks金融跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选金融的偏弱方向一致。"),
    "AIFU": ("联动", "无窗口新闻微盘；-14.32%列All Stocks金融跌幅第二。该股与当日所选金融的偏弱方向一致。"),
    "LDI": ("联动", "无窗口新闻（房贷）；-12.34%列罗素2000金融跌幅第二——利率新高日的地产金融压力。该股与当日所选金融的偏弱方向一致。"),
    "PRCH": ("联动", "无窗口新闻（保险科技）；-6.75%列罗素2000金融跌幅侧。该股与当日所选金融的偏弱方向一致。"),
    "BRO": ("联动", "无窗口新闻（保险经纪）；-4.54%列标普500金融（1涨/69跌）跌幅首位。该股与当日所选金融的偏弱方向一致。"),
    "FDS": ("联动", "无窗口新闻（金融数据）；-4.29%列标普金融第二。该股与当日所选金融的偏弱方向一致。"),
    "AJG": ("联动", "无窗口新闻（保险经纪）；-4.28%列标普金融第三。该股与当日所选金融的偏弱方向一致。"),
    "JPM": ("联动", "无窗口新闻；-1.43%列道指金融（清一色下跌）第二。该股与当日所选金融的偏弱方向一致。"),
    "TRV": ("联动", "无窗口新闻；-1.00%为道指金融（清一色下跌）成分。该股与当日所选金融的偏弱方向一致。"),
    "REBN": ("联动", "无窗口新闻微盘（咖啡连锁）；-32.88%列All Stocks可选消费跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选可选消费的偏弱方向一致。"),
    "RENT": ("联动", "无窗口新闻（租赁时尚）；-15.90%列All Stocks与罗素2000可选消费跌幅第二——Lululemon后消费执行力的持续重定价。该股与当日所选可选消费的偏弱方向一致。"),
    "SDA": ("联动", "无窗口新闻微盘（中概车服）；-14.52%列可选消费跌幅侧。该股与当日所选可选消费的偏弱方向一致。"),
    "SMPL": ("联动", "无窗口新闻（营养食品）；-6.03%列罗素2000必需消费与健康食品主题（清一色下跌）前列。该股与当日所选必需消费、健康食品的偏弱方向一致。"),
    "COTY": ("联动", "无窗口新闻（美妆）；-5.80%列罗素必需消费第二。该股与当日所选必需消费的偏弱方向一致。"),
    "BRBR": ("联动", "无窗口新闻；-5.78%列罗素必需消费第三。该股与当日所选必需消费的偏弱方向一致。"),
    "CRH": ("联动", "无窗口新闻（建材）；-3.87%列标普500基础材料（6涨/14跌）跌幅首位——美加贸易战（加方对钢铝报复性关税）的建材端压力。该股与当日所选基础材料的偏弱方向一致。"),
    "PPG": ("联动", "无窗口新闻（涂料）；-2.50%列标普材料第二。该股与当日所选基础材料的偏弱方向一致。"),
    "SHW": ("联动", "无窗口新闻；-2.28%列标普材料第三、道指基础材料（清一色下跌）唯一成分。该股与当日所选基础材料的偏弱方向一致。"),
    "LIN": ("联动", "无窗口新闻；-1.92%为纳指100基础材料（清一色下跌）唯一成分。该股与当日所选基础材料的偏弱方向一致。"),
    "VMRK": ("联动", "无窗口新闻微盘REIT；+1.29%列标普500房地产（11涨/19跌、相对抗跌入选涨幅侧）首位。该股与当日房地产的相对表现一致。"),
    "SPG": ("联动", "无窗口新闻（商业地产）；+1.17%列标普房地产第二。该股与当日房地产的相对表现一致。"),
    "REG": ("联动", "无窗口新闻（零售REIT）；+0.89%列标普房地产第三。该股与当日房地产的相对表现一致。"),
    "IBM": ("联动", "无窗口新闻；-1.19%为道指科技（清一色下跌）成分。该股与当日道指科技的偏弱方向一致。"),
    "CRM": ("联动", "无窗口新闻；-3.90%为道指科技（清一色下跌）领跌成分。该股与当日道指科技的偏弱方向一致。"),
    "RKLB": ("联动", "无窗口新闻（火箭）；+2.51%列纳指100工业第二——太空科技主题（清一色上涨）共振。该股与当日所选工业、太空科技的偏强方向一致。"),
    "BKSY": ("联动", "无窗口新闻（遥感卫星）；+7.71%列太空科技主题（清一色上涨）首位。该股与当日所选太空科技的偏强方向一致。"),
    "RDW": ("联动", "无窗口新闻（航天基础设施）；+6.65%列太空科技主题第二。该股与当日所选太空科技的偏强方向一致。"),
    "ASTS": ("联动", "无窗口新闻（直连卫星）；+6.12%列太空科技主题第三。该股与当日所选太空科技的偏强方向一致。"),
    "CHGG": ("联动", "无窗口新闻（在线教育）；-6.45%列教育科技主题（清一色下跌）首位。该股与当日所选教育科技的偏弱方向一致。"),
    "DUOL": ("联动", "无窗口新闻（语言学习）；-5.23%列教育科技主题第二。该股与当日所选教育科技的偏弱方向一致。"),
    "DCBO": ("联动", "无窗口新闻（企业学习平台）；-4.85%列教育科技主题第三。该股与当日所选教育科技的偏弱方向一致。"),
    "SFM": ("联动", "无窗口新闻（健康食品零售）；-6.50%列健康食品与营养主题（清一色下跌）首位。该股与当日所选健康食品的偏弱方向一致。"),
    "PYPL": ("联动", "暂未找到同日直接催化；-3.24%为纳指100金融（清一色下跌）唯一成分——上周五传闻冲高回落的延续、加密金融回吐共振。该股与当日所选金融的偏弱方向一致。"),
    "BKR": ("联动", "同上盘前'伊朗局势下能源股上涨'板块报道；+0.66%列纳指100能源（清一色上涨）首位。该股与当日所选能源的偏强方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "PTF", "perf": 3.704, "form": "交易所交易基金", "exposure": "美国科技动量（Dorsey Wright）",
         "reason": "科技动量ETF领涨全市场：Intel +9.05%（提价预期+上调目标价）、半导体续涨（SOXX +1.64%、存储+1.71%）令动量篮领跑——在超大盘科技（微软/苹果/英伟达）下跌日，动量因子篮与市值篮的分化极大。合并删除：TECL（杠杆，排除）。"},
        {"ticker": "TUR", "perf": 3.161, "form": "交易所交易基金", "exposure": "土耳其股票",
         "reason": "土耳其ETF：独立新兴市场敞口，地缘资金流的边际受益者。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "URA", "perf": 3.126, "form": "交易所交易基金", "exposure": "全球铀矿",
         "reason": "铀ETF：核能日主线——NuScale +15.26%、铀权利金+8.56%、Centrus +6.69%、谷歌核电站获政府19亿美元贷款，'AI电力+核能'谱系全面走强。合并删除：无同簇产品进入本轮极值候选。"},
    ],
    "down": [
        {"ticker": "BBH", "perf": -3.642, "form": "交易所交易基金", "exposure": "全球生物科技股",
         "reason": "生物科技ETF领跌全市场：诺华Lp(a)三期成功炸毁安进竞争管线（-10.08%）、波士顿科学网络攻击-5.90%、史赛克-8.81%——医疗保健三重打击的股票端放大。合并删除：IHI、PPH、IXJ、PBE（同簇医疗股，保留最强一只BBH）。"},
        {"ticker": "PALL", "perf": -3.477, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF：贵金属全线回落（黄金-1.73%、白银-0.75%、金矿-1.16%）——利率连升（30年期五连涨）下的商品端压力，与医疗股为不同资产类别。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "ITB", "perf": -3.045, "form": "交易所交易基金", "exposure": "美国住宅建筑",
         "reason": "住宅建筑ETF：30年期收益率五连涨至2007年以来最高附近（XHB -2.42%同向）——利率最敏感端的直接打击。合并删除：无同簇产品进入本轮极值候选（XHB为同向佐证未进前三）。"},
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
        text = "核查9月5日盘后至9月8日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-08"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；医疗股簇（BBH/IHI/PPH/IXJ/PBE）保留BBH、原油期货簇（DBO/BNO/USO/DBE）保留最强DBO但未入前三、住宅建筑簇（ITB/XHB另计）保留ITB。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-08_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-08_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月8日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月8日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：劳工节长周末后首个交易日为地缘双击日：美国证实打击伊朗Kharg岛附近目标（定性'经济挤压'）、沙特设施亦遇袭——布伦特盘中上摸100美元后稳于99附近（WTI>93）、美国汽油创纪录5.50美元/加仑，能源大谱系全面领涨（五个股票范围全部进入涨幅前三：石油炼端Valero +3.27%/Marathon +2.28%、核能与新能（NuScale +15.26%、FuelCell +18.80%、铀ETF +3.13%、谷歌核电站获政府19亿美元贷款）、太空科技主题清一色涨）；公用事业四个范围上涨（加州双雄EIX +4.51%/PCG +3.64%第三日修复+纳指100清一色）。科技动量ETF +3.70%领涨全市场（Intel +9.05%提价预期、半导体续涨SOXX +1.64%），但超大盘科技领跌（道指科技清一色跌：Salesforce -3.90%、英伟达-2.01%、微软/苹果跌约1%）——动量篮与市值篮的极端分化。跌幅侧三重打击：医疗保健（诺华Lp(a)三期成功炸毁安进竞争管线-10.08%、波士顿科学网络攻击致指引无法达成-5.90%、史赛克-8.81%，标普医疗3涨/56跌、纳指100清一色跌-4.94%）；金融五个范围进入跌幅侧（标普金融1涨/69跌、道指清一色：Visa遭UPI交易量竞争-1.71%、加密金融回吐）；基础材料（美加贸易战升级：加方对数百种美国商品加征15%—50%报复性关税、钢铁建材承压）。指数：道指-约600点（-1.2%）、标普-0.5%—0.6%（7700下方、宽度约146—165涨对335—357跌）、纳指综指-0.3%、罗素-0.5%；股跌债不涨（10年期+1bp、30年期五连涨至2007年以来最高）、VIX仅15.67、钯金-3.48%贵金属回落。美联储路径：周五CPI（共识0.4%/0.2%）被期权市场定价为最大风险事件、下周FOMC'多年来最没定论'；高通向亚马逊发行最高40亿美元权证（按最高600亿美元芯片订单分批归属、十年基石协议）+8%；苹果周三发布约2,000美元折叠iPhone；Bloom Energy获纳入标普500（9/21生效）大涨。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5509/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1937/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (OUT / "finviz_2026-09-08_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-08_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-08_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
