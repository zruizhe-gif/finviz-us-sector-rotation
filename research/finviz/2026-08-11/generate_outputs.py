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
    "Education Technology": "教育科技",
    "Consumer Goods": "消费品", "Energy Traditional": "传统能源",
    "Social Media": "社交媒体", "Compute": "计算芯片", "Memory": "存储",
    "Analog": "模拟芯片", "Wireless": "无线芯片", "Foundries": "晶圆代工",
    "Design Tools": "芯片设计工具", "Lithography": "光刻", "Packaging": "封装",
    "Next-Gen": "下一代半导体", "Oil": "原油", "Gas & LNG": "天然气与液化天然气",
    "Uranium": "铀", "Biofuels": "生物燃料", "Water": "水资源",
    "Waste": "废弃物处理", "Air Quality": "空气质量", "Climate": "气候科技",
    "Agriculture": "农业", "Hardware": "硬件", "Software": "软件",
    "Identity": "身份认证", "Gov & Defense": "政府与国防", "Platforms": "平台",
    "Workforce": "职业教育", "Curriculum": "课程内容", "Infrastructure": "基础设施",
    "Food": "食品", "Apparel": "服装", "Luxury": "奢侈品",
    "Farm-Direct": "农场直供", "Household": "家庭用品", "Secondhand": "二手消费",
}

THEME_COMPANY = {
    "FORM": "FormFactor Inc", "COHU": "Cohu Inc", "KLAC": "KLA Corp",
    "SMR": "NuScale Power Corp", "CLNE": "Clean Energy Fuels Corp",
    "MNTK": "Montauk Renewables Inc", "RNW": "ReNew Energy Global plc",
    "CWCO": "Consolidated Water Co Ltd", "CECO": "CECO Environmental Corp",
    "AUID": "authID Inc", "BKYI": "BIO-key International Inc",
    "YOU": "Clear Secure Inc", "UTI": "Universal Technical Institute Inc",
    "WLY": "John Wiley & Sons Inc", "GOOGL": "Alphabet Inc",
    "BYND": "Beyond Meat Inc", "UAA": "Under Armour Inc",
    "HAIN": "Hain Celestial Group Inc",
}

