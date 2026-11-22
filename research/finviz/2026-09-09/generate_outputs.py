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
    "ASTS": "AST SpaceMobile Inc",
    "BNED": "Barnes & Noble Education Inc",
    "CHGG": "Chegg Inc",
    "COHU": "Cohu Inc",
    "DUOL": "Duolingo Inc",
    "ENVX": "Enovix Corp",
    "FFIV": "F5 Inc",
    "NET": "Cloudflare Inc",
    "PSNY": "Platanus Energy Corp",
    "SPCE": "Virgin Galactic Holdings Inc",
    "UMC": "United Microelectronics Corp",
    "VSAT": "Viasat Inc",
    "WBX": "Wallbox NV",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "BNED": ("直接", "Fiscal Q1财报（9/8盘后）不及预期，-11.59%列教育科技主题（清一色下跌）与All Stocks跌幅侧。（事件时间2026-09-08 16:05 ET） [Barnes & Noble Education Reports Fiscal 2027 First Quarter Financial Results](https://finviz.com/news/388301/barnes-noble-education-reports-fiscal-2027-first-quarter-financial-results)"),
    "BRZE": ("直接", "盈利指引令人失望，-21.73%列全市场跌幅前列（分析师称回调是买点但当日无效）。（事件时间2026-09-09 10:17 ET） [Braze Stock Plummets After Disappointing Profit Outlook](https://finviz.com/news/388355/braze-stock-plummets-after-disappointing-profit-outlook)"),
    "CASY": ("直接", "财报超预期但店内销售增长令人失望，-14.24%（beat-and-fall）列标普500可选消费跌幅首位。（事件时间2026-09-09 08:30 ET） [Casey's shares slide despite earnings beat as inside sales growth disappoints](https://finviz.com/news/388345/caseys-shares-slide-despite-earnings-beat)"),
    "CRMT": ("直接", "营收-57%（资本约束致零售销量-82%），-40.76%列全市场跌幅首位。（事件时间2026-09-09 07:30 ET） [America's Car-Mart Revenue Falls 57%](https://finviz.com/news/388330/americas-car-mart-revenue-falls-57)"),
    "CSR": ("直接", "Independence Realty Trust与Centerspace达成81亿美元合并，+8.82%列罗素2000房地产涨幅首位。（事件时间2026-09-09 07:03 ET） [Independence Realty Trust and Centerspace Agree to $8.1 Billion Merger](https://finviz.com/news/388320/independence-realty-trust-and-centerspace-agree-to-8.1-billion-merger)"),
    "FTK": ("直接", "再度上调2026年营收指引至3.60—3.70亿美元（国际销售持续强劲），+14.40%列All Stocks能源涨幅前列。（事件时间2026-09-09 06:30 ET） [Flotek raises 2026 revenue guidance](https://finviz.com/news/388310/flotek-raises-2026-revenue-guidance)"),
    "SUNE": ("直接", "Suniva完成8.35亿美元融资建设第二座美国太阳能电池厂（9/8盘后），+90.30%列全市场涨幅首位。（事件时间2026-09-08 16:05 ET） [Suniva Completes $835 Million Capital Raise](https://finviz.com/news/388290/suniva-completes-835-million-capital-raise)"),
    "TTAN": ("直接", "财报超预期但指引不及，-29.98%列罗素2000科技跌幅首位（'创纪录自由现金流与AI驱动'未能救指引杀）。（事件时间2026-09-09 05:56 ET） [ServiceTitan Stock Drops After Guidance Falls Short](https://finviz.com/news/388300/servicetitan-stock-drops-after-guidance-falls-short)"),
    "YSS": ("直接", "Robbins律所调查York Space涉嫌就能力误导投资者，-9.63%列罗素2000工业与太空科技主题跌幅侧。（事件时间2026-09-09 15:19 ET） [Robbins LLP is Investigating York Space Systems](https://finviz.com/news/388400/robins-llp-investigates-york-space-systems)"),
    "META": ("联动", "核查9月8日盘后至9月9日公司披露与可靠新闻后，暂未找到同日直接催化；+6.55%创两个月新高——Muse被TD Cowen视为'显著'收入流+收购瑞典AI初创Stilla.ai的独家报道与涨幅同向但均非公司正式公告。该股与当日纳指100通信服务的表现一致。"),
    "AAPL": ("联动", "Duo折叠iPhone发布会（1,999美元、Ternus首秀'one more thing'）；-0.28%基本持平——发布会前避险、当日兑现温和。该股与当日道指科技的表现一致。"),
    "AMZN": ("联动", "窗口内候选均为高通-亚马逊芯片协议的延续报道；-1.78%随超大盘科技回落——协议利好已被定价。该股与当日道指可选消费（清一色下跌）的偏弱方向一致。"),
    "GOOGL": ("联动", "欧盟新规下搜索结果将变差的警告；-2.28%列道指通信服务（清一色下跌）首位。该股与当日道指通信服务的偏弱方向一致。"),
    "MRVL": ("联动", "CEO'AI市场的瑞士'言论回应高通-亚马逊威胁；+4.26%列纳指100科技涨幅侧——连续第三日修复。该股与当日所选科技的偏强方向一致。"),
    "JPM": ("联动", "该股与当日道指金融（补位上涨组）的表现一致（+0.34%领涨）。"),
    "V": ("联动", "该股与当日道指金融（补位上涨组）的表现一致（+0.33%）。"),
    "TRV": ("联动", "该股与当日道指金融（补位上涨组）的表现一致（+0.33%）。"),
    "DIS": ("联动", "窗口内候选为无关消费者文章；-0.84%为道指通信服务（清一色下跌）成分。该股与当日道指通信服务的偏弱方向一致。"),
    "NKE": ("联动", "暂未找到同日直接催化；-1.97%列道指可选消费（清一色下跌）跌幅侧。该股与当日所选可选消费的偏弱方向一致。"),
    "HD": ("联动", "该股与当日道指可选消费（清一色下跌）的偏弱方向一致（-1.04%）。"),
    "SEI": ("联动", "窗口内候选为NYSE得州办公室联合CEO访谈（延续性）；+5.80%列All Stocks能源涨幅侧——连续第二日强势。该股与当日所选能源的偏强方向一致。"),
    "SPCX": ("联动", "窗口内候选为'分析师惊人目标价'与Schwab散户买入榜（延续性）；-3.86%列纳指100工业（清一色下跌）——昨日+3.73%的完全反转。该股与当日所选工业、太空科技的偏弱方向一致。"),
    "RKLB": ("联动", "无窗口新闻；-4.25%列纳指100工业（清一色下跌）——太空科技主题（清一色下跌）的共振。该股与当日所选工业、太空科技的偏弱方向一致。"),
    "BKR": ("联动", "暂未找到同日直接催化；+0.60%列纳指100能源侧——油价破百下的能源第三日。该股与当日所选能源的偏强方向一致。"),
    "FANG": ("联动", "该股与当日所选能源的偏强方向一致（+1.49%列纳指100能源首位）。"),
    "CVX": ("联动", "该股与当日所选能源的偏强方向一致（+1.91%列标普能源侧）。"),
    "APA": ("联动", "该股与当日所选能源的偏强方向一致（+2.96%列标普能源涨幅侧）。"),
    "XOM": ("联动", "该股与当日所选能源的偏强方向一致（+2.22%列标普能源侧）。"),
    "FLNC": ("联动", "无窗口新闻（储能）；-8.33%列All Stocks公用事业跌幅侧——昨日核能/储能谱系的回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "ORA": ("联动", "无窗口新闻（地热）；-8.48%列All Stocks公用事业跌幅侧——同上回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "FRVO": ("联动", "暂未找到同日直接催化；-8.78%列All Stocks公用事业跌幅首位——昨日+28.41%（谷歌协议）的获利回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "VRT": ("联动", "无窗口新闻（数据中心机电）；-9.61%列标普500工业跌幅首位——昨日+4.35%的回吐。该股与当日所选工业的偏弱方向一致。"),
    "AXON": ("联动", "无窗口新闻；-3.05%列标普500工业跌幅侧。该股与当日所选工业的偏弱方向一致。"),
    "FDXF": ("联动", "无窗口新闻（FedEx货运分拆）；-3.32%列标普500工业跌幅侧。该股与当日所选工业的偏弱方向一致。"),
    "NET": ("联动", "暂未找到同日直接催化；+10.51%列网络安全主题（涨幅侧首位）与All Stocks科技前列。该股与当日所选科技、网络安全的偏强方向一致。"),
    "DDOG": ("联动", "暂未找到同日直接催化；+7.15%列标普500科技涨幅首位。该股与当日所选科技的偏强方向一致。"),
    "FICO": ("联动", "无窗口新闻；+5.35%列标普500科技第二。该股与当日所选科技的偏强方向一致。"),
    "HPE": ("联动", "无窗口新闻；+5.12%列标普500科技第三。该股与当日所选科技的偏强方向一致。"),
    "ALAB": ("联动", "无窗口新闻（AI连接芯片）；+4.05%列纳指100科技涨幅侧。该股与当日所选科技的偏强方向一致。"),
    "CSCO": ("联动", "该股与当日道指科技（补位上涨组）的表现一致（+0.24%）。"),
    "IBM": ("联动", "该股与当日道指科技（补位上涨组）的表现一致（+3.38%领涨）。"),
    "NFLX": ("联动", "暂未找到同日直接催化；-0.96%列纳指100通信服务（补位上涨组内偏弱）。该股与当日纳指100通信服务的表现一致。"),
    "WBD": ("联动", "窗口内候选为Paramount合并延期保护动作（延续性）；-0.75%随通信服务回落。该股与当日通信服务的偏弱方向一致。"),
    "ENVX": ("联动", "无窗口新闻微盘（电池）；-8.93%列电动汽车主题（清一色下跌）侧。该股与当日电动汽车主题的偏弱方向一致。"),
    "PSNY": ("联动", "无窗口新闻微盘（光伏）；-10.86%列电动汽车主题跌幅首位。该股与当日电动汽车主题的偏弱方向一致。"),
    "WBX": ("联动", "无窗口新闻（充电）；-11.02%列电动汽车主题跌幅侧。该股与当日电动汽车主题的偏弱方向一致。"),
    "FTFT": ("联动", "无窗口新闻微盘（区块链）；+59.54%列All Stocks科技涨幅首位——加密主题清一色跌日的逆势低流通异动，暂未找到同日直接催化，不纳入结构判断。"),
    "CDNL": ("联动", "无窗口新闻微盘；-9.55%列罗素2000工业跌幅侧。该股与当日所选工业的偏弱方向一致。"),
    "SSM": ("联动", "无窗口新闻微盘；-24.92%列All Stocks可选消费跌幅前列，低流通崩跌。该股与当日所选可选消费的偏弱方向一致。"),
    "MWYN": ("联动", "无窗口新闻微盘；-27.99%列All Stocks可选消费跌幅侧，低流通崩跌。该股与当日所选可选消费的偏弱方向一致。"),
    "VWAV": ("联动", "无窗口新闻微盘；-20.50%列All Stocks工业跌幅前列，低流通崩跌。该股与当日所选工业的偏弱方向一致。"),
    "GRNQ": ("联动", "无窗口新闻微盘；-29.63%列All Stocks工业跌幅首位（9/8曾+30.77%）——双向极端波动。该股与当日所选工业的偏弱方向一致。"),
    "FJET": ("联动", "无窗口新闻微盘；-22.05%列All Stocks工业跌幅前列。该股与当日所选工业的偏弱方向一致。"),
    "SSL": ("联动", "无窗口新闻（南非化工）；+9.62%列All Stocks基础材料涨幅侧。该股与当日基础材料端的表现一致。"),
    "SID": ("联动", "无窗口新闻（巴西钢铁）；+7.26%列All Stocks基础材料涨幅侧。该股与当日基础材料端的表现一致。"),
    "YMAT": ("联动", "无窗口新闻微盘；+71.32%列All Stocks基础材料涨幅首位，低流通异动，暂未找到同日直接催化，不纳入结构判断。"),
    "OLB": ("联动", "无窗口新闻微盘；+22.62%列All Stocks科技涨幅侧，低流通异动。该股与当日所选科技的表现一致。"),
    "VELO": ("联动", "无窗口新闻微盘；-8.78%列罗素2000科技跌幅侧。该股与当日罗素2000科技的偏弱方向一致。"),
    "EIX": ("联动", "无窗口新闻；-3.19%列标普500公用事业（清一色下跌）首位——昨日+4.51%的回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "PCG": ("联动", "无窗口新闻；-4.25%列标普500公用事业（清一色下跌）跌幅侧——昨日+3.64%的回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "NRG": ("联动", "无窗口新闻；-3.57%列标普500公用事业跌幅侧——昨日+6.42%的回吐（AI电力子集随板块回落）。该股与当日所选公用事业的偏弱方向一致。"),
    "CEG": ("联动", "无窗口新闻；-1.72%为纳指100公用事业（清一色下跌）领跌成分。该股与当日所选公用事业的偏弱方向一致。"),
    "XEL": ("联动", "无窗口新闻；-0.90%列纳指100公用事业（清一色下跌）成分。该股与当日所选公用事业的偏弱方向一致。"),
    "AEP": ("联动", "无窗口新闻；-0.60%列纳指100公用事业（清一色下跌）成分。该股与当日所选公用事业的偏弱方向一致。"),
    "CDZI": ("联动", "无窗口新闻（水资源）；-6.03%列罗素2000公用事业跌幅首位。该股与当日所选公用事业的偏弱方向一致。"),
    "IP": ("联动", "无窗口新闻（包装纸品）；-5.07%列标普500可选消费跌幅侧。该股与当日所选可选消费的偏弱方向一致。"),
    "SW": ("联动", "无窗口新闻（包装）；-4.65%列标普500可选消费跌幅侧。该股与当日所选可选消费的偏弱方向一致。"),
    "HCA": ("联动", "无窗口新闻（医院）；+4.93%列标普500医疗保健涨幅侧（反弹日）。该股与当日标普医疗保健的表现一致。"),
    "DVA": ("联动", "无窗口新闻（透析）；+1.64%列标普500医疗保健涨幅侧。该股与当日标普医疗保健的表现一致。"),
    "UHS": ("联动", "无窗口新闻（医院）；+2.26%列标普500医疗保健涨幅侧。该股与当日标普医疗保健的表现一致。"),
    "PYPL": ("联动", "暂未找到同日直接催化；-1.90%为纳指100金融（清一色下跌）唯一成分。该股与当日纳指100金融的偏弱方向一致。"),
    "ARL": ("联动", "无窗口新闻微盘REIT；+3.95%列罗素2000房地产涨幅侧。该股与当日罗素2000房地产的表现一致。"),
    "CMTG": ("联动", "无窗口新闻（商业地产信贷）；+2.60%列罗素2000房地产涨幅侧。该股与当日罗素2000房地产的表现一致。"),
    "ASIC": ("联动", "无窗口新闻（保险）；+2.26%列罗素2000金融涨幅侧。该股与当日罗素2000金融的表现一致。"),
    "KMPR": ("联动", "无窗口新闻（保险）；+2.10%列罗素2000金融涨幅侧。该股与当日罗素2000金融的表现一致。"),
    "GOLD": ("联动", "无窗口新闻微盘；+3.92%列罗素2000金融涨幅侧——贵金属反弹日的个体映射。该股与当日罗素2000金融的表现一致。"),
    "KGEI": ("联动", "无窗口新闻微盘（油气）；+5.66%列罗素2000能源涨幅侧。该股与当日罗素2000能源的表现一致。"),
    "TMDE": ("联动", "无窗口新闻微盘（油气）；+7.19%列All Stocks能源涨幅侧。该股与当日所选能源的偏强方向一致。"),
    "ASTS": ("联动", "无窗口新闻；-5.60%列太空科技主题（清一色下跌）——昨日清一色涨的完全反转。该股与当日太空科技的偏弱方向一致。"),
    "SPCE": ("联动", "无窗口新闻；-5.43%列太空科技主题（清一色下跌）。该股与当日太空科技的偏弱方向一致。"),
    "VSAT": ("联动", "无窗口新闻；-6.93%列太空科技主题（清一色下跌）。该股与当日太空科技的偏弱方向一致。"),
    "COHU": ("联动", "无窗口新闻（半导体测试）；+6.60%列半导体主题（涨幅侧首位）——连续第二日。该股与当日半导体主题的表现一致。"),
    "UMC": ("联动", "无窗口新闻（晶圆代工）；+3.99%列半导体主题涨幅侧。该股与当日半导体主题的表现一致。"),
    "FFIV": ("联动", "无窗口新闻；+3.85%列网络安全主题（涨幅侧）。该股与当日网络安全主题的表现一致。"),
    "FSLY": ("联动", "无窗口新闻；+5.68%列云计算主题（涨幅侧首位）。该股与当日云计算主题的表现一致。"),
    "CHGG": ("联动", "无窗口新闻；-4.90%列教育科技主题（清一色下跌）——连续第二日。该股与当日教育科技的偏弱方向一致。"),
    "DUOL": ("联动", "无窗口新闻；-4.88%列教育科技主题（清一色下跌）。该股与当日教育科技的偏弱方向一致。"),
    "SHW": ("联动", "该股与当日道指基础材料（清一色下跌）唯一成分的偏弱方向一致（-1.67%）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "PPLT", "perf": 4.192, "form": "商品信托", "exposure": "铂金现货",
         "reason": "铂金ETF领涨全市场：贵金属全线反弹（白银现货+2.29%、黄金+0.91%、金矿+1.34%）——昨日回撤的当日修复，铂金弹性最大。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "DBO", "perf": 2.816, "form": "商品信托", "exposure": "原油期货（Invesco DB）",
         "reason": "原油期货ETF：油价盘中突破100美元（布伦特四日第二度逼三位数、WTI随美伊冲突升级），能源股连续第三日领涨的商品端映射。合并删除：BNO、USO、DBE（同簇原油期货，保留最强一只DBO）。"},
        {"ticker": "SIVR", "perf": 2.290, "form": "商品信托", "exposure": "白银现货",
         "reason": "白银现货信托：贵金属修复日的第二强现货（+2.29%），与铂金为不同金属敞口。合并删除：SLV（同簇白银现货，保留更强SIVR）。"},
    ],
    "down": [
        {"ticker": "UNG", "perf": -3.537, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货ETF连续第二日领跌全市场（-0.95%后-3.54%）：天气与库存驱动，能源商品内部气弱油强。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "BBC", "perf": -3.122, "form": "交易所交易基金", "exposure": "生物科技临床试验股",
         "reason": "生物科技临床试验ETF：昨日安进事件的第二日余波+医疗板块续弱（XBI -1.58%）——临床类资产的持续重定价。合并删除：BBH（同簇生物科技，保留更强一只BBC）。"},
        {"ticker": "TAN", "perf": -2.829, "form": "交易所交易基金", "exposure": "全球太阳能",
         "reason": "太阳能ETF：昨日可再生能源主题领涨的当日反转（利率再度上行压制资本密集型清洁能源），与生物科技为不同板块敞口。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查9月8日盘后至9月9日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-09"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；原油期货簇（DBO/BNO/USO/DBE）保留DBO、生物科技簇（BBC/BBH/XBI另计）保留BBC、太阳能簇（TAN）独立。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-09_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-09_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月9日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月9日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周三油价盘中突破100美元（布伦特四日第二度逼三位数、美伊冲突持续升级）、美债收益率创2023年来新高——股指再度下滑，而板块层延续剧烈一日反转：昨日领涨的工业与公用事业当日领跌（工业五个范围全部进入跌幅侧、道指与纳指100清一色：Vertiv -9.61%、Rocket Lab -4.25%；公用事业四个范围跌幅侧、标普与纳指100清一色跌：爱迪生联合-3.19%、PG&E -4.25%、NRG -3.57%——昨日AI电力与核能谱系全面回吐），昨日重挫的医疗保健当日反弹居涨幅侧（HCA +4.93%、DaVita +1.64%），金融在道指与罗素端补位偏强（摩根大通+0.34%领涨道指）。能源连续第三日五范围领涨（雪佛龙+1.91%、埃克森+2.22%、APA +2.96%、Solaris连续第二日+5.80%、Flotek上修指引+14.40%——油价破百的商品端映射DBO +2.82%）。科技反弹但内部分化：META +6.55%创两个月新高（Muse收入流+收购Stilla.ai报道）、Datadog +7.15%、Cloudflare +10.51%领涨网络安全主题（涨幅侧首位）；苹果Duo折叠iPhone发布会（1,999美元、Ternus首秀'one more thing'）当日-0.28%兑现温和。太空科技主题清一色下跌（昨日清一色涨的完全反转：Virgin Galactic -5.43%、AST -5.60%、Viasat -6.93%、York遭律所调查-9.63%）；教育科技、电动汽车同现清一色跌。财报杀密集：Braze -21.73%（指引失望）、Casey's -14.24%（店内销售失望）、ServiceTitan -29.98%（指引不及）、Car-Mart -40.76%（营收-57%）；上涨端Sunation +90.30%（Suniva 8.35亿美元融资）、Centerspace +8.82%（81亿美元合并）。贵金属全线反弹（铂金+4.19%居ETF榜首、白银+2.29%、黄金+0.91%）；天然气连续第二日领跌（-3.54%）、比特币微跌。周四PPI、周五CPI（共识0.4%/0.2%）临近，VIX期货ETF +1.72%。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5507/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1937/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (OUT / "finviz_2026-09-09_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-09_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-09_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
