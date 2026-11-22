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
}

SUB_CN = {
    "Curriculum": "课程内容", "Platforms": "平台", "Infrastructure": "基础设施",
    "Workforce": "职业教育", "ThreatOps": "威胁情报", "App Security": "应用安全",
    "Cloud": "云安全", "Endpoint": "端点安全", "ZeroTrust": "零信任", "SIEM": "安全信息与事件管理",
    "Identity IAM": "身份与访问管理", "Network": "网络",
    "Analytics & BI": "分析与商业智能", "AI Platforms": "人工智能平台", "Providers": "数据服务商",
    "Satellites": "卫星", "Data Analytics": "数据分析", "Launch": "发射", "Defense": "国防",
    "Drones": "无人机", "SpaceTech": "太空科技", "Missiles": "导弹", "Aviation": "航空",
    "Weapons": "武器", "Manufacturing": "制造", "CyberDefense": "网络防御",
    "Silver": "白银", "Gold": "黄金", "Precious": "贵金属", "Industrial": "工业金属",
    "Battery": "电池", "Rare Earth": "稀土", "Recycling": "回收",
}

THEME_COMPANY = {
    "SNDK": "SanDisk Corp", "ESTC": "Elastic NV", "CSGP": "CoStar Group Inc",
    "MH": "McGraw Hill Inc", "DUOL": "Duolingo Inc", "LRN": "Stride Inc",
    "RPD": "Rapid7 Inc", "TENB": "Tenable Holdings Inc",
    "TSAT": "Telesat Corp", "SPIR": "Spire Global Inc", "VSAT": "Viasat Inc",
    "ONDS": "Ondas Holdings Inc", "PAAS": "Pan American Silver Corp",
    "WWR": "Westwater Resources Inc", "ERO": "Ero Copper Corp",
}

COMPANY_NAME_FIX = {
    "APP": "AppLovin Corp", "SPCX": "Space Exploration Technologies Corp",
    "PSKY": "Paramount Skydance Corp", "STRZ": "Starz Entertainment Corp",
    "ESTC": "Elastic NV", "YXT": "YXT.com Group Holding Ltd",
    "SNDK": "SanDisk Corp",
}

# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。
# 事件时间口径：8月12日16:00 ET盘后事件可解释8月13日；8月13日16:00 ET后事件不得倒推。
R = {
    # === S&P 500 批次 ===
    "TTD": ("联动", "8月初Q2财报（营收不及预期、指引疲弱）后深跌逾两成，PPI降温与收益率回落推动广告科技与通信服务普涨，作为前期超跌的高波动广告科技股随板块大幅反弹。"),
    "NFLX": ("直接", "Pershing Square当日披露再次买入奈飞股份，知名投资人加仓提振情绪，叠加通信服务板块走强。[MarketScreener](https://www.marketscreener.com/news/netflix-shares-rise-after-bill-ackman-takes-stake-ce7859d9d080f226)"),
    "PSKY": ("直接", "当日报道公司拟出售CNN等资产，为约1100亿美元的华纳兄弟探索合并扫清监管与诉讼障碍，并购推进预期升温。[TipRanks](https://www.tipranks.com/news/catalyst/paramount-skydance-jumps-as-cnn-sale-clears-mega-merger)"),
    "CBRE": ("联动", "PPI降温强化按兵不动预期、长端收益率回落，商业地产服务龙头作为利率敏感标的随房地产板块走强。"),
    "EQR": ("联动", "公寓类REIT对利率高度敏感，PPI降温与收益率回落利好REIT估值，随房地产板块上涨。"),
    "WDAY": ("直接", "路透独家报道Silver Lake正洽谈以约430亿美元收购，盘中一度上涨约30%；软件私有化预期升温。[Investing](https://www.investing.com/news/stock-market-news/exclusivesilver-lake-in-talks-to-buy-workday-sources-say-4858969)"),
    "SNDK": ("直接", "8月13日投资者日发布长期增长战略与2030年财务目标（2028—2030年营收中高双位数增长、非GAAP毛利率约80%、营业利润率约75%），并推出新一代AI闪存芯片，带动存储链大涨。[SanDisk新闻稿](https://www.sandisk.com/company/newsroom/press-releases/2026/2026-08-13-sandisk-investor-day-2026)"),
    "GDDY": ("联动", "AI与软件板块情绪升温，CFO在Oppenheimer会议及专访中强调Airo AI产品、ARPU增长与AI搜索转型，点燃AI变现预期；无财报或并购等独立硬催化。"),
    "MOS": ("直接", "Freedom Broker当日以成本压力为由将评级下调至卖出，叠加基础材料板块走弱。[TipRanks](https://blog.tipranks.com/mosaic-stock-slumps-as-harsh-downgrade-shocks-investors/)"),
    "FCX": ("联动", "铜价走弱拖累铜矿龙头，随基础材料与铜板块回落。"),
    "NEM": ("联动", "金价回落与金矿股获利回吐，贵金属板块集体走低。"),
    "GNRC": ("联动", "资金从周期股转向软件与科技，备用电源设备商随工业板块走弱。"),
    "FAST": ("联动", "工业紧固件分销商随工业板块小幅下跌。"),
    "ETN": ("联动", "随工业板块走弱；高管小额减持披露规模有限，主要驱动是工业板块轮动。"),
    "COP": ("联动", "油价当日下跌约2%拖累能源板块，综合石油巨头随板块走低。"),
    "EXE": ("联动", "油价走弱拖累天然气与能源股，随板块下跌。"),
    "OXY": ("联动", "油价下跌约2%拖累能源板块，随板块走低。"),
    # === Dow + Nasdaq 100 批次 ===
    "DIS": ("直接", "8月13日披露ESPN裁员以控成本，并公开2.88亿美元转播权成本跳增；市场聚焦成本优化，叠加通信服务领涨。[TechNews](https://ts2.tech/en/disney-stock-gains-1-5-as-espn-layoffs-expose-a-288-million-rights-cost-jump/)"),
    "GOOGL": ("联动", "随通信服务与云板块在PPI降温、收益率回落下的领涨走高。"),
    "CVX": ("单样本", "道指能源唯一样本；当日能源板块整体回落而雪佛龙逆势小涨，属个股独立波动。"),
    "SHW": ("单样本", "道指基础材料唯一样本；当日仅微涨，属材料回落背景下的孤立小波动。"),
    "MMM": ("联动", "随道指工业板块整体回落，无个股级事件。"),
    "HON": ("联动", "随道指工业回落；航空航天分拆交换要约属机械性流程，非方向性催化。"),
    "BA": ("联动", "随道指工业整体走软。"),
    "MCD": ("联动", "随可选消费在通胀降温交易中回落，无当日个股事件。"),
    "AMZN": ("联动", "AI资本开支担忧与可选消费走弱共同施压。"),
    "HD": ("直接", "8月12日盘后递交8-K：CEO因医疗原因临时休假数月并任命临时管理层；管理层不确定性为8月13日直接利空。[MarketScreener](https://www.marketscreener.com/news/the-home-depot-announces-interim-management-plans-while-ceo-takes-temporary-medical-leave-ce7859d8dd81f120)"),
    "WMT": ("联动", "随必需消费在风险偏好回升下跑输而小幅回落。"),
    "PG": ("背离", "必需消费相对滞涨，宝洁基本持平，与Walmart、Coca-Cola方向不一。"),
    "KO": ("背离", "必需消费相对滞涨，可口可乐以防御属性在收益率回落中小幅走高。"),
    "PYPL": ("单样本", "纳指金融唯一样本；利率敏感的金融科技属性在收益率回落中获资金流入。"),
    "TMUS": ("联动", "通信服务领涨，T-Mobile作为板块权重股放大涨幅。"),
    "APP": ("联动", "此前降评大跌后的超跌反弹，随通信服务与AI板块领涨修复估值。"),
    "WDC": ("直接", "SanDisk投资者日与AI存储需求带动存储链集体上涨，叠加投行上调目标价。[BingX News](https://bingx.com/ja/news/post/why-is-western-digital-wdc-stock-price-up-today-august-sandisk-outlook-lifts-ai-storage-shares)"),
    "BKR": ("联动", "随能源板块在PPI降温交易中整体回落。"),
    "FANG": ("联动", "随能源板块回落走低。"),
    "LIN": ("单样本", "纳指基础材料唯一样本；当日材料回落，林德小幅跟跌。"),
    "SPCX": ("背离", "前期自低点反弹约35%后的短线获利回吐与估值担忧，无独立负向催化。"),
    "FER": ("直接", "8月13日宣布自泛欧阿姆斯特丹交易所退市（保留纳斯达克与西班牙上市），叠加纳指工业走软。[Expansion](https://www.expansion.com/empresas/inmobiliario/2026/08/13/6a7df17d468aeb6d658b45a8.html)"),
    # === Themes 批次 ===
    "DUOL": ("联动", "教育科技主题全线上涨叠加AI软件反弹，花旗当日重申持有并上调目标价；Q2财报8月初已披露。[TipRanks](https://blog.tipranks.com/duolingo-jumps-as-investors-rethink-post-earnings-panic/)"),
    "ESTC": ("直接", "Oppenheimer当日上调目标价至100美元，并有新大额投资者入股报道；叠加网络安全与大数据主题走强。FY2027 Q1财报8月27日发布，非当日事件。[TipRanks](https://blog.tipranks.com/elastic-soars-after-bold-upgrade-and-big-new-backer/)"),
    "TENB": ("联动", "网络安全主题八个子主题全线上涨，Q2财报8月6日盘后已披露并上调指引，当日随主题与AI软件普涨。"),
    "TSAT": ("直接", "8月13日盘前公布Q2业绩转大幅净亏损、营收同比下滑，直接触发抛售。[GlobeNewswire](https://www.globenewswire.com/fr/news-release/2026/08/13/3344349/0/en/telesat-reports-results-for-the-three-and-six-months-ended-june-30-2026.html)"),
    "SPIR": ("直接", "8月12日盘后披露Q2财报，EPS不及预期0.05美元，叠加太空主题走弱。[MarketBeat](https://www.marketbeat.com/instant-alerts/spire-global-nysespir-announces-quarterly-earnings-results-misses-expectations-by-005-eps-2026-08-13/)"),
    "VSAT": ("联动", "卫星与太空主题整体走弱，公司数日前重申2027财年指引后当日随板块回落。"),
    "ONDS": ("直接", "8月12日盘后披露Q2财报：营收同比大增但EPS不及预期、亏损扩大。[Barron's](https://www.barrons.com/articles/ondas-earnings-stock-price-palantir-b69d2198)"),
    "WWR": ("联动", "当日Q2业务更新电话会亏损收窄略偏正面，但金属商品主题回落、石墨锂矿股整体承压。[Investing](https://www.investing.com/news/transcripts/earnings-call-transcript-westwater-resources-posts-smaller-q2-2026-loss-93CH-4858725)"),
    "ERO": ("联动", "铜价回落、铜矿股普跌带动。"),
    # === All Stocks 批次 ===
    "GXAI": ("直接", "8月12日盘后公布Q2财报：营收246万美元、同比约+1337%、环比+35.8%，创纪录并超预期。[Yahoo](https://finance.yahoo.com/technology/ai/articles/gaxos-delivers-record-second-quarter-201000502.html)"),
    "CURI": ("直接", "8月12日盘后公布Q2：净利润890万美元、调整后EBITDA 1140万美元创新高，AI数据授权驱动盈利并上调全年指引。[Yahoo](https://finance.yahoo.com/markets/stocks/articles/curiositystream-delivers-record-q2-earnings-200500781.html)"),
    "CCG": ("结构", "微盘低价汽车保险科技中概股，无同日财报、并购或重大公告，涨幅多为低价股情绪与资金驱动。"),
    "AZ": ("直接", "8月12日盘后Q2营收590万美元、EPS超预期，智能购物车交付近翻倍、毛利率升至42.6%；8月13日盘前Zacks上调评级至持有。[Yahoo](https://sg.finance.yahoo.com/news/a2z-reports-second-quarter-2026-201500494.html)"),
    "YXT": ("直接", "8月13日盘前公布2026上半年财报：扭亏为盈、AI收入同比近9倍增长、订阅用户恢复增长。[公司IR](https://ir.yxt.com/news-releases/news-release-details/yxtcom-reports-unaudited-financial-results-first-six-months-2026)"),
    "FIEE": ("结构", "微盘股（原Minim改名），多语言数字品牌运营平台，无同日财报或重大公告，涨幅多为低流动性微盘资金炒作。"),
    "CHCI": ("直接", "8月12日盘后公布Q2：营收2260万美元、同比约+74%，GAAP EPS 0.84美元超预期。[Seeking Alpha](https://seekingalpha.com/news/4632721-comstock-holdings-gaap-eps-of-0_84-revenue-of-22_6m)"),
    "CMCT": ("结构", "微盘办公REIT，Q2财报8月14日才披露，当日上涨属财报前超跌反弹，无同日硬事件。"),
    "CSGP": ("直接", "CEO Andy Florance自掏腰包增持约249万美元股票并给出正面展望，触发反弹。[TipRanks](https://blog.tipranks.com/costar-jumps-as-ceo-bet-and-outlook-spark-rally/)"),
    "FGL": ("融资定价", "披露重组800万美元票据并获最高2000万美元预付款股权融资（逐期折价发股），严重摊薄引发抛售。[TipRanks](https://www.tipranks.com/news/company-announcements/founder-group-restructures-us8m-note-and-secures-up-to-us20m-in-prepaid-share-financing)"),
    "SLND": ("直接", "8月12日盘后公布Q2并开电话会：EPS大幅不及预期、营收低于预期，8月13日暴跌。[Investing](https://www.investing.com/news/transcripts/earnings-call-transcript-southland-holdings-posts-steep-q2-2026-miss-93CH-4858620)"),
    "REZI": ("直接", "8月12日盘后Q2创纪录但指引偏弱、业务分拆扰动，盘后已跌；8月13日Oppenheimer下调目标价，续跌。[MarketBeat](https://www.marketbeat.com/instant-alerts/resideo-technologies-q2-earnings-call-highlights-2026-08-12/)"),
    "PAAS": ("直接", "8月12日盘后公布Q2利润不及预期（产量降、成本升、税负增），8月13日跳空低开收跌9.7%。[MarketBeat](https://www.marketbeat.com/instant-alerts/pan-american-silver-nysepaas-shares-gap-down-after-earnings-miss-2026-08-13/)"),
    "LWLG": ("直接", "8月12日盘后披露Q2：亏损扩大、营收仍极低，聚合物光子商业化推进中。[Investing](https://www.investing.com/news/company-news/lightwave-logic-q2-2026-slides-loss-widens-as-commercialization-advances-93CH-4851814)"),
    "IDR": ("直接", "8月12日盘后发布Q2，EPS与营收均不及预期，叠加金价回落。[MarketBeat](https://www.marketbeat.com/instant-alerts/idaho-strategic-resources-nyseamericanidr-releases-quarterly-earnings-results-misses-estimates-by-001-eps-2026-08-13/)"),
    "OBX": ("资本结构", "8月初完成与Galera反向合并及3.5亿美元PIPE，8月13日无独立经营事件，跌幅主要来自摊薄与PIPE股份解禁抛压。[BusinessWire](https://www.businesswire.com/news/home/20260803549139/en/)"),
    "VBIO": ("公司治理", "股东3i LP提交13D/A并致函董事会，提出以罢免CEO、改组管理层为条件的900万美元投资提议，叠加前期利好后的获利回吐。[SEC文件解读](https://tradefomo.ai/zh-CN/sec-filing-tldr/3i-lp-3i-lp-proposes-9m-investment-contingent-on-management-and-board-overhaul-at-valion-bio-inc--26-0811)"),
    "OTLK": ("融资定价", "8月13日定价5500万美元增发普通股及认股权证，摊薄引发抛售。[GlobeNewswire](https://www.globenewswire.com/news-release/2026/08/13/3344189/0/en/)"),
    # === Russell 2000 批次 ===
    "MH": ("直接", "FY2027 Q1业绩超预期（调整后EPS 0.59美元 vs 预期0.48美元、收入5.499亿美元、经常性收入增长10%），财报后延续大涨；教育科技主题全线上涨放大弹性。[MarketScreener](https://www.marketscreener.com/news/earnings-flash-mh-mcgraw-hill-inc-posts-q1-adjusted-eps-0-59-per-share-vs-factset-est-of-0-4-ce7859d9df89f322)"),
    "YSWY": ("直接", "公布Q2业绩：创纪录EBITDA并上调指引，便利店板块与必需消费小盘股走强。[Yahoo](https://finance.yahoo.com/markets/stocks/articles/yesway-inc-yswy-q2-2026-230637715.html)"),
    "LRN": ("联动", "教育科技主题全线上涨、McGraw Hill财报带动在线教育估值修复；公司新CEO与职业教育增长叙事为背景。"),
    "NCMI": ("联动", "8月11日盘后Q2与Captivate收购引发的暴跌后，8月13日随小盘通信服务板块反弹修复，无新的同日公司事件。"),
    "STRZ": ("直接", "CEO向华尔街推介独立上市故事（“被误解的资产”），小盘媒体情绪回暖。[Globe and Mail](https://www.theglobeandmail.com/investing/markets/stocks/STRZ/pressreleases/32652211/why-starz-entertainment-stock-soared-today/)"),
    "PSFE": ("直接", "8月13日公布Q2业绩：营收增长约4%，战略进展与增长计划获市场认可，股价上涨15.1%。[BusinessWire](https://www.businesswirenews.com/news/home/20260813084769/en/Paysafe-Reports-Second-Quarter-2026-Results)"),
    "NABL": ("联动", "软件与IT管理板块普涨，盈利拐点与增长指引叙事为背景；无独立同日硬催化。"),
    "RPD": ("联动", "网络安全主题八个子主题全线上涨、威胁情报子主题领涨，RPD作为主题权重股放大涨幅。"),
    "CENX": ("联动", "铝价与基础材料板块回落，小盘铝冶炼商估值承压；Q2业绩不及预期为前期事件。"),
    "ABEO": ("直接", "8月12日盘后公布Q2：EPS不及预期0.13美元、收入低于预期并转亏，股价大跌。[MarketWatch](https://www.marketwatch.com/story/abeona-shares-fall-on-swing-to-2q-loss-lower-than-expected-revenue-74ff2d39)"),
    "ADCT": ("直接", "8月13日公布Q2：业绩超预期但FDA监管担忧压过财报，股价下跌。[Investing](https://www.investing.com/news/transcripts/earnings-call-transcript-adc-therapeutics-beats-q2-2026-estimates-but-shares-fall-93CH-4858104)"),
    "PLX": ("直接", "8月13日公布Q2：盈利环比大幅回落，市场聚焦Elfabrio依赖度，股价下跌9.9%。[Barchart](https://www.barchart.com/story/news/3799651/protalix-biotherapeutics-reports-second-quarter-2026-financial-and-business-results)"),
    "HTZ": ("直接", "Pershing Square首席投资官表示已清仓，并批评公司宣布的融资计划、对管理层失去信心，股价大跌逾16%。"),
    "ALTG": ("联动", "工业设备租赁与经销随工业板块走弱，无同日公司事件。"),
}

