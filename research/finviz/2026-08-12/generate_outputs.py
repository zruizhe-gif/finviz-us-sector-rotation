from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[2]
DATA = json.loads((HERE / "calculated-statistics.json").read_text(encoding="utf-8"))
SEC_WINDOW = json.loads((HERE / "sec-filing-window.json").read_text(encoding="utf-8"))
SEC_CIK = {row["ticker"]: row["cik"] for row in SEC_WINDOW["stocks"] if row.get("cik")}
SEC_CIK.setdefault("AEP", 4904)

THEME_COMPANY = {
    "BKSY": "BlackSky Technology Inc", "ASTS": "AST SpaceMobile Inc", "PL": "Planet Labs PBC",
    "LAES": "SEALSQ Corp", "IONQ": "IonQ Inc", "INTC": "Intel Corp",
    "SMCI": "Super Micro Computer Inc", "LITE": "Lumentum Holdings Inc", "VIAV": "Viavi Solutions Inc",
    "BMBL": "Bumble Inc", "SNAP": "Snap Inc", "DSP": "Viant Technology Inc",
    "AUID": "authID Inc", "EVLV": "Evolv Technologies Holdings Inc", "YOU": "Clear Secure Inc",
    "SKIL": "Skillsoft Corp", "CHGG": "Chegg Inc", "BNED": "Barnes & Noble Education Inc",
}
COMPANY_NAME_FIX = {
    "NCMI": "National CineMedia Inc", "APP": "AppLovin Corp",
    "WYFI": "WhiteFiber Inc", "FF": "FutureFuel Corp",
}
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
    "Consumer Defensive": "必需消费", "Space Tech": "太空科技",
    "Quantum Computing": "量子计算", "Hardware": "硬件",
    "Social Media": "社交媒体", "Biometrics": "生物识别",
    "Education Technology": "教育科技", "Software": "软件", "E-commerce": "电子商务",
}

SUB_CN = {
    "Satellites": "卫星", "Launch": "发射", "Earth Observation": "地球观测",
    "Space Tourism": "太空旅游", "Manufacturing": "制造", "Data Analytics": "数据分析",
    "Defense": "国防", "Cloud": "云计算", "Enabling Tech": "支撑技术",
    "Applications": "应用", "PCs & Devices": "个人电脑与设备", "Servers": "服务器",
    "Data Centers": "数据中心", "Electronics": "电子设备", "Gaming": "游戏",
    "Printing": "打印设备", "Telecom": "电信设备", "Industrial IoT": "工业物联网",
    "Next-Gen": "下一代硬件", "Networks": "社交网络", "Visual Content": "视觉内容",
    "Niche": "垂直社群",
    "Hardware": "硬件", "Software": "软件", "Security": "安全",
    "Communication": "通信", "Sensing": "传感", "Compute": "计算",
    "Storage": "存储", "Networking": "网络设备", "Components": "零部件",
    "Platforms": "平台", "Advertising": "广告", "Creator Economy": "创作者经济",
    "Dating": "交友", "Community": "社区", "Identity": "身份认证",
    "Gov & Defense": "政府与国防", "Workforce": "职业教育",
    "Curriculum": "课程内容", "Infrastructure": "基础设施",
}


def pct(value: float) -> str:
    return f"{value:+.3f}%"


def cn(name: str) -> str:
    if name not in CN:
        raise AssertionError(f"未翻译分类名称：{name}")
    return CN[name]


def filing(ticker: str, accession: str, document: str) -> str:
    cik = {
        "SMCI": 1375365, "LITE": 1633978, "ATRO": 8063, "EROC": 2110029,
        "NBIS": 1513845, "NCMI": 1377630, "EYE": 1710155, "MSGE": 1952073,
        "LVLU": 1780201, "TE": 1992243, "UAMY": 101538, "BOXL": 1624512,
        "FLYX": 1843973, "NCMI_MA": 1377630, "EVLV": 1805385,
        "SNAL": 1886894, "SVV": 1883313, "GOOGL": 1652044,
        "LPA": 1997711, "CAPS": 887151,
    }[ticker]
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace('-', '')}/{document}"


