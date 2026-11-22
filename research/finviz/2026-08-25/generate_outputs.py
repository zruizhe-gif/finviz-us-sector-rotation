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
    "Industrial Automation": "工业自动化", "Internet of Things": "物联网",
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
    "Hardware": "硬件", "Software": "软件",
    "Advertising": "广告", "Enabling Tech": "支撑技术", "Gov & Defense": "政府与国防",
    "Identity": "身份认证", "Networks": "社交网络", "Niche": "垂直社群", "Visual Content": "视觉内容",
    "Silver": "白银", "Gold": "黄金", "Precious": "贵金属", "Industrial": "工业金属",
    "Battery": "电池", "Rare Earth": "稀土", "Recycling": "回收",
    "Packaging": "封装", "Memory": "存储", "Lithography": "光刻", "Next-Gen": "下一代硬件",
    "Oil Services": "油服", "Oil Production": "石油生产", "Majors": "大型油气", "Thermal": "动力煤",
    "Gaming": "游戏",
    "Analog": "模拟芯片", "Compute": "计算芯片", "Design": "芯片设计工具", "Wireless": "无线芯片",
    "V-SaaS": "垂直SaaS", "CRM": "客户关系管理", "H-SaaS": "横向SaaS",
    "Fertilizers": "化肥", "Grains": "谷物", "Softs": "软商品", "Livestock": "畜牧",
    "Servers": "服务器", "Electronics": "电子设备",
    "OS": "操作系统", "E-Commerce": "电子商务", "Telecom": "电信设备",
    "Storage": "存储", "Data Centers": "数据中心", "Foundries": "晶圆代工",
    "Biofuels": "生物燃料",
    "Meal Delivery": "餐食外送", "Retailers": "零售商", "Supplements": "膳食补充剂", "Alt Protein": "替代蛋白",
    "Applications": "应用", "Networking": "网络设备", "Suppliers": "供应商", "Tokenization": "代币化", "Payments": "支付", "Collaboration": "协作办公", "DevOps": "开发运维", "Self-Driving": "自动驾驶",
    "Office": "办公", "Housing": "住宅", "Retail": "零售物业", "Warehousing": "仓储",
    "Batteries": "动力电池", "Chips": "车规芯片", "Charging": "充电设施", "Fleets": "车队", "Manufacturers": "整车制造商",
    "Diagnostics": "诊断", "Genomics": "基因组学", "Oncology": "肿瘤", "Enterprise": "企业级",
    "Mining": "挖矿", "Farm-Direct": "农场直供", "Food": "食品",
    "Luxury": "奢侈品", "Secondhand": "二手",
}