# Every explanation is deliberately ticker-specific. Labels distinguish a verified
# company event from an industry read-through or a market-structure inference.
R = {
    "BESS": ("结构", "未见严格窗口内新披露；储能小盘股随电网投资主题上行，极端涨幅更受低流通盘放大；7月400MWh项目只是背景，[项目公告](https://www.globenewswire.com/news-release/2026/07/14/3326849/0/en/frontier-power-usa-selects-400-mwh-wildfire-bess-project-from-bimergen-energy-bringing-closed-and-selected-eos-backed-project-capacity-to-1-8-gwh.html)不能倒置为当日催化。"),
    "BNRG": ("结构", "热储能概念与公用事业偏强共振；8月7日已公告6比1反向拆股、但8月13日才按拆股后价格交易，[SEC文件](https://www.sec.gov/Archives/edgar/data/1901215/000121390026086735/ea030074401ex99-1.htm)不是当日新消息。"),
    "RNW": ("直接", "开盘前披露财团以每股7.02美元现金收购其余股份，确定性交易协议直接触发重估；[SEC 6-K](https://www.sec.gov/Archives/edgar/data/1848763/000119312526343552/d104914d6k.htm)。"),
    "BSIN": ("直接", "盘前Q2披露Big Sky Carbon Hub按计划推进、五年100%照付不议氦气合同仍在，并维持2027年一季度首收目标；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/101594/000143774926026862/ex_974000.htm)。"),
    "PROP": ("联动", "DJ盆地上游生产商对原油价格和小盘勘探开发风险偏好弹性较高；当日上涨与能源宽度及油价方向一致，主要体现小盘勘探开发弹性。"),
    "SMC": ("直接", "8月10日盘后发布Q2材料；中部大陆天然气处理量环比增9.9%、Double E输量增6.7%，叠加当日能源上行，构成公司经营与行业双重支撑；[SEC申报目录](https://www.sec.gov/Archives/edgar/data/2024218/000202421826000087/0002024218-26-000087-index.htm)。"),
    "QMCO": ("直接", "盘后FY2027 Q1营收8080万美元、同比增26%，高于7500万至8000万美元指引，调整后EBITDA转正至800万美元；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/709283/000162828026055272/fy27q1exhibit991.htm)。"),
    "AIFA": ("结构", "未见8月10日盘后至11日盘前新申报；7月LittleVault知识产权扩充属于旧闻，微盘股流通结构放大波动，[SEC提交记录](https://data.sec.gov/submissions/CIK0001708341.json)未支持同日直接催化。"),
    "NIQ": ("直接", "盘后Q2营收同比增8.0%、调整后EBITDA同比增21.9%，并上调全年收入增速、利润率及杠杆后自由现金流指引；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/2054696/000162828026055207/niqpressrelease-q226.htm)。"),
    "BODI": ("直接", "盘后Q2总营收同比降22.4%、订阅数降17.8%，且Q3营收指引仅4400万至4800万美元；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1826889/000119312526342355/body-ex99_1.htm)。"),
    "GETY": ("直接", "盘后Q2营收同比降2.5%、自由现金流为负1.226亿美元，循环额度所余3000万美元已于7月用尽，公司继续评估融资方案；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1898496/000162828026055270/gety-20260630xex991.htm)。"),
    "GAIA": ("直接", "盘后Q2营收同比降5%、经营现金流为负540万美元，净亏损扩大至约300万美元；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1089872/000119312526342333/gaia-ex99_1.htm)。"),
    "PETZ": ("结构", "业务主体并非典型美国地产运营商，在Finviz房地产样本中市值与流通盘都很小；跌幅主要说明分类样本噪声，不能代表REIT基本面。"),
    "NHI": ("直接", "8月10日盘后发布Q2、8月11日8:30举行电话会，价格正处于财报消化窗口；[公司日程](https://investors.nhireit.com/news/news-details/2026/NHI-Announces-Second-Quarter-2026-Earnings-Release-and-Conference-Call-Dates/default.aspx)。"),
    "VTR": ("联动", "医疗地产权重股与Welltower（WELL）、Healthpeak Properties（DOC）同步下跌，反映长久期医疗REIT估值重定价，而非单一小盘股冲击。"),
    "UZX": ("结构", "未见严格窗口内新申报；最近材料为7月F-3，跨境电商微盘股的流动性和筹资折价预期放大跌幅；[SEC提交记录](https://data.sec.gov/submissions/CIK0001969401.json)。"),
    "PRPL": ("直接", "盘后Q2净营收同比降6.5%、批发收入降19.1%，并因床垫需求疲弱下调全年营收指引至4.20亿至4.40亿美元；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1643953/000121390026087318/ea030125701ex99-1.htm)。"),
    "ONON": ("直接", "盘前Q2虽录得恒汇收入增长，但全年恒汇收入增速仅指向低20%区间、后续收入预测低于预期，增长溢价被压缩；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1858985/000185898526000018/a26q2-ex993xpressrelease.htm)。"),
    "EIX": ("联动", "加州公用事业高监管、高资本开支属性在防御轮入时弹性较大；3.037%的涨幅高于板块均值，但90.32%的标普公用事业上涨确认并非单股孤立。"),
    "CEG": ("联动", "核电与数据中心电力需求敞口叠加防御轮入；同时出现在标普500和纳斯达克100公用事业强势股，跨范围印证最强。"),
    "DUK": ("联动", "受益于监管型公用事业现金流与电网资本开支偏好；涨幅温和且同板块28涨3跌，属于宽度推动而非公司事件。"),
    "MPC": ("联动", "炼化股同时受油价抬升、成品油裂解价差和供应绕行风险定价推动，是标普能源中弹性最大的权重成分。"),
    "TPL": ("联动", "二叠纪矿权和水务收费模式令现金流直接暴露于钻探活动与油价，4.146%涨幅验证上游资产重估。"),
    "PSX": ("联动", "炼油与中游组合随原油风险溢价及产品价差走高，和Marathon Petroleum（MPC）同向强化炼化链信号。"),
    "AXON": ("联动", "公共安全设备与订阅软件订单可见度较高，市场等待CPI时资金回流高质量工业成长，涨幅显著高于工业整体。"),
    "GNRC": ("联动", "备用电源、数据中心供电与电网韧性敞口同时受益，且住宅建筑ETF上涨，家庭端设备需求预期获得交叉支持。"),
    "BLDR": ("联动", "建材分销对新屋开工与住宅成交敏感；ITB和XHB同步上涨，确认其4.335%属于住宅链轮入，并非孤立公司波动。"),
    "APP": ("延续", "8月6日财报后的估值消化延续，广告技术高增长溢价在指数走弱时继续压缩，属于财报后延续反应。"),
    "GOOGL": ("权重", "作为通信服务最大权重之一，下跌直接拖低标普、道指及教育科技平台子主题；更接近大型成长股去风险，而非整个通信服务盈利突变。"),
    "FOXA": ("联动", "传统媒体广告与内容资产随通信服务走弱；跌幅明显小于应用广告和大型互联网，显示压力并非同质。"),
    "WELL": ("联动", "医疗地产龙头与Ventas（VTR）、Healthpeak Properties（DOC）同步回落，确认医疗REIT的利率敏感估值压力。"),
    "DOC": ("联动", "医疗办公和生命科学地产现金流偏长久期，随同业下跌但幅度较小，属于板块尾部而非独立事故。"),
    "DECK": ("联动", "高端鞋服增长估值受到On Holding（ONON）财报后大跌的同业映射，跌幅比广义可选消费更深。"),
    "CVNA": ("联动", "高估值二手车平台对利率和风险偏好敏感；在等待CPI、成长股走弱的环境中出现久期压缩。"),
    "CASY": ("联动", "便利店兼燃油零售业务回落，但板块32涨22跌，说明它是个股尾部而非可选消费全面转弱。"),
    "CVX": ("联动", "道指唯一能源成分，随原油风险溢价上升；单样本清一色不能提供宽度，只能由其他范围能源上涨交叉确认。"),
    "SHW": ("结构", "道指基础材料仅一只样本；涂料对住宅修缮和建筑周期敏感，0.471%上涨与住宅建筑ETF偏强一致，但不代表完整材料板块。"),
    "JPM": ("联动", "大型银行受收益率曲线和信贷韧性预期支撑，涨幅与American Express（AXP）、Visa（V）同向但力度有限。"),
    "AXP": ("联动", "高端消费与循环信贷敞口随软着陆预期小幅走强；幅度温和，尚不足以说明消费加速。"),
    "V": ("联动", "支付网络随名义消费和跨境交易韧性小幅上行，在5只金融股中只是温和正贡献。"),
    "UNH": ("权重", "管理式医疗龙头下跌主导道指医疗走弱，成本利用率与政策不确定性的估值折价仍高于制药同业。"),
    "JNJ": ("联动", "制药和医疗器械防御股小幅回吐，跌幅远小于UnitedHealth（UNH），显示并非医疗全产业链冲击。"),
    "AMGN": ("联动", "大型生物制药随道指医疗普跌，但0.695%的幅度接近普通防御仓位调整。"),
    "DIS": ("背离", "当日小幅上涨，与Alphabet（GOOGL）大跌相反；道指通信服务的负收益实为权重结构，不是两只成分一致轮出。"),
    "AMZN": ("权重", "电商与云计算的高资本开支、长久期估值在CPI前承压，是道指可选消费负收益的主要来源。"),
    "NKE": ("联动", "运动服饰同业On Holding（ONON）财报后大跌形成估值和增长预期映射，拖累道指可选消费。"),
    "MCD": ("背离", "小幅上涨，与Amazon（AMZN）、Nike（NKE）相反，体现防御型餐饮现金流而非可选消费普跌。"),
    "XEL": ("联动", "监管型电力现金流在CPI前获防御配置，纳斯达克公用事业4只全涨验证宽度。"),
    "EXC": ("联动", "输配电资产与可预见费率基数增长受青睐；涨幅小于Constellation Energy（CEG），说明核电溢价更强。"),
    "FANG": ("联动", "二叠纪上游纯度高，随油价风险溢价上涨；纳斯达克能源两只全涨但样本很窄。"),
    "BKR": ("联动", "油服设备和液化天然气项目敞口受能源资本开支及油价走强支持，与上游FANG构成链条印证。"),
    "DXCM": ("联动", "连续血糖监测属于高质量医疗成长，在大型科技承压时获得相对资金回流。"),
    "GILD": ("联动", "抗病毒与肿瘤药现金流提供防御属性，和医疗器械成长股同涨使纳斯达克医疗不是单一子行业行情。"),
    "ISRG": ("联动", "手术机器人装机与耗材收入的可见度支持增长溢价，和Dexcom（DXCM）共同拉升医疗成长。"),
    "LIN": ("结构", "纳斯达克基础材料仅一只样本，0.392%的跌幅只代表工业气体权重股，不能外推整个材料板块。"),
    "PYPL": ("结构", "纳斯达克金融仅一只样本且只跌0.119%，更多是支付股微弱波动，不能据此判定金融轮出。"),
    "HON": ("权重", "大型综合工业的业务拆分与周期敞口估值承压，5.273%跌幅主导纳斯达克工业负收益。"),
    "SPCX": ("结构", "上市交易历史和可比估值框架仍在形成，3.928%下跌会放大样本读数，不宜外推整个航空航天工业。"),
    "ODFL": ("联动", "零担货运对工业货量和定价敏感，回落指向运输需求预期偏弱，与工业权重股压力同向。"),
    "NRGV": ("联动", "重力储能项目对电网投资与数据中心供电主题敏感；小盘股弹性高于大型监管公用事业。"),
    "CDZI": ("联动", "水资源和基础设施资产随公用事业及环境主题走强，土地水权估值令其弹性放大。"),
    "CWCO": ("财报窗口", "8月10日进入Q2披露窗口，水务运营股又与水资源子主题同涨；公司日程确认财报窗口，但未取得足以引用具体业绩数字的当期一手稿，因此不把上涨归结为某项未经核实的业绩指标。"),
    "AMPY": ("联动", "加州近海上游生产商对油价和许可风险高度敏感，油价上行令小盘勘探开发弹性释放。"),
    "CLNE": ("联动", "可再生天然气和运输燃料敞口随天然气、生物燃料主题上行，同时进入Russell能源与能源商品两处极值。"),
    "VALU": ("结构", "金融数据出版商流通盘较小，9.863%远高于Russell金融整体0.929%，主要是个股供需放大，并非银行主线。"),
    "SEZL": ("联动", "先买后付平台具有高增长、高波动和消费信贷双重敞口；上涨反映小盘金融风险偏好而非利差交易。"),
    "CD": ("结构", "数字资产相关小盘金融股受加密风险偏好驱动，7.343%涨幅不能代表Russell银行与保险盈利周期。"),
    "EVC": ("直接", "盘后Q2虽因广告技术业务令合并营收增126%，但核心媒体营收降1%、剔除政治广告后全国广告降19%，媒体分部转为经营亏损；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1109116/000119312526342346/evc-ex99_1.htm)。"),
    "IHRT": ("直接", "盘后Q2营收增1.7%，但调整后EBITDA降2.9%、多平台分部调整后EBITDA降39%；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1400891/000162828026055243/ihmediaearningsrelease2026.htm)。"),
    "UPWK": ("直接", "盘后Q2营收降2%、总服务额降4%、活跃客户降8%、净利润降22%、自由现金流降45%；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1627475/000162747526000046/upwork2q26-pressrelease.htm)。"),
    "TCMD": ("直接", "盘后Q2虽增长，但把全年营收指引上端由3.68亿美元下调至3.66亿美元，理由是耐用医疗设备客户消化库存；[SEC业绩稿](https://www.sec.gov/Archives/edgar/data/1027838/000110465926093346/tcmd-20260810xex99d1.htm)。"),
    "WVE": ("边界", "未见严格窗口内新公司事件；迁册与既有ATM登记材料早于交易窗口，不能倒置解释跌幅；[SEC文件](https://www.sec.gov/Archives/edgar/data/1631574/000119312526340679/d137806dposasr.htm)。"),
    "NUTX": ("延续", "最近Q2 8-K在8月6日提交，8月11日没有新申报；跌幅延续了财报后波动，并叠加小盘医疗流动性折价；[SEC 8-K](https://www.sec.gov/Archives/edgar/data/1479681/000162828026054274/nutx-20260806.htm)。"),
    "OFRM": ("结构", "新上市儿童食品股流通历史短、估值锚不稳定；7.274%跌幅远大于必需消费整体0.103%，公司级供需色彩更强。"),
    "NUS": ("联动", "直销美容保健品对中国需求、汇率和渠道活跃度敏感，弱势反映可选型必需消费的盈利折价。"),
    "KLC": ("联动", "托育运营商承受人工和场地成本、入园率敏感性，回落指向服务消费利润率担忧。"),
    "FORM": ("联动", "晶圆探针卡与先进封装测试需求弹性最大，7.646%与封装子主题4.649%居首一致。"),
    "COHU": ("联动", "半导体测试与检测设备随先进封装和后端资本开支预期上修，涨幅仅次于FormFactor（FORM）。"),
    "KLAC": ("权重", "制程控制设备受先进节点资本开支支持，4.011%为大型设备股确认，降低小盘股失真。"),
    "SMR": ("联动", "小型模块化反应堆受核电、数据中心电力需求和铀产业链风险偏好推动，是能源商品主题最大弹性股。"),
    "MNTK": ("联动", "可再生天然气项目现金流随生物燃料子主题上涨，和Clean Energy Fuels（CLNE）构成替代燃料交叉确认。"),
    "CECO": ("联动", "工业水与空气污染治理设备随环境资本开支预期走强，补足环境主题的设备端信号。"),
    "AUID": ("结构", "身份认证微盘股波动显著高于主题均值；四个子主题全跌确认方向，但7.605%仍主要由流动性放大。"),
    "BKYI": ("联动", "生物识别身份管理小盘股随身份认证子主题下跌，未见可覆盖主题的共同公司事件。"),
    "YOU": ("联动", "机场身份认证平台的高增长估值在风险偏好回落时压缩，与软硬件同跌形成主题宽度。"),
    "UTI": ("联动", "职业技能教育运营商对招生和就业周期敏感，4.603%跌幅对应职业教育子主题走弱。"),
    "WLY": ("联动", "课程出版和数字学习业务受教育预算与订阅增长预期压制，和课程内容子主题跌幅一致。"),
    "BYND": ("直接", "盘前8-K确定1比30反向拆股，8月13日收盘后生效、8月14日按拆股后价格交易，以恢复纳斯达克最低买价合规；[SEC 8-K](https://www.sec.gov/Archives/edgar/data/1655210/000165521026000057/bynd-20260811.htm)。"),
    "UAA": ("联动", "运动服饰估值受到On Holding（ONON）财报后冲击映射，和服装子主题2.906%的跌幅同向。"),
    "HAIN": ("联动", "天然有机食品需求与利润率预期承压，跌幅明显超过食品子主题，显示公司基本面折价更深。"),
}

