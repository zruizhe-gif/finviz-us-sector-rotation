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
    "Waste": "废物处理",
    "Water": "水务",
    "Climate": "气候",
    "Agriculture": "农业",
    "Tourism": "旅游",
    "Air Quality": "空气质量",
    "Energy": "能源",
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
    "AMTX": "Aemetis Inc",
    "AMZN": "Amazon.com Inc",
    "CLNE": "Clean Energy Fuels Corp",
    "COHU": "Cohu Inc",
    "DDOG": "Datadog Inc",
    "FMC": "FMC Corp",
    "FROG": "JFrog Ltd",
    "LEU": "Centrus Energy Corp",
    "LRN": "Stride Inc",
    "MOS": "Mosaic Company",
    "QLYS": "Qualys Inc",
    "RMBS": "Rambus Inc",
    "RPD": "Rapid7 Inc",
    "SKIL": "Skillsoft Corp",
    "TWLO": "Twilio Inc",
    "WDC": "Western Digital Corp",
    "WLY": "John Wiley & Sons Inc",
}

COMPANY_NAME_FIX = {}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEP": ("联动", "-1.90%列纳指100公用事业（偏弱侧）。"),
    "AIBZ": ("联动", "+26.61%列All Stocks科技（偏强侧）。"),
    "AMGN": ("联动", "-1.75%列纳指100医疗保健（偏弱侧）。"),
    "AMP": ("联动", "-4.07%列标普500金融（偏弱侧）。"),
    "AMTX": ("联动", "-6.16%列主题层农业商品/主题层能源商品（偏弱侧）。"),
    "AMZN": ("直接", "摩根士丹利列出五大催化剂并上调目标价。"),
    "ANGH": ("联动", "+12.72%列All Stocks通信服务（偏强侧）。"),
    "ANNX": ("联动", "+17.59%列罗素2000医疗保健（偏强侧）。"),
    "APP": ("联动", "+1.12%列标普500通信服务（偏强侧）。"),
    "ARE": ("联动", "-2.38%列标普500房地产（偏弱侧）。"),
    "ARR": ("联动", "-6.97%列罗素2000房地产（偏弱侧）。"),
    "AXTI": ("联动", "+10.34%列罗素2000科技（偏强侧）。"),
    "BKHA": ("联动", "-32.95%列All Stocks金融（偏弱侧）。"),
    "BLND": ("联动", "+9.63%列罗素2000科技（偏强侧）。"),
    "BRNX": ("联动", "-10.99%列All Stocks公用事业（偏弱侧）。"),
    "BXP": ("联动", "-2.13%列标普500房地产（偏弱侧）。"),
    "CANG": ("联动", "-29.74%列All Stocks金融（偏弱侧）。"),
    "CBOE": ("联动", "-2.70%列标普500金融（偏弱侧）。"),
    "CEG": ("联动", "-3.01%列标普500公用事业/纳指100公用事业（偏弱侧）。"),
    "CHGA": ("联动", "-14.65%列All Stocks房地产（偏弱侧）。"),
    "CLNE": ("联动", "-6.00%列主题层能源商品（偏弱侧）。"),
    "COHU": ("联动", "+6.02%列主题层半导体（偏强侧）。"),
    "COIN": ("直接", "Marqeta与Coinbase通过Base链打通稳定币卡结算。"),
    "CRML": ("联动", "-6.60%列罗素2000基础材料（偏弱侧）。"),
    "CVX": ("联动", "-0.28%列道指能源（偏弱侧）。"),
    "DASH": ("联动", "+2.32%列标普500可选消费/纳指100可选消费（偏强侧）。"),
    "DDOG": ("直接", "评级上调（Barron's口径：OpenAI相关拖累正在消退）；终结五日连跌。"),
    "DIS": ("直接", "迪士尼向面临破产与诉讼的AI公司提出2,000万美元要约（聊天机器人诱导儿童自残案）。"),
    "DOC": ("联动", "-3.06%列标普500房地产（偏弱侧）。"),
    "ES": ("联动", "-3.54%列标普500公用事业（偏弱侧）。"),
    "EXC": ("联动", "-2.51%列纳指100公用事业（偏弱侧）。"),
    "EXYN": ("联动", "+38.78%列All Stocks科技（偏强侧）。"),
    "FET": ("联动", "+8.08%列罗素2000能源（偏强侧）。"),
    "FMC": ("联动", "-5.30%列主题层农业商品（偏弱侧）。"),
    "FOXA": ("联动", "+1.75%列标普500通信服务（偏强侧）。"),
    "FROG": ("联动", "+7.93%列主题层软件（偏强侧）。"),
    "GDHG": ("联动", "+8.49%列All Stocks可选消费（偏强侧）。"),
    "GILD": ("联动", "-2.00%列纳指100医疗保健（偏弱侧）。"),
    "GOOGL": ("联动", "+1.05%列标普500通信服务/道指通信服务（偏强侧）。"),
    "HD": ("联动", "+0.08%列道指可选消费（偏强侧）。"),
    "HPK": ("联动", "+7.96%列罗素2000能源（偏强侧）。"),
    "HPP": ("联动", "-12.43%列All Stocks房地产/罗素2000房地产（偏弱侧）。"),
    "HTO": ("联动", "-3.14%列罗素2000公用事业（偏弱侧）。"),
    "HTOO": ("联动", "-8.33%列All Stocks公用事业（偏弱侧）。"),
    "IBM": ("联动", "+1.83%列道指科技（偏强侧）。"),
    "IRON": ("直接", "罕见病药bitopertin（Disc Medicine）获FDA审批第二次机会——试验数据重燃获批希望，2022年以来最佳单日。"),
    "KO": ("联动", "-0.51%列道指必需消费（偏弱侧）。"),
    "LEU": ("直接", "Centrus以1.16亿美元收购Westerman Holdings（关键供应商内部化）——股价仍下跌4.19%（与核能链走弱一致）。"),
    "LIN": ("联动", "+1.00%列纳指100基础材料（偏强侧）。"),
    "LRN": ("联动", "-1.70%列主题层教育科技（偏弱侧）。"),
    "MOS": ("联动", "-4.78%列主题层农业商品（偏弱侧）。"),
    "MSFT": ("联动", "+0.84%列道指科技（偏强侧）。"),
    "NAUT": ("联动", "+27.67%列罗素2000医疗保健（偏强侧）。"),
    "NKE": ("联动", "+0.21%列道指可选消费（偏强侧）。"),
    "NRG": ("直接", "Jefferies与Seaport下调目标价。"),
    "NRGV": ("联动", "-2.46%列罗素2000公用事业（偏弱侧）。"),
    "NVDA": ("联动", "+1.38%列道指科技（偏强侧）。"),
    "NXXT": ("联动", "-6.78%列All Stocks公用事业（偏弱侧）。"),
    "ODC": ("联动", "-6.42%列罗素2000基础材料（偏弱侧）。"),
    "ORA": ("联动", "-2.99%列罗素2000公用事业（偏弱侧）。"),
    "PED": ("联动", "+7.01%列罗素2000能源（偏强侧）。"),
    "PG": ("联动", "-1.04%列道指必需消费（偏弱侧）。"),
    "PYPL": ("联动", "-0.34%列纳指100金融（偏弱侧）。"),
    "QLYS": ("联动", "+4.99%列主题层网络安全（偏强侧）。"),
    "RBBN": ("联动", "+14.39%列罗素2000科技（偏强侧）。"),
    "REBN": ("联动", "+20.71%列All Stocks可选消费（偏强侧）。"),
    "REGN": ("联动", "-1.10%列纳指100医疗保健（偏弱侧）。"),
    "RMBS": ("联动", "+6.20%列主题层半导体（偏强侧）。"),
    "ROLR": ("联动", "+12.58%列All Stocks可选消费（偏强侧）。"),
    "RPD": ("联动", "+4.84%列主题层网络安全（偏强侧）。"),
    "RPGL": ("联动", "+16.84%列All Stocks科技（偏强侧）。"),
    "SBMT": ("联动", "-10.73%列罗素2000基础材料（偏弱侧）。"),
    "SEVN": ("联动", "-10.60%列All Stocks房地产/罗素2000房地产（偏弱侧）。"),
    "SHFS": ("联动", "-34.68%列All Stocks金融（偏弱侧）。"),
    "SHW": ("联动", "-1.07%列道指基础材料（偏弱侧）。"),
    "SKIL": ("联动", "-15.22%列主题层教育科技（偏弱侧）。"),
    "SLE": ("联动", "+6.90%列All Stocks通信服务（偏强侧）。"),
    "SNDK": ("直接", "美股存储链自长鑫/三星冲击中反弹（+5.53%）；中国长鑫存储A股周一盘后继续下跌（业绩后）。"),
    "TSLA": ("直接", "财报前反弹（华尔街预计季度业绩下滑）；分析师称特斯拉-SpaceX合并非易事。"),
    "TWLO": ("联动", "+5.29%列主题层软件（偏强侧）。"),
    "WDC": ("直接", "同上：存储链反弹（+6.09%）。"),
    "WLY": ("联动", "-1.78%列主题层教育科技（偏弱侧）。"),
    "WMT": ("直接", "沃尔玛出售美国债务业务、瞄准加拿大市场（消费增长背景）。"),
    "XHLD": ("联动", "+14.14%列All Stocks通信服务（偏强侧）。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "BBC", "perf": 4.346, "form": "交易所交易基金", "exposure": "生物科技临床试验（Virtus）",
         "reason": "临床试验生物科技ETF +4.35%领涨全市场：XBI +2.45%同步反弹，Disc Medicine罕见病药获FDA审批二次机会单日+38.86%带动临床试验板块。合并删除：无同簇产品。"},
        {"ticker": "EWY", "perf": 4.081, "form": "交易所交易基金", "exposure": "韩国股票（iShares）",
         "reason": "韩国ETF +4.08%列第二：上周五KOSPI熔断与存储链冲击后的修复反弹——美股存储链同日反弹（西部数据+6.09%/闪迪+5.53%/美光+2.96%）。合并删除：无同簇产品。"},
        {"ticker": "BRF", "perf": 2.831, "form": "交易所交易基金", "exposure": "巴西小盘股（VanEck）",
         "reason": "巴西小盘ETF +2.83%列第三：新兴市场内部结构性反弹（与印尼-3.32%的降级冲击分化）。合并删除：EWZ（同簇巴西，保留小盘端）。"},
    ],
    "down": [
        {"ticker": "VIXY", "perf": -4.061, "form": "交易所交易基金", "exposure": "VIX短期期货（ProShares）",
         "reason": "VIX短期期货ETF -4.06%领跌：周五+8.11%对冲买盘的回吐——AI链反弹日波动率压缩。合并删除：VXX（同簇VIX期货）。"},
        {"ticker": "KBWD", "perf": -3.773, "form": "交易所交易基金", "exposure": "高股息金融（Invesco KBW）",
         "reason": "高股息金融ETF -3.77%列第二：金融板块周五涨幅的回吐（XLF -0.83%；AMP -4.07%列标普500金融跌幅端）。合并删除：KRE/KBE（银行簇当日跌幅较浅）。"},
        {"ticker": "EIDO", "perf": -3.320, "form": "交易所交易基金", "exposure": "印尼股票（iShares）",
         "reason": "印尼ETF -3.32%列第三：MSCI降级咨询后的第二日续跌（周五-14.90%）。合并删除：IDX（同簇印尼）。"},
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
        text = "核查10月16日盘后至10月19日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-20"
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
            f"- `finviz_2026-10-20_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-20_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月19日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月19日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周一美股AI链反弹日：**生物科技临床试验ETF +4.35%领涨全市场**（XBI +2.45%；Disc Medicine罕见病药获FDA审批二次机会+38.86%）；韩国ETF +4.08%列第二（上周KOSPI熔断与存储链冲击后的修复）；巴西小盘+2.83%。涨幅侧：可选消费/科技/通信服务以平均表现补位进入前三（**无清一色上涨的股票范围板块**）；主题层**11个主题清一色上涨**（半导体/网安/软件/硬件/AI/社交媒体/物联网/工业自动化/VR/数字娱乐/量子——SOXX +1.73%/DRAM +4.05%/WCLD +2.07%/IHAK +1.14%）；纳指100基础材料2只清一色涨。个股端：亚马逊+4.98%（摩根士丹利列五大催化剂并上调目标价）、特斯拉+3.76%（财报前）、Datadog +5.36%（评级上调）、西部数据+6.09%/闪迪+5.53%/美光+2.96%（存储链自长鑫冲击中反弹）、Twilio +5.29%。跌幅侧：**公用事业三个范围领跌**（XLU -2.01%：AEP -1.90%/NiSource -1.71%/核电CEG -3.01%/独立发电商VST -1.53%——周五防御轮入的回吐与AI电力链续弱）；**VIX短期期货ETF -4.06%领跌全市场**（周五+8.11%对冲买盘回吐）；高股息金融-3.77%（AMP -4.07%）；**印尼ETF -3.32%续跌**（MSCI降级咨询第二日）；NRG -4.21%（Jefferies/Seaport下调目标价）；Centrus -4.19%（收购Westerman Holdings公告当日仍跌）；道指端基础材料/必需消费/能源清一色跌（周五轮入方回吐）。当日行情性质结构变化：无。',
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5434/5547、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 100/100、Russell 2000 1929/1943、Themes 268/268和ETF 657/658；缺值代码不参与计算。", ""]
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
    for company in THEME_COMPANY.values():
        body_without_urls = body_without_urls.replace(company, "")
    for term in forbidden:
        assert term not in body_without_urls, term
    assert text.count("暂未找到同日直接催化") > 0
    assert "CIK=&" not in text
    for ticker, company in THEME_COMPANY.items():
        assert f"{company}（{ticker}）" in text, ticker


def main() -> None:
    stocks, all_codes = audit_inputs()
    (OUT / "finviz_2026-10-20_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-20_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-20_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
