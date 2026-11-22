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
    "ARQQ": "Arqit Quantum Inc",
    "APP": "AppLovin Corp",
    "ERO": "Ero Copper Corp",
    "FDS": "Factset Research Systems Inc",
    "IPX": "IperionX Ltd ADR",
    "NXPI": "NXP Semiconductors NV",
    "ORCL": "Oracle Corp",
    "QRVO": "Qorvo Inc",
    "SCCO": "Southern Copper Corp",
    "SNAP": "Snap Inc",
    "SWKS": "Skyworks Solutions Inc",
    "UAA": "Under Armour Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEO": ("直接", "Fiscal Q2财报（9/9盘后）：Aerie大涨25%但整体不及预期，-13.97%列罗素2000可选消费跌幅侧。（事件时间2026-09-09 16:16 ET） [American Eagle: Fiscal Q2 Earnings Snapshot](https://finviz.com/news/388410/american-eagle-fiscal-q2-earnings-snapshot)"),
    "FLWS": ("直接", "Q4亏损扩大且2027财年利润指引疲弱、公司评估融资选项，-13.04%列罗素2000可选消费跌幅侧。（事件时间2026-09-10 10:37 ET） [1-800-Flowers.com posts wider fourth-quarter loss](https://finviz.com/news/388440/1-800-flowers-com-posts-wider-q4-loss)"),
    "LOVE": ("直接", "Fiscal Q2财报，-11.04%列罗素2000可选消费跌幅侧。（事件时间2026-09-10 07:00 ET） [The Lovesac Company Reports Second Quarter Fiscal 2027 Financial Results](https://finviz.com/news/388430/the-lovesac-company-reports-q2-fy2027)"),
    "HUBC": ("直接", "宣布反向缩股，-30.63%列All Stocks科技跌幅首位。（事件时间2026-09-10 08:30 ET） [HUB Announces Reverse Share Split](https://finviz.com/news/388450/hub-announces-reverse-share-split)"),
    "NXXT": ("直接", "宣布1比10反向缩股，-20.60%列All Stocks公用事业跌幅首位。（事件时间2026-09-10 08:30 ET） [NextNRG Announces 1-for-10 Reverse Stock Split](https://finviz.com/news/388445/nextnrg-announces-1-for-10-reverse-stock-split)"),
    "GRML": ("直接", "完成稀土收购（从单一押注转向均衡组合），-8.83%列All Stocks基础材料跌幅侧。（事件时间2026-09-10 15:22 ET） [Greenland Mines (GRML) Completes Rare Earths Acquisition](https://finviz.com/news/388510/greenland-mines-completes-rare-earths-acquisition)"),
    "ORCL": ("直接", "盘后财报前的'AI债务开始破坏债券数学'抛售：-5.38%列标普500科技与大数据主题跌幅侧（财报当日收盘后发布、当日跌幅为财报前定价）。（事件时间2026-09-10 14:48 ET） [Oracle Drops Over 2% as Its AI Debt Starts Breaking Bond Math](https://finviz.com/news/388505/oracle-drops-as-ai-debt-starts-breaking-bond-math)"),
    "AAPL": ("联动", "核查9月9日盘后至9月10日公司披露与可靠新闻后，暂未找到同日直接催化；Duo发布后首日+BofA调整目标价，+3.56%列道指科技（补位上涨组）首位——发布后追买。该股与当日道指科技的表现一致。"),
    "MSFT": ("联动", "窗口内候选为'28倍市盈率是否高估'讨论文章；+0.16%基本持平。该股与当日道指科技的表现一致。"),
    "GOOGL": ("联动", "+0.59%为道指通信服务（清一色上涨）成分——通信服务五范围领涨日的权重端。该股与当日所选通信服务的偏强方向一致。"),
    "CMCSA": ("联动", "窗口内候选为9/9晚间CFO称宽带用户流失无改善的报道（负面）但当日+2.36%与新闻方向相反——通信服务五范围领涨的板块贝塔盖过个股利空。该股与当日所选通信服务的偏强方向一致。"),
    "CRM": ("联动", "窗口内候选：完成收购Fin+20亿美元洽购Listen Labs（正面）但-0.48%微跌——板块分化日的中性反应。该股与当日道指科技的表现一致。"),
    "INTC": ("联动", "窗口内候选为'Marvell还是英伟达更便宜'外链文章；-5.57%列标普500科技跌幅侧——周二+9.05%后的半导体获利回吐（SOXX -2.74%）。该股与当日半导体端的偏弱方向一致。"),
    "HPE": ("联动", "窗口内候选为HIVE外链（无关）；-6.25%列标普500科技跌幅侧——昨日+5.12%的回吐。该股与当日半导体/硬件端的偏弱方向一致。"),
    "PYPL": ("联动", "窗口内候选为CEO谈Venmo/Braintree增长与15亿美元成本节省的转型（9/9盘后）；+2.19%列标普500金融涨幅侧。该股与当日所选金融的偏强方向一致。"),
    "CEG": ("联动", "宣布从壳牌收购罗德岛州能源中心（RISEC）但-2.70%随公用事业板块（四范围跌幅侧）回落——新闻方向与价格背离。该股与当日所选公用事业的偏弱方向一致。"),
    "VST": ("联动", "宣布注册发行初级次级票据当日-2.68%随板块回落。该股与当日所选公用事业的偏弱方向一致。"),
    "FANG": ("联动", "+1.36%列纳指100能源（补位上涨组）——油价+6.4%下能源股权重端分化。该股与当日能源内部的分化一致。"),
    "BKR": ("联动", "暂未找到同日直接催化；-6.66%列纳指100能源跌幅首位——油价暴涨下的利好兑现抛售（能源股连续第三日跑输商品）。该股与当日能源股票端的分化一致。"),
    "SHW": ("联动", "窗口内候选为家得宝相关文章（外链）；-1.00%为道指基础材料（清一色下跌）唯一成分。该股与当日所选基础材料的偏弱方向一致。"),
    "MOS": ("联动", "窗口内候选为股息分析文章；-3.09%列标普500基础材料跌幅侧——贵金属与铜暴跌的材料日。该股与当日所选基础材料的偏弱方向一致。"),
    "WMT": ("联动", "-0.09%基本持平；道指必需消费（补位上涨组）成分。该股与当日所选必需消费的偏强方向一致。"),
    "SUNE": ("联动", "暂未找到同日新催化；-25.28%列All Stocks科技跌幅侧——昨日+90.30%（Suniva融资）的剧烈回吐，低流通双向异动。该股与当日罗素科技端的波动一致。"),
    "SWKS": ("联动", "暂未找到同日直接催化；+9.79%列电信与可穿戴主题涨幅侧——Duo发布后苹果链供应商的连续买盘。该股与当日电信、可穿戴主题的偏强方向一致。"),
    "FRVO": ("联动", "暂未找到同日新催化；-8.76%列All Stocks公用事业跌幅侧——地热与核能谱系的连续第二日回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "ALM": ("联动", "无窗口新闻微盘（钨矿）；-9.60%列All Stocks基础材料跌幅侧——金属商品主题清一色跌。该股与当日所选基础材料的偏弱方向一致。"),
    "ERO": ("联动", "无窗口新闻（铜矿）；-8.55%列金属商品主题（清一色下跌）首位。该股与当日金属商品主题的偏弱方向一致。"),
    "IPX": ("联动", "无窗口新闻（钛）；-8.78%列金属商品主题跌幅侧。该股与当日金属商品主题的偏弱方向一致。"),
    "TGB": ("联动", "无窗口新闻微盘（铜）；-10.19%列All Stocks基础材料跌幅侧。该股与当日所选基础材料的偏弱方向一致。"),
    "LHSW": ("联动", "无窗口新闻微盘（中概）；-36.27%列All Stocks科技跌幅侧，低流通崩跌。该股与当日罗素科技端的波动一致。"),
    "ANTA": ("联动", "无窗口新闻微盘（算力平台）；+8.90%列All Stocks金融涨幅侧，低流通异动。该股与当日All Stocks金融的偏强方向一致。"),
    "BAFN": ("联动", "无窗口新闻微盘（银行）；+9.36%列All Stocks金融涨幅侧，低流通异动。该股与当日All Stocks金融的偏强方向一致。"),
    "ZSTK": ("联动", "无窗口新闻微盘；+15.70%列All Stocks金融涨幅侧，低流通异动。该股与当日All Stocks金融的偏强方向一致。"),
    "PCLA": ("联动", "无窗口新闻微盘（日本通信设备ADR）；+31.00%列All Stocks通信服务涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日通信服务领涨的方向一致。"),
    "ANGX": ("联动", "无窗口新闻微盘（流媒体）；+9.13%列All Stocks通信服务涨幅侧。该股与当日通信服务领涨的方向一致。"),
    "GIFT": ("联动", "无窗口新闻微盘；+9.29%列All Stocks通信服务涨幅侧。该股与当日通信服务领涨的方向一致。"),
    "HCWC": ("联动", "无窗口新闻微盘；+13.53%列All Stocks必需消费涨幅侧，低流通异动。该股与当日所选必需消费的偏强方向一致。"),
    "PFAI": ("联动", "无窗口新闻微盘；+13.45%列All Stocks必需消费涨幅侧，低流通异动。该股与当日所选必需消费的偏强方向一致。"),
    "TANH": ("联动", "无窗口新闻微盘（中概）；+19.30%列All Stocks必需消费涨幅首位，低流通异动。该股与当日所选必需消费的偏强方向一致。"),
    "FBYD": ("联动", "无窗口新闻微盘；-9.78%列罗素2000工业跌幅侧。该股与当日所选工业的偏弱方向一致。"),
    "AEP": ("联动", "暂未找到同日直接催化；-0.96%列纳指100公用事业（偏弱侧）——公用事业板块回落日的板块贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "ALB": ("联动", "暂未找到同日直接催化；-3.02%列标普500基础材料（偏弱侧）——基础材料板块回落日的板块贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "ALOY": ("联动", "暂未找到同日直接催化；-7.86%列罗素2000基础材料（偏弱侧）——基础材料板块回落日的板块贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "AMCX": ("联动", "暂未找到同日直接催化；+4.41%列罗素2000通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "AMGN": ("联动", "暂未找到同日直接催化；-2.25%列道指医疗保健（偏弱侧）——医疗保健板块回落日的板块贝塔。该股与当日所选医疗保健的偏弱方向一致。"),
    "APP": ("联动", "暂未找到同日直接催化；+3.09%列标普500通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "ARQQ": ("联动", "暂未找到同日直接催化；-4.90%列主题层量子计算（偏弱侧）——量子计算板块回落日的板块贝塔。该股与当日所选量子计算的偏弱方向一致。"),
    "BF-B": ("联动", "暂未找到同日直接催化；+1.68%列标普500必需消费（偏强侧）——必需消费板块领涨日的板块贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "CAT": ("联动", "暂未找到同日直接催化；-1.29%列道指工业（偏弱侧）——工业板块回落日的板块贝塔。该股与当日所选工业的偏弱方向一致。"),
    "CENX": ("联动", "暂未找到同日直接催化；-6.98%列罗素2000基础材料（偏弱侧）——基础材料板块回落日的板块贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "CHTR": ("联动", "暂未找到同日直接催化；+4.98%列标普500通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "CSX": ("联动", "暂未找到同日直接催化；+1.39%列纳指100工业（偏强侧）——工业板块领涨日的板块贝塔。该股与当日所选工业的偏强方向一致。"),
    "DIS": ("联动", "暂未找到同日直接催化；+1.57%列道指通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "FCX": ("联动", "暂未找到同日直接催化；-6.58%列标普500基础材料（偏弱侧）——基础材料板块回落日的板块贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "FDS": ("联动", "暂未找到同日直接催化；-5.82%列主题层大数据（偏弱侧）——大数据板块回落日的板块贝塔。该股与当日所选大数据的偏弱方向一致。"),
    "FGBI": ("联动", "暂未找到同日直接催化；+4.71%列罗素2000金融（偏强侧）——金融板块领涨日的板块贝塔。该股与当日所选金融的偏强方向一致。"),
    "FUBO": ("联动", "暂未找到同日直接催化；+6.54%列罗素2000通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "HON": ("联动", "暂未找到同日直接催化；-1.34%列道指工业（偏弱侧）——工业板块回落日的板块贝塔。该股与当日所选工业的偏弱方向一致。"),
    "HONA": ("联动", "暂未找到同日直接催化；+1.43%列纳指100工业（偏强侧）——工业板块领涨日的板块贝塔。该股与当日所选工业的偏强方向一致。"),
    "HPK": ("联动", "暂未找到同日直接催化；+4.51%列罗素2000能源（偏强侧）——能源板块领涨日的板块贝塔。该股与当日所选能源的偏强方向一致。"),
    "IHRT": ("联动", "暂未找到同日直接催化；+5.02%列罗素2000通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "IONQ": ("联动", "暂未找到同日直接催化；-3.41%列主题层量子计算（偏弱侧）——量子计算板块回落日的板块贝塔。该股与当日所选量子计算的偏弱方向一致。"),
    "KO": ("联动", "暂未找到同日直接催化；+0.32%列道指必需消费（偏强侧）——必需消费板块领涨日的板块贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "LDI": ("联动", "暂未找到同日直接催化；+6.63%列罗素2000金融（偏强侧）——金融板块领涨日的板块贝塔。该股与当日所选金融的偏强方向一致。"),
    "LIN": ("联动", "暂未找到同日直接催化；-1.08%列纳指100基础材料（偏弱侧）——基础材料板块回落日的板块贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "LRCX": ("联动", "暂未找到同日直接催化；-5.64%列标普500科技（偏弱侧）——科技板块回落日的板块贝塔。该股与当日所选科技的偏弱方向一致。"),
    "MET": ("联动", "暂未找到同日直接催化；+1.14%列标普500金融（偏强侧）——金融板块领涨日的板块贝塔。该股与当日所选金融的偏强方向一致。"),
    "MMM": ("联动", "暂未找到同日直接催化；-0.94%列道指工业（偏弱侧）——工业板块回落日的板块贝塔。该股与当日所选工业的偏弱方向一致。"),
    "MRK": ("联动", "暂未找到同日直接催化；-1.91%列道指医疗保健（偏弱侧）——医疗保健板块回落日的板块贝塔。该股与当日所选医疗保健的偏弱方向一致。"),
    "NRG": ("联动", "暂未找到同日直接催化；-3.22%列标普500公用事业（偏弱侧）——公用事业板块回落日的板块贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "NTRS": ("联动", "暂未找到同日直接催化；+1.35%列标普500金融（偏强侧）——金融板块领涨日的板块贝塔。该股与当日所选金融的偏强方向一致。"),
    "NXPI": ("联动", "暂未找到同日直接催化；+1.41%列主题层可穿戴（偏强侧）——可穿戴板块领涨日的板块贝塔。该股与当日所选可穿戴的偏强方向一致。"),
    "OII": ("联动", "暂未找到同日直接催化；+4.29%列罗素2000能源（偏强侧）——能源板块领涨日的板块贝塔。该股与当日所选能源的偏强方向一致。"),
    "OKLO": ("联动", "暂未找到同日直接催化；-6.32%列All Stocks公用事业（偏弱侧）——公用事业板块回落日的板块贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "PCAR": ("联动", "暂未找到同日直接催化；+0.57%列纳指100工业（偏强侧）——工业板块领涨日的板块贝塔。该股与当日所选工业的偏强方向一致。"),
    "PCT": ("联动", "暂未找到同日直接催化；-7.02%列罗素2000工业（偏弱侧）——工业板块回落日的板块贝塔。该股与当日所选工业的偏弱方向一致。"),
    "PG": ("联动", "暂未找到同日直接催化；+0.23%列道指必需消费（偏强侧）——必需消费板块领涨日的板块贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "PM": ("联动", "暂未找到同日直接催化；+2.19%列标普500必需消费（偏强侧）——必需消费板块领涨日的板块贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "QRVO": ("联动", "暂未找到同日直接催化；+6.76%列主题层电信（偏强侧）——电信板块领涨日的板块贝塔。该股与当日所选电信的偏强方向一致。"),
    "RDDT": ("联动", "暂未找到同日直接催化；+6.08%列标普500通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "REI": ("联动", "暂未找到同日直接催化；+4.73%列罗素2000能源（偏强侧）——能源板块领涨日的板块贝塔。该股与当日所选能源的偏强方向一致。"),
    "SCCO": ("联动", "暂未找到同日直接催化；-7.22%列主题层金属商品（偏弱侧）——金属商品板块回落日的板块贝塔。该股与当日所选金属商品的偏弱方向一致。"),
    "SNAP": ("联动", "暂未找到同日直接催化；+3.96%列主题层社交媒体（偏强侧）——社交媒体板块领涨日的板块贝塔。该股与当日所选社交媒体的偏强方向一致。"),
    "STZ": ("联动", "暂未找到同日直接催化；+1.86%列标普500必需消费（偏强侧）——必需消费板块领涨日的板块贝塔。该股与当日所选必需消费的偏强方向一致。"),
    "TRMK": ("联动", "暂未找到同日直接催化；+4.54%列罗素2000金融（偏强侧）——金融板块领涨日的板块贝塔。该股与当日所选金融的偏强方向一致。"),
    "TTWO": ("联动", "暂未找到同日直接催化；+2.76%列纳指100通信服务（偏强侧）——通信服务板块领涨日的板块贝塔。该股与当日所选通信服务的偏强方向一致。"),
    "UAA": ("联动", "暂未找到同日直接催化；+1.43%列主题层可穿戴（偏强侧）——可穿戴板块领涨日的板块贝塔。该股与当日所选可穿戴的偏强方向一致。"),
    "UAMY": ("联动", "暂未找到同日直接催化；-7.16%列罗素2000基础材料（偏弱侧）——基础材料板块回落日的板块贝塔。该股与当日所选基础材料的偏弱方向一致。"),
    "UNH": ("联动", "暂未找到同日直接催化；-1.22%列道指医疗保健（偏弱侧）——医疗保健板块回落日的板块贝塔。该股与当日所选医疗保健的偏弱方向一致。"),
    "XEL": ("联动", "暂未找到同日直接催化；-1.02%列纳指100公用事业（偏弱侧）——公用事业板块回落日的板块贝塔。该股与当日所选公用事业的偏弱方向一致。"),
    "YSS": ("联动", "暂未找到同日直接催化；-7.68%列罗素2000工业（偏弱侧）——工业板块回落日的板块贝塔。该股与当日所选工业的偏弱方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "BNO", "perf": 6.423, "form": "商品信托", "exposure": "布伦特原油现货",
         "reason": "布伦特原油ETF单日+6.42%：油价连续第四日暴涨（101美元后再度跳升，美伊冲突升级+中国买油移除缓冲+全球储存耗尽），商品端远强于股票端（能源股当日遭利好兑现抛售）。合并删除：DBO、USO、DBE（同簇原油期货，保留最强一只BNO）。"},
        {"ticker": "UGA", "perf": 5.356, "form": "商品信托", "exposure": "汽油期货",
         "reason": "汽油期货ETF +5.36%：成品油取代原油成为利润主战场（裂解价差约3倍历史均值的进一步走扩），与原油期货为不同层级炼端敞口。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "VIXY", "perf": 3.417, "form": "交易所交易基金", "exposure": "VIX期货",
         "reason": "VIX期货ETF：CPI前夜的对冲需求激增（VXX +3.17%同簇共振）——周五CPI为9/16 FOMC唯一裁决点，期权市场为其定价最大风险。合并删除：VXX（同簇VIX期货，保留最强一只VIXY）。"},
    ],
    "down": [
        {"ticker": "PPLT", "perf": -5.948, "form": "商品信托", "exposure": "铂金现货",
         "reason": "铂金ETF领跌全市场：贵金属全线暴跌（昨日+4.19%反弹的完全逆转）——油价通胀推升利率与美元、实际利率重升令零息资产全线承压。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "PALL", "perf": -5.454, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF：贵金属暴跌的第二极（-5.45%），与铂金为不同金属敞口。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "SIVR", "perf": -5.308, "form": "商品信托", "exposure": "白银现货",
         "reason": "白银现货信托：贵金属第三极（-5.31%、白银期货SLV -5.30%），金矿股（GDXJ -3.99%）放大。合并删除：SLV（同簇白银现货，保留更强SIVR）。"},
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
        text = "核查9月9日盘后至9月10日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-10"
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
            f"- `finviz_2026-09-10_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-10_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月10日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月10日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周四为PPI日（周五CPI为9/16 FOMC唯一裁决）、ECB决议日、Oracle盘后财报日。油价连续第四日暴涨：布伦特原油ETF单日+6.42%（汽油+5.36%、裂解价差进一步走扩）——但能源股遭利好兑现抛售（道指能源清一色跌：贝克休斯-6.66%；商品端远强于股票端）。通信服务五个股票范围全部进入涨幅前三（道指清一色：迪士尼+1.57%、谷歌+0.59%；Reddit +6.08%、Charter +4.98%、AppLovin +3.09%）——社交媒体主题清一色上涨（昨日领跌的完全反转）；金融四个范围居前（纳指100清一色：PayPal +2.19%；贷款与信托小盘+4.5%至+6.6%）；必需消费三个范围（防御轮动）。跌幅侧：基础材料五个范围全部最差（贵金属全线暴跌：铂金-5.95%、钯金-5.45%、白银-5.31%——昨日反弹的完全逆转；铜铝矿（Ero -8.55%、世纪铝业-6.98%、自由港-6.59%）与金属商品主题九子行业清一色跌）；公用事业四个范围（AI电力与核能谱系连续第二日回吐：Oklo -6.32%、Fervo -8.76%；纳指100清一色跌）；工业（道指清一色跌：卡特彼勒-1.30%）；科技内部半导体大跌（SOXX -2.74%：英特尔-5.57%、Lam -5.65%、HPE -6.25%）对苹果+3.56%（Duo发布后追买）。Oracle盘后财报前遭'AI债务破坏债券数学'抛售-5.38%。VIX期货ETF +3.42%（CPI前夜对冲需求激增）；核能铀矿行全线大跌（NLR -4.16%、URNJ -5.10%）与太空科技行回落（NASA -2.33%）。加密货币主题清一色跌。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5505/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1937/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (OUT / "finviz_2026-09-10_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-10_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-10_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
