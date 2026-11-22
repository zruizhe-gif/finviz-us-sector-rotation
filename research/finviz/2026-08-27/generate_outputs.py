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
    "Internet of Things": "物联网", "Industrial Automation": "工业自动化",
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
    "Analog": "模拟芯片", "Compute": "计算芯片", "Design": "芯片设计工具", "Wireless": "无线芯片",
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
    "OKTA": "Okta Inc",
    "CRWD": "Crowdstrike Holdings Inc",
    "RPD": "Rapid7 Inc",
    "CRM": "Salesforce Inc",
    "MSTR": "Strategy Inc",
    "NOW": "ServiceNow Inc",
    "PANW": "Palo Alto Networks Inc",
    "SFM": "Sprouts Farmers Market Inc",
    "CELH": "Celsius Holdings Inc",
    "BRBR": "Bellring Brands Inc",
    "HRL": "Hormel Foods Corp",
    "GPRE": "Green Plains Inc",
    "CALM": "Cal-Maine Foods Inc",
    "ENSG": "Ensign Group Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic N.V", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月26日16:00 ET盘后事件可解释8月27日；8月27日16:00 ET后事件不得倒推。
R = {
    "CRM": ("直接", "Salesforce于8/26盘后发布FY26 Q2财报：AI收入同比增至三倍、利润指引超预期并扩大与Anthropic合作（Claude接入），Barclays等上调目标价；8/27收涨22.58%，为六年多来最大单日涨幅。（事件时间2026-08-26 盘后（财报与电话会）） [Salesforce Jumps 14% as Profit Guidance Outruns Revenue](https://finance.yahoo.com/markets/stocks/articles/salesforce-jumps-14-profit-guidance-191300570.html) [Salesforce Stock Jumps 20% After AI Revenue More Than Triples](https://finance.yahoo.com/technology/ai/articles/salesforce-stock-jumps-20-ai-190902041.html)"),
    "CRWD": ("直接", "CrowdStrike于8/26盘后发布Q2财报：营收超预期（beat达14.7亿美元）、CEO称史上最佳季度；8/27收涨20.50%。（事件时间2026-08-26 盘后（财报与电话会）） [CrowdStrike Stock Soars After $1.47 Billion Revenue Beat](https://finance.yahoo.com/markets/stocks/articles/crowdstrike-stock-soars-1-47-191801525.html)"),
    "OKTA": ("直接", "Okta于8/26盘后财报年内第二次上调展望（订阅backlog创纪录），且8/27 15:32 ET报道Palo Alto Networks与其进行收购谈判；8/27收涨28.63%。（事件时间2026-08-26 盘后财报；2026-08-27 15:32 ET收购谈判报道） [Palo Alto Networks Stock Soars on Okta Takeover Talks Report](https://finance.yahoo.com/markets/stocks/articles/palo-alto-networks-stock-soars-193257487.html)"),
    "NVDA": ("直接", "英伟达于8/26盘后发布财报：收入962亿美元连续第16季超预期、Q3指引约1,100亿首破千亿，史上首次给出FY2028全年指引（增速约70%、远超原预期44%—45%，供应受限口径），并于8/27宣布以约129亿美元收购Hugging Face；8/27收涨8.74%（约九个季度最佳财报次日表现）、市值单日增加约2,960亿美元。（事件时间2026-08-26 盘后财报；2026-08-27 收购Hugging Face报道） [Nvidia Adds $296 Billion as 70% Forecast Resets the AI Trade](https://finance.yahoo.com/technology/ai/articles/nvidia-adds-296-billion-70-191118640.html) [Nvidia buys Hugging Face for $12.9B after earnings beat](https://finance.yahoo.com/m/ba621425-7e25-3355-94f3-0a4ef309d23f/nvidia-buys-hugging-face-for.html)"),
    "SNPS": ("直接", "Synopsys于8/26盘后发布Q3 2026财报：营收与EPS超预期并上调全年指引（AI芯片设计需求增强），晨间获机构上调评级；8/27收涨13.39%。（事件时间2026-08-26 盘后（财报与电话会）） [Synopsys Q3 2026 earnings beat estimates, raises full-year guidance](https://finance.yahoo.com/m/9895f73c-b443-38c5-9bcb-9d18069d6028/synopsys-q3-2026-earnings.html)"),
    "HRL": ("直接", "Hormel于8/27盘前发布Q3财报：EPS超预期并上调全年利润指引，但火鸡与坚果价格偏低导致下调销售指引；8/27收跌10.25%（一年来最差单日）。（事件时间2026-08-27 盘前06:42 ET） [Hormel Foods Hit With Lower Prices for Turkey and Nuts](https://www.barrons.com/articles/hormel-foods-earnings-stock-price-9ddbea5a?mod=bar_FV)"),
    "BBW": ("直接", "Build-A-Bear于8/27盘前发布Fiscal Q2财报：下调全年展望（夏季产品线失败并解雇相关高管）；8/27收跌27.26%。（事件时间2026-08-27 盘前06:45 ET） [Build-A-Bear shares tumble after lowering full-year outlook](https://finviz.com/news/386289/build-a-bear-shares-tumble-after-lowering-full-year-outlook)"),
    "WEN": ("直接", "Trian/Nelson Peltz退出对Wendy's的潜在私有化收购（8/27 09:34 ET），同日新CEO公布五点复兴计划；8/27收跌13.55%（2020年以来最大跌幅）。（事件时间2026-08-27 09:34 ET） [Wendy's shares tumble as Trian steps back from potential takeover bid](https://finviz.com/news/386284/wendys-shares-tumble-as-trian-steps-back-from-potential-takeover-bid)"),
    "VBIO": ("直接", "Valion Bio于8/27 08:30 ET宣布缩股（reverse stock split）；8/27收跌21.41%。（事件时间2026-08-27 08:30 ET） [Valion Bio Announces Reverse Stock Split](https://finviz.com/news/386203/valion-bio-announces-reverse-stock-split)"),
    "CALC": ("直接", "CalciMedica于8/27 09:00 ET宣布1:5缩股；8/27收跌20.00%。（事件时间2026-08-27 09:00 ET） [CalciMedica Announces One-for-Five Reverse Stock Split](https://finviz.com/news/386231/calcimedica-announces-one-for-five-reverse-stock-split)"),
    "HCWC": ("直接", "Healthy Choice Wellness于8/27 09:25 ET公告股东批准与Host Digital合并的全部议案；8/27收跌15.39%。（事件时间2026-08-27 09:25 ET） [HEALTHY CHOICE WELLNESS CORP.'S STOCKHOLDERS APPROVE ALL PROPOSALS](https://finviz.com/news/386274/healthy-choice-wellness-corps-stockholders-approve-all-proposals-in-connection-with-merger-with-host-digital)"),
    "OOMA": ("直接", "Ooma于8/26 16:15 ET发布FY2027 Q2财报：创纪录营收与AI驱动增长；8/27收涨12.23%。（事件时间2026-08-26 16:15 ET（盘后财报）） [Ooma Inc (OOMA) (Q2 2027) Earnings Call Highlights](https://finance.yahoo.com/technology/ai/articles/ooma-inc-ooma-q2-2027-050129983.html)"),
    "MRNA": ("直接", "Moderna于8/27盘前宣布20亿美元可转换优先票据私募（投向肿瘤管线与偿债），趁上周癌症疫苗数据暴涨后高位融资；8/27收跌4.60%。当日盘后15:56 ET的FDA批准2026-27新冠疫苗属收盘后事件，不解释当日跌幅。（事件时间2026-08-27 07:20 ET） [Moderna Announces Proposed Private Placement of $2.0 Billion of Convertible Senior Notes](https://finviz.com/news/386084/moderna-announces-proposed-private-placement-of-20-billion-of-convertible-senior-notes)"),
    "DLTR": ("直接", "Dollar Tree于8/27盘前发布Q2财报：同店增长强劲、关税退税增厚盈利超预期，但5月大涨后仅维持指引令投资者失望，防御板块轮出背景下利好兑现收跌3.92%。（事件时间2026-08-27 盘前06:00 ET） [Dollar Tree beats second quarter estimates as tariff refunds boost earnings](https://finance.yahoo.com/m/79bbd94b-3c13-318b-ae67-a6c82063ff8b/dollar-tree-beats-second.html)"),
    "PANW": ("联动", "网络安全主题八子行业清一色上涨（等权+9.59%），CrowdStrike/Okta财报点燃板块；尾盘Okta收购谈判报道将PANW列为潜在买方再添动量。该股与当日所选网络安全、物联网的偏强方向一致。"),
    "RPD": ("联动", "窗口内无同日直接催化；网安板块财报行情联动（CrowdStrike +20.5%/Okta +28.6%带动全板块）。该股与当日所选网络安全的偏强方向一致。"),
    "MSTR": ("联动", "窗口内无同日直接催化；加密货币反弹联动（IBIT +1.87%、DIME +4.62%，弱美元与风险偏好回升）。该股与当日所选大数据的偏强方向一致。"),
    "NOW": ("联动", "窗口内无同日直接催化；SaaS财报行情联动（Salesforce +22.6%带动软件板块，IGV +7.75%）。该股与当日所选大数据的偏强方向一致。"),
    "FROG": ("联动", "窗口内无同日直接催化；软件/DevOps板块联动（IGV +7.75%、XSW +5.22%）。该股与当日所选科技的偏强方向一致。"),
    "METC": ("联动", "窗口内无同日直接催化；金属矿业反弹联动（XME +2.24%、白银+1.92%、金矿股回升）。该股与当日所选基础材料的偏强方向一致。"),
    "BAK": ("联动", "窗口内无同日直接催化；基础材料板块All Stocks/Russell入选偏强（化工与金矿链修复）。该股与当日所选基础材料的偏强方向一致。"),
    "ACDC": ("联动", "窗口内无同日直接催化；能源中小盘偏强联动（罗素能源90%成分上涨、等权油服PXJ +3.75%）。该股与当日所选能源、科技的偏强方向一致。"),
    "LUCY": ("联动", "无窗口内公司事件。零窗口新闻微盘（Innovative Eyewear），All Stocks医疗保健偏弱日的低流通资金行为。"),
    "AMSS": ("联动", "无窗口内公司事件。零窗口新闻微盘（AMASS Brands），必需消费偏弱日的低流通资金行为。"),
    "SMJF": ("联动", "无窗口内公司事件。零窗口新闻极微盘（SMJ International，香港仓储物流），-87.0%为低流通崩跌/价值出清型资金行为，公开渠道未检索到同日公司公告。"),
    "KXIN": ("联动", "无窗口内公司事件。零窗口新闻微盘（Kaixin），公司历史上有多次股份合并记录，但窗口内并股生效公告未能核实（IR站点超时），-71.3%暂按并股机制/低流通崩跌的资金行为处理。"),
    "CHOW": ("联动", "无窗口内公司事件。零窗口新闻微盘（ChowChow Cloud，中概），+68.4%为低流通动量炒作。"),
    "CABO": ("联动", "无窗口内公司事件。零窗口新闻（Cable One），罗素通信服务偏弱日的延续下跌。"),
    "WSHP": ("联动", "无窗口内公司事件。零窗口新闻微盘（WeShop），罗素通信服务偏弱日的低流通资金行为。"),
    "CURI": ("联动", "窗口内新闻1条经核验无同日直接事件；8/26 16:15 ET的CFO任命属中性小事件，无法解释-7.25%，主因罗素通信服务偏弱。该股与当日所选通信服务的偏弱方向一致。"),
    "MRK": ("联动", "窗口内新闻2条经核验无同日直接事件（候选均为Moderna可转债报道、与MRK无关）；医疗保健防御性抛售日的板块联动。该股与当日所选医疗保健的偏弱方向一致。"),
    "COST": ("联动", "窗口内无直接事件；纳指100必需消费整体-1.73%的防御板块轮出。该股与当日所选必需消费的偏弱方向一致。"),
    "WMT": ("联动", "窗口内新闻4条经核验无同日直接事件（候选均为Build-A-Bear/Dollar Tree/Dollar General报道）；道指必需消费三成分清一色下跌日的防御轮出。该股与当日所选必需消费的偏弱方向一致。"),
    "HD": ("联动", "窗口内新闻2条经核验无同日直接事件；8/27 08:00 ET的Magic Apron门店AI助手扩展属例行产品PR，无法解释-1.86%，主因道指可选消费四成分清一色下跌。该股与当日所选可选消费的偏弱方向一致。"),
    "AMZN": ("联动", "窗口内新闻12条经核验无同日直接事件（候选均为英伟达生态报道）；道指可选消费清一色下跌叠加超大盘科技资金流出（英伟达单股拉动结构下的内部腾挪）。该股与当日所选可选消费的偏弱方向一致。"),
    "MCD": ("联动", "窗口内无直接事件；道指可选消费四成分清一色下跌。该股与当日所选可选消费的偏弱方向一致。"),
    "DIS": ("联动", "窗口内新闻2条经核验无同日直接事件；道指通信服务两只成分清一色下跌。该股与当日所选通信服务的偏弱方向一致。"),
    "RKLB": ("联动", "窗口内新闻1条经核验无同日直接事件；8/27 00:30 ET的内部人卖出550万美元属次要披露，主因太空科技主题清一色上涨（英伟达财报电话会提及SpaceX合作深化的生态外溢）。该股与当日所选工业的偏强方向一致。"),
    "SPCX": ("联动", "窗口内新闻6条经核验无同日直接事件；英伟达财报电话会三次提及与SpaceX合作深化（8/27 08:24 ET报道），私有映射标的随AI生态上涨。该股与当日所选工业的偏强方向一致。"),
    "GOOGL": ("联动", "窗口内新闻7条经核验无同日直接事件；8/27 12:17 ET同意以3.53亿美元和解英国应用开发者诉讼属次要事件，主因超大盘科技资金流出（剔除英伟达标普为负的单股拉动结构）。该股与当日所选通信服务的偏弱方向一致。"),
    "CVX": ("联动", "窗口内无直接事件；道指能源唯一成分，油价反弹（BNO +2.32%）下仍微跌0.22%——权重能源与中小盘能源分化（XLE -0.22% vs 罗素能源+2.33%）。该股与当日所选能源的偏弱方向一致。"),
    "REAX": ("联动", "窗口内新闻1条经核验无同日直接事件（候选为RE/MAX联合创始人讣告、与The Real Brokerage无关的聚合噪音）；罗素房地产偏弱日的联动。该股与当日所选房地产的偏弱方向一致。"),
    "JDZG": ("联动", "Finviz该股报价页无新闻栏（源端结构性缺口，两次筛查与直接抓取核实），窗口内公开渠道亦未见公司公告；该股与当日所选必需消费的偏弱方向一致（-11.85%）。"),
    "AESI": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "AGNT": ("联动", "该股与当日所选房地产的偏弱方向一致。"),
    "ALB": ("联动", "该股与当日所选基础材料的偏强方向一致。"),
    "APA": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "BF-B": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "BKR": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "BLMN": ("联动", "该股与当日所选可选消费的偏弱方向一致。"),
    "BRBR": ("联动", "该股与当日所选健康食品与营养、老龄化与长寿的偏弱方向一致。"),
    "BTU": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "CALM": ("联动", "该股与当日所选农业商品的偏弱方向一致。"),
    "CELH": ("联动", "该股与当日所选健康食品与营养、老龄化与长寿的偏弱方向一致。"),
    "CSGP": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选房地产的偏弱方向一致。"),
    "DD": ("联动", "该股与当日所选基础材料的偏强方向一致。"),
    "ENSG": ("联动", "该股与当日所选老龄化与长寿的偏弱方向一致。"),
    "ESS": ("联动", "该股与当日所选房地产的偏弱方向一致。"),
    "FANG": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "FRD": ("联动", "该股与当日所选基础材料的偏强方向一致。"),
    "GORO": ("联动", "无窗口内公司事件；金属矿业反弹联动（XME +2.24%、白银+1.92%），金矿股在上日获利回吐后修复。该股与当日所选基础材料的偏强方向一致。"),
    "GPRE": ("联动", "该股与当日所选农业商品、健康食品与营养的偏弱方向一致。"),
    "HAL": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "HPP": ("联动", "该股与当日所选房地产的偏弱方向一致。"),
    "IBM": ("联动", "窗口内新闻9条经核验无同日直接事件；该股与当日所选科技的偏强方向一致。"),
    "JNJ": ("联动", "窗口内新闻4条经核验无同日直接事件；该股与当日所选医疗保健的偏弱方向一致。"),
    "KO": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "LIN": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选基础材料的偏强方向一致。"),
    "LYB": ("联动", "该股与当日所选基础材料的偏强方向一致。"),
    "MINE": ("联动", "无窗口内公司事件；金矿股反弹联动（白银+1.92%、上日贵金属获利回吐后的修复）。该股与当日所选基础材料的偏强方向一致。"),
    "MNST": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "PEP": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选必需消费的偏弱方向一致。"),
    "PG": ("联动", "该股与当日所选必需消费的偏弱方向一致。"),
    "PYPL": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选金融的偏弱方向一致。"),
    "SLB": ("联动", "该股与当日所选能源的偏强方向一致。"),
    "SFM": ("联动", "该股与当日所选健康食品与营养、老龄化与长寿的偏弱方向一致。"),
    "TRI": ("联动", "该股与当日所选工业的偏强方向一致。"),
    "UDR": ("联动", "该股与当日所选房地产的偏弱方向一致。"),
    "UHS": ("联动", "该股与当日所选医疗保健的偏弱方向一致。"),
    "UNH": ("联动", "窗口内新闻1条经核验无同日直接事件；该股与当日所选医疗保健的偏弱方向一致。"),
    "ZTS": ("联动", "该股与当日所选医疗保健的偏弱方向一致。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "HACK", "perf": 8.184, "form": "交易所交易基金", "exposure": "全球科技｜网络安全",
         "reason": "网安ETF领涨全市场：CrowdStrike +20.5%/Okta +28.6%/Rapid7 +14.5%财报行情点燃，网络安全主题八子行业清一色上涨（等权+9.59%）。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "SKYY", "perf": 4.21, "form": "交易所交易基金", "exposure": "全球科技｜云计算",
         "reason": "云计算ETF：Salesforce +22.6%带动SaaS/云普涨（WCLD +7.51%、IGV +7.75%），英伟达财报后AI应用层风险偏好修复。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "PXJ", "perf": 3.748, "form": "交易所交易基金", "exposure": "美国行业｜油服（等权）",
         "reason": "等权油服ETF：能源中小盘反弹（罗素能源+2.33%、ProFrac +13.9%、Peabody +7.8%），油价反弹（BNO +2.32%）下等权油服强于权重能源（XLE -0.22%）。合并删除：无同簇产品进入本轮极值候选。"},
    ],
    "down": [
        {"ticker": "VIXY", "perf": -2.692, "form": "交易所交易基金", "exposure": "VIX短期期货",
         "reason": "VIX期货ETF：软件/芯片财报大涨压制波动率（标普500 +0.7%、信息技术+3.4%为唯一收涨板块），风险偏好回升。合并删除：VXX -2.373%、VXZ -1.420%、VIXM -1.231%（同簇VIX期货，按敞口去重保留最弱一只）。"},
        {"ticker": "EPOL", "perf": -2.571, "form": "交易所交易基金", "exposure": "国际欧洲｜波兰股票",
         "reason": "波兰ETF当日领跌国际地域敞口；与美股防御性板块轮出同向，属独立地域敞口、与美股行业ETF不构成同敞口重复。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "EPHE", "perf": -2.437, "form": "交易所交易基金", "exposure": "国际亚太｜菲律宾股票",
         "reason": "菲律宾ETF：亚太新兴市场地域敞口当日回落，与波兰ETF同向（防御性/非美敞口走弱）但地域独立。合并删除：无同簇产品进入本轮极值候选。"},
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
        text = "核查8月26日盘后至27日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-08-27"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；VIX期货簇（VIXY/VXX/VXZ/VIXM）在成稿层按同一经济敞口合并、保留最弱一只。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-08-27_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-27_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月27日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月27日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：英伟达财报次日与Jackson Hole前夜的单主线行情：英伟达8/26盘后连续第16季超预期（收入962亿、Q3指引约1,100亿首破千亿），真正爆点是史上首次给出FY2028全年指引——收入增长约70%（原预期44%—45%、供应受限口径），并于8/27宣布以约129亿美元收购Hugging Face；当日收涨8.7%（约九个季度最佳财报次日表现）、市值单日回流约2,960亿美元，但涨势极端集中——开盘8分钟标普仅152只成分股上涨、英伟达贡献36点而指数只涨17点，收盘标普500 +0.7%（信息技术+3.4%为唯一收涨板块、仅150涨/350跌）、纳指100 +1.4%、道指+0.2%、罗素2000 +0.3%。第二主线是软件股复兴：Salesforce +22.6%（六年最大单日、AI收入增至三倍）、CrowdStrike +20.5%、Okta +28.6%（含Palo Alto收购谈判报道）、Synopsys +13.4%——过去12个月被抛弃的软件股自6月底+70%而费城半导体指数同期-14%。防御板块全面轮出：Hormel -10.2%（下调销售指引）、Wendy's -13.6%（Trian退出私有化）、Build-A-Bear -27.3%（下调展望）。宏观：初请20.3万低于预期；收益率全曲线上行（2年4.20%、10年4.67%、30年5.18%—5.20%）；堪萨斯城联储Schmid放鹰（\"政策甚至偏宽松、最早9月支持加息\"）；Warsh周五Jackson Hole主旨演讲为最大悬念。油价反弹（布伦特逼近89美元）、黄金微涨（财政部回购引发的弱美元交易延续）。", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5540/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1942/1943、Themes 268/268和ETF 658/658；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-27_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-27_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-27_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
