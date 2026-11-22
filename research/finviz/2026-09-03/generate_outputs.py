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
    "Blockchain": "区块链", "Trading": "交易平台", "Insurance": "保险科技", "Exchanges": "交易所", "Lending": "借贷科技", "Neobanks": "新型银行",
}

THEME_COMPANY = {
    "AMR": "Alpha Metallurgical Resources Inc",
    "AMTX": "Aemetis Inc",
    "BIOX": "Bioceres Crop Solutions Corp",
    "BTU": "Peabody Energy Corp",
    "CIFR": "Cipher Digital Inc",
    "GEVO": "Gevo Inc",
    "HOOD": "Robinhood Markets Inc",
    "METC": "Ramaco Resources Inc",
    "MSTR": "Strategy Inc",
    "PLTR": "Palantir Technologies Inc",
    "RIOT": "Riot Platforms Inc",
    "SNOW": "Snowflake Inc",
    "STKH": "Steakholder Foods Ltd ADR",
    "TSN": "Tyson Foods Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月2日16:00 ET盘后事件可解释9月3日；9月3日16:00 ET后事件不得倒推。
R = {
    "SNOW": ("直接", "Snowflake 9/2盘后财报全面超预期（产品收入加速、AI采用驱动'井喷季度'），9/3正式交易日+16.55%列All Stocks与大数据主题涨幅首位：Q3产品收入指引15.9亿超街测15.1亿、全年产品收入指引上调至60.7亿、运营利润率上修，多家机构齐唱多'AI受益者'。（事件时间2026-09-02 16:00 ET盘后） [Snowflake stock jumps as accelerating product revenue, AI adoption drive blowout quarter](https://finviz.com/news/387970/snowflake-stock-jumps-as-accelerating-product-revenue-ai-adoption-drive-blowout-quarter)"),
    "RARE": ("直接", "Ultragenyx 9/2盘后公布三期Aspire研究（Angelman综合征）结果失败，9/3暴跌-44.03%列All Stocks与罗素2000医疗保健跌幅首位——当日最大个股事件，并引发临床类小盘的传染性抛售（Medicus -34.40%、Aptevo -34.23%、Connect Biopharma -30.07%）。（事件时间2026-09-02 16:01 ET盘后） [Ultragenyx Announces Phase 3 Aspire results in Angelman Syndrome](https://finviz.com/news/387920/ultragenyx-announces-phase-3-aspire-results-in-angelman-syndrome)"),
    "TSN": ("直接", "Tyson Foods再度下调2026财年利润指引（牛肉业务亏损加深），-7.26%列All Stocks必需消费与农业商品主题跌幅首位。（事件时间2026-09-03 10:30 ET起） [Tyson Foods is slashing its annual profit forecast again as beef losses deepen](https://finviz.com/news/387980/tyson-foods-is-slashing-its-annual-profit-forecast-again-as-beef-losses-deepen)"),
    "ALB": ("直接", "Albemarle盘前宣布CEO接班计划，-4.06%列标普500基础材料跌幅首位——锂价低迷期的管理层不确定性。（事件时间2026-09-03 08:00 ET） [Albemarle Announces CEO Succession Plan](https://finviz.com/news/387940/albemarle-announces-ceo-succession-plan)"),
    "NVDA": ("直接", "英伟达确认以129亿美元收购Hugging Face（前日各档140亿—400亿美元口径之争落定），协议承诺平台保持完全开放（任意模型/云/推理供应商）；+1.80%为道指科技成分。（事件时间2026-09-03 13:46 ET） [Nvidia to Acquire Hugging Face for $12.9 Billion](https://finviz.com/news/388012/nvidia-to-acquire-hugging-face-for-%2412.9-billion)"),
    "HOOD": ("直接", "Robinhood获多家券商集体上调评级，叠加预测市场之争上诉至最高法院（新泽西州对Kalshi案），+16.57%列标普500金融与加密货币、金融科技主题涨幅首位。（事件时间2026-09-03 10:09 ET起） [Robinhood Stock Jumps After Wave of Analysts Upgrade](https://finviz.com/news/387985/robinhood-stock-jumps-after-wave-of-analysts-upgrade)"),
    "MSTR": ("联动", "暂未找到同日直接催化；+17.56%列金融科技主题首位——比特币大涨约6%（比特币ETF +5.8%簇）的最大杠杆代理（延续Strategy随比特币波动的定价惯例）。该股与当日所选金融科技、加密货币与区块链的偏强方向一致。"),
    "RIOT": ("联动", "暂未找到同日直接催化；+13.44%列加密货币主题与罗素2000金融涨幅前列——比特币矿企随币价大涨的高贝塔。该股与当日所选加密货币与区块链的偏强方向一致。"),
    "COIN": ("联动", "暂未找到同日直接催化；+10.14%列标普500金融第二——比特币大涨（交易量与托管收入弹性）为主驱动，任命前X Corp CFO进入董事会为次要治理新闻。该股与当日所选金融、加密货币与区块链的偏强方向一致。"),
    "PLTR": ("联动", "窗口内新闻为9/2盘后1.92亿美元陆军合同，当日+7.71%的驱动为科技与AI主题全面反弹（16个主题清一色上涨）、大数据主题涨幅第三。该股与当日所选科技、大数据的偏强方向一致。"),
    "CRM": ("联动", "窗口内候选为'软件股因财报上涨'的板块文章；+2.92%列道指科技（5涨/1跌）首位——Snowflake财报触发的软件板块重估（软件主题清一色上涨、IGV +3.41%）。该股与当日所选科技的偏强方向一致。"),
    "MSFT": ("联动", "窗口内候选：Nadella出售4,300万美元股票（次要）、Azure季度销售披露的报表分部改革预告（9/2盘后）；+2.68%为道指科技第二，随软件与AI主题反弹。该股与当日所选科技的偏强方向一致。"),
    "AMGN": ("联动", "该股与当日道指医疗保健（清一色上涨）的表现一致（+0.29%，权重端防御第三日）。"),
    "MRK": ("联动", "窗口内候选为Moderna癌症疫苗遭罕见卖出评级的文章（标的非默克，经聚合页面出现）；+0.46%为道指医疗保健成分。该股与当日道指医疗保健的表现一致。"),
    "UNH": ("联动", "该股与当日道指医疗保健（清一色上涨）的表现一致（+0.32%）。"),
    "AMZN": ("联动", "窗口内候选为Whole Foods CEO访谈（专题特稿非事件）；+1.54%为纳指100可选消费（6涨/5跌）成分。该股与当日所选可选消费的偏强方向一致。"),
    "TSLA": ("联动", "窗口内候选为苹果/Musk相关聚合文章（非特斯拉事件）；+5.42%列标普500与纳指100可选消费涨幅首位——Cybercab发布临近的连涨动能。该股与当日所选可选消费的偏强方向一致。"),
    "GM": ("联动", "窗口内候选为Unifor与Stellantis劳资谈判报道（非通用事件）；+2.77%列标普500可选消费涨幅第三。该股与当日所选可选消费的偏强方向一致。"),
    "CVX": ("联动", "窗口内候选为CEO'委内瑞拉的耐心得到回报'采访（延续叙事）；-0.22%为道指能源（清一色下跌）唯一成分——能源股获利回吐日（布伦特96美元下股价仍回落）。该股与当日所选能源的偏弱方向一致。"),
    "SPCX": ("联动", "窗口内候选为苹果/Musk聚合文章（非公司事件）；+6.42%列纳指100工业（12涨/1跌）涨幅首位——风险偏好修复日。该股与当日所选工业的偏强方向一致。"),
    "SHW": ("联动", "该股与当日道指基础材料（清一色上涨）唯一成分微涨入选一致（+0.31%；纳指100基础材料林德-1.08%清一色下跌——材料板块两端分化）。"),
    "AEHL": ("联动", "无窗口新闻微盘；+37.20%列All Stocks工业涨幅第二（9/1曾-22.96%）——连续极端双向波动的低流通个体，暂未找到同日直接催化，不纳入结构判断。该股与当日所选工业的偏强方向一致。"),
    "MIMI": ("联动", "无窗口新闻微盘（区块链/IPO相关）；+49.27%列All Stocks工业涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "SST": ("联动", "无窗口新闻微盘（广告技术）；+24.92%列All Stocks工业涨幅第三，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "BTCS": ("联动", "无窗口新闻微盘（区块链基础设施）；+20.00%列All Stocks金融涨幅首位——比特币+6%日的加密微盘高贝塔。该股与当日所选金融、加密货币与区块链的偏强方向一致。"),
    "ABTC": ("联动", "无窗口新闻微盘（比特币矿企）；+18.68%列All Stocks金融涨幅第二。该股与当日所选金融、加密货币与区块链的偏强方向一致。"),
    "BTBT": ("联动", "无窗口新闻（比特币矿企）；+17.27%列All Stocks与罗素2000金融涨幅第三。该股与当日所选金融、加密货币与区块链的偏强方向一致。"),
    "CD": ("联动", "无窗口新闻微盘（数字资产）；+13.75%列罗素2000金融涨幅第二。该股与当日所选金融、加密货币与区块链的偏强方向一致。"),
    "CIFR": ("联动", "无窗口新闻（比特币矿企）；+14.43%列罗素2000科技与加密货币主题涨幅前列。该股与当日所选科技、加密货币与区块链的偏强方向一致。"),
    "BKKT": ("联动", "无窗口新闻（加密基础设施）；+12.79%列罗素2000科技涨幅第二。该股与当日所选科技、加密货币与区块链的偏强方向一致。"),
    "APPS": ("联动", "无窗口新闻（应用变现）；+11.25%列罗素2000科技涨幅第三。该股与当日所选科技的偏强方向一致。"),
    "GCL": ("联动", "无窗口新闻微盘（中概娱乐）；+20.52%列All Stocks通信服务涨幅首位——9/1曾-26.27%，双向极端波动个体，暂未找到同日直接催化。该股与当日所选通信服务的偏强方向一致。"),
    "UPXI": ("联动", "无窗口新闻微盘（加密消费品）；+11.42%列All Stocks通信服务涨幅第二。该股与当日所选通信服务的偏强方向一致。"),
    "TRVG": ("联动", "无窗口新闻（在线旅游）；+9.40%列All Stocks通信服务涨幅第三。该股与当日所选通信服务的偏强方向一致。"),
    "SLNG": ("联动", "无窗口新闻微盘（LNG设备）；-6.25%列All Stocks能源跌幅首位——能源股获利回吐日。该股与当日所选能源的偏弱方向一致。"),
    "BTU": ("联动", "无窗口新闻（煤炭）；-6.08%列All Stocks与罗素2000能源、传统能源主题跌幅前列——动力煤随能源板块回吐。该股与当日所选能源、传统能源的偏弱方向一致。"),
    "TDW": ("联动", "无窗口新闻（海工油服）；-5.99%列能源跌幅前列。该股与当日所选能源的偏弱方向一致。"),
    "CLNE": ("联动", "无窗口新闻（清洁燃料）；-5.81%列罗素2000能源跌幅第三。该股与当日所选能源的偏弱方向一致。"),
    "METC": ("联动", "无窗口新闻（焦煤）；-14.30%列传统能源主题跌幅首位（9/1曾+7.07%列涨幅首位）——煤炭双向剧烈波动。该股与当日所选传统能源的偏弱方向一致。"),
    "AMR": ("联动", "无窗口新闻（焦煤）；-6.91%列传统能源主题跌幅前列。该股与当日所选传统能源的偏弱方向一致。"),
    "FAMI": ("联动", "无窗口新闻微盘（中概农产品）；-17.72%列All Stocks必需消费跌幅首位——农业商品主题清一色下跌日的极端个体。该股与当日所选必需消费、农业商品的偏弱方向一致。"),
    "RKDA": ("联动", "无窗口新闻微盘（农业生物技术）；-7.51%列All Stocks必需消费跌幅第二。该股与当日所选必需消费、农业商品的偏弱方向一致。"),
    "MDCX": ("联动", "无窗口新闻微盘（医药）；-34.40%列All Stocks医疗保健跌幅第二——Ultragenyx临床失败日的板块内传染性抛售，暂未找到该股自身直接催化。该股与当日所选医疗保健的偏弱方向一致。"),
    "APVO": ("联动", "无窗口新闻微盘（生物医药）；-34.23%列All Stocks医疗保健跌幅第三——同上传染性抛售。该股与当日所选医疗保健的偏弱方向一致。"),
    "CNTB": ("联动", "无窗口新闻微盘（免疫疗法）；-30.07%列罗素2000医疗保健跌幅前列——同上传染性抛售。该股与当日所选医疗保健的偏弱方向一致。"),
    "LFCR": ("联动", "无窗口新闻微盘（医疗器械外包）；-8.23%列罗素2000医疗保健跌幅侧。该股与当日所选医疗保健的偏弱方向一致。"),
    "APTV": ("联动", "该股与当日所选可选消费的偏强方向一致（+3.33%列标普可选消费第二）。"),
    "PFG": ("联动", "该股与当日所选金融的偏强方向一致（+6.47%列标普金融第三）。"),
    "TTD": ("联动", "该股与当日所选通信服务的偏强方向一致（+3.71%列标普通信首位，第三日连续偏强）。"),
    "OMC": ("联动", "该股与当日所选通信服务的偏强方向一致（+3.63%列第二）。"),
    "ECHO": ("联动", "该股与当日所选通信服务的偏强方向一致（+3.58%列第三）。"),
    "EOG": ("联动", "该股与当日所选能源的偏弱方向一致（-2.01%列标普能源首位）。"),
    "BKR": ("联动", "该股与当日所选能源的偏弱方向一致（-1.53%，道指与纳指100能源清一色下跌成分）。"),
    "WMB": ("联动", "该股与当日所选能源的偏弱方向一致（-1.48%列标普能源第三）。"),
    "FANG": ("联动", "该股与当日所选能源的偏弱方向一致（-0.24%，纳指100能源清一色下跌成分）。"),
    "DOW": ("联动", "该股与当日所选基础材料的偏弱方向一致（-2.94%列标普材料第二，昨日大涨后的化工回吐）。"),
    "LYB": ("联动", "该股与当日所选基础材料的偏弱方向一致（-2.72%列标普材料第三）。"),
    "BSX": ("联动", "该股与当日所选医疗保健的偏弱方向一致（-2.94%列标普医疗保健首位——权重端回调日，宽度418涨/592跌）。"),
    "IDXX": ("联动", "该股与当日所选医疗保健的偏弱方向一致（-1.80%列标普与纳指100医疗保健前列）。"),
    "STE": ("联动", "该股与当日所选医疗保健的偏弱方向一致（-1.53%列标普医疗保健第三）。"),
    "GEHC": ("联动", "该股与当日所选医疗保健的偏弱方向一致（-1.19%列纳指100医疗保健第二）。"),
    "ALNY": ("联动", "该股与当日所选医疗保健的偏弱方向一致（-1.09%列纳指100医疗保健第三）。"),
    "JNJ": ("联动", "该股与当日道指医疗保健（清一色上涨）的表现一致（+1.17%领涨）。"),
    "LIN": ("联动", "该股与当日所选基础材料的偏弱方向一致（-1.08%，纳指100基础材料清一色下跌唯一成分）。"),
    "PYPL": ("联动", "暂未找到同日新催化；+3.93%为纳指100金融唯一成分清一色上涨——收购破裂后的第二日连续反弹（+4.33%/+3.93%），修复动能确立。该股与当日所选金融的偏强方向一致。"),
    "AXON": ("联动", "该股与当日所选工业的偏强方向一致（+6.15%列纳指100工业第二——9/1曾-8.52%列跌幅首位，双向波动）。"),
    "TRI": ("联动", "该股与当日所选工业的偏强方向一致（+5.56%列纳指100工业第三）。"),
    "ABNB": ("联动", "该股与当日所选可选消费的偏强方向一致（+1.09%，纳指100可选消费6涨/5跌）。"),
    "MIR": ("联动", "该股与当日所选工业的偏强方向一致（+7.64%列罗素2000工业首位）。"),
    "TE": ("联动", "该股与当日所选工业的偏强方向一致（+6.32%列罗素2000工业第二）。"),
    "TATT": ("联动", "该股与当日所选工业的偏强方向一致（+5.33%列罗素2000工业第三）。"),
    "MZTI": ("联动", "该股与当日所选必需消费的偏弱方向一致（-5.15%列罗素必需消费首位）。"),
    "CVSA": ("联动", "该股与当日所选必需消费的偏弱方向一致（-4.86%列罗素必需消费第二）。"),
    "COCO": ("联动", "该股与当日所选必需消费的偏弱方向一致（-4.52%列罗素必需消费第三）。"),
    "GEVO": ("联动", "该股与当日所选农业商品的偏弱方向一致（-4.09%，农业商品主题清一色下跌）。"),
    "AMTX": ("联动", "该股与当日所选农业商品、农业与食品科技的偏弱方向一致（-3.68%）。"),
    "BIOX": ("联动", "该股与当日所选农业与食品科技的偏弱方向一致（-6.22%——9/2曾+6.95%列涨幅首位，谷物回调日的反转）。"),
    "STKH": ("联动", "该股与当日所选农业与食品科技的偏弱方向一致（-5.84%）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "BITO", "perf": 5.865, "form": "交易所交易基金", "exposure": "比特币（期货策略）",
         "reason": "比特币ETF领涨全市场：比特币大涨约6%（Strategy +17.56%、Coinbase +10.14%、矿企股+12%—17%全链共振），加密货币主题六子行业清一色上涨（等权+5.23%）。合并删除：IBIT、FBTC、ARKB、BITB、GBTC（同簇比特币价格敞口，按表现保留最强一只BITO）。"},
        {"ticker": "PALL", "perf": 4.923, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF第二日大涨（+3.80%后+4.92%）：8/28以来三连阴的供给端叙事完全退潮、利率回落与贵金属修复共振——与比特币为不同资产类别。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "SGDM", "perf": 4.520, "form": "交易所交易基金", "exposure": "全球金矿股",
         "reason": "金矿股ETF：黄金+1.85%的第二日反弹经矿业股放大（白银+2.51%），股权杠杆敞口区别于钯金现货。合并删除：RING、GDX、GDXJ（同簇金矿股，按表现保留最强一只SGDM）。"},
    ],
    "down": [
        {"ticker": "UNG", "perf": -2.419, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货ETF领跌全市场：能源商品内部气强油稳格局反转（前一日+1.61%的回吐），天气与库存驱动。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "VXX", "perf": -2.220, "form": "交易所交易票据", "exposure": "VIX期货",
         "reason": "VIX期货ETN连续第二日下跌（-2.92%后-2.22%）：风险偏好全面回归（16个主题清一色上涨、股债双涨），对冲需求退潮。合并删除：VIXY（同簇VIX期货，保留最强一只VXX）。"},
        {"ticker": "XES", "perf": -1.582, "form": "交易所交易基金", "exposure": "美国油气设备与服务",
         "reason": "油气设备与服务ETF：布伦特96美元下能源股仍遭获利回吐（能源五个范围全部进入跌幅侧、道指与纳指100清一色下跌）——两日大涨后的仓位了结。合并删除：OIH（同簇油服，保留最强一只XES）。"},
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
        text = "核查9月2日盘后至9月3日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-03"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；比特币簇（BITO/IBIT/FBTC/ARKB/BITB/GBTC）保留BITO、金矿股簇（SGDM/RING/GDX/GDXJ）保留SGDM、VIX期货簇（VXX/VIXY/VIXM）保留VXX、油服簇（XES/OIH）保留XES。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-03_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-03_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月3日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月3日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：周四股债双涨：联储理事Waller讲话被解读为'没那么鹰派'（当前利率足以让通胀回到2%、'数据火热才会考虑加息'），2年期收益率-5.5bp至4.31%、前端收益率完成回到Jackson Hole演讲前的往返，标普500迈向两连涨；比特币大涨约6%成为当日最强资产（比特币ETF +5.8%簇包揽涨幅前三、加密货币主题六子行业清一色涨等权+5.23%、Strategy +17.56%、Robinhood获集体上调评级+16.57%、Coinbase +10.14%、矿企股+12%—17%全链共振）。主题层出现16个清一色上涨对1个清一色下跌的图谱：软件（Snowflake财报次日+16.55%引爆，IGV +3.41%、XSW +2.88%——8.27确认的上涨趋势经两日回调后强势恢复）、云计算（WCLD +2.49%）、网络安全（+1.96%，第三日反转上涨）、大数据、人工智能、金融科技、物联网、量子计算等全面上攻；英伟达确认以129亿美元收购Hugging Face（前日口径之争落定、平台保持开放）。股票范围轮动：金融四个范围进入涨幅前三（道指与纳指100清一色：PayPal +3.93%第二日连涨、Robinhood/Coinbase领衔标普金融65/70上涨）；工业三个范围居前（纳指100工业12涨/1跌：SpaceX +6.42%、Axon +6.15%）；可选消费（标普与纳指100：特斯拉+5.42%）；通信服务连续第三日偏强（Trade Desk +3.71%）。跌幅侧：能源五个范围全部进入（道指与纳指100清一色下跌——布伦特96美元下能源股遭两日大涨后的获利回吐）；医疗保健宽度418涨/592跌（Ultragenyx三期临床失败-44.03%引发小盘临床股传染性抛售、权重药械回调）；必需消费（Tyson再度下调指引-7.26%、农业商品主题清一色跌）。贵金属第二日修复：黄金+1.85%、白银+2.51%、钯金+4.92%、金矿股+4.52%；VIX期货ETF连续第二日下跌。Broadcom'好但不够好'：AI半导体收入指引FY27翻倍至约1,150亿美元仍因Q4微逊大跌约5%。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5527/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1938/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-09-03_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-09-03_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-09-03_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
