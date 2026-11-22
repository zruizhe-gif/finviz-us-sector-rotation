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
    "Rail": "铁路", "Air Cargo": "航空货运", "Maritime": "海运", "Trucking": "卡车运输", "Air Travel": "航空客运", "Industrial IoT": "工业物联网", "Printing": "印刷", "PCs & Devices": "个人电脑与设备",
}

THEME_COMPANY = {
    "ADBE": "Adobe Inc",
    "COHU": "Cohu Inc",
    "ETSY": "Etsy Inc",
    "FWRD": "Forward Air Corp",
    "LULU": "Lululemon Athletica Inc",
    "MRCY": "Mercury Systems Inc",
    "MRVL": "Marvell Technology Inc",
    "NOC": "Northrop Grumman Corp",
    "PLTR": "Palantir Technologies Inc",
    "SNDK": "SanDisk Corp",
    "SIMO": "Silicon Motion Technology Corp ADR",
    "STX": "Seagate Technology Holdings Plc",
    "TRUP": "Trupanion Inc",
    "WERN": "Werner Enterprises Inc",
    "XPO": "XPO Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "SNDK": "SanDisk Corp", "REAL": "The RealReal Inc",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "ADBE": ("直接", "Adobe临财报宣布CEO换帅为内部提拔（Anil Chakravarti），华尔街不买账（'内部任命、外界不满'、分析师称'董事会需换血'），-6.73%列电子商务主题跌幅侧——AI担忧叠加管理层不确定性。（事件时间2026-09-04 11:35 ET起） [Adobe Stock Sinks After Company Names Insider as New CEO](https://finviz.com/news/388101/adobe-stock-sinks-after-company-names-insider-as-new-ceo)"),
    "LULU": ("直接", "Lululemon 9/3盘后财报：Q2营收24.2亿美元不及预期、同店-9%、全年指引年内第二次下调，9/4暴跌-17.38%创2018年以来新低（'八年低点'）——新CEO下周上任接手烂摊子、分析师称修复需6—12个月。（事件时间2026-09-03 16:00 ET盘后） [Lululemon cuts full-year forecast again after Q2 2026 earnings miss](https://finviz.com/news/388060/lululemon-cuts-full-year-forecast-again-after-q2-2026-earnings-miss)"),
    "GWRE": ("直接", "Guidewire Fiscal Q4财报超预期（ARR创纪录增长）但Q1指引疲弱，-19.94%列金融科技主题与All Stocks跌幅首位——'beat estimates but sinking'的指引杀。（事件时间2026-09-03 17:13 ET报道起） [Guidewire shares tumble on weak first quarter guidance](https://finviz.com/news/388045/guidewire-shares-tumble-on-weak-first-quarter-guidance)"),
    "OXM": ("直接", "Oxford Industries（Tommy Bahama/Lilly Pulitzer母公司）下调全年指引，-15.73%列All Stocks可选消费跌幅第三。（事件时间2026-09-04 06:30 ET） [Oxford Industries Shares Fall 14.3% After Full-Year Guidance Cut](https://finviz.com/news/388090/oxford-industries-shares-fall-14.3-after-full-year-guidance-cut)"),
    "TSLA": ("直接", "美国汽车安全监管机构对近1,000辆Cybercab展开调查（正式投放即遭审查、自认证数据受质疑），叠加发布活动'不及预期'的批评，-5.92%列标普500可选消费跌幅第二——与昨日+5.42%完全反转。（事件时间2026-09-04 04:38 ET起） [U.S. auto safety regulator opens probe into nearly 1,000 Tesla Cybercabs](https://finviz.com/news/388125/u.s.-auto-safety-regulator-opens-probe-into-nearly-1000-tesla-cybercabs)"),
    "BBCP": ("直接", "Concrete Pumping Fiscal Q3营收+13%超预期并上调指引，+16.02%列罗素2000工业涨幅前列。（事件时间2026-09-04 01:01 ET） [Concrete Pumping Shares Jump 17.4% After Q3 Results Beat Expectations and Guidance Raised](https://finviz.com/news/388085/concrete-pumping-shares-jump-17.4-after-q3-results-beat)"),
    "NX": ("直接", "Quanex Building Products Fiscal Q3业绩发布（9/3盘后财报+9/4电话会总结），+22.23%列All Stocks与罗素2000工业涨幅前列。（事件时间2026-09-03 16:15 ET） [Quanex Building Products Announces Third Quarter 2026 Results](https://finviz.com/news/388050/quanex-building-products-announces-third-quarter-2026-results)"),
    "CURV": ("直接", "Torrid Holdings Q2财报（子品牌增长）并更新2026财年指引，+9.42%列罗素2000可选消费涨幅第二。（事件时间2026-09-03 16:05 ET） [Torrid Reports Second Quarter 2026 Results and Updates Fiscal 2026 Guidance](https://finviz.com/news/388055/torrid-reports-second-quarter-2026-results-and-updates-fiscal-2026-guidance)"),
    "CHPT": ("直接", "ChargePoint Q2财报电话会：利润率创纪录、零X损耗口径，+8.92%列罗素2000可选消费涨幅第三。（事件时间2026-09-04 15:00 ET） [ChargePoint Holdings Inc (CHPT) (Q2 2027) Earnings Call Highlights](https://finviz.com/news/388140/chargepoint-holdings-inc-chpt-q2-2027-earnings-call-highlights)"),
    "CMND": ("直接", "Clearmind Medicine宣布以250万美元收购无线充电公司Charging Robotics 51%股权，-31.77%列All Stocks医疗保健跌幅第二（微型股跨界并购的稀释/转向担忧）。（事件时间2026-09-04 07:32 ET） [Clearmind Medicine Agrees to Acquire 51% Stake in Charging Robotics for $2.5 Million](https://finviz.com/news/388070/clearmind-medicine-agrees-to-acquire-51-stake-in-charging-robotics)"),
    "SNDK": ("联动", "暂未找到同日直接催化；+11.90%列标普500科技、纳指100科技与半导体主题（九子行业清一色涨）涨幅首位、登顶双指数榜首（年内+600%）——存储器主题+6.31%的大涨日（韩国ETF +4.60%共振），窗口内'看多EPS上修'文章为次要佐证。该股与当日所选科技、半导体的偏强方向一致。"),
    "COIN": ("联动", "暂未找到同日直接催化；-4.18%与比特币回吐（-2.4%簇）方向一致；向SEC申请批准'股票永续合约'（9/3盘后）为创新产品新闻但非当日驱动。该股与当日所选金融科技的偏弱方向一致。"),
    "PYPL": ("联动", "暂未找到同日直接催化；早盘因'500亿美元新收购传闻'冲高，收跌-3.27%为纳指100金融清一色下跌唯一成分——传闻未证实+加密金融回落的合力。该股与当日纳指100金融的偏弱方向一致。"),
    "AMZN": ("联动", "窗口内候选为'亚马逊1,000亿美元Anthropic合同获得便宜45%的引擎'（外链解读）与地产JV（无关）；-0.15%基本持平。该股与当日道指可选消费的表现一致。"),
    "DIS": ("联动", "窗口内候选为无关理财文章；-1.73%为道指通信服务（清一色下跌）领跌成分。该股与当日所选通信服务的偏弱方向一致。"),
    "GOOGL": ("联动", "窗口内候选为Snowflake文章（聚合外链）；-1.17%为道指通信服务（清一色下跌）成分。该股与当日所选通信服务的偏弱方向一致。"),
    "JNJ": ("联动", "窗口内候选为Protolabs CEO访谈（聚合外链）；-1.15%为道指医疗保健（清一色下跌）成分。该股与当日所选医疗保健的偏弱方向一致。"),
    "NKE": ("联动", "窗口内候选全为Lululemon财报的连带报道；-0.95%为道指可选消费（1涨/3跌）成分——运动服饰情绪受Lululemon传染但幅度温和。该股与当日道指可选消费的偏弱方向一致。"),
    "SCHL": ("联动", "暂未找到同日直接催化（唯一候选为财报日期公告、例行）；-6.94%列罗素2000通信服务跌幅首位（无解释下跌，微盘教育股）。该股与当日所选通信服务的偏弱方向一致。"),
    "BKR": ("联动", "获bp海上生产增强与增产服务合同（正面新闻）但-0.22%随能源板块（道指与纳指100清一色下跌）回吐——新闻方向与价格背离。该股与当日所选能源的偏弱方向一致。"),
    "ALAB": ("联动", "窗口内候选为标普500纳入观察文章（标题指向能源股、聚合失真）；+9.75%列纳指100科技涨幅第二——AI连接芯片在半导体清一色上涨日的板块贝塔。该股与当日所选科技的偏强方向一致。"),
    "BETR": ("联动", "公司回应前CEO'不切实际的宏伟计划'（治理闹剧延续）为窗口内新闻；+9.66%列罗素2000金融涨幅第三——微盘治理事件的博弈性定价。该股与当日罗素2000金融的表现一致。"),
    "GPRO": ("联动", "无窗口新闻；+22.30%列All Stocks科技涨幅首位——周一+46%（私营光学光子公司合并转向AI）动能的延续，低流通连续异动，不纳入结构判断。该股与当日所选科技的偏强方向一致。"),
    "AEHR": ("联动", "无窗口新闻（半导体测试设备）；+13.10%列All Stocks科技涨幅第三——半导体清一色上涨日的板块贝塔。该股与当日所选科技的偏强方向一致。"),
    "KPLT": ("联动", "无窗口新闻微盘（先买后付）；+16.18%列All Stocks科技涨幅第二，低流通异动，暂未找到同日直接催化。该股与当日所选科技的偏强方向一致。"),
    "COHU": ("联动", "无窗口新闻（半导体测试）；+10.31%列半导体主题（九子行业清一色涨）第二位。该股与当日所选半导体的偏强方向一致。"),
    "SIMO": ("联动", "无窗口新闻（NAND主控芯片）；+8.70%列半导体主题第三位——存储+6.31%大涨日的核心受益链。该股与当日所选半导体的偏强方向一致。"),
    "MRVL": ("联动", "无窗口新闻；+7.05%列标普500科技与硬件主题涨幅侧——9/1'门槛效应'大跌-10.3%后的持续修复。该股与当日所选科技的偏强方向一致。"),
    "KLAC": ("联动", "无窗口新闻（半导体设备）；+7.32%列标普500科技第二。该股与当日所选科技的偏强方向一致。"),
    "CDTG": ("联动", "无窗口新闻微盘（中概环保技术）；+46.72%列All Stocks工业涨幅首位，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "GRNQ": ("联动", "无窗口新闻微盘；+30.77%列All Stocks工业涨幅第二，低流通异动，暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "ELLO": ("联动", "无窗口新闻微盘（以色列公用事业）；+11.06%列All Stocks公用事业涨幅首位，低流通异动。该股与当日所选公用事业的偏强方向一致。"),
    "NRG": ("联动", "无窗口新闻；+6.42%列All Stocks公用事业涨幅第二、标普500公用事业涨幅首位——AI电力需求的独立发电商叙事（与Constellation +4.88%、Vistra +3.52%同步），公用事业内的'AI电力'子集独立于类债主体。该股与当日所选公用事业的结构分化一致。"),
    "BTAI": ("联动", "无窗口新闻微盘（神经精神药物）；-37.11%列All Stocks医疗保健跌幅首位，低流通崩跌，暂未找到同日直接催化。该股与当日所选医疗保健的偏弱方向一致。"),
    "CDT": ("联动", "无窗口新闻微盘；-16.56%列All Stocks医疗保健跌幅第三，低流通崩跌，暂未找到同日直接催化。该股与当日所选医疗保健的偏弱方向一致。"),
    "CHAI": ("联动", "无窗口新闻微盘（Core AI Holdings，8/28曾+57%）；-9.97%列All Stocks通信服务跌幅首位——双向极端波动个体。该股与当日所选通信服务的偏弱方向一致。"),
    "GCL": ("联动", "无窗口新闻微盘（中概）；-9.88%列All Stocks通信服务跌幅第二——前两日连续大涨的回吐。该股与当日所选通信服务的偏弱方向一致。"),
    "VIOT": ("联动", "无窗口新闻微盘（中概智能家居）；-16.18%列All Stocks可选消费跌幅第二。该股与当日所选可选消费的偏弱方向一致。"),
    "XEL": ("联动", "无窗口新闻；-0.81%列纳指100公用事业（1涨/3跌）跌幅侧——独立电力商与类债公用事业的分化。该股与当日公用事业内部分化结构一致。"),
    "AEP": ("联动", "无窗口新闻；-0.17%为纳指100公用事业偏弱端，同上分化。"),
    "LVWR": ("联动", "无窗口新闻（电动摩托）；+11.30%列罗素2000可选消费涨幅首位（146/190上涨的小盘消费修复日）。该股与当日罗素2000可选消费的偏强方向一致。"),
    "GOLD": ("联动", "无窗口新闻微盘（Gold.com）；+11.21%列罗素2000金融涨幅第二——贵金属回落日的个体异动，暂未找到同日直接催化。该股与当日罗素2000金融的表现一致。"),
    "CD": ("联动", "无窗口新闻微盘（数字资产）；+11.81%列罗素2000金融涨幅首位——比特币回吐日的逆势个体，低流通异动。该股与当日罗素2000金融的表现一致。"),
    "FWRD": ("联动", "无窗口新闻（货运）；+9.69%列运输与物流主题（等权+1.14%）涨幅首位。该股与当日所选运输与物流的偏强方向一致。"),
    "XPO": ("联动", "窗口内候选为'8月运营数据与Q3指引一致'（正面校验）；+4.49%列运输与物流主题第二位。该股与当日所选运输与物流的偏强方向一致。"),
    "OABI": ("联动", "无窗口新闻微盘（抗体平台）；-8.84%列罗素2000医疗保健跌幅首位。该股与当日所选医疗保健的偏弱方向一致。"),
    "VRT": ("联动", "无窗口新闻（数据中心机电）；+4.35%列标普500工业涨幅首位——AI电力建设链的回归日。该股与当日所选工业的偏强方向一致。"),
    "HONA": ("联动", "无窗口新闻（霍尼韦尔航空航天分拆主体）；+3.90%列标普500工业第二。该股与当日所选工业的偏强方向一致。"),
    "ETN": ("联动", "无窗口新闻（电气设备）；+3.46%列标普500工业第三。该股与当日所选工业的偏强方向一致。"),
    "CEG": ("联动", "无窗口新闻；+4.88%列标普500公用事业与纳指100公用事业涨幅首位——AI电力独立发电商（与NRG、Vistra同步）。该股与当日所选公用事业的结构分化一致。"),
    "VST": ("联动", "无窗口新闻（独立电力）；+3.52%列标普500公用事业第三。该股与当日所选公用事业的结构分化一致。"),
    "DASH": ("联动", "无窗口新闻；-4.63%列标普500可选消费跌幅侧。该股与当日所选可选消费的偏弱方向一致。"),
    "VEEV": ("联动", "无窗口新闻；-3.27%列标普500医疗保健（8涨/51跌）跌幅首位。该股与当日所选医疗保健的偏弱方向一致。"),
    "MRNA": ("联动", "无窗口新闻；-2.23%列标普500医疗保健第二（前日遭降卖出的延续）。该股与当日所选医疗保健的偏弱方向一致。"),
    "VRTX": ("联动", "无窗口新闻；-2.12%列标普500医疗保健第三。该股与当日所选医疗保健的偏弱方向一致。"),
    "APA": ("联动", "无窗口新闻；-3.19%列标普500能源跌幅首位。该股与当日所选能源的偏弱方向一致。"),
    "XOM": ("联动", "无窗口新闻；-1.69%列标普500能源第三。该股与当日所选能源的偏弱方向一致。"),
    "CAT": ("联动", "无窗口新闻；+1.73%为道指工业（清一色上涨）领涨成分。该股与当日所选工业的偏强方向一致。"),
    "HON": ("联动", "无窗口新闻；+0.95%为道指工业（清一色上涨）成分。该股与当日所选工业的偏强方向一致。"),
    "BA": ("联动", "无窗口新闻；+0.83%为道指工业（清一色上涨）成分。该股与当日所选工业的偏强方向一致。"),
    "HD": ("联动", "无窗口新闻；+0.94%为道指可选消费（1涨/3跌）唯一上涨成分。该股与当日道指可选消费的分化一致。"),
    "CCEP": ("联动", "无窗口新闻；-3.11%列纳指100必需消费（清一色下跌）首位。该股与当日必需消费的偏弱方向一致。"),
    "KHC": ("联动", "无窗口新闻；-2.24%列纳指100必需消费（清一色下跌）第二。该股与当日必需消费的偏弱方向一致。"),
    "PEP": ("联动", "无窗口新闻；-1.71%列纳指100必需消费（清一色下跌）第三。该股与当日必需消费的偏弱方向一致。"),
    "NBIS": ("联动", "无窗口新闻（AI云）；+7.48%列纳指100科技涨幅侧。该股与当日所选科技的偏强方向一致。"),
    "CSX": ("联动", "无窗口新闻；+0.86%列纳指100工业（8涨/5跌）侧。该股与当日所选工业的偏强方向一致。"),
    "CURI": ("联动", "无窗口新闻微盘（流媒体）；-6.55%列罗素2000通信服务第二。该股与当日所选通信服务的偏弱方向一致。"),
    "DJT": ("联动", "无窗口新闻；-5.25%列罗素2000通信服务第三。该股与当日所选通信服务的偏弱方向一致。"),
    "NERV": ("联动", "无窗口新闻微盘；-5.54%列罗素2000医疗保健跌幅侧。该股与当日所选医疗保健的偏弱方向一致。"),
    "CTNM": ("联动", "无窗口新闻微盘；-4.95%列罗素2000医疗保健跌幅侧。该股与当日所选医疗保健的偏弱方向一致。"),
    "VAL": ("联动", "无窗口新闻（海工钻井）；-3.34%列罗素2000能源跌幅首位。该股与当日所选能源的偏弱方向一致。"),
    "SM": ("联动", "无窗口新闻（油气）；-3.09%列罗素2000能源第二。该股与当日所选能源的偏弱方向一致。"),
    "HPK": ("联动", "无窗口新闻（油气）；-2.90%列罗素2000能源第三。该股与当日所选能源的偏弱方向一致。"),
    "STX": ("联动", "无窗口新闻（硬盘）；+6.35%列硬件主题涨幅侧——存储链大涨日。该股与当日所选科技、硬件的偏强方向一致。"),
    "ETSY": ("联动", "无窗口新闻；-6.73%列电子商务主题（清一色下跌）第二（与Adobe的软件跌幅同位）。该股与当日所选电子商务的偏弱方向一致。"),
    "TRUP": ("联动", "无窗口新闻（宠物保险）；-3.44%列金融科技主题（清一色下跌）第三。该股与当日所选金融科技的偏弱方向一致。"),
    "PLTR": ("联动", "无窗口新闻；-4.49%列国防与航空航天主题（清一色下跌）首位——昨日+7.71%的回吐。该股与当日所选国防与航空航天的偏弱方向一致。"),
    "MRCY": ("联动", "无窗口新闻（国防电子）；-2.70%列国防主题第二。该股与当日所选国防与航空航天的偏弱方向一致。"),
    "NOC": ("联动", "无窗口新闻；-2.51%列国防主题第三。该股与当日所选国防与航空航天的偏弱方向一致。"),
    "TITN": ("联动", "无窗口新闻（农机经销）；+14.85%列罗素2000工业涨幅第三——财报季的农机链修复（Deere获上调背景延续），暂未找到同日直接催化。该股与当日所选工业的偏强方向一致。"),
    "WERN": ("联动", "无窗口新闻（货运）；+4.00%列运输与物流主题第三位。该股与当日所选运输与物流的偏强方向一致。"),
    "MRK": ("联动", "该股与当日道指医疗保健（清一色下跌）的表现一致（-1.32%列第二跌幅）。"),
    "AMGN": ("联动", "该股与当日道指医疗保健（清一色下跌）的表现一致（-1.55%领跌）。"),
    "FANG": ("联动", "该股与当日所选能源的偏弱方向一致（-1.83%，道指与纳指100能源清一色下跌成分）。"),
    "SHW": ("联动", "该股与当日道指基础材料（清一色上涨）唯一成分微涨入选一致（+0.44%）。"),
    "CVX": ("联动", "该股与当日所选能源的偏弱方向一致（-1.29%，道指能源清一色下跌唯一成分）。"),
    "HTOO": ("联动", "无窗口新闻微盘（绿氢）；+7.69%列All Stocks公用事业涨幅第三，低流通异动。该股与当日所选公用事业的偏强方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "PTF", "perf": 5.243, "form": "交易所交易基金", "exposure": "美国科技动量（Dorsey Wright）",
         "reason": "科技动量ETF领涨全市场：半导体主题九子行业清一色上涨（存储+6.31%、SanDisk +11.90%登顶双指数榜首）、科技动量因子满仓受益——动量因子篮与半导体行业篮为不同敞口层。合并删除：TECL（杠杆产品，排除）。"},
        {"ticker": "EWY", "perf": 4.602, "form": "交易所交易基金", "exposure": "韩国股票",
         "reason": "韩国ETF：存储器主题+6.31%的全球映射（韩国为存储双雄所在地）——独立地域敞口，AI硬件链的亚洲分支。合并删除：AIA、AAXJ、EWT（同簇亚太宽基/国别中更弱者，保留最强单一国家EWY）。"},
        {"ticker": "SOXX", "perf": 3.517, "form": "交易所交易基金", "exposure": "全球半导体",
         "reason": "半导体行业ETF：存储链领涨（SanDisk +11.90%、Silicon Motion +8.70%、Seagate +6.35%）、半导体九子行业清一色上涨——行业篮区别于动量因子篮。合并删除：XSD、SMH（同簇半导体行业，保留最强一只SOXX）。"},
    ],
    "down": [
        {"ticker": "ETHA", "perf": -2.629, "form": "交易所交易基金", "exposure": "以太坊现货",
         "reason": "以太坊ETF领跌全市场：比特币回吐日（数月来首次重上8万美元后回落）的加密全线回撤，以太坊为独立代币资产。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "FBTC", "perf": -2.528, "form": "交易所交易基金", "exposure": "比特币现货（富达）",
         "reason": "比特币ETF：周四+5.8%簇的当日回吐（-2.4%至-2.5%）——8万美元得而复失，加密金融链（Coinbase -4.18%）同步回落。合并删除：BITO、IBIT、ARKB、BITB、GBTC（同簇比特币价格敞口，保留最强一只FBTC）。"},
        {"ticker": "GDXJ", "perf": -2.494, "form": "交易所交易基金", "exposure": "全球金矿（中小型）",
         "reason": "中小金矿ETF：黄金-0.84%回吐两日反弹、钯金-1.86%——贵金属修复中断（与加密回撤同日，风险偏好的反向扰动）。合并删除：SGDM、GDX（同簇金矿股，保留最强一只GDXJ）。"},
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
        text = "核查9月3日盘后至9月4日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-04"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；半导体行业簇（SOXX/XSD/SMH）保留SOXX、比特币簇（FBTC/BITO/IBIT/ARKB/BITB/GBTC）保留FBTC、金矿股簇（GDXJ/SGDM/GDX）保留GDXJ、亚太宽基簇（EWY/AIA/AAXJ/EWT）保留单一国家最强EWY。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-04_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-04_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月4日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月4日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：非农Jobs Friday（劳工节长周末前最后交易日）：8月非农+16.2万约为共识三倍（共识约5.5万、超调查最高预估12.5万）、失业率4.1%持平、68.3万人涌入劳动力——'好消息变坏消息'，市场转向定价9月加息（口径50%—60%）、2年期+3至4bp至4.37%、10年期4.78%本周两度破4.8%、30年期5.25%处2007年以来最高附近，标普500收跌约0.4%结束两连涨（但纳指独涨、罗素2000逆势+0.25%，NYSE涨跌比1.07显示广度未垮）。当日最强主线是存储与半导体：半导体主题九子行业清一色上涨（存储器+6.31%——SanDisk +11.90%登顶双指数榜首（年内+600%）、KLA +7.32%、Marvell +7.05%）、韩国ETF +4.60%（存储双雄映射）、科技动量ETF +5.24%领涨全市场；工业与AI电力链回归（五个范围中的四个进入涨幅前三、道指工业清一色：卡特彼勒+1.73%；Vertiv +4.35%、Eaton +3.46%；独立发电商NRG +6.42%、Constellation +4.88%、Vistra +3.52%——公用事业内部的'AI电力'子集独立走强）。跌幅侧三条线：可选消费遭财报与监管双杀（Lululemon二连降指引-17.38%创2018年以来新低、Oxford降指引-15.73%、特斯拉Cybercab遭安全调查-5.92%——与昨日+5.42%完全反转）；医疗保健标普成分8涨/51跌（道指四成分清一色跌、微盘BioXcel -37.11%崩跌）；能源连续第二日回吐（道指与纳指100清一色下跌）。主题层：半导体与硬件清一色上涨对电子商务、金融科技、国防、老龄化四个清一色下跌——周四'软件上线'当日切换为'芯片回归'（IGV -2.23%、XSW -2.30%、WCLD -2.98%的跷跷板）；比特币回吐-2.4%（8万美元得而复失、以太坊-2.63%领跌ETF）、金矿-2.49%贵金属修复中断。个股事件流：Adobe临财报内部提拔CEO遭抛售-6.73%、Guidewire指引杀-19.94%、AMC与Robinhood爆发代币化股票之争、白宫（CEA主席称核心PCE三个月年化3.0%'看不到加息理由'）与市场定价正面分歧。",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5526/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1938/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (OUT / "finviz_2026-09-04_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-04_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-04_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