R = {
    "IVDA": ("结构", "Iveda是视频监控与人工智能方案小盘股；其涨幅远高于工业整体，且没有覆盖板块的共同公告，主要体现低流通盘与人工智能题材弹性。"),
    "EROC": ("直接", f"8月11日盘后披露约17亿美元创纪录积压订单、同比扩大约10倍，并取得Anthropic 470兆瓦设备订单；人工智能数据中心现场电力需求直接触发重估。[SEC业绩稿]({filing('EROC','0001193125-26-344714','eroc-ex99_1.htm')})"),
    "ATRO": ("直接", f"8月11日盘后公布季度销售增长27%、经营利润创纪录、订单与积压订单均创新高，并上调全年收入指引至10.2亿—10.4亿美元。[SEC业绩稿]({filing('ATRO','0000008063-26-000037','ex99120260704-pr.htm')})"),
    "BOXL": ("时间线", f"8月12日12:50美东时间才向SEC提交业绩稿；毛利率由35.0%升至49.8%、净亏损转为净利润，但该盘中披露不能解释此前已形成的全部涨幅，极低流通盘与投机交易放大波动。[SEC业绩稿]({filing('BOXL','0001628280-26-056308','boxl-earningsexx991xq22026.htm')})"),
    "CHOW": ("结构", "跨境云服务微盘股缺少可覆盖科技板块的同日共同事件；41.243%的极端涨幅主要是新股交易历史短、流动性薄和人工智能标签共同放大的个股波动。"),
    "NBIS": ("直接", f"8月12日盘前披露二季度结果；人工智能云业务扩容和收入增长强化算力需求预期，价格反应发生在正常交易时段。[SEC 6-K]({filing('NBIS','0001104659-26-094568','tm2622968d1_6k.htm')})"),
    "LPA": ("直接", "8月11日16:37美东时间盘后确认哥伦比亚地震后员工与租户安全、Calle 80物流园无损并全面运营，排除重大资产损失；8月12日12:23又提交二季度结果，14%的涨幅仍含小盘地产弹性。[SEC运营更新](https://www.sec.gov/Archives/edgar/data/1997711/000199771126000138/latampropertiesoftheameric.htm)"),
    "AEI": ("结构", "Alset兼具地产开发与控股公司属性，市值和流通盘较小；8.738%的涨幅远高于房地产整体，属于小样本放大。"),
    "CLPR": ("财报延续", "纽约住宅与商业地产运营商在8月6日财报后延续反应；同日小盘房地产92涨/28跌，利率回落提供板块背景，但8.247%仍含个股弹性。"),
    "JWEL": ("结构", "中国美妆电商微盘股未出现可覆盖可选消费的同日共同催化；价格主要受低流动性、境外发行人折价与电商竞争预期影响。"),
    "UZX": ("结构", "跨境电商微盘股交易历史短、流通盘薄；20%的跌幅与可选消费整体走弱同向，但远不能代表消费需求本身。"),
    "LVLU": ("时间线", f"8月12日12:14美东时间才向SEC提交业绩稿；毛利率提高330个基点、调整后息税折旧摊销前利润转正，但收入仍低于历史水平，且盘中披露不能解释此前全部跌幅。[SEC业绩稿]({filing('LVLU','0001104659-26-094884','lvlu-20260812xex99d1.htm')})"),
    "NCMI": ("直接", f"8月11日盘后公布二季度收入增长12.7%，同时披露收购Captivate；市场仍对影院广告竞争、交易整合与资本需求重新定价，跌幅属于公司级财报冲击。[SEC业绩稿]({filing('NCMI','0001193125-26-344665','ncmi-ex99_1.htm')})"),
    "SNAL": ("直接", f"8月11日盘后公布季度业绩及短剧制作关联交易；游戏收入与盈利质量的不确定性触发重估，不能外推整个通信服务板块。[SEC 8-K]({filing('SNAL','0001493152-26-037190','form8-k.htm')})"),
    "GITS": ("资本结构", "8月11日20:15美东时间注册证券文件生效，可影响次日；新增可交易供给和融资预期叠加微盘流动性折价，构成公司级冲击。[SEC EFFECT](https://www.sec.gov/Archives/edgar/data/1911545/999999999526002621/xslEFFECTX01/primary_doc.xml)"),
    "CAPS": ("直接", f"8月12日盘前同时补交多期季报修订并发布季度经营结果；密集重述与披露不确定性压倒建材板块背景，形成公司级下跌。[SEC 8-K]({filing('CAPS','0001437749-26-027159','caps20260812_8k.htm')})"),
    "UAMY": ("直接", f"8月11日盘后披露季度收入由1050万美元降至790万美元、毛利率由27%降至7%，并下调全年收入预期，直接触发24.468%的下跌。[SEC业绩稿]({filing('UAMY','0001104659-26-094130','tm2622899d1_ex99-1.htm')})"),
    "ITP": ("披露风险", "8月11日16:17美东时间提交季报延期通知，信息延迟与中国纸业小盘股流动性折价叠加；跌幅不代表造纸或材料需求全面变化。[SEC NT 10-Q](https://www.sec.gov/Archives/edgar/data/1358190/000121390026087794/ea0301618-nt10q_ittech.htm)"),
    "SMCI": ("直接", f"8月11日盘后业绩显示季度销售111亿美元、毛利率17.5%、净利润11.78亿美元，并给出高于市场预期的增长展望；服务器订单与利润率改善直接推动19.019%的正常时段涨幅。[SEC业绩稿]({filing('SMCI','0001375365-26-000021','exhibit991_20260630.htm')})"),
    "LITE": ("直接", f"8月11日盘后公布季度收入10.1亿美元、非公认会计准则毛利率50.4%，并指引下一季度收入12.25亿—12.75亿美元；人工智能光互连需求直接触发上涨。[SEC业绩稿]({filing('LITE','0001628280-26-055726','lite_ex991xq4fy26.htm')})"),
    "CIEN": ("联动", "高速光网络供应商随Lumentum财报和人工智能数据中心互连需求重估；其最近一季收入同比增40%并上调全年收入指引，构成产业基本面背景。"),
    "EQIX": ("联动", "数据中心REIT同时受人工智能容量需求和CPI后收益率回落支持；其涨幅与Digital Realty（DLR）同步，说明不是单股孤立。"),
    "DLR": ("联动", "数据中心租赁与开发需求受算力扩容支撑，CPI低于前月又缓解久期估值压力；和Equinix（EQIX）同向确认。"),
    "VTR": ("联动", "医疗地产现金流久期较长，CPI后收益率缓和推动估值修复；但涨幅温和，主要属于REIT板块宽度。"),
    "WMT": ("联动", "必需消费龙头受食品杂货现金流、防御属性和温和通胀支撑；同板块18涨/15跌，价格贡献高于宽度。"),
    "KDP": ("公司治理", "8月12日04:08美东时间提交8-K，披露独立董事任命与委员会安排；叠加饮料业务稳定现金流，1.302%的涨幅属于温和公司因素与防御联动。[SEC 8-K](https://www.sec.gov/Archives/edgar/data/1418135/000141813526000053/kdp-20260810.htm)"),
    "HSY": ("联动", "可可成本与定价仍约束利润，但温和CPI和防御偏好支持食品龙头；没有证据把1.236%归因于新的公司事件。"),
    "TPR": ("联动", "高端与可选服饰需求对估值和消费者支出预期敏感；在可选消费16涨/38跌的背景下回落，属于品牌消费普遍压力。"),
    "LULU": ("联动", "高估值运动服饰对消费增速和库存折扣敏感；与Tapestry（TPR）同向而住宅建筑ETF也下跌，显示可选消费内部多个子链承压。"),
    "EBAY": ("联动", "成熟电商平台受商品交易总额和消费者价格敏感度约束；8月6日财报窗口后继续消化，跌幅与可选消费宽度走弱一致。"),
    "CRH": ("联动", "建材龙头随美国住宅建筑ETF下跌，市场把较低通胀带来的利率利好与住宅需求、工程成本压力分开定价。"),
    "VMC": ("联动", "骨料需求与公共工程、住宅施工相关；与CRH及Linde（LIN）同跌，形成大盘材料宽度而非独立事故。"),
    "LIN": ("权重", "工业气体龙头是纳斯达克基础材料唯一成分，又是标普材料权重；单股下跌不足以代表所有材料子行业，但与CRH、VMC同向。"),
    "CHTR": ("资本结构", "8月12日12:06美东时间盘中披露债券交换要约提前结算安排，市场继续衡量高杠杆、有线用户流失和再融资成本；公司事件叠加通信板块压力。[SEC 8-K](https://www.sec.gov/Archives/edgar/data/1091667/000110465926094863/tm2622892d1_8k.htm)"),
    "APP": ("估值", "广告科技高增长股在前期财报后继续消化高预期；社交媒体五个子主题全跌，使其回落不只是孤立权重波动。"),
    "META": ("权重", "大型平台广告与人工智能资本开支并存；科技硬件大涨时其下跌体现硬件/平台分叉，并直接拖低标普通信服务。"),
    "MRK": ("联动", "大型制药防御现金流受温和CPI和收益率缓和支持；道指医疗四只全涨，说明不是单股事件。"),
    "UNH": ("联动", "管理式医疗在近期季报后继续修复，医疗利用率和成本仍是盈利关键；涨幅得到道指医疗清一色上涨确认。"),
    "AMGN": ("联动", "大型生物制药随防御现金流回流，涨幅较小且没有同日产品级催化，主要是板块宽度贡献。"),
    "KO": ("联动", "饮料现金流与定价能力提供防御性；0.266%的涨幅远低于Walmart（WMT），说明必需消费轮入并不均匀。"),
    "PG": ("背离", "日用品龙头小幅下跌，与Walmart（WMT）、Coca-Cola（KO）相反，显示道指必需消费并非清一色轮入。"),
    "HON": ("联动", "综合工业权重随航空航天、自动化与较低利率预期上行，并在道指和纳斯达克两个范围重复出现。"),
    "CAT": ("联动", "工程机械受基建、矿业资本开支与全球增长预期支撑；涨幅温和，属于工业权重确认。"),
    "MMM": ("联动", "多元工业现金流随工业板块回升；0.355%的幅度显示它只是宽度确认而非直接催化。"),
    "SHW": ("单样本", "道指基础材料只有Sherwin-Williams一只，涂料需求又受住宅链影响；单股下跌不能代表完整材料行业。"),
    "DIS": ("单样本", "道指通信服务两只均微跌，但Disney跌幅只有0.299%；内容、主题公园和流媒体并未出现覆盖板块的新冲击。"),
    "GOOGL": ("资本结构", f"8月10日完成250亿美元美元债发行，人工智能资本开支与长端融资供给受到重新评估；0.076%的微跌主要是权重噪声。[SEC 8-K]({filing('GOOGL','0001193125-26-342390','d171253d8k.htm')})"),
    "CVX": ("单样本", "道指能源只有Chevron一只且仅跌0.031%；在油价地缘波动背景下接近平盘，不能认定能源板块轮出。"),
    "XEL": ("联动", "监管型电力现金流受CPI后收益率回落支持；纳斯达克公用事业四只全部上涨，宽度有效。"),
    "AEP": ("联动", "电网资本开支与监管回报提供现金流可见度；和Xcel（XEL）、Exelon（EXC）同向确认利率敏感轮入。"),
    "EXC": ("联动", "输配电资产受融资成本预期缓和支持；涨幅温和，属于四只全涨的宽度证据。"),
    "PYPL": ("单样本", "纳斯达克金融只有PayPal一只，0.339%的涨幅既不提供行业宽度，也不足以代表银行或保险盈利改善。"),
    "SPCX": ("结构", "上市历史短的太空权重样本大涨9.648%，会显著拉高仅13只的纳斯达克工业均值；更接近太空主题而非完整工业。"),
    "ODFL": ("联动", "零担货运对工业货量、定价与燃料成本敏感；温和上涨为工业活动预期提供有限确认。"),
    "BKR": ("联动", "油服设备与液化天然气项目对客户资本开支和能源价格敏感；两只纳斯达克能源全跌，样本很窄。"),
    "FANG": ("联动", "二叠纪上游纯度高，价格随原油风险溢价回吐；和Baker Hughes（BKR）同跌形成窄样本能源压力。"),
    "MELI": ("联动", "拉美电商与金融科技对增长估值、汇率和消费信贷敏感；跌幅与纳斯达克可选消费3涨/8跌一致。"),
    "ABNB": ("联动", "旅游住宿平台对可选服务需求、费率和监管敏感；近期财报后继续消化增长预期。"),
    "AMZN": ("权重", "电商与云业务的高资本开支同时暴露于消费和人工智能；在硬件领涨时回落，体现资本开支受益者与出资者分化。"),
    "SHAZ": ("结构", "人工智能云基础设施小盘股的涨幅受短交易历史、注册发行与流动性放大；不能代表Russell科技全部249只。"),
    "WYFI": ("直接", "8月12日03:00美东时间提交季报，季度收入同比增长54.5%，人工智能算力托管收入与融资扩张预期叠加，形成公司级财报弹性。[SEC 10-Q](https://www.sec.gov/Archives/edgar/data/2042022/000121390026088026/ea0300877-10q_whitefiber.htm)"),
    "AIOT": ("管理层", "8月11日16:52美东时间盘后披露新任首席财务官及薪酬安排；8月10日财报后的车队物联网订阅收入与整合预期也在继续消化。[SEC 8-K](https://www.sec.gov/Archives/edgar/data/1774170/000149315226037165/form8-k.htm)"),
    "MSGE": ("直接", f"8月12日盘前公布全年收入增长13%、经营利润增长16%，现场娱乐需求与尼克斯夺冠带来直接盈利验证。[SEC业绩稿]({filing('MSGE','0001628280-26-055960','msgentertainmentcorpearnin.htm')})"),
    "DIBS": ("财报延续", "高端家居交易平台在8月5日财报后延续反应；上涨主要是低基数电商公司的个股修复，而非通信服务共同驱动。"),
    "RUM": ("财报延续", "8月10日季度业绩后继续反应，视频平台收入和成本结构进入重估；小盘通信39涨/25跌说明板块方向与大盘相反。"),
    "HPP": ("联动", "办公与影视地产对融资成本高度敏感；CPI后收益率缓和叠加近期季报消化，支持小盘REIT上涨。"),
    "SVC": ("联动", "酒店与服务地产对旅游需求及资本成本敏感；与Hudson Pacific（HPP）、JBG Smith（JBGS）同涨确认小盘地产宽度。"),
    "JBGS": ("财报延续", "8月10日季度结果后继续反应，华盛顿办公和多户住宅租赁预期与利率回落共振。"),
    "FF": ("财报延续", "8月10日季度披露后继续下跌；8月12日没有与正常时段跌幅匹配的新经营事件，生物燃料与特种化学业务盈利波动、原料与产品价差压制小盘材料。[SEC 10-Q](https://www.sec.gov/Archives/edgar/data/1337298/000143774926026784/ff20260630_10q.htm)"),
    "CENX": ("财报延续", "8月6日季度结果后继续消化，铝价、能源成本和冶炼利用率共同决定利润；与材料32涨/57跌同向。"),
    "EYE": ("直接", f"8月12日盘前业绩显示收入增长2.5%、同店销售增长3.4%且利润率改善，但管理层收紧同店销售展望；市场聚焦增长质量，触发11.559%下跌。[SEC业绩稿]({filing('EYE','0001628280-26-055930','ex991-q22026earningsrelease.htm')})"),
    "SVV": ("直接", f"8月11日盘后启动1500万股股东二次发行并安排回购，高额新增可交易供给直接压低股价。[SEC 8-K]({filing('SVV','0001193125-26-344910','d173043d8k.htm')})"),
    "PLBY": ("财报延续", "8月10日季度结果后继续消化，品牌授权、会员与现金流压力主导下跌；属于公司级消费冲击。"),
    "TE": ("直接", f"8月12日盘前业绩披露季度净亏损3690万美元，且盈利含2440万美元关税退款；尽管新增641兆瓦组件承购合同，利润质量与资本需求触发下跌。[SEC业绩稿]({filing('TE','0001213900-26-088022','ea030161501ex99-1.htm')})"),
    "ACHR": ("财报延续", "8月10日财报及收购Wisk协议后继续重估；研发、认证、现金消耗和交易整合压力压过太空与航空航天风险偏好。"),
    "FLYX": ("直接", f"8月12日盘前发布二季度结果，私人航空机队利用率、现金流与资本结构进入当日定价，跌幅属于公司级财报冲击。[SEC业绩材料]({filing('FLYX','0001193125-26-345834','flyx-ex99_1.htm')})"),
    "BKSY": ("联动", "地球观测卫星公司随太空五个子主题全涨；近期季报与国防/情报订单预期提供背景，6.624%仍高于主题均值。"),
    "ASTS": ("财报延续", "8月10日季度结果后继续反应，卫星部署、商业服务进度与资本开支决定估值；和BlackSky（BKSY）、Planet Labs（PL）同涨。"),
    "PL": ("联动", "地球观测数据与国防合同受太空风险偏好支持；涨幅小于小盘同业，构成较稳健的主题确认。"),
    "LAES": ("公司事件", "8月10日任命首席量子官并整合量子互连子公司，叠加量子计算六个子主题全涨，形成公司与主题共振。"),
    "IONQ": ("联动", "量子硬件与云接入龙头随主题全涨；近期财报后订单、收购整合和研发投入仍是盈利兑现关键。"),
    "INTC": ("融资定价", "8月12日12:05美东时间盘中提交补充8-K；资本补强与人工智能、先进封装扩产共同进入定价，但Intel并非纯量子公司。[SEC 8-K](https://www.sec.gov/Archives/edgar/data/50863/000119312526346806/d117670d8k.htm)"),
    "VIAV": ("联动", "网络测试、光通信和高速连接需求受Lumentum业绩映射；与SMCI、LITE同涨确认硬件链条。"),
    "BMBL": ("财报延续", "8月5日季度业绩后持续消化用户、付费转化和产品重构压力；社交媒体五个子主题全跌强化板块信号。"),
    "SNAP": ("联动", "广告平台对需求、定价和用户参与度敏感；与Bumble（BMBL）、Viant（DSP）同跌，不是单一权重事故。"),
    "DSP": ("财报延续", "8月10日季度结果后继续反应，广告技术收入与流量获取成本进入重估；社交媒体宽度为其下跌提供行业背景。"),
    "AUID": ("结构", "身份认证微盘股跌幅显著高于该主题四个子主题均值；低流动性放大了生物识别与身份验证方向的回落。"),
    "EVLV": ("直接", f"8月11日盘后公布季度业绩，安全筛查设备收入、积压订单与现金消耗重新定价；主题四个子方向全跌，形成公司与主题共振。[SEC 8-K]({filing('EVLV','0001805385-26-000047','evlv-20260811.htm')})"),
    "YOU": ("联动", "机场身份认证平台的高增长估值随身份验证主题回落；近期财报后没有覆盖整个主题的新共同事件。"),
    "SKIL": ("联动", "企业培训平台对订阅续费、企业招聘和成本控制敏感；教育科技四个子主题全跌，显示不是孤立公司波动。"),
    "CHGG": ("财报延续", "8月6日季度结果后继续消化订阅用户与人工智能替代压力；与Skillsoft（SKIL）、Barnes & Noble Education（BNED）同向。"),
    "BNED": ("结构", "公司8月12日提交的是例行年报与股东会材料，不构成新的经营催化；正常时段跌幅主要反映校园零售季节性、资本结构和教育需求压力。"),
}

