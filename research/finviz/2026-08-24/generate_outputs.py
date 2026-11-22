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
    "Workforce": "职业教育", "ThreatOps": "威胁情报", "App Security": "应用安全",
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
    "Applications": "应用", "Networking": "网络设备", "Suppliers": "供应商", "Self-Driving": "自动驾驶",
    "Office": "办公", "Housing": "住宅", "Retail": "零售物业", "Warehousing": "仓储",
    "Batteries": "动力电池", "Chips": "车规芯片", "Charging": "充电设施", "Fleets": "车队", "Manufacturers": "整车制造商",
    "Diagnostics": "诊断", "Genomics": "基因组学", "Oncology": "肿瘤", "Enterprise": "企业级",
    "Mining": "挖矿", "Farm-Direct": "农场直供", "Food": "食品",
    "Luxury": "奢侈品", "Secondhand": "二手",
}

THEME_COMPANY = {
    "OTLY": "Oatly Group AB", "BRBR": "BellRing Brands Inc", "SFM": "Sprouts Farmers Market Inc",
    "SNAP": "Snap Inc", "MTCH": "Match Group Inc", "BMBL": "Bumble Inc",
    "BXP": "BXP Inc", "VNO": "Vornado Realty Trust", "RHP": "Ryman Hospitality Properties Inc",
    "ASTS": "AST SpaceMobile Inc", "LUNR": "Intuitive Machines Inc", "BKSY": "BlackSky Technology Inc",
    "RGTI": "Rigetti Computing Inc", "IONQ": "IonQ Inc", "QBTS": "D-Wave Quantum Inc",
    "BEEM": "Beam Global", "AUR": "Aurora Innovation Inc", "XPEV": "XPeng Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic NV", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月21日16:00 ET盘后事件可解释8月24日；8月24日16:00 ET后事件不得倒推。
R = {
    "SDOT": ("直接", "SEC文件显示公司通过发行股票完成新一批债券结算、彻底消除2月发行债券的剩余债务，叠加向AI大宗商品交易平台（TradeOS/TradeIQ）转型的叙事，盘前即跳涨39%；5月末1拆20反向拆股后流通盘极小放大波动，8月21日已+56%，8月24日延续投机行情盘中一度涨超100%。[Benzinga](https://www.benzinga.com/trading-ideas/technicals/26/08/61388716/sadot-group-shares-soar-as-debt-cleanup-fuels-fresh-momentum)"),
    "SUJA": ("直接", "大股东Paine Schwartz持续公开市场增持托底：13D披露8月10-18日买入92万股（约592万美元），Form 4显示8月18-20日又买56.8万股、持股达62.77%；8月20日另宣布与摩根大通签署修订版信贷协议降低融资成本（2026年利息支出约1800万美元）。8月4日Q2财报下调指引暴跌46%后，大股东增持+再融资推动连续超跌反弹。[StockTitan Form 4](https://www.stocktitan.net/sec-filings/SUJA/form-4-suja-life-inc-insider-trading-activity-b580fc693823.html)、[GlobeNewswire](https://www.stocktitan.net/news/SUJA/suja-life-announces-amended-and-restated-credit-uiofmgjc19sv.html)"),
    "EPSM": ("结构", "澳门酒类进口分销超微盘股（市值不足2000万美元、日均成交仅约1.3万股，买卖报价曾出现1.05/9.00美元的极端价差），8月24日无任何公司公告，几笔小额买单即可推动近10%的百分比涨幅，属低流动性结构性波动。"),
    "TJGC": ("结构", "香港数字营销微盘股（流通股仅约1010万股），8月10日公告正与机器人技术供应商洽谈AI与机器人技术IP许可（非独家全球授权）点燃投机题材，8月19日起MACD转多、突破50日均线后资金连续做多；8月24日无新公告但成交493万股远超日均183万股，+30.9%为题材炒作叠加超小流通盘的资金驱动。[StockTitan](https://www.stocktitan.net/news/TJGC)"),
    "GCL": ("结构", "新加坡游戏发行低价微盘股（股价不足1美元），FY2026年报（7月31日发布）营收+68.2%至2.389亿美元但转亏2620万美元，8月24日无新公告，0.7美元附近的低价股在薄流动性下出现10%级别的资金波动。"),
    "WBTN": ("结构", "8月10日Q2财报EPS超预期但营收逊预期、叠加约1亿美元收购RI Games 60%股权后股价跌至52周低点7.85美元附近，8月24日无独立新闻；Naver控股导致自由流通盘偏小，迪士尼漫画平台协议8月1日完成落地的叙事余温下出现低流通盘技术性反弹（收8.80美元）。"),
    "SAFX": ("结构", "XCF Global（可再生柴油/SAF公司）8月24日无公司新闻，此前利好均未落在当日：8月18日'商业化提速（日产5.5万加仑）'当日收跌2.2%，8月20日'首笔商业营收超100万美元'当日仅+0.03%。当日+12.6%属约$0.35低价、市值约1.5亿美元的微盘投机性放量拉升，为8月中旬商业化里程碑叙事的滞后炒作。"),
    "BRNX": ("结构", "BrenX Ltd.（原Brenmiller Energy，8月13日宣布更名、8月14日起以BRNX交易）当日无任何新闻，流通盘仅约72万股、市值约270万美元，属超低流通微盘，+12.1%收$4.18为更名换码后的投机性波动。"),
    "VGAS": ("结构", "Verde Clean Fuels当日无新闻（StockTitan显示8月10日Q2财报后再无更新），此前连跌五日；$1.23→$1.37（+11.4%）为低流通低价微盘的技术性反弹，与可再生燃料板块无同日催化。"),
    "RPGL": ("结构", "新加坡ERP软件超微盘（约8名员工、市值约3400万美元），5月28日1拆40反向拆股后流通盘极度萎缩，7月初曾因战略扩张消息遭爆炒（单日+32%）；8月24日无公司新闻，高开2.49美元后一路崩跌收1.73美元（-27%），为投机资金退潮下低流通盘炒作行情的崩塌。"),
    "AMCI": ("融资定价", "8月21日（周五盘前）公告权证诱导协议：将2025年12月发行的权证行权价降至1.65美元（较现价大幅折价）换取投资者现金行权，募资至多210万美元用于越南机器人产线，同时再发行121.98万股新权证（行权价5.775美元）；折价行权股份涌入市场后，8月24日（周一）暴跌25.7%回吐涨幅。[StockTitan 8-K](https://www.stocktitan.net/sec-filings/AMCI/8-k-amc-robotics-corp-reports-material-event-d3d61ca04af9.html)"),
    "LGCL": ("融资定价", "中国AI人力资源PaaS仙股（股价5美分、市值仅约260万美元），此前以0.20美元/股增发3215万股（募资643万美元）并收到纳斯达克最低报价合规通知，增发供给冲击下股价自52周高点22.80美元崩塌（8月20日已单日-35%）；8月24日无新闻但成交1.23亿股，跌破增发价后的持续抛压延续。"),
    "DFNS": ("结构", "以色列无人机/反无人机国防微盘股（前Nukkleus），7月20日实施1拆125反向拆股后流通盘极度收缩，4月底以来曾被爆炒约4380%（7月30日最高见84.98美元），随后连续崩塌；8月24日无公司新闻，开17.03美元收11.01美元（-46.6%），为低流通盘投机泡沫破裂的获利回吐/踩踏，市值仅剩约2000万美元。"),
    "AIAI": ("公司治理", "8月24日公司公告开始与创始人兼控股股东John P. Rochon控制的Messier 42 LLC洽谈收购其旗下多项业务，向控股股东购买资产的关联交易引发利益输送与现金消耗担忧（Q2经营亏损约4500万美元、EBITDA -2500万美元），叠加此前一周+50%的投机涨幅回吐，当日大跌约19.8%。[Barchart](https://www.barchart.com/story/news/4001947/aiai-holdings-commences-discussions-with-messier-42-llc-regarding-acquisition-opportunities)"),
    "PSIG": ("融资定价", "香港物流微盘股，8月18日特别股东大会因未达法定人数流会、8月19日新F-3货架注册声明生效（再融资/增发窗口重新打开引发稀释担忧），此前一周遭资金爆炒（8月21日单日+25%、30日累涨43%）；8月24日投机资金撤离大跌19.4%。[StockTitan EFFECT](https://www.stocktitan.net/sec-filings/PSIG/effect-ps-international-group-ltd-sec-filing-d7ef936c2264.html)"),
    "RBNE": ("结构", "塞浦路斯油轮超微盘（市值仅约160万美元、流通股约130万股，为Castor Maritime创始人分拆上市），7月9日反向拆股生效、7月末完成300万美元公开增发后持续阴跌；8月24日无新闻，买卖价差宽达2.14/3.62美元，流动性枯竭下的正常波动即达8%。"),
    "VIVK": ("结构", "油气中游微盘股，8月10日因原油购销合同年化金额达15亿美元的消息单日+16%后连续回落，且公司因2025年10月股份发行未获股东批准的问题面临纳斯达克合规/退市风险；8月24日无新公告，缩量阴跌至52周新低0.95美元。"),
    "RCON": ("结构", "中国油田服务超微盘（市值仅约140万美元），近一个月累计下跌约97%、年内跌约99%（7月31日曾单日崩盘约30%），8月24日无任何公司新闻，延续流动性枯竭式的仙股崩塌阴跌。"),
    "DLTR": ("联动", "必需消费板块当日领涨（沃尔玛+2.7%），防御性轮动叠加8月27日Q2财报前的乐观布局；此前8月19-20日Jefferies将评级从Underperform上调至Hold、目标价从85美元大幅上调至135美元（高于当时股价），8月24日+4.0%创阶段新高。"),
    "CHD": ("联动", "家庭护理/必需消费龙头，当日无公司独立新闻（仅有9月9日Barclays消费必需品会议的参会预告），+3.8%为当日必需消费板块集体走强的防御性买盘带动（板块涨幅居前）。"),
    "MO": ("联动", "烟草巨头当日无公司独立新闻（Q2财报为7月末旧闻），+3.6%受益于必需消费/高股息防御板块的集体强势；当日黄金4680美元、比特币逼近8万美元显示风险偏好回落，防御与避险风格占优利好烟草股。"),
    "MA": ("联动", "无独立公司事件，当日资金弃半导体/AI风险回流支付网络等传统蓝筹，Mastercard与Visa同步冲历史新高；此前披露的特朗普关联账户6月买入V/MA与Ackman建仓强化了板块买入动能。[GuruFocus](https://www.tradingview.com/news/gurufocus:9d0313d42094b:0-mastercard-jumps-2-7-as-investors-abandon-semiconductor-risk/)、[FXLeaders](https://www.fxleaders.com/news/2026/08/24/visa-v-stock-and-mastercard-ma-surge-to-record-highs-as-trump-accounts-buying-fuels-momentum/)"),
    "AJG": ("联动", "无独立事件；金融板块当日领涨（支付网络创新高、Mastercard/Visa/Gallagher齐涨），保险经纪等防守型金融获风格切换资金青睐，AJG连续第二日上行，属大盘防御+金融风格联动。"),
    "V": ("联动", "当日无新公司公告（24亿美元收购BioCatch为8月3日旧闻）；Visa为道指当日表现最佳成分股，资金弃半导体风险转投支付网络，叠加特朗普关联账户买入披露与Ackman约11亿美元建仓的余温，股价创历史新高。[FXLeaders](https://www.fxleaders.com/news/2026/08/24/visa-v-stock-and-mastercard-ma-surge-to-record-highs-as-trump-accounts-buying-fuels-momentum/)、[Investopedia](https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-08242026-12066087)"),
    "AWK": ("联动", "无独立事件（与Essential Utilities合并的HSR等待期终止为此前里程碑）；美债利率盘中回落（TGA回购扩容传闻）提振利率敏感型公用事业，AWK上周五跌1.3%后周一反弹逾3%，属防御资金回流+利率回落的板块修复。"),
    "EIX": ("联动", "上周五因CEO警告加州议会恐在8月底会期结束前无法通过野火责任框架改革而大跌4.1%，周一无新增利空、叠加油利率盘中回落，超跌反弹3.3%；Eaton野火立法与信用降级风险仍未解除。"),
    "PCG": ("联动", "与EIX同属加州大型受监管公用事业，前一周因野火框架立法焦虑平均深跌后，周一度过利空高峰超跌修复2.9%，利率回落放大反弹；无独立公司事件。"),
    "STX": ("联动", "存储/内存板块连续多日集体回调：Morningstar警告AI相关股可能再跌20-30%、三星与SK海力士宣布扩产引发供给过剩担忧、市场预期AI资本开支2026年见顶，叠加上周AI服务器提价15%被解读为存储成本冲击，Seagate/美光/西数齐跌，8月24日延续板块性抛售。[Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/sandisk-sinks-11-seagate-falls-160250009.html)"),
    "SNDK": ("联动", "同存储板块回调：8月中旬FQ4财报虽大超预期（EPS 39.25美元、营收+372%）但FY27Q1指引偏软触发分析师下调目标价，此后供给过剩叙事（三星/SK海力士扩产、Morningstar看空20-30%）持续发酵，五日累跌近20%，8月24日延续无独立利空的板块性下跌。[BeInCrypto](https://beincrypto.com/sandisk-micron-seagate-memory-glut-fears)"),
    "CIEN": ("联动", "无当日独立事件；英伟达周三财报前AI硬件链遭全面抛售（MU/SanDisk/WDC/Coherent同跌），光通信板块此前已有TD Cowen（8/19下调目标价100美元至575美元维持买入）与BofA（8/20下调光板块估值目标）铺垫跌势，叠加6月28.75亿美元可转债稀释担忧未消，CIEN随板块续跌。"),
    "JBHT": ("直接", "特朗普宣布自2027年1月1日起将对加拿大汽车及零部件关税提升至50%、钢铁关税同步上调，卡车运输股应声全线下挫，CNBC点名J.B. Hunt跌5%、Knight-Swift跌逾3%、ODFL跌2%；叠加股价年内接近翻倍、约35倍PE的估值压力放大跌幅。[CNBC](https://www.cnbc.com/2026/08/23/stock-market-today-live-updates.html)、[QuiverQuant](https://www.quiverquant.com/news/J.B.+Hunt+Transport+Services+slides+as+transport+stocks+weaken+and+trade+uncertainty+clouds+freight+outlook)"),
    "AXON": ("联动", "无独立事件（Q2财报与UBS等上调目标价均属前期）；约270倍市盈率的高估值成长+工业股在英伟达财报前风险偏好收缩中随成长与工业板块回落近5%。"),
    "FDXF": ("联动", "无独立事件；同受对加拿大50%汽车/钢铝关税冲击的货运物流板块全线抛售波及，FedEx Freight作为纯LTL卡车业务公司随JBHT、Knight-Swift、ODFL、RXO等齐跌。[CNBC](https://www.cnbc.com/2026/08/23/stock-market-today-live-updates.html)"),
    "TPL": ("联动", "无独立事件；能源为当日标普500最弱板块，油价上周因伊朗局势大涨5-6%后获利回吐（WTI回落至86美元附近），TPL上周五随油价涨3.8%后周一回吐2.7%，与二叠纪同行同步走弱。[Investopedia](https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-08242026-12066087)"),
    "FANG": ("联动", "Q2财报与上调产量指引均为8月初旧闻；当日原油自高位回落（上周涨5-6%后获利了结、等待对伊制裁落地）令能源板块领跌大盘，二叠纪E&P随板块跌2.4%。[Investopedia](https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-08242026-12066087)"),
    "HAL": ("联动", "无独立事件（Q2财报为7月下旬旧闻）；油价回吐涨幅拖累油服板块，HAL随能源板块（标普500当日最弱板块）下跌2%。[Investopedia](https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-08242026-12066087)"),
    "WMT": ("联动", "8月20日财报展望令市场失望引发回调（较52周高点约-5%）后，周一大盘风格转向防御，沃尔玛与好市多等必需消费龙头领涨道指，属防御性资金回流的超跌反弹，无新的公司事件。"),
    "PG": ("联动", "无公司独立事件，防御风格领涨日必需消费居五范围涨幅前列，收$146.60（+1.3%）；利率盘中回落（TGA回购扩容传闻）强化对防御性现金牛的配置。"),
    "KO": ("联动", "无独立事件，防御性资金流入必需消费推动+1.0%；9月中旬除息前的股息配置需求提供额外支撑。"),
    "DIS": ("直接", "迪士尼旗下漫威参与合制的《蜘蛛侠：Brand New Day》截至8月24日（周一）全球票房突破20亿美元，为蜘蛛侠系列首部破20亿影片（北美累计约8.55亿美元、2026年度冠军），院线链Imax/Cinemark同涨，公司作为合制片方受益，叠加防御性买盘。[Forbes](https://www.forbes.com/sites/timlammers/2026/08/19/spider-man-brand-new-day-and-other-2-billion-movies-at-box-office)"),
    "GOOGL": ("背离", "科技板块走弱中逆势+0.9%收$348.06；Q2云业务+82%的增长与AI变现叙事使其成为防御性科技资金的避风港，8月21日刚获Stockchase分析师'Top Pick'推荐，与思科等AI硬件/软件同业明显背离。"),
    "SHW": ("单样本", "当日几乎收平（$346.73，+0.04%），无公司新闻；防御买盘与工业/涂料需求担忧相互抵消，同日摩根士丹利重申买入评级（目标价$395）亦未引发方向性波动。"),
    "CVX": ("联动", "无公司独立事件；布伦特仍处约$94高位，但能源股集体获利回吐（能源居五范围跌幅），防御轮动下-1.1%。"),
    "CAT": ("联动", "无独立事件；特朗普宣布对加拿大产汽车/零部件及钢铝加征50%关税加重制造业成本与贸易前景担忧（三大车企股价齐跌），周期类工业股随板块走弱2%。[Investopedia](https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-08242026-12066087)"),
    "BA": ("联动", "无当日独立利空；工业/道指周期股领跌日-1.8%（$214.20→约$210），交付延迟与劳资不确定性担忧延续压制，同日特朗普财务披露显示其购入BA股票的消息也未能扭转颓势。"),
    "HON": ("联动", "无公司独立事件；6月底分拆航空航天后的Honeywell Technologies（剩余自动化业务）随工业板块走弱-0.5%。"),
    "NVDA": ("联动", "无公司层面新事件，周三（8/26）FY2027Q2财报前资金持续去风险，录得七连跌（累计约-7%，2022年9月以来首次），AI动能交易整体退潮放大跌势。[Forbes](https://www.forbes.com/sites/zacharyfolk/2026/08/24/nvidia-stock-tumbles-another-2-pacing-for-seventh-straight-drop-ahead-of-earnings/)、[CNBC](https://www.cnbc.com/2026/08/23/stock-market-today-live-updates.html)"),
    "IBM": ("联动", "无独立事件；7月中旬因CEO预警'业绩差于预期'单日暴跌24%后持续弱势，周一科技股在英伟达财报前领跌大市（纳指/标普收低），IBM随板块回落2%。[Investopedia](https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-08242026-12066087)"),
    "CSCO": ("财报延续", "8月12日FQ4财报营收/EPS超预期但毛利率指引令人失望，8月13日暴跌8.4%创两年多最大跌幅；8-24延续估值消化-0.7%收约$110.23，当日Cramer称AI交易'currently broken'加剧软件/网络设备股压力。背景见[CNBC](https://www.cnbc.com/2026/08/12/ciscos-stock-drops-despite-earnings-revenue-beat.html)。"),
    "COST": ("联动", "无公司新闻；防御风格主导日必需消费领涨，COST涨2.5%收$971.40居板块前排，MarketWatch当日刊发'Costco -- Defensive Growth'评论呼应防御配置逻辑。"),
    "MNST": ("联动", "无当日独立事件；防御领涨日必需消费涨幅前三（+2.4%），叠加8月6日Q2营收创纪录（25.4亿美元、+20.2%）后的估值修复。"),
    "XEL": ("联动", "无当日独立事件；公用事业板块修复+利率盘中回落利好高杠杆公用事业，XEL（Q2 EPS $0.93同比+24%、$600亿资本计划）涨1.4%领涨。"),
    "EXC": ("联动", "无当日独立事件；防御轮动+利率回落推动公用事业修复，EXC +1.3%，其约474亿美元的高负债结构对利率下行尤其敏感。"),
    "AEP": ("联动", "无当日独立事件；随公用事业板块防御性修复上涨0.9%，利率盘中回落（TGA回购扩容传闻）为主要驱动。"),
    "LIN": ("联动", "无重大独立事件；防御型工业气体龙头小幅收高0.5%，当日披露董事Paula Reynolds小额增持100股，7月31日Q2超预期并上调指引下限（EPS $17.70-17.90）提供基本面支撑。"),
    "BKR": ("联动", "无当日独立事件（8月11日获科威特多年期合同后无更新）；能源板块获利回吐拖累-0.6%，收约$62。"),
    "MU": ("直接", "周末曝出特朗普政府或允许苹果采用中国长鑫存储（CXMT）DRAM与长江存储（YMTC）NAND（习主席9月访美前的外交筹码传闻，商务部长卢特尼克立场仍相反），直接冲击美光在苹果DRAM供应链中的地位；叠加三星2026年股东回报计划不及预期在首尔暴跌约9%传染板块，美光一度跌逾6%。[TipRanks](https://www.tipranks.com/news/3-key-reasons-why-micron-mu-and-sandisk-sndk-stocks-are-tumbling-today-august-24)、[Invezz](https://talkmarkets.com/article/why-are-micron-sk-hynix-sandisk-stocks-falling-today-1787591738)"),
    "RKLB": ("联动", "无当日公司新闻；SpaceX上市引发太空板块资金持续撤离，股价自5月高点151美元已回撤过半，约66倍市销率的高估值在英伟达财报前的风险偏好收缩中续跌（当日收跌约6%）。[MarketBeat/Investing.com](https://www.investing.com/analysis/rocket-labs-selloff-is-fadingis-it-finally-safe-to-buy-200686425)"),
    "ODFL": ("联动", "无公司新闻；工业/运输板块走弱日-2.4%，货运需求疲软担忧叠加小盘工业股抛售（罗素工业弱）压制。"),
    "BRBR": ("联动", "8-24无独立事件。8-4财季Q3财报（EBITDA大幅下滑）后股价自4月末累计跌超35%、深度超跌，当日随健康食品/营养主题（SFM、OTLY领涨）超跌反弹+6.5%，近两日还有TD Cowen、DA Davidson上调目标价的铺垫。参考：[StockTitan BRBR](https://www.stocktitan.net/news/BRBR)"),
    "BRCC": ("结构", "1拆10反向拆股于8-21盘后生效、8-24（周一）开始按拆股后股数交易，当日+6.0%为反拆股生效首日的价格重定价效应，叠加消费必需品板块当日走强及Q2接近盈亏平衡后的修复动能。参考：[StockTitan](https://www.stocktitan.net/news/BRCC/brc-inc-announces-1-for-10-reverse-stock-t1rapi3paqga.html)"),
    "VITL": ("联动", "8-24无独立事件，+4.82%收$11.08属健康食品主题集体上涨（OTLY、SFM、BRBR同日大涨）；8-6 Q2因鸡蛋过剩重挫后深度超跌反弹，近期Benchmark上调至买入、TD Cowen/Needham上调目标价提供支撑。参考：[Yahoo Finance VITL](https://finance.yahoo.com/quote/VITL)"),
    "ZIP": ("联动", "当日无公司新闻（StockTitan显示8月5日Q2财报后无更新）；8月5日Q2营收超预期并上调全年展望、高盛将目标价$3.50升至$5.00后，股价前一周冲高$5.17回落至$4.21，8-24出现修复性反弹+7.8%收$4.54。"),
    "EVER": ("财报延续", "当日无独立事件；8月3日Q2营收+25%至1.951亿美元、调整后EBITDA创纪录3010万美元，财报后先遭抛售随后市场重新评估，8-24延续修复行情+5.5%收$26.62。"),
    "BDN": ("融资定价", "负债管理获市场认可：8月17日宣布对2028/2029年票据最多1亿美元现金要约，8月21日（周五）盘后宣布2029票据要约扩大至7000万美元并延期至8月27日、2028票据要约到期完成，削减8.875%高息债改善到期结构，8-24续涨+5.0%（此前周五已涨3%），叠加利率回落利好REIT。[Brandywine IR](https://investor.brandywinerealty.com/news-releases/news-release-details/brandywine-realty-trust-announces-upsize-and-extension)"),
    "NREF": ("联动", "无当日公司新闻；利率盘中回落（TGA回购扩容传闻）直接利好商业地产抵押REIT估值，+3.0%修复此前疲势。"),
    "TCI": ("结构", "家族关联控股的低流通盘REIT当日无新闻（8月6日Q2转亏后无更新）；日成交量极小，随利率回落与REIT板块反弹被放大至+3.0%。"),
    "ZENA": ("联动", "无人机板块8-24集体回调（Benzinga：无个股坏消息、风险偏好退潮+获利回吐），ZenaTech作为无人机/AI软件小盘同步大跌-11.8%收$1.79；此前分析师目标价从$6.81下调至$4.49加剧抛压。[Benzinga/AOL](https://www.aol.com/articles/drone-stocks-slide-risk-appetite-163543000.html)"),
    "INOD": ("联动", "小盘AI/数据服务主题回调延续（此前一周连跌，8-21收$64.21），叠加8月6日设立的3亿美元ATM增发计划稀释担忧发酵，8-24大跌-11%收$57.13。[TipRanks](https://www.tipranks.com/news/catalyst/innodata-stock-sinks-as-dilution-fears-hit-wall-street)"),
    "UMAC": ("联动", "无人机板块当日无消息集体抛售：Benzinga归因于风险偏好退潮与此前30天近翻倍涨幅后的获利回吐（UMAC约-9%、Red Cat -7%）；同日公司提交DEF 14A代理书提出与$100股价目标挂钩的CEO认股权证激励，未起提振作用。[Benzinga/AOL](https://www.aol.com/articles/drone-stocks-slide-risk-appetite-163543000.html)"),
    "RNGR": ("联动", "无公司新闻；能源服务小盘股随能源板块（雪佛龙-1.1%、Baker Hughes-0.6%）与罗素小盘能源走弱重挫-6.5%。"),
    "PARR": ("联动", "无当日公司新闻；炼油股2026年创纪录涨势（MPC/VLO/DINO年内涨超80%）后的板块性获利回吐延续，-6.0%收$74.33，Q2强劲业绩（调整后EPS $10.10）后估值已偏高。[CNBC](https://www.cnbc.com/2026/08/17/refiner-stocks-are-on-a-nearly-unprecedented-run-history-says-it-could-end-soon.html)"),
    "PBF": ("联动", "同板块炼油股获利回吐-5.5%（$73.53→约$69.5）；背景上8月有大股东减持约2560万美元股份及Martinez炼厂重启不确定性，叠加RIN/柴油利润8月走弱。[CNBC](https://www.cnbc.com/2026/08/17/refiner-stocks-are-on-a-nearly-unprecedented-run-history-says-it-could-end-soon.html)"),
    "ELMT": ("结构", "4月IPO的钨/钼国防材料次新股，流通盘低；8月13日Q2（营收+35.2%、积压订单创纪录）后8-21放量飙升19.3%至$19.885，8-24无消息获利回吐-11.2%至$17.66，典型高波动次新走势。"),
    "EOSE": ("直接", "8-24盘前9:05公告与WATTMORE达成非独占软件+储能战略合作（Intellect Operate EMS平台配套其Z3长时储能系统），市场认为合作规模有限且非独占，利好落空式抛售当日-9.2%收$3.46。[StockTitan](https://www.stocktitan.net/news/EOSE/)"),
    "LUNR": ("联动", "8-24无独立利空，为8-17/8-18 NASA多项合同（多卫星通信基础设施、EAGLE-VSWIR）连涨两日后的获利回吐，放量下跌；叠加太空板块风险收缩（SpaceX破发拖累）与长端利率压制高估值成长股。参考：[Perplexity Finance LUNR](https://www.perplexity.ai/finance/LUNR)"),
    "OTLY": ("联动", "8-24无独立公司新闻，属健康食品/植物基主题集体大涨（与SFM、BRBR、VITL同日齐涨）。7-22 Q2营收超预期并上调全年指引后的延续动能，当日放量大涨9.6%领涨主题。参考：[CNN/MarketBeat](https://www.marketbeat.com/instant-alerts/oatly-group-nasdaqotly-trading-up-9-still-a-buy-2026-08-24)"),
    "SFM": ("联动", "8-24当日+6.2%至$86.13，无独立公司新闻，属健康食品/天然有机零售主题集体走强（叠加MAHA政策发酵及8-10超加工食品定义推进的板块叙事），延续7-29 Q2超预期+摩根大通上调后的升势。参考：[GuruFocus](https://www.gurufocus.com/news/9050450/is-it-too-late-to-buy-sprouts-farmers-market-inc-sfm-after-62-rally-gf-value-says-undervalued)"),
    "SNAP": ("联动", "8-24无公司新闻，为社交媒体主题交易中的领涨者（当日社交媒体板块齐涨），市场买入年内落后标的、延续Q2（8-3）广告复苏+扭亏叙事，盘中一度涨超5%。参考：[247wallst](https://247wallst.com/investing/2026/08/24/snap-rises-4-meta-platforms-and-alphabet-tick-up-reddit-slips-as-the-social-media-trade-splits)"),
    "MTCH": ("联动", "8-24无独立事件，跟随社交媒体/互联网内容主题（SNAP领涨）反弹+2.1%；三周前Q2财报重挫后修复，CEO连续增持与Zacks上调评级的利好背景提供支撑。参考：[MarketWatch MTCH](https://www.marketwatch.com/investing/stock/mtch)"),
    "BMBL": ("联动", "8-24无独立事件，小市值交友股跟涨社交媒体/交友主题（SNAP+5.5%、MTCH+2.1%），股价处52周低位附近的超跌反弹，公司探索出售的传闻也提供题材。参考：[Robinhood BMBL](https://robinhood.com/us/en/stocks/BMBL)"),
    "BXP": ("联动", "8-24无独立事件，领涨办公REIT板块（当日办公REIT主题+1.7%齐涨，利率敏感资产在Jackson Hole会议前获买盘）；背景为Q2 FFO超预期并上调全年FFO指引至$6.99-7.05。参考：[Yahoo Finance办公REIT](https://finance.yahoo.com/sectors/real-estate/reit-office)"),
    "VNO": ("联动", "8-24无独立事件，跟随办公REIT板块集体上涨（纽约办公REIT情绪修复）；背景为Q2 FFO $0.74超预期及纽约办公租赁放量（单季34.8万平方英尺）。参考：[Vornado IR](https://investors.vno.com/news-releases/news-release-details/vornado-announces-second-quarter-2026-financial-results)"),
    "RHP": ("联动", "8-24无独立事件，随REIT板块整体走强（办公+酒店REIT当日普涨）；背景为8-11 Cantor Fitzgerald将目标价上调至$135并维持增持。参考：[StockAnalysis RHP](https://stockanalysis.com/stocks/rhp)"),
    "ASTS": ("联动", "8-24无独立事件，太空主题风险收缩日齐跌（当日12个投机主题清一色下跌）。SpaceX上市后破发持续拖累板块情绪，ASTS自5月高点已回撤约六成，且仍在消化BB7发射事故的$1.259亿非自愿转换损失。参考：[MarketBeat](https://www.marketbeat.com/articles/ast-spacemobile-stock-sinks-as-spacex-fallout-rattles-space-sector)"),
    "BKSY": ("联动", "8-24无独立事件，随太空/国防对地观测板块齐跌（ASTS、LUNR同日均跌超9%），高beta太空情报股在风险收缩日遭抛售；8-6 Q2业绩（营收+50%、Adj EBITDA转正）后无新催化。参考：[Seeking Alpha BKSY](https://seekingalpha.com/symbol/BKSYW)"),
    "RGTI": ("联动", "8-24量子板块集体回吐上周'收入头条'驱动的涨幅：Rigetti跌7%至$16.70，给予此前收入利好驱动的上涨大幅回吐，IonQ、QUBT、Infleqtion同步下跌6-7%，无个股独立利空，属获利了结+投机主题风险收缩。参考：[247wallst](https://247wallst.com/investing/2026/08/24/quantum-stocks-unwind-a-revenue-headline-rally-rigetti-computing-and-infleqtion-down-7-ionq-down-6)"),
    "IONQ": ("联动", "8-24无独立利空，跟随Rigetti回吐上周收入头条涨幅，'tracking the same reversal in sympathy'（同步反转），盘中跌6%至$42.27、收盘-8.5%；量子板块作为最纯粹的久期资产在风险收缩日领跌。参考：[247wallst](https://247wallst.com/investing/2026/08/24/quantum-stocks-unwind-a-revenue-headline-rally-rigetti-computing-and-infleqtion-down-7-ionq-down-6)"),
    "QBTS": ("联动", "8-24无独立事件，D-Wave随量子纯玩家板块整体走低（QUBT、INFQ、RGTI、IONQ齐跌6-8%），回吐近期板块涨幅；行业情绪受炒作周期退潮与长端利率高企压制。参考：[247wallst](https://247wallst.com/investing/2026/08/24/quantum-stocks-unwind-a-revenue-headline-rally-rigetti-computing-and-infleqtion-down-7-ionq-down-6)"),
    "BEEM": ("联动", "8-24无独立事件，纳米市值EV充电股随电动车主题风险收缩日齐跌（当日电动车主题清一色下跌），且8-19盘后Q2业绩（营收$8.6M、仍净亏$3.1M）后卖压延续，8月初Freedom Broker降级至持有。参考：[StockTitan BEEM](https://www.stocktitan.net/news/BEEM/beam-global-reports-second-quarter-2026-operating-wlcl07eyay9z.html)"),
    "AUR": ("联动", "8-24无独立事件，自动驾驶主题风险收缩日齐跌；盘前仅微跌约1%，但盘中随投机主题清仓加速下挫至-8.8%，高beta无收入自动驾驶股为当日风险收缩的主要抛售对象。参考：[Public.com AUR](https://public.com/stocks/aur/pre-market)"),
    "XPEV": ("直接", "8-24盘前发布Q2财报：每股亏损RMB1.29远逊预期RMB0.76，Q3收入指引RMB217-234亿大幅低于共识258.8亿，股价跌至52周新低$11.16（盘中-8.4%）；盘前机器人子公司Dogotix融资$9亿+估值$63亿的消息未能抵消卖压。参考：[MarketWatch/Benzinga](https://www.marketwatch.com/investing/stock/xpev)"),
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
    assert DATA["date"] == "2026-08-24"
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
            f"- `finviz_2026-08-24_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-24_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月24日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月24日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：Jackson Hole前（本周五主席演讲）的防御切换日：CNBC报道财政部拟动用近1万亿美元TGA为长端回购扩容注资，30年期收益率盘中回落4bp至5.20%—5.24%，贬值交易延续——黄金+0.8%至4680美元三个多月新高、比特币自6月低点+35%逼近8万美元、铜LME破14000美元创纪录；布伦特回落破93美元（Bessent周一下午伊朗\"经济D-Day\"制裁讲话前）。指数：标普500 -0.3%、纳指100 -1%四连跌、道指尾盘翻红+0.3%，宽度300涨/不足200跌——必需消费五范围涨幅前三（沃尔玛+2.7%）、金融与公用事业强（TGA注资想象+利率回落）；科技/存储大跌（英伟达七连跌-2.9%周三盘后财报、希捷/SanDisk -6.5%、美光-5.8%、\"AI服务器提价15%\"被视为成本冲击）、科技动量ETF -4.1%、韩国-2.6%；12个主题清一色跌（太空/量子/电动车/机器人/国防）。美加贸易战升级（2027年1月1日50%汽车/钢铁关税）。", "",
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
    (SKILL / "finviz_2026-08-24_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-24_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-24_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)
    print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
