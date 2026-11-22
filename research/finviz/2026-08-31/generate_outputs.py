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
    "Music": "音乐", "Video": "视频", "Gaming": "游戏",
    "DTC": "直面消费者", "Marketplaces": "交易平台", "Omnichannel": "全渠道零售", "Grocery": "食品杂货",
    "Gambling": "博彩", "Betting": "体育投注", "Ads & Media": "广告与媒体", "Social": "社交",
}

THEME_COMPANY = {
    "AMR": "Alpha Metallurgical Resources Inc",
    "BALY": "Ballys Corp",
    "BIOX": "Bioceres Crop Solutions Corp",
    "CRWD": "Crowdstrike Holdings Inc",
    "GENI": "Genius Sports Limited",
    "HYFM": "Hydrofarm Holdings Group Inc",
    "LSF": "Laird Superfood Inc",
    "METC": "Ramaco Resources Inc",
    "OKTA": "Okta Inc",
    "PINS": "Pinterest Inc",
    "RDDT": "Reddit Inc",
    "REAL": "The RealReal Inc",
    "SAIL": "Sailpoint Inc",
    "SLB": "SLB Ltd",
    "TTWO": "Take-Two Interactive Software Inc",
    "UBER": "Uber Technologies Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月28日16:00 ET盘后事件可解释8月31日；8月31日16:00 ET后事件不得倒推。
R = {
    "AMZN": ("直接", "亚马逊8/31午后遭FTC准备提起广告定价诉讼的报道冲击，且联邦贸易监管机构与22州指控其以秘密附加费收取200亿美元，当日创逾一个月最大跌幅、收跌2.50%，为道指可选消费（清一色下跌）领跌成分。（事件时间2026-08-31 14:51 ET起） [Amazon stock falls as FTC prepares ad-pricing lawsuit](https://finance.yahoo.com/m/1859590e-707c-340a-83ea-fc5765034024/amazon-stock-falls-as-ftc.html) [US trade regulator and 22 states accuse Amazon of taking $20bn with secret surcharges](https://finance.yahoo.com/economy/policy/articles/us-trade-regulator-22-states-194152421.html)"),
    "HLF": ("直接", "Herbalife 8/31盘前宣布计划中的CEO交接并重申Q3与全年2026指引，市场对换帅定价负面，收跌11.59%列罗素必需消费跌幅首位。（事件时间2026-08-31 06:50 ET） [Herbalife Announces Planned CEO Transition](https://finviz.com/news/386753/herbalife-announces-planned-ceo-transition) [Herbalife Reaffirms Third Quarter and Full Year 2026 Guidance](https://www.businesswire.com/news/home/20260831893738/en/)"),
    "KPTI": ("直接", "Karyopharm 8/31盘前宣布向FDA提交XPOVIO（selinexor）联合ruxolitinib治疗骨髓纤维化的补充新药申请（sNDA），收涨10.16%列罗素医疗保健涨幅首位。（事件时间2026-08-31 07:30 ET） [Karyopharm Submits Supplemental New Drug Application to the FDA for XPOVIO Plus Ruxolitinib](https://finviz.com/news/386791/karyopharm-submits-supplemental-new-drug-application-to-the-fda-for-xpovio-selinexor-plus-ruxolitinib-for-patients-with-myelofibrosis)"),
    "SLB": ("直接", "SLB 8/31盘前宣布收购Kelvion以扩张数据中心基础设施业务，收涨4.83%列标普500能源涨幅首位，与当日能源板块全面领涨（美伊冲突推高油价）共振，并现身传统能源主题涨幅前列。（事件时间2026-08-31 06:50 ET） [SLB to Acquire Kelvion, Expanding its Role Across Data Center Infrastructure](https://finviz.com/news/386754/slb-to-acquire-kelvion-expanding-its-role-across-data-center-infrastructure)"),
    "NVDA": ("直接", "英伟达8/31宣布以35亿美元可转债投资联发科、深化十年期AI芯片合作并开放NVLink Fusion生态（黄仁勋：双方独立且盈利），收涨1.49%为道指科技成分涨幅首位。（事件时间2026-08-31 09:43 ET起） [Nvidia investing $3.5 billion in MediaTek for AI chip partnership](https://finance.yahoo.com/m/af4ede93-efe2-3abe-98bb-55cefac4083e/nvidia-investing-%243.5-billion.html) [Nvidia Makes MediaTek Partnership Even Bigger, Huang Says](https://finance.yahoo.com/video/nvidia-makes-mediatek-partnership-even-134345562.html)"),
    "PINS": ("直接", "Pinterest CFO Julia Donnelly辞职（8/28盘后公告、落在研究窗口内），8/31收跌6.38%，列社交媒体与电子商务两大主题跌幅前列。（事件时间2026-08-28 16:56 ET） [Pinterest stock dips as CFO Julia Donnelly resigns](https://finance.yahoo.com/markets/stocks/articles/pinterest-stock-falls-cfo-julia-205613233.html) [Pinterest CFO exit puts spotlight on growth](https://finance.yahoo.com/m/d1ec9575-6e94-348c-be57-c8b8615ae9cd/pinterest-cfo-exit-puts.html)"),
    "EIX": ("直接", "爱迪生联合（EIX）-23.07%列标普500与All Stocks公用事业跌幅首位、创2001年以来最大单日跌幅：加州野火基金立法最终未纳入公用事业责任保护条款，至少三家券商下调评级。Finviz行情页新闻表无条目（源缺口），经彭博节目字幕交叉核验确认立法事件。该股与当日所选公用事业的偏弱方向一致。"),
    "PCG": ("直接", "PG&E（PCG）-20.06%列标普500与All Stocks公用事业跌幅第二、2020年以来最差单日：加州野火基金立法未纳入公用事业责任保护、遭多家券商下调评级，与爱迪生联合同日崩跌。Finviz新闻表无条目（源缺口），经彭博节目字幕交叉核验确认。该股与当日所选公用事业的偏弱方向一致。"),
    "PYPL": ("联动", "窗口内无新公司事件，上周五Stripe/Advent放弃逾500亿美元收购的延续消化；当日-1.85%为纳指100金融唯一成分、清一色下跌领跌。该股与当日所选金融的偏弱方向一致。"),
    "GOOGL": ("联动", "窗口内新闻35条经核验无同日直接事件（候选多为亚马逊FTC诉讼页外链与OpenAI广告收入10亿美元的竞争压力报道）；-2.09%与通信服务板块三个范围进入跌幅前列一致——周五领涨主线的反转。该股与当日所选通信服务的偏弱方向一致。"),
    "TTWO": ("联动", "窗口内无同日直接事件；-6.67%列标普500与纳指100通信服务、社交媒体与数字娱乐主题跌幅首位，周五反弹主题的集中回吐。该股与当日所选通信服务的偏弱方向一致。"),
    "CRWD": ("联动", "Finviz新闻表无条目，经彭博收盘节目字幕交叉核验：与CLEAR战略合作（CLEAR One身份平台集成Falcon风险检测）且上周财报大超预期后连涨，+6%创纪录收盘，列网络安全主题（清一色上涨）领涨个股。该股与当日所选网络安全、科技的偏强方向一致。"),
    "SNDK": ("联动", "窗口内无同日直接事件；存储链延续上周财报行情强势（美光财报临近），+5.50%列标普500科技涨幅第二。该股与当日所选科技的偏强方向一致。"),
    "QCOM": ("联动", "窗口内无同日直接事件（候选为博通毛利率与英特尔相关外链报道）；+3.83%列标普500科技涨幅第三，科技板块反弹日。该股与当日所选科技的偏强方向一致。"),
    "OKTA": ("联动", "窗口内新闻表无Okta自身新事件；+4.10%列网络安全主题（清一色上涨）第二位，Palo Alto与Okta收购谈判报道的延续发酵为最可能驱动（延续性因素）。该股与当日所选网络安全的偏强方向一致。"),
    "WMT": ("联动", "窗口内新闻3条经核验无同日重要事件（DOJ鸦片类处方5000万美元和解金额不具重要性）；+1.73%列标普500必需消费涨幅第二、道指必需消费第一。该股与当日所选必需消费的偏强方向一致。"),
    "CVX": ("联动", "窗口内无同日直接事件（候选为埃克森美孚编辑性外链）；+2.12%为道指能源清一色上涨的唯一成分领涨。该股与当日所选能源的偏强方向一致。"),
    "XOM": ("联动", "窗口内无同日直接事件（候选为编辑性文章外链）；+2.71%列标普500能源涨幅第三，原油+3%驱动板块整体走强。该股与当日所选能源的偏强方向一致。"),
    "TPL": ("联动", "窗口内无同日直接事件；+2.73%列标普500能源涨幅第二，能源板块日的二线油气资产表现。该股与当日所选能源的偏强方向一致。"),
    "NKE": ("联动", "窗口内唯一候选为财报日期公告（例行）；-1.36%为道指可选消费（当日清一色下跌）第二跌幅，周五领涨板块的反转。该股与当日所选可选消费的偏弱方向一致。"),
    "HD": ("联动", "窗口内无同日直接事件；-0.72%为道指可选消费（清一色下跌）成分。该股与当日所选可选消费的偏弱方向一致。"),
    "DIS": ("联动", "窗口内无同日直接事件；-0.51%为道指通信服务（清一色下跌）成分。该股与当日所选通信服务的偏弱方向一致。"),
    "CRM": ("联动", "窗口内候选均为泛软件财报点评（外链），无Salesforce自身事件；+0.60%为道指科技成分涨幅第二。该股与当日所选科技的偏强方向一致。"),
    "CSCO": ("联动", "窗口内无同日直接事件；+0.51%为道指科技成分涨幅第三。该股与当日所选科技的偏强方向一致。"),
    "KO": ("背离", "窗口内无新闻条目；-1.10%在道指必需消费上涨组内为唯一下跌成分，防御消费内部个股轮动（沃尔玛强、可口可乐弱）。"),
    "PG": ("联动", "窗口内无同日直接事件；+0.93%为道指必需消费上涨成分。该股与当日所选必需消费的偏强方向一致。"),
    "DG": ("联动", "窗口内无同日直接事件（9/2财报临近）；+3.14%列标普500必需消费涨幅首位。该股与当日所选必需消费的偏强方向一致。"),
    "HRL": ("联动", "窗口内无同日直接事件；+1.30%列标普500必需消费涨幅第三。该股与当日所选必需消费的偏强方向一致。"),
    "HWM": ("联动", "窗口内无同日直接事件；-7.51%列标普500工业跌幅首位，航空航天链回调。该股与当日所选工业的偏弱方向一致。"),
    "AXON": ("联动", "窗口内无同日直接事件；-5.69%列标普500工业跌幅第二。该股与当日所选工业的偏弱方向一致。"),
    "TXT": ("联动", "窗口内无同日直接事件；-2.99%列标普500工业跌幅第三。该股与当日所选工业的偏弱方向一致。"),
    "SRE": ("联动", "窗口内无同日直接事件；-3.10%列标普500公用事业跌幅第三，加州双雄崩跌外的同板块压制。该股与当日所选公用事业的偏弱方向一致。"),
    "BKR": ("联动", "窗口内无同日直接事件；+1.83%列纳指100能源（清一色上涨）领涨。该股与当日所选能源的偏强方向一致。"),
    "FANG": ("联动", "窗口内无同日直接事件；+1.42%列纳指100能源（清一色上涨）成分。该股与当日所选能源的偏强方向一致。"),
    "LIN": ("联动", "窗口内无同日直接事件；+0.01%为纳指100基础材料清一色上涨唯一成分、微涨入选。该股与当日所选基础材料的偏强方向一致。"),
    "SPCX": ("联动", "窗口内无同日直接事件（候选为苹果CEO交接与OpenAI-Cursor外链报道）；+1.55%列纳指100工业涨幅首位。该股与当日所选工业的偏强方向一致。"),
    "TRI": ("联动", "窗口内无同日直接事件；+1.03%列纳指100工业涨幅第二。该股与当日所选工业的偏强方向一致。"),
    "ODFL": ("联动", "窗口内无同日直接事件；+0.67%列纳指100工业涨幅第三。该股与当日所选工业的偏强方向一致。"),
    "XEL": ("联动", "窗口内无同日直接事件；-0.99%列纳指100公用事业跌幅首位。该股与当日所选公用事业的偏弱方向一致。"),
    "CEG": ("联动", "窗口内无同日直接事件；-0.72%列纳指100公用事业跌幅第二。该股与当日所选公用事业的偏弱方向一致。"),
    "EXC": ("联动", "窗口内无同日直接事件；-0.48%列纳指100公用事业跌幅第三。该股与当日所选公用事业的偏弱方向一致。"),
    "SOC": ("联动", "窗口内无同日直接事件；+7.57%列All Stocks与罗素2000能源涨幅首位，美伊冲突推高油价日的小盘油气高贝塔。该股与当日所选能源的偏强方向一致。"),
    "WTI": ("联动", "窗口内无同日直接事件；+3.92%列罗素2000能源涨幅第二。该股与当日所选能源的偏强方向一致。"),
    "VTOL": ("联动", "窗口内无同日直接事件；+3.80%列罗素2000能源涨幅第三（近海直升机服务）。该股与当日所选能源的偏强方向一致。"),
    "GPRK": ("联动", "无窗口内公司事件；+11.90%列All Stocks能源涨幅首位，原油+3%日的小盘油商高贝塔。该股与当日所选能源的偏强方向一致。"),
    "DLXY": ("联动", "无窗口内公司事件；+8.51%列All Stocks能源涨幅第二，板块日个体表现。该股与当日所选能源的偏强方向一致。"),
    "GPRO": ("联动", "无窗口内公司事件。零窗口新闻微盘，+46.06%为低流通动量异动，暂未找到同日直接催化。该股与当日所选科技的偏强方向一致。"),
    "TP": ("联动", "无窗口内公司事件。零窗口新闻微盘，+30.91%为低流通动量，暂未找到同日直接催化。该股与当日所选科技的偏强方向一致。"),
    "DPRO": ("联动", "无窗口内公司事件。零窗口新闻微盘（无人机概念），+21.39%为低流通动量，暂未找到同日直接催化。该股与当日所选科技的偏强方向一致。"),
    "NCRA": ("联动", "无窗口内公司事件。零窗口新闻微盘，+49.74%为低流通动量，暂未找到同日直接催化。该股与当日所选必需消费的偏强方向一致。"),
    "COOT": ("联动", "无窗口内公司事件。零窗口新闻微盘，+28.87%为低流通动量，暂未找到同日直接催化。该股与当日所选必需消费的偏强方向一致。"),
    "FAMI": ("联动", "无窗口内公司事件。零窗口新闻微盘（中概），+17.82%为低流通动量，暂未找到同日直接催化。该股与当日所选必需消费的偏强方向一致。"),
    "FNGR": ("联动", "无窗口内公司事件。零窗口新闻微盘（中概），-43.97%为低流通崩跌（此前8/27已现无解释异动并如实记录），暂未找到同日直接催化。该股与当日所选通信服务的偏弱方向一致。"),
    "GCL": ("联动", "无窗口内公司事件。零窗口新闻微盘（中概），-26.27%为低流通崩跌，暂未找到同日直接催化。该股与当日所选通信服务的偏弱方向一致。"),
    "AENT": ("联动", "无窗口内公司事件。零窗口新闻微盘，-10.75%列All Stocks通信服务跌幅第三。该股与当日所选通信服务的偏弱方向一致。"),
    "WAVE": ("联动", "无窗口内公司事件。零窗口新闻微盘（波浪发电），-7.58%列All Stocks公用事业跌幅第三。该股与当日所选公用事业的偏弱方向一致。"),
    "WHLR": ("联动", "无窗口内公司事件。零窗口新闻微盘REIT，-36.45%列All Stocks房地产跌幅首位，暂未找到同日直接催化。该股与当日所选房地产的偏弱方向一致。"),
    "DUO": ("联动", "无窗口内公司事件。零窗口新闻微盘（中概地产平台），-20.85%列All Stocks房地产跌幅第二，暂未找到同日直接催化。该股与当日所选房地产的偏弱方向一致。"),
    "GIPR": ("联动", "无窗口内公司事件。零窗口新闻微盘REIT，-13.97%列All Stocks房地产跌幅第三。该股与当日所选房地产的偏弱方向一致。"),
    "WYFI": ("联动", "无窗口内公司事件。零窗口新闻微盘（碳纤维），+6.59%列罗素2000科技涨幅第二。该股与当日所选科技的偏强方向一致。"),
    "WOLF": ("联动", "无窗口内公司事件。零窗口新闻（碳化硅），+6.00%列罗素2000科技涨幅第三，科技反弹日修复。该股与当日所选科技的偏强方向一致。"),
    "NAUT": ("联动", "无窗口内公司事件。零窗口新闻微盘，+9.79%列罗素医疗保健涨幅第二。该股与当日所选医疗保健的偏强方向一致。"),
    "CDXS": ("联动", "无窗口内公司事件。零窗口新闻微盘（酶工程），+6.92%列罗素医疗保健涨幅第三。该股与当日所选医疗保健的偏强方向一致。"),
    "TRON": ("联动", "无窗口内公司事件。零窗口新闻微盘，-15.87%列罗素可选消费跌幅首位。该股与当日所选可选消费的偏弱方向一致。"),
    "LIND": ("联动", "无窗口内公司事件。零窗口新闻（探险旅游），-10.24%列罗素可选消费跌幅第二。该股与当日所选可选消费的偏弱方向一致。"),
    "LVWR": ("联动", "无窗口内公司事件。零窗口新闻（哈雷电动），-9.63%列罗素可选消费跌幅第三。该股与当日所选可选消费的偏弱方向一致。"),
    "REAX": ("联动", "无窗口内公司事件。零窗口新闻微盘（地产经纪），-10.01%列罗素房地产跌幅首位。该股与当日所选房地产的偏弱方向一致。"),
    "CLDT": ("联动", "无窗口内公司事件。零窗口新闻（酒店REIT），-4.68%列罗素房地产跌幅第二。该股与当日所选房地产的偏弱方向一致。"),
    "CWK": ("联动", "无窗口内公司事件。零窗口新闻（商业地产服务），-4.46%列罗素房地产跌幅第三。该股与当日所选房地产的偏弱方向一致。"),
    "COCO": ("联动", "无窗口内公司事件。零窗口新闻微盘（椰子水），-4.85%列罗素必需消费跌幅第二。该股与当日所选必需消费的偏弱方向一致。"),
    "BRCC": ("联动", "无窗口内公司事件。零窗口新闻微盘（咖啡），-4.74%列罗素必需消费跌幅第三。该股与当日所选必需消费的偏弱方向一致。"),
    "SAIL": ("联动", "窗口内无同日直接事件；+3.68%列网络安全主题（清一色上涨）涨幅第三，板块并购叙事延续。该股与当日所选网络安全的偏强方向一致。"),
    "HYFM": ("联动", "无窗口内公司事件；+9.15%列农业与食品科技主题涨幅首位，农业商品强势延续。该股与当日所选农业与食品科技的偏强方向一致。"),
    "LSF": ("联动", "无窗口内公司事件；+6.38%列农业与食品科技主题涨幅第二。该股与当日所选农业与食品科技的偏强方向一致。"),
    "BIOX": ("联动", "无窗口内公司事件；+4.88%列农业与食品科技主题涨幅第三。该股与当日所选农业与食品科技的偏强方向一致。"),
    "METC": ("联动", "无窗口内公司事件；+7.07%列传统能源主题涨幅首位（焦煤），煤炭随能源板块走强。该股与当日所选传统能源的偏强方向一致。"),
    "AMR": ("联动", "无窗口内公司事件；+4.19%列传统能源主题涨幅第三（焦煤）。该股与当日所选传统能源的偏强方向一致。"),
    "RDDT": ("联动", "无窗口内公司事件；-3.39%列社交媒体主题跌幅第三。该股与当日所选社交媒体的偏弱方向一致。"),
    "GENI": ("联动", "无窗口内公司事件；-7.48%列数字娱乐主题跌幅首位（体育数据）。该股与当日所选数字娱乐的偏弱方向一致。"),
    "BALY": ("联动", "无窗口内公司事件；-4.98%列数字娱乐主题跌幅第三（博彩）。该股与当日所选数字娱乐的偏弱方向一致。"),
    "REAL": ("联动", "无窗口内公司事件；-6.31%列电子商务主题跌幅第二（二手奢侈品）。该股与当日所选电子商务的偏弱方向一致。"),
    "UBER": ("联动", "无窗口内公司事件；-4.02%列电子商务主题跌幅第三。该股与当日所选电子商务的偏弱方向一致。"),
    "APP": ("联动", "无窗口内公司事件；-1.79%列纳指100通信服务（清一色下跌）跌幅第三。该股与当日所选通信服务的偏弱方向一致。"),
    "SHW": ("联动", "无窗口内公司事件；-1.75%为道指基础材料（清一色下跌）唯一成分。该股与当日所选基础材料的偏弱方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "USO", "perf": 3.084, "form": "商品信托", "exposure": "WTI原油期货",
         "reason": "美国原油基金领涨全市场：美伊约一个月来首次互袭，布伦特+3%重上91美元、WTI站上90美元，能源为当日唯一全面领涨板块。合并删除：DBO、BNO、DBE（同簇原油/能源期货，按敞口去重保留最强一只）。"},
        {"ticker": "OIH", "perf": 2.599, "form": "交易所交易基金", "exposure": "全球能源｜油服设备",
         "reason": "VanEck油服ETF：油价跳升与SLB收购Kelvion扩张数据中心基础设施共同点燃油服链，与原油期货为不同资产层（公司现金流对油价与资本开支的杠杆）。合并删除：IEZ（iShares油服设备、同簇，保留更强一只）。"},
        {"ticker": "FENY", "perf": 2.073, "form": "交易所交易基金", "exposure": "美国能源板块宽基",
         "reason": "富达能源板块指数ETF：五个股票范围能源全部进入涨幅前三、道指与纳指100能源清一色上涨，板块市值篮（含大型油气）为第三层次敞口。合并删除：PXI（能源动量、同簇因子重叠，保留更强一只）。"},
    ],
    "down": [
        {"ticker": "PALL", "perf": -3.916, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF领跌全市场：上周五+4.92%（全市场最强）的供给驱动独涨当日全数回吐，供给端逻辑退潮、资金回流利率主线，两日极端分化显示商品内部分化由单一叙事驱动。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "TAN", "perf": -2.220, "form": "交易所交易基金", "exposure": "全球能源｜太阳能",
         "reason": "太阳能ETF：利率重定价延续（10年期收益率破4.75%为2025年1月以来最高）直接打击资本密集型清洁能源，与加州公用事业崩跌同向。独立敞口（太阳能设备链）与原油、钯金不构成重复。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "PGJ", "perf": -2.211, "form": "交易所交易基金", "exposure": "中国股票",
         "reason": "中国股票ETF：中概整体承压（通信服务与房地产跌幅前列的多只中概微盘为佐证），独立地域敞口。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查8月28日盘后至31日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-08-31"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；原油期货簇（USO/DBO/BNO/DBE）保留USO、油服簇（OIH/IEZ）保留OIH、能源宽基簇（FENY/PXI）保留FENY。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-08-31_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-31_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月31日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月31日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：上周五Warsh在Jackson Hole鹰派演讲后的第一个交易日兼8月收官日，股债延续双跌：10年期收益率升破4.75%（2025年1月以来最高），9月加息定价维持在约五至六成（盘前一度62%、收盘口径约五五开）。当日最大驱动为美伊约一个月来首次互袭——布伦特+3%重上91美元、WTI站上90美元，能源成为五个股票范围全部进入涨幅前二的唯一板块（道指与纳指100能源清一色上涨：雪佛龙、贝克休斯、Diamondback），油服设备（OIH +2.60%）与原油期货（USO +3.08%）占据ETF涨幅前二。公用事业遭加州野火立法未纳入责任保护的重击：PG&E -20.06%（2020年以来最差）、爱迪生联合 -23.07%（2001年以来最大跌幅）、至少三家券商下调评级。周五的领涨主线完全反转：可选消费与通信服务双双领跌（道指两板块清一色下跌；亚马逊遭FTC与22州秘密附加费指控 -2.50%、Take-Two -6.67%、谷歌 -2.09%、Pinterest CFO辞职 -6.38%），通信服务四个范围进入跌幅前列。科技内部结构切换：标普科技进入涨幅侧（CrowdStrike +5.77%、SanDisk +5.50%、高通 +3.83%；英伟达宣布35亿美元投资联发科 +1.49%），网络安全主题八子行业清一色上涨；罗素医疗保健反弹（Karyopharm FDA提交sNDA +10.16%）。商品端钯金-3.92%领跌（回吐周五全部涨幅）、太阳能 -2.22%与中概 -2.21%居后；房地产四个范围中的两个进入跌幅前三。个股无解释异动：GoPro +46.06%、FingerMotion -43.97%等微盘。", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5529/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1940/1943、Themes 268/268和ETF 658/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-31_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-31_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-31_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