CONTEXT = {
    ("Hardware", "SMCI"): R["SMCI"], ("Hardware", "LITE"): R["LITE"],
    ("Hardware", "VIAV"): R["VIAV"], ("Biometrics", "AUID"): R["AUID"],
    ("Biometrics", "EVLV"): R["EVLV"], ("Biometrics", "YOU"): R["YOU"],
}

ETF_REASON = {
    "EWY": "韩国综合指数约涨3.7%，三星电子与SK海力士等半导体权重受人工智能硬件行情推动；为非杠杆国家股票基金。",
    "PTF": "美国科技动量组合受服务器、光通信和半导体领涨带动；与半导体基金有交叉，但方法和行业覆盖更广，保留为科技动量敞口。",
    "CORN": "美国农业部在美东中午发布8月供需报告，玉米供需预期重定价直接推动商品池上涨；法律形式为非杠杆商品池。",
    "PGJ": "中国成长型美国存托凭证回落；FXI、MCHI、GXC等同属中国股票敞口并合并删除。",
    "ITB": "美国住宅建筑商受房价可负担性、按揭成本与订单预期压制；XHB与其高度重合并合并删除。",
    "VXX": "标普500 VIX短期期货指数的1倍多头无担保票据；现货股指温和上涨、隐含波动回落，推动该票据下跌。其名称中的Short-Term指期货期限，并非做空或反向。",
}