CONTEXT = {}

ETF_SELECTION = {
    "up": [
        {"ticker": "SKYY", "perf": 3.906, "form": "交易所交易基金", "exposure": "云计算",
         "reason": "云计算主题四个子主题全部上涨，SKYY领涨；AI基础设施与软件云化需求推动，与网络安全、科技动量ETF构成当日科技敞口最强组合。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "HACK", "perf": 2.549, "form": "交易所交易基金", "exposure": "网络安全",
         "reason": "网络安全主题八个子主题全部上涨，Rapid7（RPD）、Elastic（ESTC）、Tenable（TENB）等权重股同步走强；利率回落改善高久期软件估值。合并删除：无同簇产品进入本轮极值候选。"},
        {"ticker": "QTEC", "perf": 2.235, "form": "交易所交易基金", "exposure": "科技动量（纳斯达克100科技板块）",
         "reason": "存储与AI硬件链领涨带动纳斯达克100科技板块指数走强；与半导体基金有交叉但行业覆盖更广，保留为科技动量敞口。合并删除：无同簇产品进入本轮极值候选。"},
    ],
    "down": [
        {"ticker": "PALL", "perf": -4.064, "form": "商品信托", "exposure": "钯金",
         "reason": "钯金价格回落，铂族金属需求与汽车催化转换预期承压；非杠杆商品信托，与金矿股、白银矿业为不同金属敞口。合并删除：PPLT（铂金）-2.509%属另一金属敞口，未合并。"},
        {"ticker": "RING", "perf": -3.098, "form": "交易所交易基金", "exposure": "全球金矿股",
         "reason": "金价与黄金矿业股当日回落，此前累计涨幅后的获利回吐叠加美元实际利率波动；Newmont（NEM）等权重股同步下跌。合并删除：GDXJ -3.013%；GDX -2.957%；SGDM -2.160%（同簇金矿股，按敞口去重只保留最极端一只）。"},
        {"ticker": "SIL", "perf": -2.880, "form": "交易所交易基金", "exposure": "白银矿业股",
         "reason": "白银与白银矿业股回落，Pan American Silver（PAAS）当日下跌约9.7%；白银矿业与金矿股为不同经济敞口，按原任务要求分别保留。合并删除：SLV（白银信托）-1.524%为白银现货信托敞口，未合并。"},
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
        text = "核查8月12日盘后至13日公司披露与可靠新闻后，暂未找到同日直接催化；" + text
    return f"{company}（{stock['ticker']}）**{pct(stock['perf'])}**【{label}】{text}"


def width(row: dict) -> str:
    return (f"{row['count']}只；{row['up']}涨/{row['down']}跌/{row['flat']}平；"
            f"上涨{row['up_pct']:.2f}%/下跌{row['down_pct']:.2f}%；整体{pct(row['overall_perf'])}")


def subthemes(row: dict, direction: str) -> str:
    ordered = sorted(row["subthemes"], key=lambda x: x["perf"], reverse=direction == "up")[:4]
    result = []
    for x in ordered:
        name = SUB_CN.get(x["display"], SUB_CN.get(x["name"], x["display"]))
        if re.search(r"[A-Za-z]", name):
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
    assert DATA["date"] == "2026-08-13"
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
            f"- `finviz_2026-08-13_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-13_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月13日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月13日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：7月PPI终值需求环比持平、低于预期，核心PPI同比约4.2%；初请失业金20.9万人。温和通胀数据压低收益率（10年期约-7.5bp），标普500上涨0.7%收于7,800点附近创纪录、罗素2000创新高，存储与AI硬件链领涨，能源与材料随油价回落。[美国劳工统计局PPI](https://www.bls.gov/news.release/ppi.nr0.htm)", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5527/5537、S&P 500 500/500、Dow 30 30/30、Nasdaq 100 101/102、Russell 2000 1945/1946、Themes 268/268和ETF 658/659；缺值代码不参与计算。", ""]
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
    (SKILL / "finviz_2026-08-13_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-13_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-13_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)
    print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