CONTEXT = {
    ("Education Technology", "GOOGL"): ("权重", "Alphabet（GOOGL）并非纯教育公司，其下跌通过平台分类拖累教育科技读数；四个子主题全跌才是主题方向证据，不能把Alphabet本身写成教育行业催化。"),
    ("Environmental Sustainability", "RNW"): R["RNW"],
    ("Environmental Sustainability", "CWCO"): R["CWCO"],
    ("Commodities Energy", "CLNE"): R["CLNE"],
}

ETF_REASON = {
    "EWY": "韩国股票由半导体和出口权重带动；当日半导体主题清一色上涨，构成产业链交叉确认。",
    "EWS": "新加坡银行、地产和工业权重共同提供低波动顺周期敞口，区域资金偏好强于美股大盘。",
    "ITB": "美国住宅建筑链轮入，标普工业中的Builders FirstSource（BLDR）和Generac（GNRC）同步偏强；XHB被合并去重。",
    "EWZ": "巴西股汇风险暴露与大宗商品权重同时承压；BRF属同一国家小盘敞口，合并后不重复计票。",
    "PGJ": "中国互联网和成长型美国存托凭证回落，并获MCHI、FXI、GXC及两只A股基金同向确认；全部合并为中国股票敞口。",
    "XHS": "美国医疗服务与提供商普跌，和Russell医疗尾部、道指UnitedHealth（UNH）走弱互证；IHF属同簇产品。",
}


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
    company = stock.get("company") or THEME_COMPANY[stock["ticker"]]
    return f"{company}（{stock['ticker']}）**{pct(stock['perf'])}**【{label}】{text}"