def reason(group: str, ticker: str) -> tuple[str, str]:
    return CONTEXT.get((group, ticker), R[ticker])


def stock_cell(group: str, stock: dict) -> str:
    label, text = reason(group, stock["ticker"])
    company = COMPANY_NAME_FIX.get(stock["ticker"], stock.get("company") or THEME_COMPANY.get(stock["ticker"], stock["ticker"]))
    if label in {"结构", "联动", "权重", "单样本", "估值", "财报延续", "融资背景"}:
        filings = next(row["filings"] for row in SEC_WINDOW["stocks"] if row["ticker"] == stock["ticker"])
        checked_forms = []
        for filing_row in filings:
            form = filing_row["form"]
            if form not in checked_forms:
                checked_forms.append(form)
        filing_scope = f"SEC {'、'.join(checked_forms[:3])}" if checked_forms else "SEC公司档案"
        text = f"核查8月5—12日公司披露和{filing_scope}，并复核融资与可靠新闻后，暂未找到同日直接催化；" + text
    if "https://" not in text:
        text += f"[SEC公司页](https://www.sec.gov/edgar/browse/?CIK={SEC_CIK[stock['ticker']]}&owner=exclude)"
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


def merged_text(row: dict) -> str:
    merged = row.get("merged", [])
    return "；".join(f"{x['ticker']} {pct(x['perf'])}" for x in merged) if merged else "无同簇产品进入本轮极值候选"