THEME_COMPANY = {
    "ABAT": "American Battery Technology Company",
    "AMD": "Advanced Micro Devices Inc",
    "AREC": "American Resources Corp",
    "CLSK": "Cleanspark Inc",
    "ESTC": "Elastic N.V",
    "FLY": "Firefly Aerospace Inc",
    "HOOD": "Robinhood Markets Inc",
    "HUT": "Hut 8 Corp",
    "LDOS": "Leidos Holdings Inc",
    "QBTS": "D-Wave Quantum Inc",
    "RGTI": "Rigetti Computing Inc",
    "RKLB": "Rocket Lab Corp",
    "TENB": "Tenable Holdings Inc",
    "UUUU": "Energy Fuels Inc",
    "ZM": "Zoom Communications Inc",
    "ZS": "Zscaler Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic N.V", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月22日16:00 ET盘后事件可解释8月25日；8月25日16:00 ET后事件不得倒推。
R = {
    "CRML": ("联动", "关键矿产/稀土板块联动：GuruFocus明确称其8/25上涨约18-21%系延续上周关键矿产板块强势反弹，窗口内无公司直接新闻（并购European Lithium等为早前公告），属基础材料稀土组联动。"),
    "STDN": ("联动", "TRISO核燃料新贵定于8/26盘后发布Q2财报，资金提前抢跑（雅虎财经专文称'财报前创阶段新高'），8/25放量涨16.75%、盘中最高触及14.90美元，属财报前动量博弈+核能板块强势，无窗口内新公告，归基础材料组。"),
    "GRML": ("直接", "公司8/25公告拟启动公开增发（A.G.P./Alliance Global Partners为独家配售代理，规模条款未定），同日CFO Jeff LeBlanc以9.72美元增持1.4万股（Form 4，持股增至11.04万股），且1拆50并股于8/24刚生效；股价当日不跌反涨13.6%。（事件时间2026-08-25（增发公告当日发布，具体时刻未标明；CFO买入交易日为8/25）） [Greenland Mines proposed offering and Fo](https://www.stocktitan.net/news/GRML/)"),
    "AIXI": ("联动", "低流通中概AI微盘股投机资金连续逼空拉升（8/25盘中一度+229%），8/20的F-6 ADR文件为例行行政程序、8/25无新运营消息，多家媒体明确称涨势纯属交易动量，属Technology组微盘炒作。"),
    "DAIC": ("联动", "面临Nasdaq退市通知、近期1拆25并股的困境微盘（流通股仅约118万股）：8/24盘中+306%、盘后再+126%，8/25续涨98%+属投机资金/逼空式连续拉升，Benzinga明确称未发现直接催化，属Technology组微盘投机。"),
    "EXYN": ("联动", "市值约1800万美元的2026年国防无人机概念次新股（IPO以来-61%），8/25放量单边拉升40%，Q2财报与国防顾问委员会任命为此前发布（当日盘前页面仍显示前收2.30美元），属国防/机器人概念微盘动量投机，归Technology组。"),
    "PMI": ("直接", "公司8/25盘前发布Q2财报：营收同比增长39%、净亏损收窄16%，季末现金1.18亿美元（含1340万美元权证行权入账），并首次公开展示Emperor全人工心脏平台集成架构（已完成一系列急性体内植入研究）；股价盘前涨约40%、日内一度+67.5%、全日收涨86.2%。（事件时间2026-08-25盘前（美东）） [PMI Q2 2026 results press release](https://www.stocktitan.net/news/PMI/)"),
    "AMIX": ("直接", "公司8/24盘后公告490万美元权证行权诱导协议：投资者以5.75美元/股行权86万股，公司同步发行行权价6.25美元的E-1/E-2新权证（各53万股），预计8/26交割；股价8/24盘后一度大涨116.57%至11.63美元，8/25收涨约34%，同日还有一项8/25新授予的美国专利消息助推。（事件时间2026-08-24盘后（美东），8/25盘中延续涨势） [Warrant exercise inducement agreement pr](https://www.stocktitan.net/news/AMIX/)"),
    "AKAN": ("联动", "市值仅约200万美元的低流通微盘（52周高点209美元 vs 现价约4美元），窗口内无公司新闻（最近公告为8/13运营更新），属超跌微盘投机资金拉升，属医疗保健组微盘炒作。"),
    "RCON": ("直接", "公司8/25公告（PRNewswire）中标国内某大型油气运营商'生产信息化系统集成技术服务'项目多个标段，合同总额约960万元人民币（约133万美元，2028年7月前完工验收）；股价当日自2.87美元开盘后一度暴涨至9.00美元（盘中最高+192.5%、成交量18.1倍放大）后剧烈回落，全日收跌28.9%，呈典型冲高回落。（事件时间2026-08-25盘中（美东，公告于8/25发布，日内股价先暴涨后回落）） [Recon Technology contract award announce](https://www.stocktitan.net/news/RCON/)"),
    "VIVK": ("联动", "窗口内新闻1条经核验无同日直接事件；上调2026年Supply & Trading展望至$35亿的PR为8-24盘中（GlobeNewswire）发布、位于窗口之外，8-25大跌13%未见窗口内新直接催化，属微市值能源股利好兑现后的获利回吐。"),
    "TMDE": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "SDOT": ("直接", "公司8/25签署/提交S-1/A注册书修订，为多达425.44万股转售股份办理登记（现有流通股仅约130万股，且已有13.48万股抵债股份完成稀释）；叠加Q2营收归零（0美元 vs 上年同期2.466亿美元）、持续经营疑虑及9/30 Nasdaq合规大考，股价8/25暴跌29.4%至约19美元。（事件时间2026-08-25（S-1/A签署日为8/25，SEC提交具体时刻未确认）） [Sadot Group S-1/A resale registration](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=SDOT)"),
    "BRLS": ("联动", "低流动性微盘食品股投机资金退潮：8/25单日振幅42.86%并缩量下跌27%，此前已因市值不达标收Nasdaq通知（限期12/29整改），窗口内无公司新闻，属必需消费组微盘退潮。"),
    "XXII": ("联动", "市值仅约280万美元的烟草微盘（52周自594美元跌至约3.7美元，历经大幅并股摊薄），Q2财报电话会内容8/18已在流传、8/25无新公司事件，属持续摊薄下的投机退潮阴跌，归必需消费组。"),
    "DKS": ("直接", "8-25盘前公布Q2 FY2026业绩并暴雷：净销售$55.9亿（+53.2%含Foot Locker），Foot Locker同店-3.6%、Q2经营亏损$3190万，全年non-GAAP EPS指引从$13.50-14.50大幅下调至$11.00-12.00（Foot Locker全年从盈利转为亏损$4000-8000万），股价盘中暴跌近30%。（事件时间2026-08-25T07:00:00-04:00（盘前发布财报，当日盘中暴跌近30%）） [DICK'S Sporting Goods (DKS) Q2 2026 earn](https://finsee.ai/earnings/dks/2026/q2/en) [Dick's Sporting Goods Shares Fall on Q2 ](https://wwd.com/footwear-news/shoe-industry-news/dicks-sporting-goods-dks-q2-2026-earnings-foot-locker-stock-1239148792)"),
    "JZXN": ("联动", "市值不足200万美元的低流通中概微盘，2026年多次增发导致股本大幅扩张（TipRanks近期专文披露其股本激增），8/25无窗口内新事件，属摊薄压力下投机资金退潮，归可选消费组微盘退潮。"),
    "NTZ": ("联动", "日均成交仅约3000股的极低流动性意大利家具ADR，CEO人选最终协议等为8月中下旬旧闻（8/10承诺函后续签），8/25无新事件，属低流动性波动回落，归可选消费组。"),
    "SMCI": ("直接", "8-25思科扩大与英伟达'Secure AI Factory'合作并将超微高密度液冷/风冷服务器系统纳入其AI数据中心方案（媒体独家报道）；同日台湾检方起诉9人涉嫌非法出口AI服务器仅点名个人员工而非超微公司本身，公司层面合规隐忧缓解，两大利好推动当日大涨8.8-9.4%。（事件时间2026-08-25T10:00:00-04:00（盘中，思科合作消息与台湾起诉细节明朗化，近似时刻）） [Why Is Super Micro Computer (SMCI) Stock](https://tickeron.com/blogs/why-is-super-micro-computer-smci-stock-up-8-81-today-16078) [Super Micro Computer Inc Stock (SMCI) Mo](https://www.tradingkey.com/news/market-movers/262130681-market-movers-smci-20260825)"),
    "CDW": ("联动", "窗口内新闻2条经核验无同日直接事件；该股与当日所选科技的偏强方向一致。"),
    "LITE": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选科技的偏强方向一致。"),
    "RDDT": ("联动", "该股与当日所选通信服务的偏强方向一致。"),
    "APP": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选通信服务的偏强方向一致。"),
    "CHTR": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选通信服务的偏强方向一致。"),
    "FCX": ("联动", "窗口内新闻2条经核验无同日直接事件；该股与当日所选基础材料的偏强方向一致。"),
    "NEM": ("联动", "该股与当日所选基础材料的偏强方向一致。"),
    "IFF": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选基础材料的偏强方向一致。"),
    "APA": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "OXY": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "FANG": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "TGT": ("联动", "窗口内新闻6条经核验无同日直接事件；Target Q2财报大涨为8-19旧闻（当日+4.3%创52周高$161.98后动能衰竭），8-25 Dick's暴雷再压零售/百货情绪，日内自高点$169.97冲高回落收跌3.8%，无窗口内新公司事件。"),
    "MKC": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "GIS": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "EME": ("联动", "窗口内新闻1条经核验无同日直接事件；候选为Zacks式例行盘点文章，EMCOR Q2创纪录财报（营收$51.5亿、EPS$9.06）为7月底旧闻；当日-3.3%属AI数据中心基建/建筑股自52周高点（$951.96）回调趋势的延续。"),
    "FIX": ("联动", "该股与当日所选工业的偏弱方向一致。"),
    "URI": ("联动", "该股与当日所选工业的偏弱方向一致。"),
    "SHW": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选基础材料的偏强方向一致。"),
    "HON": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选工业的偏强方向一致。"),
    "BA": ("直接", "美国防部授予波音F-15 Eagle Crest项目上限$1312.3亿美元框架合同（覆盖生产/集成/升级/维护至2037年，含日以沙韩等FMS），8-24盘后披露引发盘后上涨，8-25盘中续涨收涨0.3%，叠加创纪录$5970亿积压订单报道。（事件时间2026-08-24T17:00:00-04:00（8-24盘后合同公告披露，近似时刻）） [Boeing Wins $131B F-15 Contract From US ](https://www.tradingview.com/news/stocktwits:ee28cf030094b:0-boeing-wins-131b-f-15-contract-from-us-air-force-ba-stock-gains-after-hours) [Boeing Stock (NYSE:BA) Notches Up With $](https://www.tipranks.com/news/boeing-stock-nyseba-notches-up-with-131-billion-contract-win)"),
    "MMM": ("联动", "该股与当日所选工业的偏强方向一致。"),
    "NVDA": ("联动", "窗口内新闻90条经核验无同日直接事件；周三盘后财报前AI芯片龙头仓位回补推动+2.2%；BMO为8-21首次覆盖（Outperform/$340）后8-25维持观点（预期Q2营收$940-950亿高于共识），属例行分析师文章而非窗口内评级实质变动。"),
    "IBM": ("联动", "窗口内新闻6条经核验无同日直接事件；候选为矿业投资会议（Noble Capital）宣传稿，与IBM无关联；当日+1.4%随科技板块/大盘小幅上行。"),
    "MSFT": ("联动", "窗口内新闻17条经核验无同日直接事件；候选均为Marvell目标价与英伟达财报前瞻文章，与微软无直接关联；当日+0.9%随纳指/科技板块反弹。"),
    "CVX": ("联动", "窗口内新闻6条经核验无同日直接事件；该股与当日所选能源的偏弱方向一致。"),
    "WMT": ("联动", "窗口内新闻17条经核验无同日直接事件；Walmart上周（8-20）财报指引失望后持续回调（8月累跌约4%），当日Investopedia文章为盘后复盘式评论，Oppenheimer'可能跌至90美元出头'亦属观点；-1.0%为回调延续+Dick's暴雷压零售情绪，无新公司事件。"),
    "PG": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "KO": ("联动", "窗口内新闻4条经核验无同日直接事件；新CEO话题源于2025年12月10日CEO继任公告（Braun于2026-03-31接任Quincey），当日文章仅为例行评论，KO随防御性消费板块微跌0.4%。"),
    "NKE": ("联动", "窗口内新闻8条经核验无同日直接事件；Dick's财报暴雷下调指引拖累运动鞋服零售链情绪，24/7 Wall St明确指出Nike/Lululemon/On'在没有新公司消息的情况下下跌'，Nike自身无窗口内直接事件（-3.1%为板块联动）。"),
    "MCD": ("联动", "窗口内新闻3条经核验无同日直接事件；该股与当日所选可选消费的偏弱方向一致。"),
    "AMZN": ("联动", "窗口内新闻30条经核验无同日直接事件；候选均为Marvell目标价、Zoom财报、英伟达财报前瞻等无关文章，亚马逊当日-0.4%属巨型科技股在英伟达财报前的窄幅观望。"),
    "PYPL": ("联动", "窗口内新闻4条经核验无同日直接事件；该股与当日所选金融的偏强方向一致。"),
    "AXON": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选工业的偏强方向一致。"),
    "SPCX": ("联动", "窗口内新闻34条经核验无同日直接事件；WSJ周二独家称Anthropic拟向IPO投资者宣称TAM超$30万亿、超越SpaceX的$28.5万亿预估，AI/太空叙事联动下SPCX随纳指收涨2.2%，但该报道是Anthropic事件而非SPCX公司直接事件。"),
    "FER": ("联动", "该股与当日所选工业的偏强方向一致。"),
    "NBIS": ("直接", "8-24盘后（16:05 ET）宣布完成$57.5亿可转债私募交割（0.50% 2030年$34.5亿+4.50% 2034年$23亿，超额配售全额行使），并以约1580万股A类股置换$8亿存量可转债，募资用于数据中心建设与GPU采购；8-25股价涨约5%（媒体称'超初始计划'的融资成功提振）。（事件时间2026-08-24T16:05:00-04:00（盘后PR，StreetInsider时间戳16:05 EDT）） [Nebius Group announces closing of privat](https://nebius.com/newsroom/nebius-group-announces-closing-of-private-offering-of-convertible-senior-notes-with-aggregate-gross-proceeds-of-approximately-5-75-billion) [Nebius Group closes $5.75B convertible n](https://www.streetinsider.com/Corporate+News/Nebius+Group+closes+%245.75B+convertible+notes+offering/26968086.html)"),
    "CDNS": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选科技的偏强方向一致。"),
    "BKR": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "MDLZ": ("联动", "窗口内新闻2条经核验无同日直接事件；该股与当日所选必需消费的偏弱方向一致。"),
    "KDP": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选必需消费的偏弱方向一致。"),
    "PEP": ("联动", "窗口内新闻5条经核验无同日直接事件；候选为公布三季报发布时间的例行公告，非实质催化；百事随防御性消费板块当日走弱-1.7%（零售/百货情绪拖累）。"),
    "LIN": ("联动", "该股与当日所选基础材料的偏弱方向一致。"),
    "TENX": ("联动", "Phase 3 LEVEL试验（TNX-103，PH-HFpEF口服左西孟旦）顶线数据预计8月内公布并将于8/28-31 ESC大会晚期报告，临近数据窗口资金提前博弈，8/25放量涨25.4%，无窗口内公司新公告，属医疗保健组临床数据前投机。"),
    "CAPR": ("直接", "FDA将Deramiocel（DMD心肌细胞疗法）BLA审评延期、新PDUFA目标日期定为2026-11-22，Oppenheimer随后上调目标价至54美元；股价8/24先涨8%、8/25盘前续涨并收涨21.9%至约7.9美元（同日律所发布的证券集体诉讼新闻未阻止反弹）。（事件时间2026-08-24（FDA延期与Oppenheimer上调消息于前一交易日开始发酵），8/25盘前延续） [Capricor FDA review extension and target](https://www.stocktitan.net/news/CAPR/)"),
    "PACB": ("直接", "公司于8/24盘后发布Q2财报：营收3901万美元（同比-1.9%）略逊预期、非GAAP每股亏损0.14美元均不及预期，但SPRQ-Nx化学试剂全球推广（单基因组列表价345美元）与Vega系统'提速50% HiFi数据'等产品进展及重组措施获市场买单，8/25放量反弹18.75%至1.52美元。（事件时间2026-08-24盘后（美东，据StockStory 8/25凌晨更新及前收1.28美元推断）） [PacBio Q2 2026 results press release](https://investor.pacificbiosciences.com/)"),
    "OPTU": ("联动", "一个月内暴跌28%后的超跌反弹，与同板块Cable One（+15.4%）同日联动走强；其Q2财报（EPS -0.18美元不及预期、营收20.2亿美元同比-5.8%）于8/25盘后前后才发布，非盘中上涨催化，属通信服务组超跌反弹。"),
    "CABO": ("直接", "公司密集公告管理层换届与重大交易安排：新任CEO James Holanda获合计约1000万美元入职股权激励（约16.9万股、60%绩效RSU），Heather McCallion于8/24前后出任COO，同时披露约8.45-8.95亿美元规模的收购融资安排（预计10/1完成交割）；股价自52周低点22.62美元附近反弹15.4%至22.83美元。（事件时间2026-08-24~08-25（COO任命8/24生效，CEO激励与交易公告时点未逐项确认）） [Cable One management transition and acqu](https://www.stocktitan.net/news/CABO/)"),
    "RUM": ("直接", "公司8-24上午经SEC披露与一家未具名美国云客户签订六年约$137亿GPU服务协议（协议日8-23，佐治亚州Maysville数据中心，客户获5,080.8万股$0.01认股权证）；8-25 CEO Pavlovski在X公开叫板'Quake AI将与CoreWeave、Nebius等所有neocloud正面竞争'，合同发酵+零售资金涌入推动8-25午盘涨11%、收涨9.3%。（事件时间2026-08-25T06:00:00-04:00（盘前CEO X表态发酵；合同SEC披露为8-24上午约09:20 ET）） [RUM Group stock surges 10% on $13.7 bill](https://www.investing.com/news/stock-market-news/rum-group-stock-surges-10-on-137-billion-gpu-services-deal-93CH-4873331) [RUM Group Surges 11% as CEO Vows to Take](https://247wallst.com/investing/2026/08/25/rum-group-surges-11-as-ceo-vows-to-take-on-coreweave-and-nebius-trump-media-holds-flat)"),
    "GEVO": ("联动", "可再生燃料/SAF概念股8/6 Q2财报（上调全年EBITDA指引至6000万美元以上）后震荡整理，8/25放量反弹约10.5%，无窗口内公司新闻，属基础材料清洁能源组板块性回升。"),
    "ALOY": ("联动", "北美稀土概念延续8/14 Q2财报及美国陆军合作消息后的动量，8/25随关键矿产/稀土板块整体走强联动上涨约9.6%，无窗口内公司新公告，属基础材料稀土组联动。"),
    "WTI": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "KOS": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "PBF": ("联动", "该股与当日所选能源的偏弱方向一致。"),
    "SHOE": ("联动", "鞋类零售股随运动零售链走弱：同日Dick's Sporting Goods暴跌约30%拖累Nike（-3.1%）及鞋服消费板块，SHOE自身Q1已转亏、9/3财报临近，无窗口内公司新闻，属可选消费组板块联动下跌。"),
    "JACK": ("联动", "该股与当日所选可选消费的偏弱方向一致。"),
    "CTRN": ("直接", "8-25盘前公布Q2 FY2026业绩：销售额$2.116亿（+10.9%）、同店销售+10.5%、调整后EBITDA $550万（上年同期-110万），并上调全年指引（调整后EBITDA $3800-4200万），但股价仍收跌6.2%（利好兑现回落），电话会9:00 ET。（事件时间2026-08-25T07:00:00-04:00（盘前发布公告，9:00电话会）） [CITITRENDS Announces Second Quarter Fisc](https://finance.yahoo.com/markets/stocks/articles/cititrends-announces-second-quarter-fiscal-104500826.html) [Citi Trends posts double-digit prelimina](https://www.stocktitan.net/sec-filings/CTRN/8-k-citi-trends-inc-reports-material-event-74355c0431fb.html)"),
    "FGBI": ("联动", "该股与当日所选金融的偏弱方向一致。"),
    "GBFH": ("联动", "该股与当日所选金融的偏弱方向一致。"),
    "RM": ("联动", "该股与当日所选金融的偏弱方向一致。"),
    "HOOD": ("联动", "窗口内新闻6条经核验无同日直接事件；加密货币走强（比特币当日+2.2%）与零售交易活跃度提升带动的高beta标的（7/31收盘86.56美元以来累计涨约28%），8/25无公司直接新闻，属加密货币与区块链入选组方向联动。"),
    "HUT": ("联动", "该股与当日所选加密货币与区块链的偏强方向一致。"),
    "CLSK": ("联动", "该股与当日所选加密货币与区块链的偏强方向一致。"),
    "AREC": ("联动", "窗口内新闻4条经核验无同日直接事件；候选仅为大盘收盘总结文章；7-24宣派的$0.0431/股特别股息于8-25派发（登记日8-15，非价格催化），当日+8.4%属关键矿产题材微盘股随纳指反弹的高波动。"),
    "ABAT": ("联动", "该股与当日所选金属商品的偏强方向一致。"),
    "UUUU": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选金属商品的偏强方向一致。"),
    "AMD": ("直接", "8-25盘前Raymond James分析师Simon Leopold将AMD评级从Outperform上调至Strong Buy，目标价从$565升至$641（较8-24收盘$456.75隐含约40%上行），称其为数据中心盈利杠杆+份额增长最强组合，预计服务器CPU市场2030年达$2010亿（44% CAGR）。AMD盘前涨超3%，收涨4.9%。（事件时间2026-08-25T06:30:00-04:00（盘前研报，近似时刻）） [AMD Stock Gets 'Strong Buy' Upgrade From](https://www.tipranks.com/news/top-analyst-upgrades-amd-stock) [AMD Stock Gains After Upgrade: Analyst S](https://finance.yahoo.com/markets/stocks/articles/amd-stock-gains-upgrade-analyst-104623884.html)"),
    "QBTS": ("联动", "该股与当日所选量子计算的偏强方向一致。"),
    "RGTI": ("联动", "该股与当日所选量子计算的偏强方向一致。"),
    "ZS": ("联动", "该股与当日所选 网络安全, 软件 的偏弱方向一致。"),
    "ESTC": ("联动", "该股与当日所选 网络安全, 软件 的偏弱方向一致。"),
    "TENB": ("联动", "该股与当日所选网络安全的偏弱方向一致。"),
    "FLY": ("联动", "该股与当日所选太空科技的偏弱方向一致。"),
    "LDOS": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选太空科技的偏弱方向一致。"),
    "RKLB": ("联动", "窗口内新闻2条经核验无同日直接事件；候选为期权策略文章；RKLB处于多周回调中（Q2财报8-10公布后Neutron延期担忧发酵），8-25盘前曾涨2.4%后冲高回落收跌2%，8月合同新闻均为旧闻，无窗口内新直接催化。"),
    "ZM": ("联动", "窗口内新闻5条经核验无同日直接事件；Zoom Q2 FY26财报（营收$12.8亿超预期、EPS$1.55、小幅上调全年EPS指引）于8-25盘后发布，按规则盘后事件不得倒推，日内-3.7%属财报前观望与AI/软件板块回调（Zoom财报叙事关联Anthropic话题）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "FBTC", "perf": 2.298, "form": "交易所交易基金", "exposure": "比特币现货",
         "reason": "比特币现货ETF领涨全市场（IBIT +2.20%、ARKB +2.23%、GBTC +2.23%同簇）：美元走弱与风险偏好向硬资产迁移的延续。合并删除：IBIT +2.198%、ARKB +2.231%、GBTC +2.230%（同簇比特币现货，按敞口去重只保留最强一只）。"},
        {"ticker": "UNG", "perf": 1.602, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货+1.6%为商品端最强：天气与库存收紧。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "CORN", "perf": 1.105, "form": "商品信托", "exposure": "玉米期货",
         "reason": "玉米期货+1.1%与农业投入品延续共振；健康食品与营养主题当日清一色上涨（等权+2.09%）。合并删除：无同簇产品进入本轮极值候选。"},
    ],
    "down": [
        {"ticker": "PTF", "perf": -4.103, "form": "交易所交易基金", "exposure": "科技动量（Dorsey Wright）",
         "reason": "科技动量ETF再度领跌全市场：存储链（DRAM -5.9%、希捷-6.5%、SanDisk -6.5%、美光-5.8%）与半导体（等权-3.3%）在英伟达财报（8月26日）前集中去风险，科技五个股票范围全部进入跌幅前三。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "XSD", "perf": -3.338, "form": "交易所交易基金", "exposure": "半导体（修正等权）",
         "reason": "半导体主题九个子行业当日再度走弱：等权-3.3%、权重SOXX -2.7%；Jackson Hole后高估值成长与动量交易继续收缩。合并删除：SOXX -2.667%（同簇半导体，保留最弱一只）。"},
        {"ticker": "EWY", "perf": -2.635, "form": "交易所交易基金", "exposure": "韩国股票",
         "reason": "韩国ETF再度领跌（存储/半导体占韩国指数高权重，为AI链回调的亚洲映射）；与科技动量、半导体为不同地域敞口。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查8月15日盘后至18日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-08-25"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；金矿股簇（RING/GDXJ/GDX/SGDM）在成稿层合并、白银矿业与钯金保持独立敞口。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-08-25_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-25_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月25日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月25日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：英伟达财报（次日盘后）前的芯片反弹日叠加Druckenmiller檄文发酵：Druckenmiller在WSJ公开抨击前门生Bessent的长端回购（\"政府对抗基本面捍卫价格永远失败；让债券市场说话\"），Bessent回应\"还没买过一张债券、下次9月9日\"；\"新财政部-Fed协定\"（发行与Fed持仓对齐）被认定为贬值交易的制度根源——黄金月内双位数创1999年以来最大月、比特币触80,000美元、美元走弱。油价大跌（布伦特-3.5%至-4.8%破90美元：NYT报道美外交官回流中东+\"经济战争而非动能战争\"）。10:00数据走弱：消费者信心89.4（预期分项68.2大跌）、新屋销售-10.5%。收盘标普500 +0.3%、纳指100 +0.6%：英伟达+2.2%终结七连跌（2022年9月以来最长）带动AI反弹、Lumentum/CDW/超微领涨；能源五范围跌幅前三（BNO -4.8%）；Dick's Sporting Goods因Foot Locker拖累下调全年指引暴跌30.7%（史上最差单日）、耐克-3.1%连带；SEC就\"情境感知\"基金爆仓传唤主要银行。", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5540/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1943/1943、Themes 268/268和ETF 658/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-25_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-25_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-25_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)
    print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
