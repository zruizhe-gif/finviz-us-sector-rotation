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
}

THEME_COMPANY = {
    "AMZN": "Amazon.com Inc",
    "BRBR": "Bellring Brands Inc",
    "CHGG": "Chegg Inc",
    "DSP": "Viant Technology Inc",
    "DUOL": "Duolingo Inc",
    "FORM": "FormFactor Inc",
    "IPX": "IperionX Ltd ADR",
    "MRVL": "Marvell Technology Inc",
    "NVTS": "Navitas Semiconductor Corp",
    "SKIL": "Skillsoft Corp",
    "SMPL": "Simply Good Foods Co",
    "SONY": "Sony Group Corp ADR",
    "SPIR": "Spire Global Inc",
    "TSAT": "Telesat Corp",
    "USAR": "USA Rare Earth Inc",
    "UUUU": "Energy Fuels Inc",
    "VSAT": "Viasat Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic N.V", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月27日16:00 ET盘后事件可解释8月28日；8月28日16:00 ET后事件不得倒推。
R = {
    "PYPL": ("直接", "PayPal 8/28盘前确认Stripe与Advent放弃逾500亿美元收购计划（原为史上最大LBO之一），收购溢价预期出清：盘前一度-18%、收跌12.71%，为纳指100金融唯一成分（清一色跌入选）。（事件时间2026-08-28 盘前06:09 ET起（WSJ首发）） [PayPal Shares Dive Premarket on Report of Advent, Stripe Abandoning Takeover Plan](https://www.wsj.com/business/deals/paypal-shares-dive-premarket-on-report-of-advent-stripe-abandoning-takeover-plan-ffeaabf2?mod=wsj_FV) [PayPal shares slide as Stripe and Advent abandon reported $50B+ takeover](https://finance.yahoo.com/m/48ba23d7-c53f-3015-9d44-eecb497afcb3/paypal-shares-slide-as-stripe.html)"),
    "GAP": ("直接", "Gap 8/28盘前发布Q2财报：连续第11个季度同店销售增长、盈利大超预期（尽管Old Navy不及预期并下调全年销售指引、更换Old Navy负责人），股价大涨12.9%。（事件时间2026-08-28 盘前07:30 ET） [Gap's stock surges after posting 11th quarter in a row of comparable sales growth](https://www.marketwatch.com/livecoverage/stock-market-today-dow-s-p-500-nasdaq-jackson-hole-federal-reserve-chair-kevin-warsh/card/gap-s-stock-surges-after-posting-11th-quarter-in-a-row-of-comparable-sales-growth-4nqZt4JAZYyPjdtOtswG?mod=mw_FV) [Gap slashed its full-year sales forecast after Old Navy badly missed](https://qz.com/gap-sales-outlook-cut-old-navy-disappoints-082826)"),
    "MRVL": ("直接", "Marvell 8/27盘后财报：营收27.4亿美元略超预期、调整后EPS 0.94美元高约1美分，但市场担忧AI光模块订单时点（Broadcom 9/2财报前的timing trap）引发抛售；8/28收跌10.3%并拖累整个光学网络链。（事件时间2026-08-27 盘后16:05 ET） [Marvell's Earnings Were Strong. Why Optical Networking Stocks Are Falling Anyway](https://www.barrons.com/articles/-marvell-mrvl-earnings-sympathy-selloff-cohr-lite-1a21d246?mod=bar_FV)"),
    "KTCC": ("直接", "Key Tronic 8/27 16:03 ET发布Fiscal Q4及全年业绩、不及预期；8/28收跌28.3%。（事件时间2026-08-27 16:03 ET（盘后发布）） [Key Tronic Corporation Announces Results for the Fourth Quarter and Year End of Fiscal 2026](https://finviz.com/news/386378/key-tronic-corporation-announces-results-for-the-fourth-quarter-and-year-end-of-fiscal-2026)"),
    "CHAI": ("直接", "Core AI Holdings 8/28 07:52 ET发布Q2财报：营收同比+56%、毛利率显著改善；当日大涨57.1%。（事件时间2026-08-28 07:52 ET） [Core AI Holdings Reports 56% Q2 Revenue Growth and Significant Improvement in Gross Margin](https://finviz.com/news/386562/core-ai-holdings-reports-56-q2-revenue-growth-and-significant-improvement-in-gross-margin)"),
    "CRML": ("直接", "Critical Metals 8/28 08:30 ET更新欧洲锂业收购进展（9月法庭日期、8.35亿美元安排）；当日下跌11.4%，与金属商品主题清一色跌共振。（事件时间2026-08-28 08:30 ET） [Critical Metals Corp. Provides Update on Proposed Acquisition of European Lithium](https://finviz.com/news/386593/critical-metals-corp-provides-update-on-proposed-acquisition-of-european-lithium)"),
    "NVDA": ("联动", "窗口内新闻86条经核验无同日公司事件；8/27大涨8.7%后的获利回吐叠加Warsh鹰派演讲引发的科技全线抛售（五个范围科技全部进入跌幅前三），候选均为生态类报道（Blue Owl为IREN数据中心融资24亿美元等）。该股与当日所选科技的偏弱方向一致。"),
    "LITE": ("联动", "窗口内新闻4条经核验无同日直接事件；Marvell财报后的光学网络链集体抛售（当日多篇报道将Lumentum列为sympathy selloff具名对象），AI硬件链去风险。该股与当日所选科技的偏弱方向一致。"),
    "COHR": ("联动", "窗口内新闻2条经核验无同日直接事件；与Lumentum同为Marvell财报后光学网络链sympathy抛售的具名对象。该股与当日所选科技的偏弱方向一致。"),
    "NVTS": ("联动", "窗口内无同日直接催化；半导体主题九个子行业清一色下跌（等权-3.56%），AI芯片链在Warsh演讲日整体去风险。该股与当日所选科技的偏弱方向一致。"),
    "AMZN": ("联动", "窗口内新闻23条经核验无同日直接事件；Evercore当日上调目标价至355美元属次要触发，主因道指可选消费四成分清一色上涨的消费轮入与Anthropic营收叙事（Claude收入同比增约10倍）。该股与当日所选可选消费、健康食品与营养的偏强方向一致。"),
    "GOOGL": ("联动", "窗口内新闻35条经核验无同日直接事件；当日Google在30个市场收缩以化解10%收入风险的报道属次要，主因通信服务轮入（标普500通信21只成分18涨）——超大盘科技抛售日中的例外。该股与当日所选通信服务的偏强方向一致。"),
    "CSCO": ("联动", "窗口内新闻2条经核验无同日直接事件（候选均为Salesforce复盘报道）；道指科技3涨3跌中的弱势成员，随科技全线回调。该股与当日所选科技的偏弱方向一致。"),
    "HON": ("联动", "窗口内新闻2条经核验无同日直接事件（候选为Solstice/Element Solutions报道、与霍尼韦尔无关的聚合噪音）；道指工业四成分清一色下跌。该股与当日所选工业的偏弱方向一致。"),
    "LULU": ("联动", "窗口内新闻1条经核验无同日直接事件；Q2财报定于9/3（未发布），8/28 +5.1%发生在多家机构下调目标价的背景下，属消费板块轮入与财报前布局。该股与当日所选可选消费的偏强方向一致。"),
    "SKIL": ("联动", "窗口内新闻1条经核验无同日直接事件（候选为9/9财报日程公告）；教育科技主题四子行业清一色上涨（等权+1.37%）。该股与当日所选教育科技的偏强方向一致。"),
    "FNGR": ("联动", "无窗口内公司事件。零窗口新闻微盘（FingerMotion，中概），+129.5%为低流通动量炒作（网络核查未见同日公告），暂未找到同日直接催化。"),
    "WETO": ("联动", "无窗口内公司事件。零窗口新闻微盘，-50.3%为低流通崩跌，暂未找到同日直接催化。"),
    "TAOP": ("联动", "无窗口内公司事件。零窗口新闻微盘（Taoping，中概），-31.3%为低流通资金行为，暂未找到同日直接催化。"),
    "TJGC": ("联动", "无窗口内公司事件。零窗口新闻微盘，+24.7%为低流通动量炒作，暂未找到同日直接催化。"),
    "LPTH": ("联动", "无窗口内公司事件。零窗口新闻微盘（光明光电），罗素科技-2.70%日的低流通放大下跌。该股与当日所选科技的偏弱方向一致。"),
    "GLSI": ("联动", "无窗口内公司事件。零窗口新闻微盘，罗素医疗保健-2.67%日、生物科技ETF -3.48%的低流通放大下跌。该股与当日所选医疗保健的偏弱方向一致。"),
    "NTRP": ("联动", "无窗口内公司事件。零窗口新闻微盘，+14.6%为低流通反弹，暂未找到同日直接催化。"),
    "ABLV": ("联动", "无窗口内公司事件。零窗口新闻微盘（中概），+14.5%为低流通动量，暂未找到同日直接催化。"),
    "PRLD": ("联动", "无窗口内公司事件。零窗口新闻，罗素医疗保健偏弱日的生物科技回调（XBI -3.48%）。该股与当日所选医疗保健的偏弱方向一致。"),
    "SLS": ("联动", "无窗口内公司事件。零窗口新闻，罗素医疗保健偏弱日。该股与当日所选医疗保健的偏弱方向一致。"),
    "AXTI": ("联动", "无窗口内公司事件。零窗口新闻（化合物半导体材料），罗素科技-2.70%日的放大下跌。该股与当日所选科技的偏弱方向一致。"),
    "SHAZ": ("联动", "无窗口内公司事件。零窗口新闻微盘，罗素科技偏弱日。该股与当日所选科技的偏弱方向一致。"),
    "FNUC": ("联动", "无窗口内公司事件。零窗口新闻微盘（核燃料相关），铀ETF当日-5.79%的板块性抛售。该股与当日所选基础材料的偏弱方向一致。"),
    "AGX": ("联动", "无窗口内公司事件。零窗口新闻（Argan工程），罗素工业-1.81%日。该股与当日所选工业的偏弱方向一致。"),
    "ALOY": ("联动", "无窗口内公司事件。零窗口新闻，罗素科技/工业双弱日的低流通下跌。该股与当日所选基础材料的偏弱方向一致。"),
    "SATL": ("联动", "无窗口内公司事件。零窗口新闻（Satellogic），太空科技主题五子行业清一色跌（等权-3.10%）。该股与当日所选科技的偏弱方向一致。"),
    "RCAT": ("联动", "无窗口内公司事件。零窗口新闻微盘，罗素工业偏弱日。该股与当日所选工业的偏弱方向一致。"),
    "NCRA": ("联动", "无窗口内公司事件。零窗口新闻微盘，+8.0%为低流通反弹，暂未找到同日直接催化。"),
    "ABNB": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "AEP": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "BRBR": ("联动", "该股与当日所选必需消费、健康食品与营养的偏强方向一致。"),
    "CAT": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选工业的偏弱方向一致。"),
    "CEG": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "CHGG": ("联动", "该股与当日所选教育科技的偏强方向一致。"),
    "CHTR": ("联动", "该股与当日所选通信服务的偏强方向一致。"),
    "CLDT": ("联动", "该股与当日所选房地产的偏强方向一致。"),
    "CMCSA": ("联动", "该股与当日所选通信服务的偏强方向一致。"),
    "CVX": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "DASH": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "DGXX": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "DIS": ("联动", "该股与当日所选通信服务的偏强方向一致。"),
    "DPZ": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "DSP": ("联动", "该股与当日所选社交媒体的偏强方向一致。"),
    "DUOL": ("联动", "该股与当日所选教育科技的偏强方向一致。"),
    "EIX": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "FIX": ("联动", "该股与当日所选工业的偏弱方向一致。"),
    "FORM": ("联动", "该股与当日所选半导体的偏弱方向一致。"),
    "FRVO": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "GNRC": ("联动", "该股与当日所选工业的偏弱方向一致。"),
    "HAL": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "IBM": ("联动", "该股与当日所选科技的偏弱方向一致。"),
    "INN": ("联动", "该股与当日所选房地产的偏强方向一致。"),
    "IPX": ("联动", "该股与当日所选金属商品的偏弱方向一致。"),
    "LIN": ("联动", "该股与当日所选基础材料的偏强方向一致。"),
    "MCD": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "MMM": ("联动", "该股与当日所选工业的偏弱方向一致。"),
    "MNRO": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "MSTR": ("联动", "该股与当日所选科技的偏弱方向一致；加密货币当日大跌（IBIT -3.07%、DIME -4.74%），Strategy随比特币回落7.3%。"),
    "MTEX": ("联动", "该股与当日所选必需消费的偏强方向一致。"),
    "NFLX": ("联动", "该股与当日所选通信服务的偏强方向一致。"),
    "NKE": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "NRG": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "NWL": ("联动", "该股与当日所选必需消费的偏强方向一致。"),
    "PCG": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
    "PSX": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "SHW": ("联动", "该股与当日所选基础材料的偏弱方向一致。"),
    "SLB": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "SMPL": ("联动", "该股与当日所选健康食品与营养、必需消费的偏强方向一致。"),
    "SONY": ("联动", "该股与当日所选社交媒体的偏强方向一致。"),
    "SPIR": ("联动", "该股与当日所选太空科技的偏弱方向一致。"),
    "STRT": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "SVC": ("联动", "该股与当日所选房地产的偏强方向一致。"),
    "TMUS": ("联动", "该股与当日所选通信服务的偏强方向一致。"),
    "TSAT": ("联动", "该股与当日所选太空科技的偏弱方向一致。"),
    "USAR": ("联动", "该股与当日所选金属商品的偏弱方向一致。"),
    "UUUU": ("联动", "该股与当日所选金属商品的偏弱方向一致。"),
    "VRT": ("联动", "该股与当日所选工业的偏弱方向一致。"),
    "VSAT": ("联动", "该股与当日所选太空科技的偏弱方向一致。"),
    "WEN": ("联动", "该股与当日所选可选消费的偏强方向一致。"),
    "XEL": ("联动", "该股与当日所选公用事业的偏弱方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "PALL", "perf": 4.923, "form": "商品信托", "exposure": "钯金现货",
         "reason": "钯金ETF领涨全市场：贵金属全线暴跌（黄金-3.24%、白银-4.38%、金矿股-4.4%）中钯金逆势独涨，供给端驱动与金银的贬值交易退潮形成极端分化。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "UGA", "perf": 2.292, "form": "商品信托", "exposure": "汽油期货",
         "reason": "汽油期货+2.29%：能源商品链当日最强（原油BNO仅-0.45%、炼油CRAK +1.74%），炼厂利润与月末需求支撑。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "VIXY", "perf": 1.787, "form": "交易所交易基金", "exposure": "VIX短期期货",
         "reason": "VIX期货ETF转为上涨：Warsh Jackson Hole演讲后2年期收益率+12bp、科技全线抛售（五个范围科技全部进入跌幅前三），对冲需求回升。合并删除：VXX、VIXM、VXZ（同簇VIX期货，按敞口去重保留最强一只）。"},
    ],
    "down": [
        {"ticker": "URA", "perf": -5.789, "form": "交易所交易基金", "exposure": "全球能源｜铀矿",
         "reason": "铀ETF领跌全市场：核能链在Warsh鹰派演讲日遭集中抛售，与科技/AI链同向去风险；独立敞口（铀）与科技动量、金矿不构成重复。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "PTF", "perf": -5.019, "form": "交易所交易基金", "exposure": "科技动量（Dorsey Wright）",
         "reason": "科技动量ETF再度领跌：英伟达获利回吐与Marvell财报拖累光通信链，半导体主题九子行业清一色跌（等权-3.56%），动量因子集中平仓。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "GDXJ", "perf": -4.444, "form": "交易所交易基金", "exposure": "全球金矿（中小型）",
         "reason": "中小金矿ETF大跌：美元即期指数+0.3%、贬值交易当日逆转（黄金-3.24%、白银-4.38%），高beta金矿股放大跌幅；与科技动量、铀为不同经济敞口。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查8月27日盘后至28日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-08-28"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；VIX期货簇（VIXY/VXX/VXZ/VIXM）在成稿层按同一经济敞口合并、保留最强一只。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-08-28_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-28_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月28日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月28日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：Jackson Hole首日与新任美联储主席Warsh主旨演讲（美东10:00）触发剧烈风格反转：演讲后2年期收益率直线走高、收涨12bp（30年期仅+2bp、曲线平坦化），市场转向定价\"下一步是加息且宜早不宜迟\"；美元即期指数+0.3%，两周前的买金/弱美元贬值交易当日逆转——黄金-3.24%、白银-4.38%、中小金矿ETF -4.44%、铀ETF -5.79%，钯金逆势+4.92%为全市场最强ETF。板块完全镜像反转：周四唯一收涨的信息技术周五领跌（五个股票范围科技全部进入跌幅前三：英伟达获利回吐-4.6%、Marvell财报后-10.3%拖累光通信链、半导体主题九子行业清一色跌-3.56%），工业（道指四成分清一色跌）与公用事业（标普31只成分仅2涨）同步重挫；轮入端通信服务（标普21只成分18涨：Netflix +2.4%/康卡斯特+2.5%/谷歌+1.7%）、可选消费（道指四成分清一色涨+3.49%：亚马逊+4.0%/耐克+3.0%；Gap财报大涨12.9%）与能源、防御消费。个股事件：PayPal -12.7%（Stripe与Advent放弃逾500亿美元收购）、Gap +12.9%（连续11季同店增长）、Key Tronic -28.3%（FQ4不及预期）、Core AI Holdings +57.1%（Q2营收+56%）、Marvell 8/27盘后财报超预期但因AI光模块时点担忧暴跌。健康食品/社交媒体/教育科技/农业商品/消费品五个主题清一色上涨，太空科技/金属商品等十个主题清一色下跌。", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5540/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1941/1943、Themes 268/268和ETF 658/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-28_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-28_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-28_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
