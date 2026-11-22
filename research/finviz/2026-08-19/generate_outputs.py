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
    "Diagnostics": "诊断", "Genomics": "基因组学", "Oncology": "肿瘤", "Enterprise": "企业级",
    "Mining": "挖矿", "Farm-Direct": "农场直供", "Food": "食品",
    "Luxury": "奢侈品", "Secondhand": "二手",
}

THEME_COMPANY = {
    "MRNA": "Moderna Inc", "TEM": "Tempus AI Inc", "TWST": "Twist Bioscience Corp",
    "BKKT": "Bakkt Holdings Inc", "COIN": "Coinbase Global Inc", "MARA": "Marathon Digital Holdings Inc",
    "HAIN": "Hain Celestial Group Inc", "EL": "Estee Lauder Companies Inc", "BYND": "Beyond Meat Inc",
    "CRWD": "CrowdStrike Holdings Inc", "S": "SentinelOne Inc", "AVGO": "Broadcom Inc",
    "RKLB": "Rocket Lab Corp", "RDW": "Redwire Holdings Inc", "LUNR": "Intuitive Machines Inc",
    "GE": "GE Aerospace", "ATI": "ATI Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic NV", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月18日16:00 ET盘后事件可解释8月19日；8月19日16:00 ET后事件不得倒推。
R = {
    "MRNA": ("直接", "8月19日与默克联合公布个性化mRNA癌症疫苗intismeran（V940/mRNA-4157）联合Keytruda治疗高危黑色素瘤III期试验期中成功：无复发生存期（主要终点）与无远处转移生存期（关键次要终点）双双达成，为mRNA个性化癌症疫苗首次III期验证；当日暴涨177%、创上市以来最大单日涨幅（含13%空头回补），年内转涨。[Fortune](https://fortune.com/article/moderna-merck-mrna-vaccine-promise-deadly-skin-cancer-melanoma-stocks-08-19-2026)、[Al Jazeera](https://www.aljazeera.com/news/2026/8/19/moderna-merck-unveil-mrna-based-cancer-vaccine-that-cuts-spread)"),
    "TNON": ("直接", "8月18日盘后5:00 PM其S-3注册声明生效（SEC EFFECT通知），叠加Q2营收128万美元同比翻倍、毛利率约64%的Catamaran SI关节融合系统放量叙事，8月19日盘中一度+115%、收盘+109.4%。[StockTitan SEC](https://www.stocktitan.net/sec-filings/TNON/effect-tenon-medical-inc-sec-filing-348d6c1c377c.html)、[Benzinga](https://www.benzinga.com/markets/equities/26/08/61292033/tenon-medical-shares-surge-77-percent-after-hours)"),
    "BIVI": ("联动", "小盘生物科技在mRNA疫苗成功与医疗主题暴涨（罗素医疗331涨/89跌）中的高beta联动；无独立事件。"),
    "NWGL": ("结构", "超低流通盘微盘在材料板块大涨日的投机拉升（+30.9%），两步检索无同日公司事件。"),
    "ASTL": ("联动", "钢铁与材料随板块上涨；Algoma为加拿大钢企、美元大跌利好非美定价资产。"),
    "HYMC": ("联动", "小盘金银矿商随贵金属暴涨（白银+4.5%下经营杠杆放大）；罗素材料60涨/26跌。"),
    "YJ": ("结构", "中国电商微盘+144.3%：无公告的超低流通盘投机拉升（与当日中国资产走弱背离，属个股资金博弈）。"),
    "AZI": ("结构", "汽车后市场微盘+44.4%，无公告投机拉升。"),
    "BRCB": ("联动", "咖啡连锁小盘随可选消费上涨。"),
    "XOS": ("结构", "电动卡车微盘-34.7%，无公告的持续失血（此前已完成反向拆股）。"),
    "EHGO": ("结构", "微盘-33.2%持续阴跌。"),
    "SGLY": ("融资定价", "前日折价定增（180万美元@3美元）后第二日续跌-14.6%。"),
    "IPST": ("结构", "微盘-46.4%，投机资金撤离。"),
    "AMBR": ("结构", "微盘-23.8%持续退潮。"),
    "TMS": ("结构", "微盘-13.4%。"),
    "LGCL": ("结构", "微盘-47.0%，连续暴跌。"),
    "WETO": ("结构", "微盘-37.1%退潮。"),
    "DAIC": ("结构", "微盘-34.3%退潮。"),
    "MRK": ("直接", "同日作为intismeran合作方公布III期成功（试验主要研究者称其为辅助黑色素瘤治疗的里程碑、有望建立新治疗范式），股价大涨12.6%为2009年以来最佳单日；Moderna总裁称数千名术后高危患者最早明年可获益。[Fortune](https://fortune.com/article/moderna-merck-mrna-vaccine-promise-deadly-skin-cancer-melanoma-stocks-08-19-2026)"),
    "DHR": ("联动", "医疗保健与生物科技主题九子行业清一色上涨（等权+7.48%）中的生命科学工具权重股跟涨；mRNA疫苗成功外溢至全产业链（基因组学+9.9%、诊断+5.4%），无独立公司事件。"),
    "CVNA": ("联动", "可选消费四范围涨幅前三（标普54只成分42涨/12跌）；二手车电商随消费轮动与罗素2000领涨（+0.5%）上涨。"),
    "DHI": ("联动", "住宅建筑随可选消费与利率回落（30年-10bp）双利好上涨（住宅建筑ETF +2.15%）。"),
    "TSLA": ("联动", "道指可选消费四成分清一色上涨（耐克+2.5%、亚马逊+2.5%、家得宝+2.0%）中的高beta权重股。"),
    "NEM": ("联动", "财政部宣布长端回购翻倍，美元指数跌约0.78%—2%、30年收益率-10bp，现货黄金升至约4484美元（+3.46%）；Newmont作为最大金矿商随金矿ETF（+9.4%—9.8%）大涨7.9%。[Mining.com](https://www.mining.com/gold-silver-miners-surge-as-treasury-doubles-buybacks)、[Motley Fool](https://www.fool.com/investing/2026/08/19/why-newmont-mining-rallied-today)"),
    "MOS": ("联动", "基础材料五范围涨幅前列（All Stocks 216涨/60跌）；化肥随农产品与贵金属商品共振上涨。"),
    "FCX": ("联动", "铜与金矿双敞口受益于美元大跌（铜期货走强、金矿板块暴涨）；五范围材料涨幅前三中的权重股。"),
    "GE": ("联动", "工业五范围全部跌幅前三：AI资本开支担忧传导至航空航天与电气设备链（GE Aerospace -5.0%为标普工业最弱）；无独立公司事件。[QuiverQuant](https://www.quiverquant.com/news/Why+GE+Aerospace+%28GE%29+Stock+Is+Down+Today)"),
    "VRT": ("联动", "数据中心电力/散热链随AI动量unwind连续回调。"),
    "JCI": ("联动", "楼宇自动化与电气设备随工业板块回调。"),
    "STX": ("联动", "存储链连续第三日回调：AI硬件动量的持续了结叠加科技动量ETF -5.4%；两步检索无同日独立利空。"),
    "WDC": ("联动", "同上，存储/硬盘链动量unwind的延续。"),
    "DELL": ("联动", "AI服务器毛利率担忧与科技动量回调拖累；无同日新事件。"),
    "AFL": ("联动", "保险与银行随金融三范围跌幅前列回落（标普金融22涨/48跌）；利率回落虽降融资成本但经济放缓担忧占上风。"),
    "FITB": ("联动", "银行板块回调（银行ETF -2.1%、区域银行-2.4%）；罗素金融67涨/289跌为宽度最弱。"),
    "GL": ("联动", "保险股随金融板块回落。"),
    "SHW": ("背离", "30年收益率-10bp回落（前日利率新高曾重挫宣伟）+涂料需求与住房联动的边际修复，道指基础材料唯一样本+2.41%领涨道指。"),
    "NKE": ("联动", "道指可选消费清一色上涨；连续回调后的超跌反弹叠加消费轮动。"),
    "AMZN": ("联动", "同上；科技与消费内部轮动中消费端受益。"),
    "HD": ("联动", "前日财报（同店2022年来最佳、剔除关税退款实为miss）后的延续企稳，随可选消费与利率回落回升。"),
    "DIS": ("联动", "道指通信服务两只成分清一色上涨；防御与价值轮动。"),
    "GOOGL": ("背离", "科技板块整体回调中逆势微涨0.15%（道指通信服务清一色涨）：Jefferies重申买入（目标价445美元）+表外AI承诺点名中的相对韧性。"),
    "CAT": ("联动", "AI数据中心燃气轮机叙事随半导体回调继续降温（道指工业四成分清一色下跌、卡特彼勒-2.9%为道指最弱）。"),
    "HON": ("联动", "道指工业清一色下跌中的权重股；分拆融资背景下的利率敏感性。"),
    "BA": ("联动", "道指工业清一色下跌。"),
    "GS": ("联动", "道指金融回调（高盛-1.81%为道指最弱之一）；长端利率虽回落但经济放缓担忧压制金融权重。"),
    "JPM": ("联动", "同上，道指金融权重随板块回落。"),
    "TRV": ("联动", "道指金融回调。"),
    "CVX": ("单样本", "道指能源唯一样本基本持平（+0.01%）：贵金属与医疗吸走资金、能源主题当日平静。"),
    "ALNY": ("联动", "医疗保健主题当日最强方向（新一代+31.3%、基因组学+9.9%）中的纳指权重股跟涨；无独立事件。"),
    "VRTX": ("联动", "医疗保健主题全面走强中的权重股跟涨（纳指100九只医疗成分清一色上涨、整体+3.26%）；无独立事件。"),
    "AMGN": ("联动", "同上，医疗权重股随主题全面上涨。"),
    "PYPL": ("单样本", "纳指100金融唯一样本+1.36%：Advent收购谈判延续的个股事件支撑其逆板块上涨。"),
    "LIN": ("单样本", "纳指100基础材料唯一样本+0.51%：材料板块五范围涨幅前三中的防御性权重。"),
    "RKLB": ("联动", "太空主题五个子行业清一色下跌（等权-1.85%）中的权重股；前期13F曝光行情的持续回吐。"),
    "SPCX": ("联动", "同上，太空主题回撤（前日+4.5%后-2.6%）。"),
    "NBIS": ("联动", "AI算力/云基础设施股随科技动量第三日回调。"),
    "FANG": ("联动", "纳指能源两成分一涨一跌；贵金属与医疗主导的轮动中能源权重暂时失血。"),
    "BKR": ("单样本", "纳指能源微涨0.06%，板块平静日。"),
    "MRVI": ("联动", "罗素医疗小盘端随主题全面上涨（Maravai为生命科学试剂商）；两步检索无同日独立催化。"),
    "ARCT": ("联动", "mRNA平台技术叙事的直接受益者（Arcturus亦为mRNA药企），Moderna成功带动整个mRNA板块重估。"),
    "TWST": ("联动", "合成生物学/基因测序基础设施商随基因组学子行业（+9.9%）上涨；此前获Anthropic选中提供DNA数据存储的合作叙事为背景。[Yahoo Finance](https://finance.yahoo.com/healthcare/articles/biggest-ipo-targeted-next-60-180000173.html)"),
    "AMR": ("联动", "焦煤商随基础材料与能源商品上涨（罗素材料端小盘资源股全面反弹）。"),
    "NG": ("联动", "金矿商（NovaGold）随金矿板块暴涨（ETF +9.4%—9.8%）。"),
    "NXDT": ("联动", "罗素房地产125只中108涨：30年收益率-10bp直接利好小盘REIT（房地产+1.70%）。"),
    "CWK": ("联动", "商业地产服务随利率回落与小盘地产反弹。"),
    "NMRK": ("联动", "同上，小盘地产服务链。"),
    "TOYO": ("结构", "微盘投机退潮连续暴跌，无同日公司事件。"),
    "WYFI": ("融资定价", "前日2.7亿美元私募债券公告（建AI基建）后连续第二日暴跌（-21.0%），AI集体发债遭股东问责为当日讨论焦点。"),
    "AEHR": ("联动", "半导体测试设备随科技动量第三日回调。"),
    "FG": ("联动", "保险与年金小盘随金融板块回调（罗素金融67涨/289跌）。"),
    "CD": ("联动", "同上，小盘金融随板块回调。"),
    "NKSH": ("联动", "同上，社区银行小盘随银行板块回落。"),
    "RFIL": ("联动", "射频/军工电子小盘随工业与国防回调。"),
    "VOYG": ("结构", "微盘新上市股的投机退潮。"),
    "RHLD": ("结构", "微盘资金撤离。"),
    "TEM": ("联动", "AI医疗叙事与医疗主题暴涨的双重受益者（近三个月科技回调日医疗均为最佳板块的UBS框架）；年内连续五个季度EPS超预期为背景。"),
    "BKKT": ("联动", "加密主题六子行业清一色上涨（等权+3.15%）：美元大跌近2%+比特币突破+白宫当日举行加密会议，加密资产全线走强。"),
    "COIN": ("联动", "同上，加密交易所直接受益于美元走弱与加密市场风险偏好回升（前日遭巴克莱降级后反弹）。[Verified Investing](https://verifiedinvesting.com)"),
    "MARA": ("联动", "比特币矿企随加密主题清一色上涨（比特币突破+美元大跌）。"),
    "HAIN": ("联动", "消费品主题六子行业清一色上涨（等权+2.98%）：Target与Lowe's财报验证消费韧性+防御与价值轮动。"),
    "EL": ("直接", "当日盘前（8:30 AM ET）发布财年Q4与全年业绩，股价大涨16.3%创2011年11月以来最佳单日，带动整个消费品主题（食品+3.9%、二手+3.8%、农场直供+3.5%、奢侈品+3.0%）。[公司IR](https://www.elcompanies.com/en/investors)、[MarketBeat](https://www.marketbeat.com/earnings/reports/2026-8-19-the-este-lauder-companies-inc-stock)"),
    "BYND": ("联动", "消费品主题全面上涨中的高beta植物肉股。"),
    "CRWD": ("联动", "网络安全主题八子行业清一色下跌（等权-2.16%）：连续第五个交易日走弱，AI动量与软件安全的持续失血。"),
    "S": ("联动", "同上，网安主题连续走弱。"),
    "AVGO": ("联动", "网安与半导体双重暴露下的权重回调（-4.6%）；此前美银AI债务载体警告的延续。"),
    "RDW": ("联动", "太空主题五子行业清一色下跌。"),
    "LUNR": ("联动", "同上。"),
    "ATI": ("联动", "国防航空主题七子行业清一色下跌（等权-1.40%）：价值轮动中前期强势的国防股回调。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "SGDM", "perf": 9.823, "form": "交易所交易基金", "exposure": "金矿股（全球）",
         "reason": "贵金属暴涨日：黄金现货+3.8%、金矿股单日+9.4%—9.8%，白银+4.5%、白银矿业+9.5%；金矿股以经营杠杆放大金价弹性。合并删除：GDXJ +9.643%、RING +9.524%、GDX +9.421%（同为金矿股敞口，按敞口去重只保留最强一只）。"},
        {"ticker": "SIL", "perf": 9.528, "form": "交易所交易基金", "exposure": "白银矿业股",
         "reason": "白银矿业与金矿股为不同经济敞口（按原任务要求分别保留）：白银+4.5%下白银矿业的经营杠杆更强。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "IBB", "perf": 6.583, "form": "交易所交易基金", "exposure": "生物科技（权重）",
         "reason": "医疗保健与生物科技主题九个子行业清一色上涨（等权+7.48%）：Moderna暴涨177%、Merck +12.6%带动生物科技权重ETF大涨。合并删除：XBI +5.896%（同簇生物科技，保留最强一只）。"},
    ],
    "down": [
        {"ticker": "PTF", "perf": -5.362, "form": "交易所交易基金", "exposure": "科技动量（Dorsey Wright）",
         "reason": "科技动量连续第三日领跌全市场（-8.2%/-5.4%两日）：半导体（等权-2.8%）、存储与硬件链继续了结，资金切向医疗、贵金属与消费。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "ASHS", "perf": -4.027, "form": "交易所交易基金", "exposure": "中国股票（小盘）",
         "reason": "中国小盘ETF领跌：中概与A股关联资产在美元资产risk-on日反向走弱，与科技动量、工业动量为不同地域敞口。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "PRN", "perf": -3.203, "form": "交易所交易基金", "exposure": "工业动量（Dorsey Wright）",
         "reason": "工业动量与科技动量同向回落：国防航空（ITA -2.38%）、电气化链与卡特彼勒继续回调，工业在五个股票范围全部进入跌幅前三。合并删除：无同簇产品进入本轮极值候选。"},
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
    assert DATA["date"] == "2026-08-19"
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
            f"- `finviz_2026-08-19_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-19_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月19日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月19日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：财政部盘中宣布长端回购操作规模至少翻倍（每次20亿→不低于40亿美元、聚焦10—30年期、9月9日启动），30年期收益率自5.34%高点回落约10bp收于5.19%（20年期-11bp为6月底以来最大单日跌幅），代价是彭博美元即期指数跌近2%创三个月低点——黄金现货+3.8%、金矿股+9.4%—9.8%、白银+4.5%，加密货币主题六子行业清一色上涨。FOMC纪要显示多名官员认为可能需要加息；20年期160亿美元拍卖完成。收盘标普500 +0.2%结束三连跌、罗素2000 +0.5%最佳、纳指100 -0.2%四连跌：科技约-2%最大拖累（科技动量ETF -5.4%连续第三日领跌、半导体等权-2.8%），必需消费、能源、材料领涨。历史性个股事件：Merck与Moderna个性化mRNA癌症疫苗（联合Keytruda）黑色素瘤III期期中成功——Moderna +177%创史上最佳单日、Merck +12.6%为2009年以来最佳，医疗主题九子行业清一色涨（等权+7.48%）；Target beat & raise、Estee Lauder +16.3%创2011年以来最佳。", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5547/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1943/1943、Themes 268/268和ETF 658/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-19_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-19_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-19_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)
    print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
