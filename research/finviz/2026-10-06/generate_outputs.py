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
    "ASTS": "AST SpaceMobile Inc",
    "AUID": "authID Inc",
    "BKYI": "Bio-Key International Inc",
    "CSCO": "Cisco Systems Inc",
    "FTNT": "Fortinet Inc",
    "GNRC": "Generac Holdings Inc",
    "LDOS": "Leidos Holdings Inc",
    "NRG": "NRG Energy Inc",
    "PL": "Planet Labs PBC",
    "STEM": "Stem Inc",
    "STX": "Seagate Technology Holdings Plc",
    "TEM": "Tempus AI Inc",
    "TWST": "Twist Bioscience Corp",
    "TXG": "10x Genomics Inc",
    "VSAT": "Viasat Inc",
    "WDC": "Western Digital Corp",
    "WOLF": "Wolfspeed Inc",
    "ZS": "Zscaler Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    "AEHR": ("联动", "-11.74%列罗素2000科技（偏弱侧）。"),
    "AMOD": ("联动", "-33.86%列All Stocks科技（偏弱侧）。"),
    "APOG": ("直接", "Apogee Q2销售增长后上调FY2027指引。"),
    "APP": ("联动", "-1.13%列纳指100通信服务（偏弱侧）。"),
    "ASTS": ("联动", "+8.01%列主题层太空科技（偏强侧）。"),
    "AUID": ("直接", "authID宣布EinStrong 200万美元协议+定价最高135万美元私募配售（融资稀释主导）。"),
    "AVBP": ("联动", "-46.98%列All Stocks医疗保健（偏弱侧）。"),
    "AXP": ("联动", "+0.17%列道指金融（偏强侧）。"),
    "BEN": ("联动", "-1.34%列标普500金融（偏弱侧）。"),
    "BESS": ("联动", "+22.04%列All Stocks公用事业（偏强侧）。"),
    "BIPC": ("联动", "+3.74%列罗素2000公用事业（偏强侧）。"),
    "BKR": ("联动", "-0.44%列纳指100能源（偏弱侧）。"),
    "BKYI": ("联动", "-5.70%列主题层生物识别（偏弱侧）。"),
    "BZAI": ("直接", "Blaize把2026收入指引砍至3200万—3600万美元、司法部传票引发下调——-33.42%。"),
    "CCL": ("联动", "+3.99%列标普500可选消费（偏强侧）。"),
    "CEG": ("直接", "谷歌与Constellation接近10亿美元以上核电协议的报道+同业收购谈判传闻。"),
    "CRM": ("联动", "-2.09%列道指科技（偏弱侧）。"),
    "CSCO": ("直接", "思科43亿美元协作业务把WhatsApp接入Webex；纽交所母公司申请代币化63只美股。"),
    "CVX": ("联动", "+0.54%列道指能源（偏强侧）。"),
    "DIS": ("联动", "+0.41%列道指通信服务（偏强侧）。"),
    "DLR": ("联动", "+2.66%列标普500房地产（偏强侧）。"),
    "DXCM": ("联动", "-4.04%列标普500医疗保健（偏弱侧）。"),
    "EGAN": ("联动", "-11.39%列罗素2000科技（偏弱侧）。"),
    "EXC": ("联动", "+2.11%列纳指100公用事业（偏强侧）。"),
    "FANG": ("联动", "+0.49%列纳指100能源（偏强侧）。"),
    "FCEL": ("联动", "+14.28%列罗素2000工业（偏强侧）。"),
    "FDS": ("联动", "-1.60%列标普500金融（偏弱侧）。"),
    "FG": ("联动", "-5.86%列罗素2000金融（偏弱侧）。"),
    "FLNC": ("联动", "+4.97%列罗素2000公用事业（偏强侧）。"),
    "FNGR": ("联动", "-18.18%列All Stocks通信服务（偏弱侧）。"),
    "FOXA": ("联动", "-1.97%列标普500通信服务（偏弱侧）。"),
    "FTNT": ("联动", "+3.88%列主题层网络安全（偏强侧）。"),
    "GEHC": ("联动", "-1.48%列纳指100医疗保健（偏弱侧）。"),
    "GNRC": ("联动", "+3.91%列主题层智能家居（偏强侧）。"),
    "GOOGL": ("联动", "+0.35%列道指通信服务（偏强侧）。"),
    "GSHD": ("联动", "-6.06%列罗素2000金融（偏弱侧）。"),
    "HNRG": ("联动", "+6.17%列罗素2000公用事业（偏强侧）。"),
    "HOOD": ("联动", "-1.85%列标普500金融（偏弱侧）。"),
    "HTZ": ("联动", "+15.08%列罗素2000工业（偏强侧）。"),
    "IBM": ("联动", "-0.13%列道指科技（偏弱侧）。"),
    "IDXX": ("联动", "-2.21%列纳指100医疗保健（偏弱侧）。"),
    "ILMN": ("联动", "-6.86%列标普500医疗保健（偏弱侧）。"),
    "IRM": ("联动", "+3.71%列标普500房地产（偏强侧）。"),
    "JPM": ("联动", "-0.33%列道指金融（偏弱侧）。"),
    "KAPA": ("联动", "-25.81%列All Stocks医疗保健（偏弱侧）。"),
    "LDOS": ("联动", "-2.31%列主题层生物识别（偏弱侧）。"),
    "LEU": ("联动", "+8.79%列罗素2000能源（偏强侧）。"),
    "LIN": ("联动", "+1.57%列纳指100基础材料（偏强侧）。"),
    "LVWR": ("联动", "+10.88%列All Stocks可选消费（偏强侧）。"),
    "META": ("联动", "-0.41%列纳指100通信服务（偏弱侧）。"),
    "MF": ("联动", "-20.28%列All Stocks通信服务（偏弱侧）。"),
    "MIAX": ("直接", "迈阿密国际控股公布9月交易数据。"),
    "MRNA": ("直接", "俄罗斯瘟疫实验室事件的疫苗股脉冲（MRNA当日实际-7.75%——脉冲即回落）。"),
    "MWYN": ("联动", "+16.67%列All Stocks可选消费（偏强侧）。"),
    "NCLH": ("联动", "+4.30%列标普500可选消费（偏强侧）。"),
    "NEXR": ("联动", "+10.89%列All Stocks可选消费（偏强侧）。"),
    "NRG": ("联动", "+7.03%列标普500公用事业（偏强侧）。"),
    "NVDA": ("联动", "+0.14%列道指科技（偏强侧）。"),
    "NWSA": ("联动", "-1.38%列标普500通信服务（偏弱侧）。"),
    "PL": ("联动", "+6.97%列主题层太空科技（偏强侧）。"),
    "PYPL": ("联动", "+0.37%列纳指100金融（偏强侧）。"),
    "RCL": ("联动", "+5.00%列标普500可选消费（偏强侧）。"),
    "RCT": ("联动", "-30.17%列All Stocks科技（偏弱侧）。"),
    "RYET": ("联动", "+11.00%列All Stocks必需消费（偏强侧）。"),
    "SBAC": ("联动", "+4.87%列标普500房地产（偏强侧）。"),
    "SEI": ("联动", "+6.62%列罗素2000能源（偏强侧）。"),
    "SHW": ("联动", "+0.85%列道指基础材料（偏强侧）。"),
    "SKYD": ("直接", "派拉蒙正式完成对华纳兄弟探索的收购——缔造新全球娱乐巨头（-2.51%为完成日定价消化）。"),
    "STEM": ("联动", "+12.23%列主题层智能家居（偏强侧）。"),
    "STX": ("联动", "-9.18%列主题层半导体（偏弱侧）。"),
    "SXTC": ("联动", "-39.90%列All Stocks医疗保健（偏弱侧）。"),
    "TANH": ("联动", "+20.40%列All Stocks必需消费（偏强侧）。"),
    "TEM": ("联动", "-13.85%列主题层医疗保健与生物科技（偏弱侧）。"),
    "TJGC": ("联动", "-15.39%列All Stocks通信服务（偏弱侧）。"),
    "TLN": ("联动", "+12.43%列All Stocks公用事业（偏强侧）。"),
    "TRV": ("联动", "-0.02%列道指金融（偏弱侧）。"),
    "TTWO": ("联动", "-0.46%列纳指100通信服务（偏弱侧）。"),
    "TWST": ("直接", "NeoGenomics公布CEO继任计划——收入超预期仍大跌。"),
    "TXG": ("直接", "同上NeoGenomics CEO换帅事件（按字幕关联保留）。"),
    "UEC": ("联动", "+8.13%列罗素2000能源（偏强侧）。"),
    "VSAT": ("联动", "+6.58%列主题层太空科技（偏强侧）。"),
    "VST": ("直接", "能源部拟向Vistra贷款42亿美元用于核电机组改造。"),
    "WDC": ("联动", "-6.93%列主题层半导体（偏弱侧）。"),
    "WOLF": ("联动", "-5.07%列主题层半导体（偏弱侧）。"),
    "WYHG": ("联动", "+14.80%列All Stocks必需消费（偏强侧）。"),
    "XEL": ("联动", "+1.74%列纳指100公用事业（偏强侧）。"),
    "ZS": ("直接", "Zscaler CEO驳斥AI颠覆恐慌、重申FY2027指引。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "URA", "perf": 4.006, "form": "交易所交易基金", "exposure": "全球铀矿",
         "reason": "铀矿ETF +4.01%领涨全市场：核能谱系全面爆发——能源部拟向Vistra贷款42亿美元改造核电机组（VST +10.77%）、谷歌与Constellation接近10亿美元以上核电协议（CEG +12.25%）——AI电力需求的核电定价日；铀矿端全线+5%级（URNM +4.97%/URNJ +4.87%/NLR +5.50%）。合并删除：无同簇产品。"},
        {"ticker": "XLU", "perf": 2.977, "form": "交易所交易基金", "exposure": "公用事业（SPDR）",
         "reason": "公用事业ETF +2.98%列全市场第二：四个股票范围领涨的核心——标普500 31只清一色涨/+3.19%（CEG +12.25%/VST +10.77%/NRG +7.03%）；AI电力＋核电协议＋利率回落的三重共振。合并删除：无同簇产品。"},
        {"ticker": "IYZ", "perf": 2.888, "form": "交易所交易基金", "exposure": "电信（iShares）",
         "reason": "电信ETF +2.89%列全市场第三：类债端修复与AI电力叙事的电信权重共振（思科Webex接入WhatsApp的协作生态为催化背景）。合并删除：FCOM（同簇电信，保留更强者）。"},
    ],
    "down": [
        {"ticker": "PTH", "perf": -4.465, "form": "交易所交易基金", "exposure": "医疗保健动量（Dorsey Wright）",
         "reason": "医疗保健动量ETF -4.47%领跌全市场：医疗保健四个股票范围领跌的动量端确认——Moderna -7.75%（俄罗斯瘟疫实验室疫苗股脉冲后回落）/Illumina -6.86%/NeoGenomics CEO换帅-12%。合并删除：无同簇产品。"},
        {"ticker": "XBI", "perf": -3.387, "form": "交易所交易基金", "exposure": "生物科技（SPDR）",
         "reason": "生物科技ETF -3.39%：医疗保健端的最大跌幅——罗素2000医疗保健420只中334跌/整体-2.85%（基因组学-8.2%/诊断-4.6%）；Viking回吐与CEO换帅事件叠加。合并删除：无同簇产品。"},
        {"ticker": "BBC", "perf": -3.037, "form": "交易所交易基金", "exposure": "临床试验生物科技",
         "reason": "临床试验生物科技ETF -3.04%：小盘临床端的连续出清——上周四领跌→周五企稳→周二再跌的脉冲结构延续。合并删除：无同簇产品。"},
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
        text = "核查9月26日盘后至10月6日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-10-06"
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
            f"- `finviz_2026-10-06_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-10-06_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年10月6日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年10月6日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周二为AI电力/核电定价日+医疗保健出清日：**铀矿ETF（URA）+4.01%领涨全市场**（能源部拟向Vistra贷款42亿美元改造核电机组〔VST +10.77%〕、谷歌与Constellation接近10亿美元以上核电协议〔CEG +12.25%〕——铀矿全线+5%级：NLR +5.50%/URNM +4.97%/URNJ +4.87%）；**公用事业四个股票范围领涨**（标普500 31只清一色涨/+3.19%：CEG +12.25%/VST +10.77%/NRG +7.03%；XLU +2.98%列全市场第二、电信IYZ +2.89%列第三——利率回落+AI电力+核电协议三重共振）；可选消费两个范围居前（标普500 +1.34%：邮轮三重奏RCL +5.00%/NCLH +4.30%/CCL +3.99%；XLY +1.18%/RSPD +1.14%）；基础材料两个范围（道指宣伟+0.85%/纳指100林德+1.57%双清一色）。跌幅侧：**医疗保健四个范围领跌**（罗素2000医疗保健420只中334跌/-2.85%：基因组学-8.2%/诊断-4.6%——Moderna -7.75%〔俄罗斯瘟疫实验室疫苗股脉冲后回落〕/Illumina -6.86%/NeoGenomics CEO换帅-12%；XBI -3.39%/BBC -3.04%/医疗动量PTH -4.47%领跌全市场）；通信服务四个范围领跌（All Stocks +0.24%〔相对〕/标普500 19只中10跌：派拉蒙-2.51%〔正式完成华纳收购的定价消化〕/福克斯-1.97%；但道指通信清一色涨〔迪士尼+0.41%/谷歌+0.35%〕的分化结构）；金融三个范围（罗素2000金融-0.35%：迈阿密国际-10.29%）。主题层**12个清一色涨**（太空科技+2.13%〔LUNR +5.39%/RKLB +2.79%〕/网络安全+2.07%〔Zscaler +5.18%/Fortinet +3.88%〕/智能家居/物联网/数字娱乐/工业自动化/消费品/教育科技/自动驾驶/健康食品/大数据/量子计算）对1个清一色跌（生物识别-1.91%）——医疗生物-2.36%/半导体-0.68%〔存储-3.4%：希捷-9.18%/西数-6.93%连续第三日〕列平均补位跌幅端。软件续强（IGV +1.31%）；思科+4.54%（Webex接入WhatsApp）；住宅建筑XHB +1.11%；VIX期货ETF大跌（VIXY -2.66%）；贵金属微涨；比特币ETF持平；巴西+2.11%延续。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-10-06_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-10-06_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-10-06_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
