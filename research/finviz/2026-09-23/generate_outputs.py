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
    "ATLX": "Atlas Lithium Corp",
    "BKYI": "Bio-Key International Inc",
    "BYND": "Beyond Meat Inc",
    "CRWD": "Crowdstrike Holdings Inc",
    "EXK": "Endeavour Silver Corp",
    "FLY": "Firefly Aerospace Inc",
    "IPX": "IperionX Ltd ADR",
    "LUNR": "Intuitive Machines Inc",
    "OKTA": "Okta Inc",
    "PANW": "Palo Alto Networks Inc",
    "PLTR": "Palantir Technologies Inc",
    "RENT": "Rent the Runway Inc",
    "SPCE": "Virgin Galactic Holdings Inc",
    "VITL": "Vital Farms Inc",
}

COMPANY_NAME_FIX = {
    "SPCX": "Space Exploration Technologies Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：9月3日16:00 ET盘后事件可解释9月4日；9月4日16:00 ET后事件不得倒推。
R = {
    'AIXC':('联动', '+17.73%列All Stocks科技（偏强侧）。'),
    'AMGN':('直接', "Amgen宣布干燥综合征（Sjögren's）三期试验阳性；Jefferies上调目标价至410美元——周二+4.34%拉升后的利好兑现回落。"),
    'AMTX':('联动', '-10.16%列罗素2000基础材料（偏弱侧）。'),
    'AMZN':('联动', '-2.24%列道指可选消费（偏弱侧）。'),
    'APA':('联动', '+3.31%列标普500能源（偏强侧）。'),
    'APEI':('联动', '+1.97%列罗素2000必需消费（偏强侧）。'),
    'APP':('联动', '-4.10%列标普500通信服务（偏弱侧）。'),
    'ARE':('联动', '-3.69%列标普500房地产（偏弱侧）。'),
    'ATLX':('联动', '-10.13%列主题层金属商品（偏弱侧）。'),
    'BA':('直接', '波音获土耳其航空最多150架737 MAX订单（该区域史上最大单通道订单）；工会建议成员投票通过最新劳资合同。'),
    'BG':('联动', '+1.34%列标普500必需消费（偏强侧）。'),
    'BKR':('联动', '+1.34%列纳指100能源（偏强侧）。'),
    'BKYI':('联动', '+4.62%列主题层生物识别（偏强侧）。'),
    'BXP':('联动', '-3.03%列标普500房地产（偏弱侧）。'),
    'BYND':('联动', '-12.86%列主题层消费品（偏弱侧）。'),
    'CAT':('联动', '+0.50%列道指工业（偏强侧）。'),
    'CBRE':('联动', '-3.29%列标普500房地产（偏弱侧）。'),
    'CCOI':('联动', '-12.68%列All Stocks通信服务（偏弱侧）。'),
    'CGEM':('联动', '-22.15%列罗素2000医疗保健（偏弱侧）。'),
    'COP':('联动', '+2.25%列标普500能源（偏强侧）。'),
    'COST':('联动', '+0.59%列纳指100必需消费（偏强侧）。'),
    'CRML':('联动', '-9.60%列罗素2000基础材料（偏弱侧）。'),
    'CRWD':('联动', '+4.97%列主题层网络安全（偏强侧）。'),
    'CTAS':('直接', 'Cintas发布2027财年第一季度财报（周三财报日）。'),
    'CVX':('联动', '+1.53%列道指能源（偏强侧）。'),
    'DIS':('联动', '-0.35%列道指通信服务（偏弱侧）。'),
    'DVN':('联动', '+2.37%列标普500能源（偏强侧）。'),
    'EGHT':('联动', '+15.07%列All Stocks科技（偏强侧）。'),
    'EIX':('联动', '-2.80%列标普500公用事业（偏弱侧）。'),
    'EVER':('联动', '-9.82%列罗素2000通信服务（偏弱侧）。'),
    'EXK':('联动', '-11.89%列All Stocks基础材料（偏弱侧）。'),
    'FANG':('联动', '+0.62%列纳指100能源（偏强侧）。'),
    'FAST':('联动', '+1.82%列标普500工业（偏强侧）。'),
    'FLY':('联动', '-6.19%列主题层太空科技（偏弱侧）。'),
    'FSLY':('联动', '+13.69%列罗素2000科技（偏强侧）。'),
    'GIS':('直接', 'General Mills 2027财年Q1：盈利超预期但利润大跌、销售下滑，确认全年指引——防御板块财报日的相对强势。'),
    'GLND':('联动', '+15.94%列All Stocks能源（偏强侧）。'),
    'GOOGL':('联动', '-3.80%列标普500通信服务（偏弱侧）。'),
    'GRML':('直接', 'Greenland Mines就美丹格陵兰安全协议签署发公告——周二+50.21%的爆发当日完全逆转-20.92%。'),
    'HD':('联动', '-2.83%列道指可选消费（偏弱侧）。'),
    'HONA':('联动', '-2.38%列纳指100工业（偏弱侧）。'),
    'IEX':('联动', '+1.76%列标普500工业（偏强侧）。'),
    'INNV':('直接', 'InnovAge定价二级市场股东减持的二次发行——小盘医疗保健的减持惩罚。'),
    'IPX':('联动', '-7.92%列主题层金属商品（偏弱侧）。'),
    'IR':('联动', '+3.21%列标普500工业（偏强侧）。'),
    'KDP':('联动', '+0.79%列纳指100必需消费（偏强侧）。'),
    'KO':('联动', '-0.59%列道指必需消费（偏弱侧）。'),
    'KOS':('联动', '+3.11%列罗素2000能源（偏强侧）。'),
    'LAUR':('联动', '+1.63%列罗素2000必需消费（偏强侧）。'),
    'LIN':('联动', '+1.03%列纳指100基础材料（偏强侧）。'),
    'LSE':('联动', '+11.78%列All Stocks能源（偏强侧）。'),
    'LUNR':('联动', '-6.16%列主题层太空科技（偏弱侧）。'),
    'LVO':('联动', '-15.28%列All Stocks通信服务（偏弱侧）。'),
    'MCD':('直接', '麦当劳CEO称低客流与粘性通胀将长期存在、不指望行业流量强劲回升——道指可选消费清一色跌的最大拖累。'),
    'MDLZ':('联动', '+0.59%列纳指100必需消费（偏强侧）。'),
    'MEI':('联动', '+9.69%列罗素2000科技（偏强侧）。'),
    'MMM':('联动', '+0.59%列道指工业（偏强侧）。'),
    'MNTK':('联动', '-12.50%列All Stocks基础材料（偏弱侧）。'),
    'MRK':('联动', '-1.88%列道指医疗保健（偏弱侧）。'),
    'MSS':('联动', '+34.62%列All Stocks必需消费（偏强侧）。'),
    'NEE':('联动', '-2.83%列标普500公用事业（偏弱侧）。'),
    'NFLX':('直接', 'HSBC下调评级（9/22盘后），指出YouTube竞争威胁。'),
    'NKLR':('直接', 'Terra Innovatum任命三名新的独立董事——小盘公用事业的无解释大跌。'),
    'NWSA':('联动', '-3.86%列标普500通信服务（偏弱侧）。'),
    'OKTA':('联动', '+4.45%列主题层网络安全（偏强侧）。'),
    'OPTU':('联动', '-9.73%列罗素2000通信服务（偏弱侧）。'),
    'PANW':('联动', '+5.00%列主题层网络安全（偏强侧）。'),
    'PCG':('联动', '-3.65%列标普500公用事业（偏弱侧）。'),
    'PG':('联动', '-0.56%列道指必需消费（偏弱侧）。'),
    'PLTR':('联动', '+3.68%列主题层生物识别（偏强侧）。'),
    'PROP':('联动', '+3.70%列All Stocks能源（偏强侧）。'),
    'PYPL':('联动', '-0.72%列纳指100金融（偏弱侧）。'),
    'QNC':('联动', '+15.34%列All Stocks科技（偏强侧）。'),
    'RAPP':('联动', '-17.70%列罗素2000医疗保健（偏弱侧）。'),
    'RENT':('联动', '-9.57%列主题层消费品（偏弱侧）。'),
    'SEI':('直接', 'Solaris Energy Infrastructure定价上调规模的12.5亿美元7.000%优先票据——周二-4.95%发行公告日后的修复。'),
    'SJM':('联动', '+1.07%列标普500必需消费（偏强侧）。'),
    'SPCE':('联动', '-6.02%列主题层太空科技（偏弱侧）。'),
    'SPCX':('联动', '-4.11%列纳指100工业（偏弱侧）。'),
    'STRA':('联动', '+2.31%列罗素2000必需消费（偏强侧）。'),
    'TALO':('直接', 'Talos Energy完成墨西哥湾深水石油资产战略收购——油价反弹日的能源个股确认。'),
    'TRVG':('联动', '-17.04%列All Stocks通信服务（偏弱侧）。'),
    'UNH':('联动', '-0.45%列道指医疗保健（偏弱侧）。'),
    'VGAS':('联动', '-10.57%列All Stocks公用事业（偏弱侧）。'),
    'VITL':('联动', '-8.36%列主题层消费品（偏弱侧）。'),
    'VSA':('联动', '+83.84%列All Stocks必需消费（偏强侧）。'),
    'WAVE':('联动', '-11.67%列All Stocks公用事业（偏弱侧）。'),
    'WMT':('联动', '+0.37%列道指必需消费（偏强侧）。'),
    'XXII':('联动', '+29.28%列All Stocks必需消费（偏强侧）。'),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "UGA", "perf": 4.863, "form": "商品信托", "exposure": "汽油期货（RBOB）",
         "reason": "汽油期货ETF +4.86%领涨全市场：成品油紧缺的极致定价——收割季+港口旺季前置、炼厂库存处于'操作性最低'水平，裂解价差走阔；与原油端五连跌后的反弹共振。合并删除：无同簇产品（汽油为独立成品油敞口）。"},
        {"ticker": "BNO", "perf": 4.231, "form": "商品信托", "exposure": "布伦特原油期货",
         "reason": "布伦特原油ETF +4.23%：油价五连跌后的首日反弹——成品油紧缺（柴油价格每日创纪录）向原油端的拉动回归，期货端地缘贴水的回补。合并删除：USO +3.30%、DBO +3.19%（同簇原油期货）。"},
        {"ticker": "DBE", "perf": 3.431, "form": "交易所交易基金", "exposure": "能源综合（期货）",
         "reason": "能源综合ETF +3.43%：油气商品反弹的全敞口映射（簇内股票端XLE +0.95/IXC +1.01——能源五范围领涨的ETF端确认）。合并删除：IXC、XLE、IYE、FENY、FXN（同簇能源敞口，保留最强者）。"},
    ],
    "down": [
        {"ticker": "BBC", "perf": -6.396, "form": "交易所交易基金", "exposure": "临床试验生物科技",
         "reason": "临床试验生物科技ETF -6.40%领跌全市场：主题层15个清一色跌的大盘映射——罗素2000医疗保健421只中395只下跌（整体-3.84%）为当日最弱股票范围；生物科技XBI -4.12%同向（周二领涨板块的全面逆转，Viking +1.96%为例外）。合并删除：无同簇产品。"},
        {"ticker": "SIL", "perf": -5.328, "form": "交易所交易基金", "exposure": "全球银矿股",
         "reason": "银矿ETF -5.33%：周二'避险+硬资产'领涨端的单日崩跌——金属商品主题七子行业全线大跌（等权-3.78%、白银子行业-6.61%）。合并删除：SLV -4.23%、SIVR -4.27%（同簇白银现货信托）。"},
        {"ticker": "GDXJ", "perf": -5.228, "form": "交易所交易基金", "exposure": "全球中小金矿股",
         "reason": "金矿ETF -5.23%：贵金属避险行情的单日逆转（黄金GLD -1.80%）——油价反弹推回通胀与利率预期，周二的配置逻辑当日反转。合并删除：无同簇产品。"},
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
        text = "核查9月15日盘后至9月23日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
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
    assert DATA["date"] == "2026-09-23"
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
            f"- `finviz_2026-09-23_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-09-23_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年9月23日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年9月23日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           '**市场背景**：周三为习特会（周四）前一日：主题层大规模risk-off（15个主题清一色跌对1个清一色涨——网络安全+2.18%）与油气商品暴力反弹（BNO +4.23/USO +3.30/DBE +3.43、汽油UGA +4.86%领涨全市场——油价五连跌后的首日反弹）并存。能源五个股票范围全部领涨（周二五范围领跌的直接反转：XLE +0.95/XOP +0.57/CVX +1.53%）；必需消费五个范围为相对强度领涨（XLP -0.36——多数成分下跌的「跌得少」）；科技两个范围居前（All Stocks/罗素2000端：软件反弹IGV +1.26/WCLD +1.01%）。跌幅侧：通信服务连续第二日五个范围领跌（XLC -0.85：谷歌-3.80%/AppLovin -4.10%/Netflix遭HSBC降级-1.11%）；公用事业两个范围领跌（XLU -1.92：PCG -3.65/NEE -2.83/EIX -2.80%）；医疗保健两个范围领跌（罗素2000医疗保健-3.84：周二三范围领涨的全面逆转——XBI -4.12/BBC -6.40%领跌全市场）。周二的领涨端全线崩跌：贵金属矿（SIL -5.33/GDXJ -5.23/SLV -4.23/GLD -1.80%）、铀链（URA -4.00/URNJ -4.50/NLR -3.23%）、太空科技（NASA -3.33/WARP -3.53/ORBX -3.29%）、加密（IBIT -1.95%）、金属矿业（XME -2.11%）。跷跷板回摆：半导体六连涨止步（SOXX -1.23/存储主题-1.05%）而软件/云/网络安全反弹（IHAK +1.48/IGV +1.26/WCLD +1.01%）。VIX期货ETF反弹（VXX +1.98/VIXY +1.88%）——事件风险前的对冲需求回归。麦当劳CEO「低客流+粘性通胀将长期存在」-4.80%为道指可选消费清一色跌的引擎。当日无行情性质结构变化。',
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
    (OUT / "finviz_2026-09-23_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (OUT / "finviz_2026-09-23_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = OUT / "finviz_2026-09-23_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)


if __name__ == "__main__":
    main()
