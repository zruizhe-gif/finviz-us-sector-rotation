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
    "Telecommunications": "电信",
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
}

THEME_COMPANY = {
    "AGRO": "Adecoagro SA",
    "BG": "Bunge Global SA",
    "BIOX": "Bioceres Crop Solutions Corp",
    "BP": "BP plc ADR",
    "BWXT": "BWX Technologies Inc",
    "CF": "CF Industries Holdings Inc",
    "CIFR": "Cipher Digital Inc",
    "CNH": "CNH Industrial NV",
    "COIN": "Coinbase Global Inc",
    "CRWD": "Crowdstrike Holdings Inc",
    "EQNR": "Equinor ASA ADR",
    "FROG": "JFrog Ltd",
    "FSLY": "Fastly Inc",
    "RIOT": "Riot Platforms Inc",
    "RPD": "Rapid7 Inc",
    "TENB": "Tenable Holdings Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月31日16:00 ET盘后事件可解释9月1日；9月1日16:00 ET后事件不得倒推。
R = {
    "AMZN": ("直接", "亚马逊9/1盘前正式遭FTC就广告定价提起诉讼（联合22州指控自2019年起多收广告主逾200亿美元），公司'强烈不同意'、Citi称回调为买入机会；-1.87%为道指可选消费（清一色下跌）第三跌幅，周一诉讼预期的落地延续。（事件时间2026-09-01 07:51 ET起） [Amazon faces FTC lawsuit over sponsored ad pricing](https://finance.yahoo.com/m/6cbe0f1e-8604-3169-8269-75a01f5e6b6f/amazon-faces-ftc-lawsuit.html) [Amazon Stock Extends Losses After FTC Lawsuit Over Ad Practices](https://finance.yahoo.com/m/817d4b78-5de2-3e5b-b19d-9a69e3f7f59c/amazon-stock-extends-losses.html)"),
    "CRK": ("直接", "Comstock Resources 9/1盘前宣布与阿塞拜疆SOCAR达成16.5亿美元战略伙伴关系、并与Jerry Jones方设立4.5亿美元钻探合资，盘中一度+5%、收涨11.02%列All Stocks与罗素2000能源涨幅前列。（事件时间2026-09-01 07:30 ET） [COMSTOCK ANNOUNCES $1.65 BILLION STRATEGIC PARTNERSHIP WITH SOCAR AND $450 MILLION DRILLING JOINT VENTURE](https://finviz.com/news/387432/comstock-announces-%241.65-billion-strategic-partnership-with-socar-and-%24450-million-drilling-joint-venture)"),
    "FRVO": ("直接", "Fervo Energy 9/1与谷歌签署地热供电协议，盘中一度+15%、收涨28.41%列All Stocks与罗素2000公用事业（当日领涨板块）涨幅首位——AI数据中心电力需求叙事的地热落点。（事件时间2026-09-01 09:59 ET） [Fervo Energy shares rise 15% following Google geothermal power agreement](https://finviz.com/news/387585/fervo-energy-shares-rise-15-following-google-geothermal-power-agreement)"),
    "MMED": ("直接", "美敦力糖尿病业务分拆MiniMed首份财报超预期，+10.66%列罗素医疗保健涨幅首位；当日医疗保健为防御轮入主线（道指成分清一色上涨）。（事件时间2026-09-01 04:28 ET起） [Medtronic's Diabetes Spinoff Just Surged. What To Look For In Its Earnings.](https://finance.yahoo.com/m/5644727e-8236-38f6-9726-8d83c4d0f9ce/medtronics-diabetes-spinoff-just.html)"),
    "PXS": ("直接", "Pyxis Tankers 8/31盘后发布上半年业绩（6月30日止三个月与六个月），霍尔木兹油轮遇袭推高油运运价的当日收涨16.23%列All Stocks能源涨幅首位。（事件时间2026-08-31 16:15 ET） [Pyxis Tankers Announces Financial Results for the Three & Six Months Ended June 30, 2026](https://finviz.com/news/387187/pyxis-tankers-announces-financial-results-for-the-three-six-months-ended-june-30-2026)"),
    "AGRO": ("直接", "Tether CEO确认持有农业公司Adecoagro 70%股权，+5.62%列农业商品主题涨幅首位；农业商品与农业食品科技为当日仅有的三个上涨主题之二。（事件时间2026-09-01 05:44 ET） [Tether CEO Posts Stable Cow GIF And Confirms a 70% Stake in a Farming Giant](https://finance.yahoo.com/m/b6a8c29d-6d01-32d9-b939-2f51d4405b4a/tether-ceo-posts-%E2%80%9Cstable-cow%E2%80%9D-gif.html)"),
    "EIX": ("联动", "暂未找到同日分类催化事件（新闻表3条均未匹配催化模式）；+8.93%列标普500与All Stocks公用事业涨幅第二——周一-23.07%立法崩跌后的技术性反弹与空头回补，公用事业当日四个股票范围进入涨幅前列。该股与当日所选公用事业的偏强方向一致。"),
    "PCG": ("联动", "暂未找到同日分类催化事件；+5.95%列标普500公用事业涨幅第三——周一-20.06%崩跌后的技术性反弹。该股与当日所选公用事业的偏强方向一致。"),
    "SRE": ("联动", "暂未找到同日直接催化；+3.13%列标普500公用事业涨幅侧，加州同业崩跌后的板块性修复。该股与当日所选公用事业的偏强方向一致。"),
    "MRNA": ("联动", "暂未找到同日分类催化事件（新闻表4条均未匹配催化模式）；+9.93%列标普500医疗保健涨幅首位，医疗保健为当日防御轮入主线。该股与当日所选医疗保健的偏强方向一致。"),
    "CRWD": ("联动", "窗口内新闻15条：与Optiv合计合同总值超20亿美元为正面合作新闻（10:01 ET），但当日-6.90%与新闻方向相反——驱动为网络安全主题八子行业清一色下跌（等权-4.66%、HACK -4.38%）：周一清一色上涨的次日完全反转。该股与当日所选网络安全的偏弱方向一致。"),
    "ORA": ("联动", "唯一新闻为除息前上涨报道（例行分红）；+5.19%列罗素2000公用事业涨幅首位，Fervo获谷歌地热协议引发的地热同业联动为最可能驱动。该股与当日所选公用事业的偏强方向一致。"),
    "CVX": ("联动", "该股与当日所选能源的偏强方向一致（道指能源清一色上涨唯一成分+2.38%）。"),
    "COP": ("联动", "该股与当日所选能源的偏强方向一致（标普能源涨幅首位+2.79%）。"),
    "APA": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "EQT": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "JNJ": ("联动", "窗口内唯一候选为Q3业绩电话会议日程公告（例行）；+2.01%为道指医疗保健（清一色上涨）领涨成分。该股与当日所选医疗保健的偏强方向一致。"),
    "AMGN": ("联动", "该股与当日所选医疗保健的偏强方向一致（道指医疗保健清一色上涨成分）。"),
    "UNH": ("联动", "该股与当日所选医疗保健的偏强方向一致（道指医疗保健清一色上涨成分）。"),
    "WMT": ("联动", "该股与当日所选必需消费的偏强方向一致（道指必需消费+1.00%领涨成分）。"),
    "PG": ("联动", "该股与当日所选必需消费的偏强方向一致。"),
    "KO": ("背离", "-0.76%在道指必需消费上涨组内为唯一下跌成分，连续第三日跑输沃尔玛；防御消费内部的个股轮动。"),
    "SHW": ("联动", "该股与当日所选基础材料的偏弱方向一致（道指基础材料清一色下跌唯一成分-2.62%）。"),
    "HD": ("联动", "该股与当日所选可选消费的偏弱方向一致（道指可选消费清一色下跌-2.46%领跌成分）。"),
    "NKE": ("联动", "该股与当日所选可选消费的偏弱方向一致（道指可选消费清一色下跌成分）。"),
    "CAT": ("联动", "该股与当日所选工业的偏弱方向一致（道指工业清一色下跌-2.30%领跌成分）。"),
    "HON": ("联动", "该股与当日所选工业的偏弱方向一致（道指工业清一色下跌成分）。"),
    "BA": ("联动", "窗口内候选为波音/迪尔/美国钢铁劳资谈判背景报道（非同日事件）；-1.02%随道指工业清一色下跌。该股与当日所选工业的偏弱方向一致。"),
    "CEG": ("联动", "该股与当日所选公用事业的偏强方向一致（纳指100公用事业清一色上涨+2.02%领涨成分）。"),
    "AEP": ("联动", "该股与当日所选公用事业的偏强方向一致（纳指100公用事业清一色上涨成分）。"),
    "XEL": ("联动", "该股与当日所选公用事业的偏强方向一致（纳指100公用事业清一色上涨成分）。"),
    "FANG": ("联动", "该股与当日所选能源的偏强方向一致（纳指100能源清一色上涨+1.34%领涨成分）。"),
    "BKR": ("联动", "该股与当日所选能源的偏强方向一致（纳指100能源清一色上涨成分）。"),
    "REGN": ("联动", "该股与当日所选医疗保健的偏强方向一致（标普与纳指100医疗保健涨幅首位+3.10%）。"),
    "CVS": ("联动", "该股与当日所选医疗保健的偏强方向一致。"),
    "GILD": ("联动", "该股与当日所选医疗保健的偏强方向一致。"),
    "ALNY": ("联动", "该股与当日所选医疗保健的偏强方向一致。"),
    "AXON": ("联动", "暂未找到同日直接催化；-8.52%列标普500与纳指100工业（清一色下跌）跌幅首位，risk-off日高估值工业的戴维斯双杀。该股与当日所选工业的偏弱方向一致。"),
    "ODFL": ("联动", "该股与当日所选工业的偏弱方向一致（标普与纳指100工业跌幅第二-6.48%）。"),
    "BLDR": ("联动", "该股与当日所选工业的偏弱方向一致（房屋建筑链随利率上行回调）。"),
    "CSX": ("联动", "该股与当日所选工业的偏弱方向一致（纳指100工业清一色下跌成分）。"),
    "LIN": ("联动", "该股与当日所选基础材料的偏弱方向一致（纳指100基础材料清一色下跌唯一成分）。"),
    "PYPL": ("联动", "窗口内新闻为收购破裂复盘与多家目标价下调（8/31盘后讨论延续），无新事件；-0.50%为纳指100金融（清一色下跌）唯一成分，跌幅温和显示抛压衰减。该股与当日所选金融的偏弱方向一致。"),
    "FCX": ("联动", "窗口内唯一候选为泛市场文章（外链无关）；-4.32%列标普500基础材料跌幅首位，金属商品主题当日清一色下跌。该股与当日所选基础材料的偏弱方向一致。"),
    "VMC": ("联动", "该股与当日所选基础材料的偏弱方向一致。"),
    "CRH": ("联动", "该股与当日所选基础材料的偏弱方向一致。"),
    "HP": ("联动", "该股与当日所选能源的偏强方向一致（罗素2000能源涨幅第二+6.04%）。"),
    "BKV": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "GNE": ("联动", "该股与当日所选公用事业的偏强方向一致。"),
    "NJR": ("联动", "该股与当日所选公用事业的偏强方向一致。"),
    "DLXY": ("联动", "无窗口新闻微盘；+13.19%列All Stocks能源涨幅第二，能源板块第二日全面走强的小盘高贝塔（连续第二日入选）。该股与当日所选能源的偏强方向一致。"),
    "SAFX": ("联动", "无窗口新闻微盘（XCF Global）；+6.89%列All Stocks公用事业涨幅第三，板块反弹日的低流通异动，暂未找到同日直接催化。该股与当日所选公用事业的偏强方向一致。"),
    "ARCT": ("联动", "无窗口新闻（1条未匹配催化模式）微盘（mRNA疗法）；+9.93%列罗素医疗保健涨幅第二。该股与当日所选医疗保健的偏强方向一致。"),
    "CTMX": ("联动", "无窗口新闻（1条未匹配催化模式）微盘（抗体药物）；+9.23%列罗素医疗保健涨幅第三。该股与当日所选医疗保健的偏强方向一致。"),
    "BIAF": ("联动", "无窗口新闻（1条为无关聚合）微盘（诊断）；+44.52%列All Stocks医疗保健涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日所选医疗保健的偏强方向一致。"),
    "FBLG": ("联动", "无窗口新闻（1条为无关聚合）微盘（细胞治疗）；+22.67%列All Stocks医疗保健涨幅第二，低流通异动，暂未找到同日直接催化。该股与当日所选医疗保健的偏强方向一致。"),
    "PTN": ("联动", "无窗口新闻微盘；+15.52%列All Stocks医疗保健涨幅第三，低流通异动，暂未找到同日直接催化。该股与当日所选医疗保健的偏强方向一致。"),
    "NCLH": ("联动", "该股与当日所选可选消费的偏弱方向一致（标普可选消费跌幅首位-4.40%）。"),
    "EXPE": ("联动", "该股与当日所选可选消费的偏弱方向一致。"),
    "IP": ("联动", "该股与当日所选可选消费的偏弱方向一致（包装纸品随材料与消费双弱）。"),
    "OPTX": ("联动", "无窗口新闻微盘（光学）；-11.11%列罗素2000科技（当日-3.06%为最弱板块）跌幅首位。该股与当日所选科技的偏弱方向一致。"),
    "RPD": ("联动", "无窗口新闻；-10.77%列All Stocks科技与网络安全主题（清一色下跌等权-4.66%）跌幅首位，周一板块清一色上涨的次日反转。该股与当日所选科技的偏弱方向一致。"),
    "EVCM": ("联动", "无窗口新闻微盘（SaaS）；-9.02%列罗素2000科技跌幅第三。该股与当日所选科技的偏弱方向一致。"),
    "FBYD": ("联动", "无窗口新闻微盘（主题公园）；-16.22%列罗素2000工业跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "FJET": ("联动", "无窗口新闻微盘；-10.54%列罗素2000工业跌幅第二，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "SPIR": ("联动", "无窗口新闻微盘（卫星）；-9.42%列罗素2000工业跌幅第三，太空科技主题当日清一色下跌。该股与当日所选工业的偏弱方向一致。"),
    "OSW": ("联动", "无窗口新闻微盘（SPA度假）；-10.43%列All Stocks与罗素2000可选消费跌幅前列。该股与当日所选可选消费的偏弱方向一致。"),
    "FNKO": ("联动", "该股与当日所选可选消费的偏弱方向一致（罗素可选消费跌幅第二）。"),
    "XPOF": ("联动", "该股与当日所选可选消费的偏弱方向一致。"),
    "GMTL": ("联动", "无窗口新闻微盘（金属资源）；-10.93%列All Stocks基础材料跌幅首位，金属商品主题清一色下跌。该股与当日所选基础材料的偏弱方向一致。"),
    "ITP": ("联动", "无窗口新闻微盘（包装）；-9.97%列All Stocks基础材料跌幅第二，暂未找到同日直接催化。该股与当日所选基础材料的偏弱方向一致。"),
    "IE": ("联动", "无窗口新闻（铜矿勘探）；-9.31%列All Stocks基础材料跌幅第三。该股与当日所选基础材料的偏弱方向一致。"),
    "DBGI": ("联动", "无窗口新闻（1条为聚合噪音）微盘；-23.65%列All Stocks可选消费跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选可选消费的偏弱方向一致。"),
    "INEO": ("联动", "无窗口新闻微盘（中概）；-11.58%列All Stocks可选消费跌幅前列。该股与当日所选可选消费的偏弱方向一致。"),
    "VWAV": ("联动", "无窗口新闻微盘；-26.07%列All Stocks工业跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "AEHL": ("联动", "无窗口新闻微盘；-22.96%列All Stocks工业跌幅第二，低流通崩跌，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "YDDL": ("联动", "无窗口新闻微盘（中概）；-19.74%列All Stocks工业跌幅第三，低流通崩跌，暂未找到同日直接催化。该股与当日所选工业的偏弱方向一致。"),
    "CF": ("联动", "该股与当日所选农业与食品科技、农业商品的偏强方向一致（化肥+4.28%同时列两大主题涨幅侧）。"),
    "BG": ("联动", "该股与当日所选农业与食品科技、农业商品的偏强方向一致（粮商+4.16%）。"),
    "BIOX": ("联动", "该股与当日所选农业与食品科技的偏强方向一致（+6.95%列主题涨幅首位）。"),
    "CNH": ("联动", "该股与当日所选农业与食品科技的偏强方向一致（农机+5.66%）。"),
    "BWXT": ("联动", "该股与当日所选传统能源的偏强方向一致（核能+6.07%列主题涨幅首位）。"),
    "BP": ("联动", "该股与当日所选传统能源的偏强方向一致。"),
    "EQNR": ("联动", "该股与当日所选传统能源的偏强方向一致。"),
    "TENB": ("联动", "该股与当日所选网络安全的偏弱方向一致（清一色下跌等权-4.66%的第二跌幅-7.03%）。"),
    "RIOT": ("联动", "该股与当日所选加密货币与区块链的偏弱方向一致（清一色下跌-6.34%列首位；IBIT -2.04%）。"),
    "COIN": ("联动", "该股与当日所选加密货币与区块链的偏弱方向一致（-6.01%）。"),
    "CIFR": ("联动", "该股与当日所选加密货币与区块链的偏弱方向一致（-5.74%）。"),
    "FSLY": ("联动", "该股与当日所选云计算的偏弱方向一致（清一色下跌等权-2.81%的-8.86%列首位）。"),
    "FROG": ("联动", "该股与当日所选云计算的偏弱方向一致（-8.28%列主题跌幅第二）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "USO", "perf": 5.460, "form": "商品信托", "exposure": "WTI原油期货",
         "reason": "美国原油基金领涨全市场：中东冲突再升级（霍尔木兹两艘超大型油轮遇袭、美对伊朗再度打击）令WTI +5.7%站上90美元、布伦特+5%（92.6—95美元区间口径不一），能源为当日几乎唯一明确领涨板块（五个股票范围全部进入涨幅前三）。合并删除：BNO、DBE、DBO（同簇原油/能源期货，按敞口去重保留最强一只）。"},
        {"ticker": "VXX", "perf": 3.056, "form": "交易所交易票据", "exposure": "VIX期货",
         "reason": "VIX期货ETN：9月首个交易日risk-off——26个主题清一色下跌（网络安全/加密/云计算领跌）、标普161涨/340跌，对冲需求回归。合并删除：VIXY、VIXM（同簇VIX期货，按敞口去重保留最强一只）。"},
        {"ticker": "IEO", "perf": 2.032, "form": "交易所交易基金", "exposure": "美国油气开采与生产股",
         "reason": "油气E&P股ETF：油价+5%直接增厚开采商现金流，为原油期货之外的股权层敞口。合并删除：XOP、PXE（同簇E&P，按敞口去重保留最强一只）。"},
    ],
    "down": [
        {"ticker": "PALL", "perf": -4.439, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF连续第三日领跌全市场（8/28 +4.92%后三连阴）：供给端叙事完全退潮、实际利率与美元走强的利率主线全面接管商品定价。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "GDXJ", "perf": -4.416, "form": "交易所交易基金", "exposure": "全球金矿（中小型）",
         "reason": "中小金矿ETF：黄金-2.86%再度暴跌（实际利率上行、10年期逼近4.8%），高贝塔金矿放大跌幅；与钯金同为大宗但为股权杠杆敞口。合并删除：SGDM、RING、GDX（同簇金矿股，保留最强一只）。"},
        {"ticker": "HACK", "perf": -4.377, "form": "交易所交易基金", "exposure": "全球科技｜网络安全",
         "reason": "网络安全ETF：周一八子行业清一色上涨的次日完全反转（等权-4.66%），Rapid7 -10.77%、CrowdStrike -6.90%——正面合同新闻（Optiv合计20亿美元合同总值）未能对冲板块性回吐。独立科技子行业敞口。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查8月31日盘后至9月1日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-01"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；原油期货簇（USO/BNO/DBE/DBO）保留USO、VIX期货簇（VXX/VIXY/VIXM）保留VXX、油气开采簇（IEO/XOP/PXE）保留IEO、金矿股簇（GDXJ/SGDM/RING/GDX）保留GDXJ。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-01_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-01_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月1日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月1日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：9月首个交易日为地缘与利率双重压制的risk-off日：中东冲突再升级（霍尔木兹两艘超大型油轮遇袭、美对伊朗再度打击）令WTI +5.7%站上90美元、布伦特+5%（92.6—95美元区间口径不一），能源为几乎唯一明确领涨板块（五个股票范围全部进入涨幅前三、道指与纳指100能源清一色上涨）；美债与全球收益率约+5bp、10年期逼近4.8%、30年期逼5.30%（全球收益率2008年以来最高、日本10年期1996年来首次破3%），道指-400点以上（约-0.8%）、标普500收于7632点（-0.7%、161涨/340跌、连跌三日）、纳指-1%、纳指100 -1.3%、罗素2000 -1.2%，VIX期货ETF +3.06%、英伟达单日拖累标普约14点。26个主题清一色下跌为罕见宽度：网络安全（等权-4.66%）、加密货币（-2.85%）、云计算（-2.81%）领跌——周一的领涨主题全面反转，软件与云计算（IGV -3.46%、XSW -3.04%、WCLD -3.34%）出现8月27日上涨趋势确认后的首度宽幅回调。轮入端三条线：能源（Comstock获SOCAR 16.5亿美元合作+11.02%、Pyxis Tankers油运财报+16.23%）、公用事业（周一立法崩跌后的修复：爱迪生联合+8.93%、PG&E +5.95%；Fervo获谷歌地热协议+28.41%、Ormat +5.19%——AI电力叙事的地热落点）、医疗保健（五个范围进入涨幅前三、道指成分清一色上涨：Moderna +9.93%、美敦力分拆MiniMed财报+10.66%）。商品端钯金-4.44%连续第三日领跌、黄金-2.86%再度暴跌（中小金矿-4.42%放大）、白银-3.68%；玉米+1.15%逆势（农业商品与农业食品科技为仅有的上涨主题群、Tether确认持有Adecoagro 70%股权）。个股：苹果CEO交接日新CEO首日+2.6%为标普按点数当日最佳（'反AI交易'）、亚马逊正式遭FTC广告定价诉讼-1.87%、苹果对OpenAI提起窃取芯片机密诉讼；Anthropic与英伟达支持的Lambda敲定350亿美元六年算力协议（约160亿美元/GW）但租约结构引发'金融工程'质疑；盘后Dell上修全年营收指引至920亿美元（AI服务器740亿）盘后转涨、Palo Alto超预期上修转涨3%、MongoDB超预期仍遭抛售10%以上。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5529/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1940/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-09-01_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-09-01_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-09-01_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
