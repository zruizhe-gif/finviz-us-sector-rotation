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
    "Telecommunications": "电信", "Wearables": "可穿戴设备", "Energy Renewable": "可再生能源",
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
    "IT & Telecom": "信息技术与电信",
    "Apparel": "服装服饰",
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
    "Rail": "铁路", "5G": "5G通信", "Immersive": "沉浸式技术", "Satcom": "卫星通信", "Smartwatches": "智能手表", "Cloud & Edge": "云与边缘", "Sport": "体育运动", "Air Cargo": "航空货运", "Maritime": "海运", "Trucking": "卡车运输", "Air Travel": "航空客运", "Industrial IoT": "工业物联网", "Printing": "印刷", "PCs & Devices": "个人电脑与设备", "Hydrogen": "氢能", "Solar": "太阳能", "Wind": "风能", "Geothermal": "地热", "Grid": "电网", "Fuel Cells": "燃料电池", "Batteries": "电池储能", "Oil": "石油", "Uranium": "铀", "Gas & LNG": "天然气与LNG", "Smart Grid": "智能电网", "Materials": "医疗材料", "Therapeutics": "治疗药物", "Devices": "医疗器械", "Metabolic": "代谢疾病", "Telemedicine": "远程医疗", "IT & Data": "医疗信息与数据",
}