def width(row: dict) -> str:
    return (f"{row['count']}只；{row['up']}涨/{row['down']}跌/{row['flat']}平；"
            f"上涨{row['up_pct']:.2f}%/下跌{row['down_pct']:.2f}%；整体{pct(row['overall_perf'])}")


def subthemes(row: dict, direction: str) -> str:
    ordered = sorted(row["subthemes"], key=lambda x: x["perf"], reverse=direction == "up")[:4]
    return "；".join(f"{cn(x['display'])}{pct(x['perf'])}" for x in ordered)


def render_range(key: str) -> list[str]:
    block = DATA["ranges"][key]
    theme = key == "themes"
    display_label = "主题" if theme else block["label"]
    out = [f"## {SECTION_LABEL[key]}", "",
           f"核验入口：[Finviz {display_label} 1-Day Map]({MAP_URLS[key]})。", ""]
    if theme:
        out += ["一致性按子主题判定，不按主题内重复股票；大类收益为全部有效子主题的等权平均。", ""]
    if theme:
        out += ["| 方向 | 主题与入选身份 | 子主题宽度与等权收益 | 主要子主题及个股原因 |",
                "|---|---|---|---|"]
    else:
        out += ["| 方向 | 板块与入选身份 | 宽度与整体收益 | 入选个股及原因 |",
                "|---|---|---|---|"]
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