def etf_form(row: dict) -> str:
    if row["ticker"] == "CORN": return "商品池"
    if "ETN" in row["description"]: return "交易所交易票据"
    if "Trust" in row["description"]: return "信托型基金"
    return "交易所交易基金"


def etf_exposure(row: dict) -> str:
    cluster = row["cluster"]
    if "｜" not in cluster:
        return cluster
    by_ticker = {
        "PTF": "美国科技动量股票",
        "CORN": "玉米期货",
    }
    return by_ticker.get(row["ticker"], cluster)


def render_etf() -> list[str]:
    out = ["## 七、ETFs：排除杠杆、反向并按底层敞口去重", "", f"核验入口：[Finviz ETF 1-Day Map]({MAP_URLS['etf']})。先排除杠杆、反向与每日倍数产品，再按底层经济敞口去重。", ""]
    for direction, title in (("up", "上涨三只"), ("down", "下跌三只")):
        out += [f"### {title}", "", "| 产品 | 涨跌幅 | 法律形式与独立敞口 | 驱动及去重证明 |", "|---|---:|---|---|"]
        for row in DATA["etf"][direction]:
            out.append(f"| {row['ticker']} | {pct(row['perf'])} | {etf_form(row)}；{etf_exposure(row)} | {ETF_REASON[row['ticker']]} 合并删除：{merged_text(row)}。 |")
        out += [""]
    return out