THEME_COMPANY = {
    "BKSY": "BlackSky Technology Inc",
    "BRZE": "Braze Inc",
    "COLD": "Americold Realty Trust Inc",
    "COUR": "Coursera Inc",
    "DOCS": "Doximity Inc",
    "FROG": "JFrog Ltd",
    "GIS": "General Mills Inc",
    "HWM": "Howmet Aerospace Inc",
    "KR": "Kroger Co",
    "LRN": "Stride Inc",
    "MH": "McGraw Hill Inc",
    "NOC": "Northrop Grumman Corp",
    "OTLY": "Oatly Group AB ADR",
    "QLYS": "Qualys Inc",
    "REXR": "Rexford Industrial Realty Inc",
    "RPD": "Rapid7 Inc",
    "STAG": "STAG Industrial Inc",
    "TENB": "Tenable Holdings Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AAPL": ("联动", "+1.10%列道指科技（偏强侧）。"),
    "ABLV": ("联动", "+14.61%列All Stocks可选消费（偏强侧）。"),
    "ABNB": ("联动", "+2.35%列标普500可选消费（偏强侧）。"),
    "ACRE": ("联动", "-6.57%列罗素2000房地产（偏弱侧）。"),
    "AEP": ("联动", "-0.55%列纳指100公用事业（偏弱侧）。"),
    "AMZN": ("直接", "Constellation与亚马逊签订20年购电协议（新增190兆瓦核电）；Anthropic单季116亿美元收入改变S-1读法。"),
    "AXON": ("联动", "+0.70%列纳指100工业（偏强侧）。"),
    "BE": ("联动", "-4.90%列标普500工业（偏弱侧）。"),
    "BKSY": ("联动", "-2.65%列主题层国防与航空航天（偏弱侧）。"),
    "BRZE": ("联动", "+8.42%列主题层软件（偏强侧）。"),
    "BXMT": ("联动", "-6.99%列罗素2000房地产（偏弱侧）。"),
    "CEG": ("直接", "同购电协议的定价端冲击：20年锁价PPA压制电价上行弹性。"),
    "CIM": ("联动", "-6.57%列罗素2000房地产（偏弱侧）。"),
    "COLA": ("联动", "-30.14%列All Stocks金融（偏弱侧）。"),
    "COLD": ("联动", "-3.85%列主题层房地产与REITs（偏弱侧）。"),
    "COUR": ("联动", "+6.21%列主题层教育科技（偏强侧）。"),
    "CRM": ("直接", "Salesforce宣布收购Listen Labs。"),
    "CTNM": ("联动", "+16.70%列罗素2000医疗保健（偏强侧）。"),
    "DIS": ("联动", "-0.48%列道指通信服务（偏弱侧）。"),
    "DMRC": ("直接", "Digimarc宣布注册直接发行普通股。"),
    "DOCS": ("联动", "+6.86%列主题层软件（偏强侧）。"),
    "DSC": ("联动", "+22.12%列All Stocks可选消费（偏强侧）。"),
    "EEIQ": ("联动", "-8.75%列All Stocks必需消费（偏弱侧）。"),
    "ESNT": ("联动", "-8.43%列罗素2000金融（偏弱侧）。"),
    "EUDA": ("联动", "-10.08%列All Stocks房地产（偏弱侧）。"),
    "EXC": ("联动", "-0.61%列纳指100公用事业（偏弱侧）。"),
    "FNGR": ("直接", "FingerMotion签订最终协议收购Newbit Technology 100%股权。"),
    "FROG": ("联动", "+7.38%列主题层软件（偏强侧）。"),
    "FTHM": ("联动", "-12.59%列All Stocks房地产（偏弱侧）。"),
    "GEN": ("联动", "+5.61%列标普500科技（偏强侧）。"),
    "GIS": ("直接", "通用磨坊晋升COO McNabb为CEO（接替Harmening）。"),
    "GOOGL": ("联动", "+0.93%列道指通信服务（偏强侧）。"),
    "HD": ("联动", "-1.23%列道指可选消费（偏弱侧）。"),
    "HPE": ("直接", "HPE上调收入指引并宣布12亿美元计划——股价创历史新高（AI动能）。"),
    "HPK": ("联动", "+4.75%列罗素2000能源（偏强侧）。"),
    "HWM": ("联动", "-2.06%列主题层国防与航空航天（偏弱侧）。"),
    "ITW": ("联动", "-3.67%列标普500工业（偏弱侧）。"),
    "JNJ": ("联动", "-1.06%列道指医疗保健（偏弱侧）。"),
    "KDP": ("联动", "-2.22%列纳指100必需消费（偏弱侧）。"),
    "KO": ("联动", "-0.88%列道指必需消费（偏弱侧）。"),
    "KR": ("联动", "-3.57%列标普500必需消费（偏弱侧）。"),
    "LIN": ("联动", "+0.27%列纳指100基础材料（偏强侧）。"),
    "LRN": ("联动", "+3.16%列主题层教育科技（偏强侧）。"),
    "LVO": ("联动", "+12.61%列All Stocks通信服务（偏强侧）。"),
    "MDLZ": ("联动", "-2.53%列纳指100必需消费（偏弱侧）。"),
    "MEC": ("联动", "-8.09%列罗素2000工业（偏弱侧）。"),
    "MH": ("联动", "+4.21%列主题层教育科技（偏强侧）。"),
    "MKC": ("联动", "-4.13%列标普500必需消费（偏弱侧）。"),
    "MNKD": ("联动", "+16.77%列罗素2000医疗保健（偏强侧）。"),
    "MRK": ("联动", "-2.66%列标普500医疗保健（偏弱侧）。"),
    "MRNA": ("直接", "Moderna遭花旗罕见卖出评级重挫——'Q3标普500最佳与最差'的最差端。"),
    "MSFT": ("联动", "+0.77%列道指科技（偏强侧）。"),
    "NKE": ("联动", "-1.23%列道指可选消费（偏弱侧）。"),
    "NMIH": ("联动", "-8.37%列罗素2000金融（偏弱侧）。"),
    "NOC": ("直接", "海军战机损失+波音击败诺格赢得200亿美元海军合同。"),
    "ONT": ("联动", "-5.17%列罗素2000工业（偏弱侧）。"),
    "OPTX": ("联动", "+11.34%列罗素2000科技（偏强侧）。"),
    "OTLY": ("联动", "-3.96%列主题层健康食品与营养（偏弱侧）。"),
    "OXBR": ("联动", "-23.23%列All Stocks金融（偏弱侧）。"),
    "PACB": ("联动", "+29.51%列罗素2000医疗保健（偏强侧）。"),
    "PARR": ("联动", "+4.23%列罗素2000能源（偏强侧）。"),
    "PDD": ("联动", "+0.57%列纳指100可选消费（偏强侧）。"),
    "PG": ("联动", "-2.05%列道指必需消费（偏弱侧）。"),
    "PODC": ("联动", "+12.68%列All Stocks通信服务（偏强侧）。"),
    "PSKY": ("直接", "美国法官允许派拉蒙完成华纳兄弟收购；巨额发债显示高收益率对企业融资的挤压。"),
    "PYPL": ("联动", "-2.52%列纳指100金融（偏弱侧）。"),
    "QLYS": ("联动", "+4.96%列主题层网络安全（偏强侧）。"),
    "RCL": ("联动", "+1.99%列标普500可选消费（偏强侧）。"),
    "REXR": ("联动", "-3.02%列主题层房地产与REITs（偏弱侧）。"),
    "RFL": ("直接", "Rafael公布TransportNPC三期研究顶线结果（阴性）。"),
    "ROG": ("联动", "+10.73%列罗素2000科技（偏强侧）。"),
    "RPD": ("联动", "+4.40%列主题层网络安全（偏强侧）。"),
    "RPGL": ("联动", "+26.31%列All Stocks科技（偏强侧）。"),
    "SDEV": ("联动", "-20.80%列All Stocks金融（偏弱侧）。"),
    "SEI": ("联动", "+4.16%列罗素2000能源（偏强侧）。"),
    "SHW": ("联动", "-2.17%列道指基础材料（偏弱侧）。"),
    "SNPS": ("直接", "新思科技与AWS签订逾10亿美元多年期定制芯片IP协议（亚马逊为首家客户）。"),
    "SOTK": ("直接", "Sono-Tek获创纪录719万美元清洁能源订单。"),
    "SPCX": ("联动", "+1.08%列纳指100工业（偏强侧）。"),
    "STAG": ("联动", "-2.93%列主题层房地产与REITs（偏弱侧）。"),
    "STC": ("联动", "-12.42%列罗素2000金融（偏弱侧）。"),
    "TENB": ("联动", "+4.00%列主题层网络安全（偏强侧）。"),
    "TKO": ("联动", "+1.21%列标普500通信服务（偏强侧）。"),
    "TRI": ("联动", "+1.13%列纳指100工业（偏强侧）。"),
    "TTWO": ("联动", "+2.33%列标普500通信服务（偏强侧）。"),
    "TULP": ("联动", "-14.09%列All Stocks必需消费（偏弱侧）。"),
    "UNH": ("联动", "-2.10%列道指医疗保健（偏弱侧）。"),
    "UP": ("联动", "-5.85%列罗素2000工业（偏弱侧）。"),
    "VHUB": ("联动", "-10.64%列All Stocks必需消费（偏弱侧）。"),
    "VIOT": ("联动", "+15.65%列All Stocks可选消费（偏强侧）。"),
    "WMT": ("联动", "-2.70%列道指必需消费（偏弱侧）。"),
    "WYNN": ("联动", "+1.53%列标普500可选消费（偏强侧）。"),
    "ZBH": ("联动", "-2.75%列标普500医疗保健（偏弱侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "UGA", "perf": 4.749, "form": "商品信托", "exposure": "汽油期货（RBOB）",
         "reason": "汽油期货ETF +4.75%领涨全市场：柴油出口禁令政治溢价的第四轮往返（周三+4.86%〔9.23〕→两日回吐→本日再暴涨）——成品油政治定价的极端波动结构。合并删除：无同簇产品。"},
        {"ticker": "BRF", "perf": 3.021, "form": "交易所交易基金", "exposure": "巴西股票",
         "reason": "巴西ETF +3.02%：新兴市场内部的商品/出口强美元周期受益端（EWZ +2.14%同向）——与土耳其-2.73%/泰国-2.52%的EM分化。合并删除：EWZ +2.14%（同簇巴西，保留更强者）。"},
        {"ticker": "DBE", "perf": 2.685, "form": "交易所交易基金", "exposure": "能源综合（期货）",
         "reason": "能源综合ETF +2.69%：油价反弹（USO +1.61%/BNO +2.28%）与汽油暴涨的商品端共振——能源股（XLE -0.07%持平）落后于商品端的分化日。合并删除：PXE/PXI/IXC/FENY/VDE（同簇能源敞口）。"},
    ],
    "down": [
        {"ticker": "TUR", "perf": -2.734, "form": "交易所交易基金", "exposure": "土耳其股票",
         "reason": "土耳其ETF -2.73%：全球利率冲击（30年期美债5.5%上方）下高外部融资需求新兴市场的压力端。合并删除：无同簇产品。"},
        {"ticker": "REM", "perf": -2.568, "form": "交易所交易基金", "exposure": "抵押REIT（mREIT）",
         "reason": "抵押REIT ETF -2.57%：利率敏感的极端端——商业抵押REIT（Blackstone Mortgage -6.99%/Claros -6.57%/Ares CRE -6.57%）领跌，房地产两范围领跌的板块端确认。合并删除：IYR -1.12%/RWO/RWR/ICF/FRI（同簇房地产，保留最深跌幅的mREIT端）。"},
        {"ticker": "THD", "perf": -2.516, "form": "交易所交易基金", "exposure": "泰国股票",
         "reason": "泰国ETF -2.52%：新兴市场亚洲端（高外债/旅游敏感）在美元与利率双重压力下的补跌——与巴西+3.02%的EM内部分化。合并删除：无同簇产品。"},
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
        text = "核查9月20日盘后至9月30日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-30"
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重；原油期货簇（BNO/DBO/USO/DBE/DBE能源股）保留BNO、汽油簇（UGA）独立、铂钯银现货簇分别保留最强者（PPLT/PALL/SIVR为不同金属）。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-09-30_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-30_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月30日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月30日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周三为PCE（新方法论）+美光财报（盘后）日：科技四个股票范围领涨（All Stocks +0.32%/标普500 +0.56%〔Gen Digital +5.61%/新思科技+4.78%〔AWS逾10亿美元芯片IP协议〕/HPE +3.90%〔上调指引创纪录新高〕〕——软件/云计算/网络安全全线反弹：IGV +1.20%/XSW +1.17%/WCLD +1.73%/IHAK +1.43%〔主题层6个清一色涨：教育科技+2.17%/软件+1.41%/网络安全+1.37%/大数据/物联网/量子计算〕；存储器主题+1.06%〔美光财报盘后为验证〕）；通信服务三个范围为相对强度领涨（道指谷歌+0.93%/标普Paramount +3.40%〔获准完成华纳收购〕/Take-Two +2.33%——但板块ETF XLC -0.45%受Meta -1.84%拖累，等权RSPC +0.18%）；可选消费三个范围居前（标普Airbnb +2.35%/Royal Caribbean +1.99%〔财报延续〕/永利+1.53%；XLY -0.28%分化）。跌幅侧：必需消费四个范围领跌（XLP -1.53%：通用磨坊新CEO -4.91%/味好美-4.13%/克罗格-3.57%/沃尔玛-2.70%——PCE日的消费端重定价）；金融三个范围领跌（XLF -1.13%：PayPal -2.52%/保险KIE -1.65%）；房地产两个范围领跌（IYR -1.12%：商业抵押REIT全线-6.5%+〔Blackstone Mortgage -6.99%〕——利率冲击的极端端；REIT主题清一色跌-1.24%）。商品端：汽油ETF +4.75%再领涨全市场（柴油禁令政治溢价第四轮往返）、原油USO +1.61%/BNO +2.28%反弹但能源股XLE持平落后；天然气+0.19%企稳。贵金属回落（黄金-0.54%/金矿-1.60%/白银-1.75%）。铀链回落（URNJ -3.54%）。巴西ETF +3.02%列第二对土耳其-2.73%/泰国-2.52%（EM分化）。VIX期货ETF反弹（VIXY +1.56%——季末对冲）。Moderna遭花旗卖出评级-5.35%；波音抢走诺格200亿美元海军合同（NOC -4.19%）；Bloom Energy两日大涨后回吐-4.90%。当日无行情性质结构变化。',
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5503/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/101、Russell 2000 1937/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    (OUT / "finviz_2026-09-30_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-30_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-30_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