def etf_form(description: str) -> str:
    if "ETN" in description:
        return "交易所交易票据"
    if "Trust" in description:
        return "信托型基金"
    return "交易所交易基金"


def render_etf() -> list[str]:
    out = ["## 七、ETFs：排除杠杆、反向并按底层敞口去重", "", f"核验入口：[Finviz ETF 1-Day Map]({MAP_URLS['etf']})。先排除杠杆、反向与每日倍数产品，再按底层经济敞口去重。", ""]
    for direction, title in (("up", "上涨三只"), ("down", "下跌三只")):
        out += [f"### {title}", "", "| 产品 | 涨跌幅 | 法律形式与独立敞口 | 驱动及去重证明 |", "|---|---:|---|---|"]
        for row in DATA["etf"][direction]:
            out.append(f"| {row['ticker']} | {pct(row['perf'])} | {etf_form(row['description'])}；{row['cluster']} | {ETF_REASON[row['ticker']]} 合并删除：{merged_text(row)}。 |")
        out += [""]
    return out


def selected_mentions() -> list[str]:
    return [x["ticker"] for key in RANGE_ORDER for d in ("selected_up", "selected_down")
            for row in DATA["ranges"][key][d] for x in row["extreme"]]


def expected_txt() -> tuple[list[str], list[str]]:
    stocks = sorted(set(selected_mentions()))
    etfs = [x["ticker"] for d in ("up", "down") for x in DATA["etf"][d]]
    return stocks, sorted(set(stocks + etfs))