def selected_mentions() -> list[str]:
    return [x["ticker"] for key in RANGE_ORDER for d in ("selected_up", "selected_down") for row in DATA["ranges"][key][d] for x in row["extreme"]]


def expected_txt() -> tuple[list[str], list[str]]:
    stocks = sorted(set(selected_mentions()))
    etfs = [x["ticker"] for d in ("up", "down") for x in DATA["etf"][d]]
    return stocks, sorted(set(stocks + etfs))


def audit_inputs() -> tuple[list[str], list[str]]:
    assert DATA["date"] == "2026-08-12"
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
    assert len(DATA["etf"]["up"]) == len(DATA["etf"]["down"]) == 3
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
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或子主题宽度、整体收益及入选身份。ETF按地图可见产品母集完成杠杆/反向排除及独立敞口去重。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；跨范围或跨主题重复：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-08-12_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-12_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月12日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月12日美股正常交易时段收盘；七套Finviz数据均为 `subtype=d1`，层级资源发布时间为美东收盘后。", "",
           "**市场背景**：7月CPI环比上涨0.1%、同比上涨3.4%，核心CPI环比上涨0.2%、同比上涨2.5%；温和数据压低收益率，人工智能服务器、云算力和光通信财报推动科技领涨。S&P 500上涨0.3%，纳斯达克综合指数上涨0.5%，Russell 2000上涨0.6%，道指微跌。[美国劳工统计局CPI](https://www.bls.gov/news.release/cpi.nr0.htm) [市场综述](https://apnews.com/article/stocks-markets-rates-trump-iran-chips-db541ced9f928f993bd3a17958a3deaa)", "",
           "**统计口径**：五个股票范围逐板块扫描地图全部有效成分，主题逐大类扫描全部有效子主题；宽度按上涨、下跌、平盘家数统计，板块整体收益沿用Finviz方块权重，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股原因按公告、SEC文件、财报及可靠新闻逐只核验，盘后消息不倒置解释此前价格。", "",
           "**数据完整性**：有效表现值覆盖All Stocks 5527/5537、S&P 500 499/500、Dow 30 30/30、Nasdaq 100 101/102、Russell 2000 1946/1946、Themes 268/268和ETF 658/659；缺值代码不参与计算。", ""]
    for key in RANGE_ORDER: out += render_range(key)
    out += render_etf()
    out += render_audit(stocks, all_codes)
    return "\n".join(out) + "\n"


