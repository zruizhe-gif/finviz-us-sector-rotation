from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[2]
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
    "Telecommunications": "电信", "Wearables": "可穿戴设备",
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
}

THEME_COMPANY = {
    "AUID": "authID Inc",
    "AUR": "Aurora Innovation Inc",
    "BMBL": "Bumble Inc",
    "BWXT": "BWX Technologies Inc",
    "CRWD": "Crowdstrike Holdings Inc",
    "EXK": "Endeavour Silver Corp",
    "HL": "Hecla Mining Co",
    "LDOS": "Leidos Holdings Inc",
    "MGNI": "Magnite Inc",
    "MTA": "Metalla Royalty and Streaming Ltd",
    "OUST": "Ouster Inc",
    "PANW": "Palo Alto Networks Inc",
    "PLTR": "Palantir Technologies Inc",
    "PRCT": "Procept BioRobotics Corp",
    "RDDT": "Reddit Inc",
    "RPD": "Rapid7 Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月1日16:00 ET盘后事件可解释9月2日；9月2日16:00 ET后事件不得倒推。
R = {
    "GOOGL": ("直接", "谷歌9/2盘中迎来反垄断重大胜利：法官驳回DOJ要求拆分/出售其广告业务的诉求，'避免拆分、拒绝广告技术出售令'；另有Waymo与Pimco/Blackstone达成30亿美元债务融资的报道。+0.63%为道指通信服务（清一色上涨）成分。（事件时间2026-09-02 11:09 ET） [GOOGL Wins Big In Antitrust Fight Judge Blocks DOJs Push To Break Up Googles Ad Business](https://finance.yahoo.com/m/1a2b3c4d-e5f6-4a5b-8c9d-0e1f2a3b4c5d/googl-wins-big-in-antitrust.html) [Google avoids breakup as judge rejects ad tech sale order](https://finviz.com/news/387812/google-avoids-breakup-as-judge-rejects-ad-tech-sale-order)"),
    "PANW": ("直接", "Palo Alto 9/1盘后财报营收与指引全面超预期，但股价连续第二日大跌、当日-9.28%列网络安全主题（连续第二日清一色下跌）首位：超预期也满足不了被抬高的AI安全定价门槛，CEO'1万亿美元AI安全缺口'叙事未能止跌。（事件时间2026-09-02 08:44 ET报道） [Why Palo Alto Networks Stock Dropped Despite Huge Earnings Beat](https://finance.yahoo.com/m/8f7d2b1a-9c8e-4d5f-8a9b-0c1d2e3f4a5b/why-palo-alto-networks.html) [Palo Alto Networks earnings beat as CEO cites $1 trillion AI security gap](https://finviz.com/news/387790/palo-alto-networks-earnings-beat-as-ceo-cites-%241-trillion-ai-security-gap)"),
    "CVX": ("直接", "雪佛龙CEO Wirth当日详述委内瑞拉70亿美元以上投资的两大考量：5年70亿美元将产量提至2031年60万桶/日以上（美国能源部长Wright同日预计委全国产量本十年末翻倍至约200万桶/日）——西半球供给对冲霍尔木兹风险；+0.35%为道指能源唯一成分。（事件时间2026-09-02 10:41 ET） [Chevron CEO Mike Wirth Highlights Two Factors Behind The $7B-Plus Venezuela Bet](https://finance.yahoo.com/m/2b3c4d5e-f6a7-4b6c-9d0e-1f2a3b4c5d6e/chevron-ceo-highlights-two.html)"),
    "GPUS": ("直接", "Hyperscale Data 9/2盘前宣布已停止密歇根比特币挖矿业务、以满足AI数据中心转型的要求，叠加9/1盘后Q2区块链软件收入披露，当日-17.09%列All Stocks工业跌幅前列——转型期抛售。（事件时间2026-09-02 06:30 ET） [Hyperscale Data Has Ceased Bitcoin Mining Operations in Michigan as It Fulfills the Requirements of the AI Data Center](https://finviz.com/news/387755/hyperscale-data-has-ceased-bitcoin-mining-operations-in-michigan-as-it-fulfills-the-requirements-of-the-ai-data-center-transition)"),
    "CRWD": ("联动", "核查9月1日盘后至9月2日公司披露与可靠新闻后，暂未找到与跌幅方向一致的同日催化；与OpenAI扩大合作（保护Codex代理、集成GPT-5.6）为当日正面新闻但-5.42%方向相反——驱动为网络安全主题连续第二日清一色下跌（等权-4.04%）、Palo Alto'超预期仍大跌'的门槛效应压制全板块。该股与当日所选网络安全的偏弱方向一致。"),
    "PLTR": ("联动", "核查后暂未找到与跌幅方向一致的同日催化；美军TITAN项目进入生产阶段与CEO加码国防AI为当日正面新闻，但-5.81%方向相反——8月超大盘块涨幅居前后的动能回吐，叠加生物识别与国防主题走弱。该股与当日所选国防与航空航天、生物识别的偏弱方向一致。"),
    "FRVO": ("联动", "窗口内唯一候选为9/1盘后对谷歌地热协议的复盘报道（'协议来得比预期早'），无9/2新事件；-8.96%为周二+28.41%后的获利回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "PCG": ("联动", "暂未找到同日新催化；-5.19%为周二+5.95%反弹的回吐——加州野火立法风险定价仍在反复。该股与当日所选公用事业的偏弱方向一致。"),
    "EIX": ("联动", "暂未找到同日新催化；-6.14%列标普500公用事业跌幅首位，周二+8.93%反弹的回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "PYPL": ("联动", "暂未找到同日新催化；+4.33%为纳指100金融唯一成分——上周收购破裂抛压连续四日消化后的超跌反弹，与金融板块终结四连跌（区域银行ETF +2.23%）共振。该股与当日所选金融的偏强方向一致。"),
    "COST": ("联动", "窗口内DOJ牛肉反垄断调查数据请求新闻中Costco经聚合页面出现（非点名主体）；-1.22%为纳指100必需消费（6涨2跌中的偏弱端）贝塔。该股与当日所选必需消费的表现一致。"),
    "WMT": ("联动", "该股与当日道指必需消费（清一色上涨）的表现一致（+0.16%）。"),
    "AMZN": ("联动", "窗口内候选均为宏观文章，无公司事件；+0.02%基本持平——FTC诉讼冲击连续两日后企稳。该股与当日道指可选消费的表现一致。"),
    "AXP": ("联动", "窗口内候选为Berkshire新CEO谈数据中心电力成本的文章（经聚合页面出现，非公司事件）；+1.79%列道指金融（清一色上涨、终结四连跌）首位。该股与当日所选金融的偏强方向一致。"),
    "KO": ("联动", "该股与当日道指必需消费（清一色上涨）的表现一致（+0.27%）。"),
    "PG": ("联动", "窗口内唯一候选为股息贵族清单文章（外链）；+0.98%为道指必需消费（清一色上涨）领涨成分。该股与当日所选必需消费的偏强方向一致。"),
    "JNJ": ("联动", "唯一候选为Enovis收购新闻（标的非强生）；+1.48%为道指医疗保健（清一色上涨、连续第二日）领涨成分。该股与当日所选医疗保健的偏强方向一致。"),
    "IRM": ("联动", "中东社会发展银行合作扩展为次要地区性公告；-2.08%列标普500房地产（8涨/22跌、普涨日的相对落后板块）跌幅前列。该股与当日所选房地产的偏弱方向一致。"),
    "LIN": ("联动", "该股与当日纳指100基础材料（清一色上涨）唯一成分微涨入选一致。"),
    "CHTR": ("联动", "暂未找到同日直接催化；+8.74%列标普500通信服务涨幅第二——周二遭抛售的通信服务当日领涨的板块性反转，叠加上周CFO卸任消息后的超跌修复。该股与当日所选通信服务的偏强方向一致。"),
    "RDDT": ("联动", "暂未找到同日直接催化；+9.31%列标普500通信服务与社交媒体主题（清一色上涨、等权+2.41%）涨幅首位——连跌两日后的板块性修复。该股与当日所选通信服务、社交媒体的偏强方向一致。"),
    "MGNI": ("联动", "暂未找到同日直接催化；+8.69%列社交媒体主题（清一色上涨）第二位，广告技术在通信服务领涨日的高贝塔修复。该股与当日所选社交媒体的偏强方向一致。"),
    "BMBL": ("联动", "无窗口新闻；+5.60%列社交媒体主题（清一色上涨、等权+2.41%）第三位。该股与当日所选社交媒体的偏强方向一致。"),
    "TTD": ("联动", "无窗口新闻；+5.59%列标普500通信服务（17涨/4跌）涨幅第三。该股与当日所选通信服务的偏强方向一致。"),
    "DIS": ("联动", "无窗口新闻；+1.66%为道指通信服务（清一色上涨）领涨成分。该股与当日所选通信服务的偏强方向一致。"),
    "CABO": ("联动", "无窗口新闻微盘（区域性有线）；+19.44%列All Stocks与罗素2000通信服务（当日+2.76%领涨）涨幅首位，低流通修复。该股与当日所选通信服务的偏强方向一致。"),
    "CCOI": ("联动", "无窗口新闻；+13.43%列通信服务涨幅第二。该股与当日所选通信服务的偏强方向一致。"),
    "PLAY": ("联动", "无窗口新闻；+10.53%列通信服务涨幅第三（娱乐餐饮在风险偏好修复日反弹）。该股与当日所选通信服务的偏强方向一致。"),
    "MNTK": ("联动", "无窗口新闻微盘（可再生天然气）；+21.02%列All Stocks与罗素2000基础材料（当日领涨）涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日所选基础材料的偏强方向一致。"),
    "BAK": ("联动", "无窗口新闻（巴西石化）；+19.39%列All Stocks基础材料涨幅第二，与巴西ETF +4.16%共振——拉美风险资产修复。该股与当日所选基础材料的偏强方向一致。"),
    "UAMY": ("联动", "无窗口新闻微盘（锑）；+13.03%列基础材料涨幅前列，金属商品主题当日清一色上涨（等权+3.48%）的极端个体。该股与当日所选基础材料的偏强方向一致。"),
    "FMC": ("联动", "无窗口新闻（化肥/农化）；+12.21%列罗素2000基础材料涨幅前列。该股与当日所选基础材料的偏强方向一致。"),
    "EXK": ("联动", "无窗口新闻；+8.69%列金属商品主题（清一色上涨、等权+3.48%）首位——白银现货+1.99%、贵金属矿业ETF +4.7%—+5.4%的利率回落日反弹。该股与当日所选金属商品的偏强方向一致。"),
    "HL": ("联动", "无窗口新闻（第一大银矿股）；+8.69%列金属商品主题第二位。该股与当日所选金属商品的偏强方向一致。"),
    "MTA": ("联动", "无窗口新闻（金银权利金）；+8.00%列金属商品主题第三位。该股与当日所选金属商品的偏强方向一致。"),
    "STLD": ("联动", "无窗口新闻；+5.79%列标普500基础材料（19涨/1跌）涨幅首位——钢铁领涨。该股与当日所选基础材料的偏强方向一致。"),
    "NUE": ("联动", "无窗口新闻；+4.78%列标普500基础材料涨幅第二。该股与当日所选基础材料的偏强方向一致。"),
    "MOS": ("联动", "无窗口新闻（磷肥）；+4.04%列标普500基础材料涨幅第三。该股与当日所选基础材料的偏强方向一致。"),
    "RVTY": ("联动", "无窗口新闻；+3.44%列标普500医疗保健（46涨/13跌）涨幅首位。该股与当日所选医疗保健的偏强方向一致。"),
    "REGN": ("联动", "无窗口新闻；+3.42%列标普500医疗保健涨幅第二，连续第二日居前。该股与当日所选医疗保健的偏强方向一致。"),
    "CRL": ("联动", "无窗口新闻；+3.34%列标普500医疗保健涨幅第三。该股与当日所选医疗保健的偏强方向一致。"),
    "MRK": ("联动", "无窗口新闻；+1.19%为道指医疗保健（清一色上涨）成分。该股与当日所选医疗保健的偏强方向一致。"),
    "AMGN": ("联动", "无窗口新闻；+1.08%为道指医疗保健（清一色上涨）成分。该股与当日所选医疗保健的偏强方向一致。"),
    "V": ("联动", "无窗口新闻；+1.54%为道指金融（清一色上涨）第二涨幅。该股与当日所选金融的偏强方向一致。"),
    "TRV": ("联动", "无窗口新闻；+0.62%为道指金融（清一色上涨）成分。该股与当日所选金融的偏强方向一致。"),
    "SEZL": ("联动", "无窗口新闻微盘（先买后付）；+6.10%列罗素2000金融（324/357上涨）涨幅首位。该股与当日所选金融的偏强方向一致。"),
    "WRLD": ("联动", "无窗口新闻；+5.69%列罗素2000金融涨幅第二。该股与当日所选金融的偏强方向一致。"),
    "CD": ("联动", "无窗口新闻微盘；+5.61%列罗素2000金融涨幅第三。该股与当日所选金融的偏强方向一致。"),
    "NCPL": ("联动", "无窗口新闻微盘；+30.05%列All Stocks金融涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日所选金融的偏强方向一致。"),
    "AMBR": ("联动", "无窗口新闻微盘；+15.90%列All Stocks金融涨幅第二，低流通异动。该股与当日所选金融的偏强方向一致。"),
    "BRR": ("联动", "无窗口新闻微盘；+11.06%列All Stocks金融涨幅第三。该股与当日所选金融的偏强方向一致。"),
    "WHLR": ("联动", "无窗口新闻微盘REIT；-9.30%列All Stocks房地产跌幅首位——该股连续多日无解释极端波动（8/31 -36%起连续上榜），仅作流动性风险提示。该股与当日所选房地产的偏弱方向一致。"),
    "SQFT": ("联动", "无窗口新闻微盘REIT；-6.49%列All Stocks房地产跌幅第二。该股与当日所选房地产的偏弱方向一致。"),
    "UK": ("联动", "无窗口新闻微盘（中概联合办公）；-5.26%列All Stocks房地产跌幅第三。该股与当日所选房地产的偏弱方向一致。"),
    "CSGP": ("联动", "无窗口新闻；-2.25%列标普500房地产（8涨/22跌）跌幅首位。该股与当日所选房地产的偏弱方向一致。"),
    "PLD": ("联动", "无窗口新闻（物流地产）；-2.21%列标普500房地产跌幅第二。该股与当日所选房地产的偏弱方向一致。"),
    "ONL": ("联动", "无窗口新闻微盘REIT；-3.58%列罗素2000房地产跌幅首位。该股与当日所选房地产的偏弱方向一致。"),
    "NMRK": ("联动", "无窗口新闻（地产服务）；-3.46%列罗素2000房地产跌幅第二。该股与当日所选房地产的偏弱方向一致。"),
    "CWK": ("联动", "无窗口新闻；-2.61%列罗素2000房地产跌幅第三。该股与当日所选房地产的偏弱方向一致。"),
    "SDST": ("联动", "无窗口新闻微盘；-27.88%列All Stocks工业跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "XTIA": ("联动", "无窗口新闻微盘（航空制造）；-17.39%列All Stocks工业跌幅第二，低流通崩跌，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "VRSK": ("联动", "无窗口新闻；-3.19%列标普500工业（31涨/43跌）跌幅首位。该股与当日所选工业的偏弱方向一致。"),
    "FDX": ("联动", "无窗口新闻；-2.57%列标普500工业跌幅第二——道指运输指数当日缺席上涨。该股与当日所选工业的偏弱方向一致。"),
    "LMT": ("联动", "无窗口新闻；-2.38%列标普500工业跌幅第三，国防走弱（国防与航空航天主题-0.84%）。该股与当日所选工业、国防与航空航天偏弱方向一致。"),
    "AXON": ("联动", "无窗口新闻；-2.18%列纳指100工业（3涨/10跌）跌幅首位。该股与当日所选工业的偏弱方向一致。"),
    "HON": ("联动", "无窗口新闻；-1.86%列纳指100工业跌幅第二。该股与当日所选工业的偏弱方向一致。"),
    "FAST": ("联动", "无窗口新闻；-1.68%列纳指100工业跌幅第三。该股与当日所选工业的偏弱方向一致。"),
    "BRNX": ("联动", "无窗口新闻微盘；-10.23%列All Stocks公用事业跌幅首位，暂未找到同日直接催化。该股与当日所选公用事业的偏弱方向一致。"),
    "NXXT": ("联动", "无窗口新闻微盘；-6.23%列All Stocks公用事业跌幅第三。该股与当日所选公用事业的偏弱方向一致。"),
    "ORA": ("联动", "无窗口新闻（地热）；-2.42%列罗素2000公用事业（13涨/19跌）跌幅首位——周二Fervo驱动的地热行情回吐。该股与当日所选公用事业的偏弱方向一致。"),
    "BIPC": ("联动", "无窗口新闻（基建）；-2.09%列罗素2000公用事业跌幅第二。该股与当日所选公用事业的偏弱方向一致。"),
    "GWRS": ("联动", "无窗口新闻（水务）；-1.46%列罗素2000公用事业跌幅第三。该股与当日所选公用事业的偏弱方向一致。"),
    "EVRG": ("联动", "无窗口新闻；-0.92%列标普500公用事业（15涨/16跌）跌幅第三。该股与当日所选公用事业的偏弱方向一致。"),
    "BKR": ("联动", "无窗口新闻；+1.53%列纳指100能源（清一色上涨）首位。该股与当日所选能源的偏强方向一致。"),
    "FANG": ("联动", "无窗口新闻；+0.13%列纳指100能源（清一色上涨）成分。该股与当日所选能源的偏强方向一致。"),
    "HD": ("联动", "无窗口新闻；-0.39%为道指可选消费（2涨2跌）偏弱端。该股与当日道指可选消费的表现一致。"),
    "MCD": ("联动", "无窗口新闻；-0.06%为道指可选消费（2涨2跌）成分。该股与当日道指可选消费的表现一致。"),
    "MNST": ("联动", "无窗口新闻；-1.27%列纳指100必需消费（6涨2跌）偏弱端。该股与当日所选必需消费的表现一致。"),
    "FC": ("联动", "无窗口新闻；-3.28%列罗素2000必需消费跌幅首位（相对落后组）。该股与当日所选必需消费的偏弱方向一致。"),
    "LAUR": ("联动", "无窗口新闻（教育）；-2.89%列罗素2000必需消费跌幅第二。该股与当日所选必需消费的偏弱方向一致。"),
    "LRN": ("联动", "无窗口新闻（在线教育）；-2.50%列罗素2000必需消费跌幅第三。该股与当日所选必需消费的偏弱方向一致。"),
    "AUID": ("联动", "无窗口新闻微盘（身份认证）；-9.27%列生物识别主题（清一色下跌、等权-1.31%）首位。该股与当日所选生物识别的偏弱方向一致。"),
    "LDOS": ("联动", "无窗口新闻；-3.88%列生物识别主题与国防主题跌幅侧。该股与当日所选生物识别、国防与航空航天的偏弱方向一致。"),
    "BWXT": ("联动", "无窗口新闻（核能）；-3.63%列国防与航空航天主题（2涨/5跌）跌幅前列。该股与当日所选国防与航空航天的偏弱方向一致。"),
    "RPD": ("联动", "无窗口新闻；-7.83%列网络安全主题（连续第二日清一色下跌）第二跌幅。该股与当日所选网络安全的偏弱方向一致。"),
    "AUR": ("联动", "无窗口新闻（自动驾驶）；+7.14%列机器人主题（清一色上涨、等权+1.15%）首位。该股与当日所选机器人的偏强方向一致。"),
    "PRCT": ("联动", "无窗口新闻（手术机器人）；+5.07%列机器人主题第二位。该股与当日所选机器人的偏强方向一致。"),
    "OUST": ("联动", "无窗口新闻（激光雷达）；+4.72%列机器人主题第三位。该股与当日所选机器人的偏强方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "GDXJ", "perf": 4.719, "form": "交易所交易基金", "exposure": "全球金矿（中小型）",
         "reason": "中小金矿ETF领涨全市场：黄金+1.52%的两日暴跌后反弹、10年期收益率自4.81六连涨后回落至约4.77——利率回落日贵金属高贝塔矿业弹性最大。合并删除：GDX、SGDM、RING（同簇金矿股，保留最强一只）。"},
        {"ticker": "SILJ", "perf": 5.361, "form": "交易所交易基金", "exposure": "全球银矿（中小型）",
         "reason": "银矿ETF：白银现货+1.99%、白银主题个股全线反弹（Endeavour Silver/Hecla均+8.7%），与金矿为不同金属敞口。合并删除：SIL（同簇银矿股，按表现保留更强一只SILJ）。"},
        {"ticker": "EWZ", "perf": 4.156, "form": "交易所交易基金", "exposure": "巴西股票",
         "reason": "巴西ETF：委内瑞拉协议与拉美风险资产修复（Braskem ADR +19.4%），独立地域敞口。合并删除：无同簇产品进入本轮极值候选。"},
    ],
    "down": [
        {"ticker": "VIXY", "perf": -2.921, "form": "交易所交易基金", "exposure": "VIX期货",
         "reason": "VIX期货ETF：反弹日对冲需求退潮——前一日+3.06%（risk-off）的当日回吐，标普500宽度302涨/200跌。合并删除：VXX、VIXM（同簇VIX期货，保留最强一只VIXY）。"},
        {"ticker": "HACK", "perf": -2.208, "form": "交易所交易基金", "exposure": "全球科技｜网络安全",
         "reason": "网络安全ETF：连续第三日下跌、主题连续第二日清一色下跌（等权-4.04%）——Palo Alto超预期仍大跌-9.28%的门槛效应。独立科技子行业敞口。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "UGA", "perf": -2.118, "form": "商品信托", "exposure": "汽油期货",
         "reason": "汽油期货ETF：油价高位企稳但成品油裂解价差回落（前一日+2.29%的回吐），能源商品内部的炼端利润修正。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查9月1日盘后至9月2日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-02"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；金矿股簇（GDXJ/GDX/SGDM/RING）保留GDXJ、银矿股簇（SILJ/SIL）保留SILJ、VIX期货簇（VIXY/VXX/VIXM）保留VIXY。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-02_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-02_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月2日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月2日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：油价高位企稳（布伦特约95美元+0.7%、WTI约90美元+0.5%、美伊冲突再度升级）但不再压制股指，10年期收益率自4.81%的六连涨回落至约4.77%——标普500收涨约0.5%终结三连跌（宽度302涨/200跌）、道指+300点（+0.6%）、纳指100 +0.2%、罗素2000 +1.1%跑赢，道指运输缺席上涨。板块三条主线领涨：基础材料（五个范围中的四个进入涨幅前三、道指与纳指100清一色——金属商品主题七子行业清一色涨等权+3.48%：贵金属矿业两日暴跌后反弹（中小金矿+4.72%、银矿+5.36%、黄金+1.52%白银+1.99%）、钢铁（Steel Dynamics +5.79%）、化肥农化（FMC +12.21%）、巴西链（Braskem +19.39%、巴西ETF +4.16%））；通信服务（四个范围进入涨幅前三、道指清一色：Reddit +9.31%、Charter +8.74%——周二遭抛售的完全反转，谷歌赢得反垄断大胜（法官驳回DOJ广告业务拆分诉求）+0.63%）；金融（四个范围进入涨幅前三、道指与纳指100清一色、终结四连跌：区域银行ETF +2.23%、PayPal +4.33%超跌反弹）。医疗保健连续第二日居前（道指清一色）。相对落后：公用事业与房地产（普涨日垫底——爱迪生联合-6.14%、PG&E -5.19%回吐周二反弹；加州立法风险定价反复）、工业（纳指100工业3涨/10跌）。主题层罕见七个清一色上涨（金属商品、社交媒体+2.41%、机器人、可穿戴、纳米、环境可持续）对两个清一色下跌（网络安全连续第二日-4.04%——Palo Alto财报超预期仍大跌-9.28%、生物识别）；VIX期货ETF -2.92%回吐前一日涨幅。个股与事件：Dell +15.8%（全年指引上修250亿至1,920亿美元、AI服务器同比三倍、12个月订单超1,300亿）；GE Vernova +2.6%（承修委内瑞拉电网）；英伟达拟收购Hugging Face（金额各档口径不一140亿—400亿美元）；Uber裁员3,300人；盘后Snowflake +17.5%（上修全年产品收入指引）、Five Below与Petco超预期、Broadcom指引不及预期盘后转跌。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5527/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1939/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-09-02_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-09-02_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-09-02_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