def read_codes(path: Path) -> list[str]:
    return [x.strip() for x in path.read_text(encoding="utf-8-sig").splitlines() if x.strip()]


def audit_inputs() -> tuple[list[str], list[str]]:
    assert DATA["date"] == "2026-08-11"
    stocks, all_codes = expected_txt()
    assert set(stocks) == set(R), f"逐股原因缺失或多余：missing={set(stocks)-set(R)} extra={set(R)-set(stocks)}"
    assert read_codes(SKILL / "finviz_2026-08-11_stocks.txt") == stocks
    assert read_codes(SKILL / "finviz_2026-08-11_all_codes.txt") == all_codes
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
    out = ["## 一致性优先最终复核", "",
           "| 范围 | 清一色上涨完整候选 | 最终上涨3项 | 清一色下跌完整候选 | 最终下跌3项 |",
           "|---|---|---|---|---|"]
    for key in RANGE_ORDER:
        b = DATA["ranges"][key]
        display_label = "主题" if key == "themes" else b["label"]
        out.append(f"| {display_label} | {len(b['uniform_up'])}项：{candidate_text(b['uniform_up'])} | {selected_text(b['selected_up'])} | {len(b['uniform_down'])}项：{candidate_text(b['uniform_down'])} | {selected_text(b['selected_down'])} |")
    mentions = selected_mentions()
    duplicates = {k: v for k, v in Counter(mentions).items() if v > 1}
    out += ["", "复核结论：六个范围均先扫描全部有效板块或全部子主题；清一色候选先于平均表现排序，不足三项才补位。表内每个入选项均披露完整宽度或完整子主题宽度、等权收益及入选身份。", "",
            "## 代码文件审计", "",
            f"- 报告共有{len(mentions)}次个股提及，去重后{len(stocks)}只；重复仅来自跨范围或跨主题交叉：" + "、".join(f"{k}×{v}" for k, v in sorted(duplicates.items())) + "。",
            f"- `finviz_2026-08-11_stocks.txt`：{len(stocks)}行、{len(stocks)}只唯一股票代码，不含ETF。",
            f"- `finviz_2026-08-11_all_codes.txt`：{len(all_codes)}行、{len(all_codes)}只唯一代码，等于{len(stocks)}只股票加6只最终ETF，股票与ETF交集为0。",
            "- 结构核验结果：五个股票范围与主题各1张4列表、每张6个数据行；ETF共2张4列表、各3个数据行；候选身份、宽度恒等式、逐股原因覆盖及两个TXT集合均一致。", ""]
    return out