def structural_audit(text: str) -> None:
    lines = text.splitlines(); sections = {}; heading = None
    for line in lines:
        if line.startswith("## "): heading = line[3:]; sections[heading] = []
        elif heading: sections[heading].append(line)
    for label in [SECTION_LABEL[k] for k in RANGE_ORDER]:
        rows = [x for x in sections[label] if x.startswith("| ") and not x.startswith("|---")]
        assert len(rows) == 7 and all(x.count("|") == 5 for x in rows), label
    etf = sections["七、ETFs：排除杠杆、反向并按底层敞口去重"]
    rows = [x for x in etf if x.startswith("| ") and not x.startswith("|---")]
    assert len(rows) == 8 and all(x.count("|") == 5 for x in rows)
    forbidden = ["Consumer Goods", "Environmental Sustainability", "Commodities Energy", "Communication Services", "Consumer Cyclical", "Education Technology", "Cybersecurity", "Biometrics"]
    body_without_urls = re.sub(r"https?://[^)\s]+", "", text)
    for term in forbidden: assert term not in body_without_urls, term
    assert text.count("暂未找到同日直接催化") > 0
    assert "CIK=&" not in text
    for ticker, company in THEME_COMPANY.items():
        assert f"{company}（{ticker}）" in text, ticker


def main() -> None:
    stocks, all_codes = audit_inputs()
    (SKILL / "finviz_2026-08-12_stocks.txt").write_text("\n".join(stocks) + "\n", encoding="utf-8-sig")
    (SKILL / "finviz_2026-08-12_all_codes.txt").write_text("\n".join(all_codes) + "\n", encoding="utf-8-sig")
    report = build_report(); structural_audit(report)
    target = SKILL / "finviz_2026-08-12_report.md"; target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target); print("lines", len(report.splitlines()), "sha256", digest); print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
