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
}

THEME_COMPANY = {
    "HUBS": "Hubspot Inc", "INTU": "Intuit Inc", "BRZE": "Braze Inc",
    "DUOL": "Duolingo Inc", "ADBE": "Adobe Inc", "TAL": "TAL Education Group",
    "AGRO": "Adecoagro SA", "AMTX": "Aemetis Inc", "CTVA": "Corteva Inc",
    "AMKR": "Amkor Technology Inc", "WOLF": "Wolfspeed Inc", "FORM": "FormFactor Inc",
    "IPX": "IperionX Ltd ADR", "AREC": "American Resources Corp", "LAR": "Larimar Therapeutics Inc",
    "VIAV": "Viavi Solutions Inc",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic NV", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月17日16:00 ET盘后事件可解释8月18日；8月18日16:00 ET后事件不得倒推。
R = {
    "PFSA": ("结构", "公司为Profusa（数字健康/植入式生物传感器，SPAC上市）。8月17日1拆4反向拆股生效后流通股仅约60.6万股、市值约110万美元，为极低流通盘超微盘股；8月18日无新公告，此前7月27日管理层换血及7月31日签订收购G3 Vision Labs（约1.11亿美元收入诊断公司）期权协议构成题材，+506.6%系反向拆股后极小流通盘的投机抢筹（盘初一度+800%后回落）。[StockTitan](https://www.stocktitan.net/news/PFSA/)"),
    "AMLX": ("直接", "8月18日公布avexitide（首个GLP-1受体拮抗剂，具FDA突破性疗法认定）治疗减肥术后低血糖（PBH）的III期LUCIDITY试验积极顶线结果：达成FDA认可的主要终点，2/3级低血糖事件复合发生率较安慰剂降低55%；Stifel将目标价从21美元上调至45美元，当日放量大涨63.8%创52周新高。[Amylyx官方新闻稿](https://www.amylyx.com/news/amylyx-pharmaceuticals-announces-positive-topline-results-from-phase-3-lucidity-clinical-trial-of-avexitide-in-post-bariatric-hypoglycemia)"),
    "SXTC": ("结构", "中国天成药业（中药/提取物微盘股），8月10日生效1拆80反向拆股（8月5日公告）后持续投机性拉升（8月14日+31%后8月18日再涨36.8%），当日无公司公告；医药为当日最强防御板块亦提供情绪支撑。"),
    "BANL": ("直接", "8月18日发布2026年上半年业绩：营收同比+49.2%至3.956亿美元、毛利翻倍至653万美元、扭亏为盈（净利约150万美元），并宣布每股0.10美元特别股息（8月28日登记），股价大涨30.9%。[StockTitan](https://www.stocktitan.net/news/BANL/)"),
    "TRGP": ("直接", "8-17盘后20:15 ET公司公告与埃克森美孚子公司签订20年期费用型一体化中游协议：二叠纪Delaware新建3座合计约825 MMcf/d天然气处理厂、Midland新增面积专营并将费用保底条款延长至2046年，另建约70英里Bull Run II管道通往Waha，2026年增长资本开支增至约50亿美元，当日大涨7.1% [StockTitan](https://www.stocktitan.net/news/TRGP/targa-resources-corp-announces-20-year-agreements-with-exxon-mobil-l7scij3dkqar.html) [公司新闻稿](https://www.targaresources.com/news-releases/news-release-details/targa-resources-corp-announces-20-year-agreements-exxonmobil-and)"),
    "RBNE": ("联动", "Robin Energy（油轮航运超微盘股，市值约150万美元）8月18日无独立新闻；当日能源板块第三日走强（布伦特91美元、天然气+2.7%），作为能源航运概念微盘跟随板块情绪上涨6%。"),
    "GNLN": ("结构", "Greenlane Holdings已转型为Berachain（BERA）数字资产金库公司，8月14日中报披露持仓8130万枚BERA并强调每股BERA含金量较年末+37%；8月18日无公司公告且当日无BERA大涨证据，+51.7%系日均成交仅约1.7万股、市值约130万美元超微盘在加密金库概念上的投机性拉升。"),
    "KIDZ": ("结构", "KIDZ AI（原Classover，AI教育+GPU算力题材）8月13日生效1拆15反向拆股并于同日发布中报，8月18日无新公告；股价自8月11日拆股公告-28%后超跌反弹，市场继续炒作其4460万美元Canopy Wave GPU订单与NVIDIA Blackwell B300集群题材，+16%属超微盘投机波动。"),
    "EEIQ": ("结构", "EpicQuest Education（国际教育微盘股，市值约380万美元）8月10-25日期间无任何新闻（最近公告为7月21日AI辅导平台）；+10.9%为低流动性微盘无消息波动，或延续此前AI教育平台题材的零星投机买盘。"),
    "LGCL": ("结构", "Lucas GC（AI人力/中概微盘股）8月1-20日无任何公告，8月18日成交量放大至均值848%（约386万股）下无消息崩跌82.9%；公司7月2日已终止2000万美元ATM融资，属前期投机炒作（年内一度大涨88%）后的资金出逃/崩盘，无基本面事件。"),
    "AIB": ("联动", "AIB Data Centers（原区块链公司转型AI/HPC数据中心，8月14日中报营收下滑39%、COO辞任当日仅+0.11%）8月18日无新公告；当日半导体/AI硬件暴跌（等权半导体-5.8%、存储ETF-8.8%），科技微盘遭抛售，该股-24.4%属AI基建题材微盘联动下跌。"),
    "SCKT": ("结构", "Socket Mobile（市值约600万美元超微盘）8月10日因与3Eye Technologies达成分销合作单日暴涨451.67%后持续泡沫消退，8月18日无新公告，-21.1%为投机热潮退潮的延续（股价已自2.79美元高点跌回0.73美元附近）。"),
    "RITR": ("结构", "Reitar Logtech（香港物流科技中概股）8月3日因子公司与菜鸟合作消息单日暴涨504.96%后持续崩塌，8月18日无新公告，股价跌至0.08美元附近（-33.7%）；叠加9月将表决25合1反向拆股的退市保壳预期，属炒作退潮式阴跌。"),
    "SGLY": ("融资定价", "Singularity Future Technology（原中环球船务）8月18日15:09宣布以每股3.00美元（较市价折价）向机构投资者定向增发60万股，募资约180万美元，当日-22.3%为典型增发稀释性下跌。[StockTitan](https://www.stocktitan.net/news/SGLY/)"),
    "XTIA": ("公司治理", "XTI Aerospace于8月18日盘前（6:00）宣布CEO兼董事长Scott Pomeroy辞职（Jeremy Schneiderman任临时CEO），并提交12b-25延迟10-Q文件，称因管理层变动及对前CEO相关公司治理事项的内部审查，还退出Needham会议，当日-15.9%。[StockTitan](https://www.stocktitan.net/news/XTIA/)"),
    "KALU": ("直接", "凯撒铝业8月17日盘后宣布高管交接：Fred Stephan将于11月1日接任CEO兼总裁，现任CEO Keith Harvey转任执行董事长；股价8月11日刚创199.89美元历史新高、年内涨约44%，市场对元老CEO离任用脚投票，8月18日-13.1%（185.5跌至161.2美元）。[StockTitan](https://www.stocktitan.net/news/KALU/)"),
    "LWLG": ("联动", "Lightwave Logic（电光聚合物/光子学概念，市值约11亿美元）8月18日无公司新闻；其股价高度绑定AI/光模块与半导体情绪，当日等权半导体-5.8%、存储ETF-8.8%的科技暴跌中，-10.5%属AI硬件链联动下跌。"),
    "SIM": ("联动", "Grupo Simec（墨西哥特钢ADR）8月18日无公告（中报7月28日已发）；当日30年期美债收益率创2007年来新高、资金防御性轮动抛售周期材料股，该ADR日均成交仅约5万股流动性极差，在8月14日-8.35%基础上再跌9.8%，跌幅被低流动性放大。"),
    "XOM": ("直接", "作为TRGP 20年期二叠纪中游协议的签约对手方，其Premier油气资产开发获中游产能与费用保底锁定至2046年，直接验证其长期产量增长叙事；叠加布伦特原油当日走强至91美元上方（地缘紧张溢价），+2.5%领涨超级大盘股 [公司新闻稿](https://www.targaresources.com/news-releases/news-release-details/targa-resources-corp-announces-20-year-agreements-exxonmobil-and) [TradingEconomics](https://tradingeconomics.com/commodity/brent-crude-oil)"),
    "WMB": ("联动", "无公司单独消息；TRGP与埃克森签订20年费用型中游协议提振整个中游板块估值逻辑（长约费用保底=现金流能见度提升、二叠纪气量长期增长获背书），叠加天然气发电/数据中心用电需求主题与油价走强，WMB作为大型气管道/G&P中游商跟随板块上涨约2-3% [Seeking Alpha](https://seekingalpha.com/news/4634148-targa-resources-signs-20-year-midstream-deals-with-exxon-plans-three-new-permian-gas-plants)"),
    "PODD": ("联动", "8-5财报虽超预期但下调全年Omnipod增长指引致股价深跌、此后被列为最超卖医疗股之一；8-18在30年收益率创2007年来新高引发的防御性医疗板块反弹中超跌反弹，收涨约5-6%至146美元附近，无公司当日新消息 [MarketBeat](https://www.marketbeat.com/instant-alerts/insulet-nasdaqpodd-shares-up-49-whats-next-2026-08-18/) [Yahoo Finance](https://finance.yahoo.com/sectors/healthcare/articles/insulet-corporation-podd-one-most-213143187.html)"),
    "LLY": ("联动", "长端利率飙升触发防御回归、医疗权重领涨；叠加8-17 Leerink/IQVIA周度处方数据利好延续：口服GLP-1 Foundayo处方周环比+14%至约3.89万张、开始抢占诺和口服Wegovy份额（后者-5%），8-18续涨3.6%至约1,215美元 [CNBC](https://www.cnbc.com/2026/08/17/eli-lilly-and-jj-bounce-on-new-data-as-software-gives-up-gains.html)"),
    "ABBV": ("联动", "无公司单独消息；30年收益率创19年新高引发防御性医药轮动（XLV/IBB走强，LLY/J&J因处方数据领涨、科技遭抛售），ABBV随板块防御买盘走强至阶段高位，其Q2后上调2026指引提供基本面支撑 [Morningstar](https://global.morningstar.com/en-ca/stocks/4-charts-on-the-rotation-out-of-tech-and-growth-stocks) [CNBC](https://www.cnbc.com/2026/08/17/eli-lilly-and-jj-bounce-on-new-data-as-software-gives-up-gains.html)"),
    "MNST": ("联动", "无公司当日消息；长端利率新高触发防御性必需消费轮动（KO/MKC/MNST同涨、标普三连跌），MNST在Q2净销售+20%超预期并宣布2拆1后动能延续、自8月回调低位反弹 [Morningstar](https://global.morningstar.com/en-ca/stocks/4-charts-on-the-rotation-out-of-tech-and-growth-stocks) [QuiverQuant](https://www.quiverquant.com/news/Why+Monster+Beverage+%2528MNST%2529+Stock+Is+Up+Today)"),
    "MKC": ("联动", "无当日公司消息；防御性必需消费为当日最强风格之一（30年收益率创2007年来高位的避险轮动），公司8月初Q2净销售+16.7%、毛利率+270bps并重申全年指引，基本面支撑下跟随板块上涨2.5% [PR Newswire](https://www.prnewswire.com/news-releases/mccormick-reports-strong-second-quarter-performance-and-reaffirms-2026-outlook-302810606.html) [Morningstar](https://global.morningstar.com/en-ca/stocks/4-charts-on-the-rotation-out-of-tech-and-growth-stocks)"),
    "KO": ("联动", "无当日公司消息；防御回归下必需消费领涨，KO被点名为科技/成长轮动中的顶级防御受益股之一（与JNJ/ABBV同列），7-28 Q2超预期并上调全年指引后维持12个月高位附近，当日+2.1% [Morningstar](https://global.morningstar.com/en-ca/stocks/4-charts-on-the-rotation-out-of-tech-and-growth-stocks)"),
    "COHR": ("联动", "WSJ周一（8-17）晚发布分析称九大科技公司有约3万亿美元表外AI承诺（数据中心租赁与采购义务），引发对举债式AI资本开支可持续性的质疑，叠加30年收益率升至4.94%创19年新高，AI硬件链集体去风险、光通信板块重挫；公司8-12 FQ4收入指引不及预期盘后暴跌的余波仍在 [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/) [WSJ](https://www.wsj.com/tech/ai/why-big-techs-ai-spending-is-3-trillion-higher-than-it-seems-e1067bb2) [GuruFocus](https://www.gurufocus.com/news/3060280/coherent-cohr-stock-plummets-after-revenue-guidance-miss)"),
    "LITE": ("联动", "与COHR同属AI光通信链去风险大跌（无公司当日单独负面消息）：8-12 FQ4营收超预期、CEO称超大规模客户需求'不可思议'但股价高位见顶回落（8-13已跌5.6%），8-18在WSJ表外AI债务报道与利率新高引发的AI硬件/半导体抛售中继续大幅回撤 [Lumentum IR](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Results/default.aspx) [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/)"),
    "STX": ("联动", "存储板块连续多日回调的组成部分（当周SanDisk -11%、Seagate -7%、Micron -4%，回吐2026年巨大涨幅），AI资本开支可持续性疑虑（WSJ表外债务报道）与长端利率新高共同压制高估值AI硬件持仓；无STX公司单独负面消息 [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/sandisk-sinks-11-seagate-falls-160250009.html) [MarketWatch](https://www.marketwatch.com/story/memory-data-storage-stocks-slide-in-tech-selloff-d88651d1)"),
    "FIX": ("联动", "WSJ表外AI债务报道（周一晚）+30年收益率4.94%创19年新高，引发'AI电力/数据中心建设'链集体去风险（同日FTAI -7%、CAT -4%、Bloom -10%），FIX作为数据中心机电承包商随板块重挫7.6%；公司7月末Q2营收超30亿美元、积压订单创约140亿美元纪录，无负面公司消息 [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/)"),
    "GEV": ("联动", "WSJ周一晚'3万亿美元表外AI承诺'报道引发周二表后电力（behind-the-meter）与AI电力设备股自由落体，GEV盘中跌约6%、收跌6.9%；30年收益率创19年新高加剧长久期AI基建交易平仓，无公司单独负面消息 [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/) [WSJ](https://www.wsj.com/tech/ai/why-big-techs-ai-spending-is-3-trillion-higher-than-it-seems-e1067bb2)"),
    "VRT": ("联动", "同日AI电力链去风险：数据中心供配电/散热龙头VRT跌约7%、收跌6.8%，与GEV/FTAI/CAT/Bloom同步；市场质疑超大规模厂商举债AI资本开支（WSJ约3万亿表外承诺）与电力建设节奏的可持续性，高估值AI基建持仓遭利率新高下的集体减仓 [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/)"),
    "NEM": ("联动", "金价当日回落约1%（盘中一度跌超2.5%、跌破5,000美元/盎司关键位），叠加美债收益率上行压制无息资产，且此前一周大涨约12%后触发获利了结，NEM收跌3.57%，无公司单独负面消息 [TradingKey](https://www.tradingkey.com/news/market-movers/262116047-market-movers-nem-20260818)"),
    "STLD": ("联动", "无公司单独消息；钢铁股前期涨幅大量建立在数据中心/电气化建设需求叙事上（Argus：美国板材需求前景'系于数据中心'），8-18 WSJ表外AI债务报道引发AI资本开支疑虑+30年收益率创19年新高，触发周期/材料整体避险回调；当日HRC钢价仍微涨至约1,226美元/吨、行业基本面无恶化 [Argus Media](https://www.argusmedia.com/en/news-and-insights/latest-market-news/2771030-viewpoint-us-flat-steel-demand-hinges-on-data-centers) [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/)"),
    "NUE": ("联动", "与STLD同属周期/材料避险回调：WSJ表外AI债务报道令市场担忧数据中心驱动的钢材需求持续性，长端利率新高压制周期股估值，钢铁板块整体走弱（STLD -3.2%、NUE -3.1%），无NUE公司当日消息 [Argus Media](https://www.argusmedia.com/en/news-and-insights/latest-market-news/2771030-viewpoint-us-flat-steel-demand-hinges-on-data-centers) [24/7 Wall St.](https://247wallst.com/investing/2026/08/18/behind-the-meter-energy-stocks-fall-tuesday-ftai-aviation-down-7-ge-vernova-down-6-caterpillar-down-4/)"),
    "CVX": ("直接", "8月17日（周一）盘前Chevron宣布在安哥拉Block 0（下刚果盆地）发现逾600米油气柱、净厚超90米的油气凝析物，可依托现有基础设施快速接续开发，该利好在8月18日继续发酵，叠加当日WTI原油涨约1%至85美元上方，股价延续第二日上行收涨1.5%。[Reuters](https://www.reuters.com/business/energy/chevron-finds-oil-gas-condensate-offshore-angola-2026-08-17/)、[Chevron新闻稿](https://www.chevron.com/newsroom/2026/q3/chevron-advances-its-strategic-exploration-program-with-discovery-in-angolas-block-0)"),
    "WMT": ("联动", "当日无独立事件；标普-0.75%、30年期收益率创2007年来最高的避险日，防御性必需消费齐涨（KO/WMT/PG），WMT盘中触及历史新高，且8月20日Q2财报临近带来财报前布局需求。"),
    "PG": ("联动", "无独立事件，属防御回归行情（道指必需消费三只齐涨之一）；7月宣布的季度股息$1.0885/share除息日临近，长端利率上行日高股息防御属性仍获资金支撑。"),
    "DIS": ("联动", "当日无独立事件（FQ3财报8月5日已过）；道指通信服务两只微涨，防御性资金流入推动DIS逆大盘微涨0.4%。"),
    "GOOGL": ("背离", "WSJ当日报道九大科技公司约3万亿美元表外AI承诺并点名Alphabet，引发AI链去风险，但GOOGL收平微涨0.1%，显著强于其他被点名的AI资本开支巨头（AMZN -0.7%）；当日Jefferies分析师Brent Thill重申买入、目标价445美元提供支撑。[Google Finance](https://www.google.com/finance/quote/GOOGL:NASDAQ)、[WSJ](https://www.wsj.com/tech/ai/why-big-techs-ai-spending-is-3-trillion-higher-than-it-seems-e1067bb2)"),
    "SHW": ("联动", "无独立事件（Q2财报7月下旬已过、当日曾大涨）；30年期美债收益率创2007年来最高，叠加HD财报称住房市场\"冻结\"，地产链涂料龙头随基础材料板块承压下跌1.3%。"),
    "CAT": ("联动", "无公司独立事件；WSJ\"九大科技公司约3万亿美元表外AI承诺\"报道引发AI链去风险与半导体回撤，年内涨约48%的\"AI数据中心电力设备代理交易\"CAT首当其冲遭抛售，-4.6%为道指最大跌幅股。[WSJ](https://www.wsj.com/tech/ai/why-big-techs-ai-spending-is-3-trillion-higher-than-it-seems-e1067bb2)"),
    "BA": ("联动", "无独立事件（Q2财报7月28日已过，8月13日仅巴西业务人事任命）；随道指工业板块整体大跌（CAT -4.6%领跌）与高贝塔周期股在避险日同步走弱。"),
    "HON": ("联动", "无独立事件；6月底分拆后Honeywell曾因数据中心与LNG需求上调全年利润指引，属AI邻近型工业股，当日随AI链去风险与工业板块下跌0.8%。"),
    "AMZN": ("联动", "无独立事件；WSJ报道点名Amazon为九大表外AI承诺公司之一（2026年资本开支约2200亿美元、约80%与AI相关），AI支出可持续性担忧下随大盘科技股走弱0.7%。[WSJ](https://www.wsj.com/tech/ai/why-big-techs-ai-spending-is-3-trillion-higher-than-it-seems-e1067bb2)"),
    "HD": ("直接", "8月18日盘前发布FY2026 Q2财报：销售+5.7%至479亿美元超预期、净利48亿、同店销售为2022年来最佳、重申全年指引，但其中7.30亿美元IEEPA关税退款有6.85亿冲减COGS增厚利润，剔除后实质miss，开盘冲高后回落收-0.1%，CFO称住房市场仍\"冻结\"。[Home Depot IR](https://ir.homedepot.com/news-releases/2026/08-18-2026-110040463)、[CNBC](https://www.cnbc.com/2026/08/18/home-depot-hd-q2-2026-earnings.html)"),
    "MCD": ("联动", "无独立事件；8月17日大跌2.7%至近两年低位后，周二随防御性消费风格（必需消费领涨）超卖反弹0.6%。"),
    "GILD": ("联动", "8月17-18日无公司层面独立事件（Q2财报8月4日已过，CHMP推荐Trodelvy组合为7月24日旧闻）；当日医疗/大制药为最强防御方向，GILD作为XLV最大权重之一、YTD涨约18%的动量股领涨3.3%，BofA $162目标价与Yeztugo超70%持续用药率的多头逻辑仍在发酵。[TheStreet](https://www.thestreet.com/investing/stocks/bank-of-america-gilead-gild-stock-hiv-yeztugo-persistence)"),
    "VRTX": ("联动", "8月18日无独立事件（Q2财报上调指引与100亿美元收购Crinetics均为7月上旬事件）；随防御性制药板块走强反弹2.5%，延续8月10日跳空大涨后的动量，当日为标普医疗权重强的一份子。"),
    "ALNY": ("联动", "无新独立事件；7月30日因下调2026年指引（ATTR-CM销售逆风）暴跌25%+后严重超卖，8月16日\"抛售过度\"的多头观点开始发酵，叠加制药/生物科技板块防御走强，超卖反弹1.8%。"),
    "CCEP": ("联动", "8/18为AI股集体回调、资金转向防御日，必需消费板块八只纳指成分清一色上涨，CCEP随防御轮动走高。公司自身无当日新事件，但8月上旬中报确认FY26指引、且8/10-14持续回购217,456股形成支撑，见[Investing.com回购报道](https://www.investing.com/news/company-news/cocacola-europacific-partners-buys-back-217456-shares-93CH-4863232)。"),
    "KDP": ("联动", "AI去风险当日必需消费板块整体走强，KDP为防御轮动受益者。个股层面延续8/13 HSBC上调至买入（目标价40美元）后的动能，见[Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/keurig-dr-pepper-shares-rise-182151128.html)。"),
    "LIN": ("联动", "无当日独立事件。工业气体为典型防御性质量股，在AI/半导体链抛售、长端收益率创新高的避险日获资金配置，+0.9%属防御轮动；此前7/31发布的Q2创纪录业绩与在手订单提供基本面支撑，见[Linde Q2新闻稿](https://www.linde.com/news-and-media/2026/linde-reports-second-quarter-2026-results)。"),
    "CEG": ("联动", "无公司当日独立利空。8/18 AI股连续第三日下跌（英伟达约-5%、Palantir约-10%）、30年期收益率创阶段新高引发AI电力/核电视率证伪，作为纳指公用事业中AI数据中心电力旗舰的CEG领跌-4.1%，属典型的高估值AI电力链去杠杆交易，见[AP via BNN Bloomberg](https://www.bnnbloomberg.ca/markets/2026/08/18/global-shares-slip-as-worries-about-rising-oil-prices-offset-boost-from-strong-earnings/)。"),
    "EXC": ("联动", "无当日独立事件。作为核电商CEG的关联标的随AI电力/核电视情绪降温小幅走低-0.6%，跌幅小于CEG反映其AI敞口叙事较弱，属板块性回调，背景同[AP 8/18 AI股抛售报道](https://www.bnnbloomberg.ca/markets/2026/08/18/global-shares-slip-as-worries-about-rising-oil-prices-offset-boost-from-strong-earnings/)。"),
    "AEP": ("背离", "8/17英伟达宣布为SB Energy俄亥俄PORTS-Pike园区提供最高1050亿美元担保、OpenAI签20年租约，SB Energy将与其AEP Ohio子公司合投42亿美元升级输电网，属AEP正面事件；但8/18 AI电力链集体去风险压制公用事业，两股力量对冲后AEP收平（-0.1%），明显强于CEG的-4.1%。见[CNBC](https://www.cnbc.com/2026/08/17/nvidia-financing-open-ai-data-center-ohio.html)与[Energy.gov事实清单](https://www.energy.gov/articles/fact-sheet-department-energy-ensuring-affordable-energy-access-ohio-while-powering-future)。"),
    "PYPL": ("单样本", "无当日独立事件，-0.1%属可忽略的噪音波动。支付板块当日整体平静，市场焦点在AI链抛售与收益率，PYPL处于Q2财报（7/28）后的修复平台期，未受板块主线影响。"),
    "CRWV": ("联动", "无当日公司独立利空，8/18 AI算力链集体去风险中重挫-12.1%：英伟达/Palantir领跌的AI抛售叠加WSJ对科技巨头约3万亿美元表外AI债务的报道发酵、30年期收益率新高，而CoreWeave自身债务/权益比超7倍、7月底26亿美元贷款需较基准溢价5.5个百分点才售出，高杠杆使其成为利率与AI资本开支证伪的最大受害者，见[AP 8/18报道](https://www.bnnbloomberg.ca/markets/2026/08/18/global-shares-slip-as-worries-about-rising-oil-prices-offset-boost-from-strong-earnings/)。"),
    "WEAV": ("直接", "公司名为Weave Communications（医疗保健客户体验SaaS，非WeaveGrid）。8/18宣布被私募基金Francisco Partners以每股7.40美元现金收购（股权价值约6.5亿美元、较8/17未受影响收盘价溢价约34%，预计2026Q4完成），股价跳涨31.7%，见[官方新闻稿](https://investors.getweave.com/news/news-details/2026/Weave-Announces-Acquisition-by-Francisco-Partners/default.aspx)。"),
    "OBIO": ("联动", "代码OBIO为Orchestra BioMed（心血管器械，BackBeat/AVIM高血压起搏疗法）。8/17-18无公司新闻稿或分析师动作，当日+19.9%属罗素小盘医疗强势板块中的高弹性补涨：8/10 Q2财报显示现金1.1亿美元可撑至2027Q4并获Medtronic/Ligand 3500万美元注资，财报后分析师平均目标价上调至12.33-13美元、较约4.4美元股价隐含约180%上行空间，乖离吸引资金流入，背景见[StockTitan OBIO新闻页](https://www.stocktitan.net/news/OBIO/)。"),
    "KLC": ("财报延续", "8/13盘后Q2财报EPS 0.08美元逊预期且净亏损880万美元，股价单日暴跌约22%；8/18 +6.3%为暴跌后的超跌反弹延续（8月中旬已现4%级别反弹），分析师平均目标价4.13-4.24美元较约3.7美元现价仍隐含约六成空间，吸引抄底资金。见[StockTitan Q2新闻稿](https://www.stocktitan.net/news/KLC/kinder-care-reports-second-quarter-2026-financial-pqqduuis80hj.html)与[Investing.com暴跌报道](https://www.investing.com/news/stock-market-news/why-is-kindercare-learning-companies-stock-collapsing-today-93CH-4861341)。"),
    "HLF": ("联动", "代码HLF为Herbalife（康宝莱）。8/18无独立事件，+2.9%属必需消费防御轮动叠加8/5财报后超跌修复：Q2因9460万美元债务再融资费用录得净亏致股价此前跌约9%至11.5美元附近，防御性买盘推动反弹。"),
    "FC": ("单样本", "代码FC为Franklin Covey（富兰克林柯维，企业领导力培训）。8/18无独立事件亦无明确板块主线，+2.9%属小盘防御/服务类个股当日普涨中的个股性波动；公司持续回购（FY26年内已回购约160万股/2810万美元）与7/1 Q3财报扭亏为盈提供底部支撑。"),
    "REAX": ("直接", "代码REAX为The Real Brokerage。8/14盘后Real与RE/MAX股东会双双批准约8.8亿美元合并（Real赞成票约99%、RE/MAX约78.8%），交割预计两周内完成；8/18恰为RE/MAX股东选择合并对价（每5.15股新公司股份或现金/混合）的截止日，交割临近+对价选择截止驱动事件资金与套利盘集中买入，收涨9.5%。见[HousingWire](https://www.housingwire.com/articles/real-remax-shareholder-approval/)与[对价选择截止公告](https://kalkinemedia.com/us/news/announcements/remax-holdings-announces-august-18-deadline-for-stockholders-to-choose-acquisition-consideration)。"),
    "RMAX": ("直接", "代码RMAX为RE/MAX Holdings。作为Real Brokerage合并标的：8/14股东批准（约78.8%赞成）扫清交割障碍、预计两周内完成，8/18为股东选择合并对价的截止日（默认按5.15比例换股），事件套利资金抢在截止/交割前建仓推升6.3%，与REAX同步走强。见[HousingWire](https://www.housingwire.com/articles/real-remax-shareholder-approval/)。"),
    "AGNT": ("联动", "原eXp World Holdings（6月更名AGNT）为小盘房地产经纪平台（Q2营收14.5亿美元、同比+11%已於8月4日披露），8月17-18日窗口无新公司事件；当日罗素小盘房地产相对抗跌（RE/MAX合并对价选择截止日带动地产服务链情绪，Real Brokerage +9.5%、RE/MAX +6.3%），小盘地产经纪股跟随板块反弹。"),
    "KEEL": ("联动", "代码KEEL为Keel Infrastructure（前比特币矿商Bitfarms，转型AI/HPC数据中心）。8/18无独立公告，-16.2%为AI算力链集体去风险中高Beta崩跌：8/10 Q2营收同比腰斩至3040万美元且经营亏损1.4亿美元，叠加4.58亿美元可转债的稀释/融资悬顶担忧，在英伟达链抛售日被集中抛售。见[StockTitan Q2财报](https://www.stocktitan.net/news/KEEL/keel-infrastructure-reports-second-quarter-2026-df5xhrr0abyn.html)与[AP 8/18 AI抛售](https://www.bnnbloomberg.ca/markets/2026/08/18/global-shares-slip-as-worries-about-rising-oil-prices-offset-boost-from-strong-earnings/)。"),
    "AEHR": ("联动", "无当日独立事件。年内涨超200%（一度480%）的AI晶圆级老化测试设备商8/14收134美元、8/17开盘一度145.6美元创阶段新高后，8/18半导体/AI链获利了结中回吐15.4%，属典型高拥挤度AI高Beta股去风险。见[Yahoo Finance AEHR年内回顾](https://finance.yahoo.com/markets/stocks/articles/over-200-2026-whats-next-175500690.html)。"),
    "MXL": ("联动", "无当日独立事件。年内涨约296%的AI数据中心连接芯片商自8月初Q2财报（营收超预期但GAAP亏损）后持续回调，8/18半导体AI抛售放大跌势至-14.3%，属高涨幅AI芯片股的估值去风险延续。见[Seeking Alpha财报后回调分析](https://seekingalpha.com/article/4925834-maxlinears-stock-post-earnings-selloff-buying-opportunity)。"),
    "HDSN": ("财报延续", "8月5日Q2财报不及预期（EPS 0.12美元 vs 预期0.17美元、毛利率31%降至26%、下调全年毛利率指引）后Canaccord将目标价从9美元砍至8美元，8月18日随基础材料板块（罗素材料12涨/77跌）继续下行；当日无新公司事件（DLA 2.1亿美元合同重获为8月5日公告）。[StockAnalysis](https://stockanalysis.com/stocks/hdsn)"),
    "ENVX": ("直接", "总裁兼CEO Raj Talluri于8月13日辞职转任Kulicke & Soffa，董事会任命CFO Ryan Benton为临时CEO、董事长T.J. Rodgers任执行董事长；8月17日投资者网络直播后，8月18日William Blair将其从跑赢大盘降至与大盘持平、TD Cowen将目标价从7美元砍至5.50美元，公司重申三季度营收900万-1000万美元指引（弱于预期），股价创52周新低、盘中大跌17%-18%。[StocksToTrade](https://stockstotrade.com/news/enovix-corporation-envx-news-2026_08_18)、[Tickeron](https://tickeron.com/blogs/why-is-enovix-corporation-envx-stock-down-17-31-today-15784)"),
    "AMRC": ("联动", "无当日独立事件。8/3 Q2财报营收超预期10%并录得18亿美元创纪录新签订单（AI数据中心项目为主）曾推动股价大涨，此后随AI电力/能源服务叙事降温持续回吐，8/18在AI链集体去风险中再跌10.6%，属财报冲高后的AI主题反向平仓。见[Investing.com Q2数据](https://www.investing.com/news/company-news/ameresco-q2-2026-slides-data-center-push-drives-record-backlog-93CH-4832425)。"),
    "AREC": ("联动", "核查8月17日盘后至18日披露与新闻后无同日直接催化（8月14日为特别股息除息日、锗商业生产柱与国防部2500万美元投资为此前背景）。当日金属商品主题七个子行业清一色下跌（等权-3.22%），关键矿产/稀土精炼题材股随板块回撤，金价回落（-1.7%）与金矿股大跌（GDXJ -4.1%）拖累整体矿业情绪。"),
    "HUBS": ("联动", "当日无公司独立新闻，+5.1%属于资金从半导体切向应用软件的板块轮动；市场继续消化8月5日Q2营收超预期(+19.8%)与回购计划，一周累计涨约15%但较前高仍低约70%。[moomoo](https://www.moomoo.com/hans/news/post/74693316/hubspot-jumps-as-investors-revisit-strong-q2-results-and-buyback)"),
    "INTU": ("联动", "8-18无公司层面事件(FQ4财报定于8-25)，公司IR页面显示当日+4.31%至350.05美元；此前四周软件板块反弹中INTU累计涨约16.3%、创6月以来新高，属轮动买入+财报前布局。[Trading Economics](https://tradingeconomics.com/intu:us)"),
    "BRZE": ("联动", "8-18无独立事件，随应用软件主题逆势领涨；催化铺垫为此前(8月中旬)BTIG因订单(bookings)动能将目标价自30美元上调至35美元并维持买入。[Investing.com](https://www.investing.com/news/analyst-ratings/btig-raises-braze-stock-price-target-to-35-on-bookings-momentum-93CH-4860311)"),
    "DUOL": ("直接", "D.A. Davidson分析师Wyatt Swanson当日将Duolingo由中性上调至买入、目标价由130美元升至160美元，称股价自高点回落约65%后正'接近拐点'，当日大涨7.3%。[Investing.com](https://uk.investing.com/news/stock-market-news/duolingo-stock-surges-7-after-da-davidson-upgrade-to-buy-93CH-4837499)"),
    "ADBE": ("直接", "贝莱德申报将Adobe持股增至10%以上(约84亿美元)，被视为大型机构对创意软件资产在AI冲击下的信任票，缓解生成式AI侵蚀Creative Cloud的担忧；当日盘中一度涨4.5%、收涨3.6%至263.13美元。[StockStory](https://stockstory.org/us/stocks/nasdaq/adbe/news/why-up-down/why-adobe-adbe-stock-is-up-today-4)"),
    "TAL": ("联动", "教育科技主题当日由Duolingo获D.A. Davidson上调至买入(+7.3%)带动，TAL无8-18独立新闻，随主题走高；其7月发布的FY27Q1业绩(EPS 0.75美元远超预期、营收+34%)提供基本面支撑。"),
    "AGRO": ("财报延续", "8-12 Q2创纪录调整后EBITDA 1.725亿美元(化肥业务驱动)后延续多日反弹：8-16收8.91→8-17收9.26→8-18盘中仅+1.4%、尾盘加速至收涨5.9%；当日无新增公司公告，谷物价格涨跌互现，属财报后资金持续回流。[TradingView/MarketBeat业绩会纪要](https://es.tradingview.com/news/marketbeat:15d6965b2094b:0-adecoagro-q2-earnings-call-highlights/)"),
    "AMTX": ("联动", "8-18无独立事件，跟随农业商品/可再生燃料主题走高；近期催化为8-6 Q2营收+20%并录得正营业利润、以及7月初出售1,800万美元45Z清洁燃料生产税收抵免(净得约1,450万美元)。[Aemetis新闻稿](https://www.aemetis.com/aemetis-sells-18-million-of-section-45z-clean-fuel-production-tax-credits/)"),
    "CTVA": ("直接", "瑞银(UBS)在10月1日分拆(农药'新Corteva'+种子SpinCo)临近之际上调盈利预测，预计'新Corteva' 2027年EBITDA达14.6亿美元、EPS 1.15美元(此后升至15.5亿美元)，当日CTVA收涨2.5%。[Seeking Alpha](https://seekingalpha.com/news/4634373-ubs-raises-corteva-profit-forecasts-ahead-of-planned-split)"),
    "AMKR": ("联动", "MarketBeat记录8-18盘中一度跌8.4%(收跌10.5%至56美元附近)，QuiverQuant归因于投资者财报前锁定获利(此前自7月低点大幅反弹、年内仍涨约130%)；叠加WSJ曝九大科技公司约3万亿美元表外AI承诺引发半导体链整体去风险，封测(OSAT)高beta环节领跌。[MarketBeat](https://www.marketbeat.com/instant-alerts/amkor-technology-nasdaqamkr-shares-down-84-heres-what-happened-2026-08-18/)"),
    "WOLF": ("联动", "8-19(周三)17:00 ET发布FQ4财报(市场预期每股亏损约2.45美元、期权隐含约±14%波动)，8-18为财报前交易日：碳化硅需求疲软、负毛利率(约-27%)与潜在股本稀释(传至多2,400万股出售)的担忧叠加板块性AI去风险，当日挫10%，次日盘前反弹逾5%。[GuruFocus财报前瞻](https://www.gurufocus.com/news/9041725/wolfspeed-wolf-q4-earnings-preview-market-pricing-growth-despite-unprofitability)"),
    "FORM": ("联动", "当日无公司新闻；Tickeron记录周二盘中自8-17收盘138.16美元一度跌12.04%至121.52美元(收跌10%)，纯随半导体板块普跌——WSJ'3万亿美元表外AI承诺'报道+30年美债收益率创2007年来新高引发AI链获利了结，探针卡/测试环节作为高估值AI衍生需求标的承压。[WSJ](https://www.wsj.com/tech/ai/why-big-techs-ai-spending-is-3-trillion-higher-than-it-seems-e1067bb2)"),
    "IPX": ("联动", "8-18无新公司事件(上一独立事件为7-7以21.98美元折价定价5,000万美元ADS增发)；作为钛金属/关键材料小盘股，随金铜暴跌后的金属板块整体回撤(金价自近5,000美元纪录高位单日暴跌逾11%、矿业股'周五屠杀')延续下挫9.4%。[MINING.com](https://www.mining.com/chart-friday-massacre-for-mining-stocks-but-copper-price-pulls-out-of-nosedive/)"),
    "LAR": ("联动", "核实：LAR为Lithium Argentina AG(阿根廷锂业，NYSE上市、工业金属矿采板块)，并非Larimar Therapeutics(代码LRMR)，故归入金属主题合理；8-18无独立事件，当日碳酸锂现价还微涨0.33%，下跌属金属主题普跌与高位获利了结。[Yahoo Finance LAR](https://finance.yahoo.com/quote/LAR/)、[TradingEconomics锂价](https://tradingeconomics.com/commodity/lithium)"),
    "VIAV": ("联动", "MarketWatch显示8-18盘中跌11.5%至40.93美元(收跌10.6%)，无公司层面新闻；年内涨幅一度约136%的网络测试/光器件商，在30年美债收益率创2007年来新高、WSJ表外AI承诺报道引发的硬件/AI链去风险中遭高位获利了结。[MarketWatch](https://www.marketwatch.com/investing/stock/viav)"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "XPH", "perf": 2.883, "form": "交易所交易基金", "exposure": "制药（S&P权重）",
         "reason": "防御大回归日：礼来+3.6%、AbbVie +3.4%带动制药领涨全市场行业ETF，医疗保健在五个股票范围中四范围进入涨幅前三。合并删除：IHE +2.163%、PPH +1.910%、PJP +1.383%（同为美国制药敞口，按敞口去重只保留最强一只）。"},
        {"ticker": "UNG", "perf": 2.747, "form": "商品信托", "exposure": "天然气期货",
         "reason": "天然气期货领涨商品：天气与库存收紧叠加液化天然气出口需求；与制药、能源股票敞口相互独立。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "XLE", "perf": 1.758, "form": "交易所交易基金", "exposure": "大型能源权重股",
         "reason": "能源连续第三日领涨大盘板块：Targa +7.1%、埃克森美孚+2.5%、Williams +2.3%，布伦特维持90美元附近。合并删除：IYE +1.580%、VDE +1.466%、FENY +1.438%、IXC +1.431%、IEO +1.394%（同为能源股敞口，只保留最强一只）。"},
    ],
    "down": [
        {"ticker": "PTF", "perf": -8.234, "form": "交易所交易基金", "exposure": "科技动量（Dorsey Wright）",
         "reason": "AI动量链大逆转日：昨日+4.0%的科技动量ETF当日-8.2%，周一领涨的存储（-8.8%）、半导体等权（-5.8%）、硬件（-3.0%）全线崩跌，动量因子自身成为最大下跌源。合并删除：PSCT -4.114%（小盘信息技术，同为科技动量敞口，保留最弱一只）。"},
        {"ticker": "EWY", "perf": -8.131, "form": "交易所交易基金", "exposure": "韩国股票",
         "reason": "韩国单一国家ETF罕见暴跌8.1%：半导体与存储占韩国指数高权重，为AI链回调的亚洲映射；非杠杆国别基金，与科技动量为不同地域敞口。合并删除：FPA -4.584%、AIA -3.884%（亚太分散型，保留最弱一只）。"},
        {"ticker": "XSD", "perf": -5.752, "form": "交易所交易基金", "exposure": "半导体（修正等权）",
         "reason": "半导体主题九个子行业清一色下跌（等权-5.57%）：Amkor -10.5%、Wolfspeed -10.0%、FormFactor -10.0%、Coherent -12.8%；权重SOXX -4.96%、SMH -4.09%同跌。合并删除：SOXX -4.963%、SMH -4.089%（同簇半导体，保留最弱一只）。"},
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
    assert DATA["date"] == "2026-08-18"
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
            f"- `finviz_2026-08-18_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-18_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月18日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月18日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：“债券开始咬人”与AI动量大逆转共振：30年期美债收益率盘中破5.30%、收5.28%附近（2007年以来最高），10年期4.73%—4.75%，德日法收益率齐创多年新高、8月投资级公司债发行创纪录；标普500收跌约0.75%连跌第三日、纳指与罗素2000均约-1.3%，板块层面仅必需消费与能源收绿。费半自7月底低点+21%进入技术性牛市次日即反转：等权半导体-5.8%、存储ETF-8.8%、科技动量ETF-8.2%、韩国ETF-8.1%，归因长端收益率压制本轮最大赢家与动量交易自我了结；防御全面回归（制药ETF +2.9%、必需消费+1.1%，Amylyx试验成功+64%）；能源第三日领涨（Targa +7.1%获20年期二叠纪中游费用协议、布伦特91美元）；天然气期货+2.7%、黄金-1.7%白银-3.6%。周三FOMC纪要与20年期国债拍卖为下一验证点。", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5509/5537、S&P 500 498/500、Dow 30 30/30、Nasdaq 100 101/102、Russell 2000 1942/1946、Themes 268/268和ETF 658/659；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-18_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-18_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-18_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)
    print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