def build_report() -> str:
    stocks, all_codes = audit_inputs()
    out = ["# 2026年8月11日 Finviz 美股热力图日报", "",
           "**数据时点**：2026年8月11日美股正常交易时段收盘；Finviz页面时钟显示 `Tue AUG 11 2026 11:52 PM ET`，统计对象为 `subtype=d1`。", "",
           "**市场背景**：标普500下跌0.35%，纳斯达克综合指数下跌0.74%，道琼斯工业平均指数下跌0.22%；市场等待CPI，原油受地缘风险溢价推动，能源和公用事业相对占优，大型成长与通信权重承压。[市场综述](https://www.reuters.com/business/wall-st-futures-muted-us-iran-impasse-lifts-oil-prices-2026-08-11/) [原油综述](https://www.reuters.com/business/energy/oil-steadies-near-one-week-highs-us-iran-peace-deal-hopes-dim-2026-08-11/)", "",
           "**统计口径**：五个股票范围先逐板块扫描全部有效成分，主题先逐大类扫描全部子主题；宽度按上涨、下跌、平盘家数统计，整体收益沿用锁定的Finviz市值权重口径，主题按子主题等权。先选清一色候选，不足三项才按整体收益补位；个股涨跌来自同一份锁定统计底稿，原因核验不反向改写机械结果。", ""]
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
    labels = [SECTION_LABEL[k] for k in RANGE_ORDER]
    for label in labels:
        table_rows = [x for x in sections[label] if x.startswith("| ") and not x.startswith("|---")]
        assert len(table_rows) == 7, (label, len(table_rows))  # one header + six data rows
        assert all(x.count("|") == 5 for x in table_rows), label
    etf = sections["七、ETFs：排除杠杆、反向并按底层敞口去重"]
    etf_rows = [x for x in etf if x.startswith("| ") and not x.startswith("|---")]
    assert len(etf_rows) == 8  # two headers + six data rows
    assert all(x.count("|") == 5 for x in etf_rows)
    assert "https://finviz.com/quote.ashx" not in text
    forbidden = ["Consumer Goods", "Environmental Sustainability", "Commodities Energy",
                 "Communication Services", "Consumer Cyclical", "Education Technology"]
    # English scope names in map link labels are permitted; sector/theme names are not.
    body_without_urls = re.sub(r"https?://[^)\s]+", "", text)
    for term in forbidden:
        assert term not in body_without_urls, term


def main() -> None:
    report = build_report()
    structural_audit(report)
    target = SKILL / "finviz_2026-08-11_report.md"
    target.write_text(report, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(target)
    print("lines", len(report.splitlines()), "sha256", digest)
    print("REPORT_AUDIT_OK")


if __name__ == "__main__":
    main()
