# Bloomberg Open Interest 节目内部研究（2026-09-28 周一）

## 元信息

| 项目 | 内容 |
|---|---|
| 本地字幕绝对路径 | `E:\Skill\finviz-us-sector-rotation - Zcode\finviz-us-sector-rotation-v0.2\script\open interest-2026-09-28.txt` |
| 字幕 SHA-256 | `fb1a260285cec4982d875eec8abae2919f7e5f3037fd79dbdf70d4caeb195ae9`（python hashlib 本地计算，完整 64 位十六进制） |
| 节目日期 | 2026-09-28（周一）——**开盘前后两小时档："火箭与收益率一起冲进外太空"**。当日主线：油价因特朗普否决伊朗重开霍尔木兹方案再涨（Brent 盘中高 $107）、**10Y 5.2151（2007 年以来最高）、30Y 2004 年以来最高**、标普 -0.4%~-0.5%、纳指 -0.75%~-1%；**SpaceX Starship 首次入轨全程直播**（发动机空中熄火→"go for orbit"→入轨成功→26 星全部署）；**英伟达 +$1,500 亿回购（总额 $2,350 亿、史上最大）**；**MongoDB CEO 被 Meta 挖角、股价一度 -20%+**；贵金属矿领跌（金 -3~-4%） |
| 节目名称与主持人 | Bloomberg Open Interest（纽约开盘档）。**Danny Berger**（字幕作"Danny Ber/Danny Berger"）主持；**Matt Miller 休陪产假**（00:27:09）；记者团：**Ed Ludlow**（Bloomberg Tech 主持，"Ed Ledllo/Lllo"，SpaceX 直播）、**Nora Melinda**（"Nor Melinda/Norinda/Nora"，Top Calls 与 Movers）、**Seth Figerman**（Bloomberg Tech 编辑）、**Ryan Vastelica**（"Ryan Vistella"，科技记者）、**Michael McKe**（"Michael McKe/Mickey"（部分）国际经济与政策记者）、**Kaylee Lines**（Balance of Power 联合主持，华盛顿） |
| 字幕全文读取状态 | 已完整读取：全文 2,613 行（wc -l 计 2,613 个换行符，行尾 CRLF、末行带尾换行），Read 分 2 段读至 EOF：1–1400、1401–2613，末行 [01:32:22] 'This is Bloomberg Open Interest.'，无遗漏、无明显时段空档 |
| 时长/结构 | 00:00:00–01:32:22（约 92 分钟）。嘉宾出场序：**Ed Ludlow**（SpaceX Starship 直播三段：熄火疑云→决定入轨→入轨与部署）→ **Tom Leighton**（Akamai 联合创始人/CEO，$120 亿 Anthropic 协议后首访）→ **Lori Calvacina**（RBC 美股策略主管，开盘定调）→ Nora Top Calls（Roblox/First Solar/Sweetgreen）→ **Ed Ludlow**（Starship 入轨确认）+ **Seth Figerman**（英伟达回购+Meta 企业级+MongoDB）→ **Steven Flynn**（Bloomberg Intelligence 高级信用分析师，Paramount $440 亿发债）→ **Michael McKe**（数据周+13/19 位 FOMC 票委讲话）→ **Christina Hooper**（Man Group 首席市场策略师，"实质性抛售"警报）→ **Mark Champion**（Bloomberg Opinion 专栏作者，伊朗/柴油禁令全球视角）→ **Rich Steinmeier**（LPL Financial CEO，AI 与财富管理）→ **Ryan Vastelica**（英伟达/Meta/MongoDB）→ **Kaylee Lines**（中美 $600 亿关税互减+伊朗谈判）→ **Nikki Shields**（MKS PAMP 研究主管，贵金属聚焦）→ Nora Movers 收尾 |

> 说明：字幕为机器转写，存在拼写失真（人名/机构名/数字）。本文为内部研究文件，仅使用该字幕文件内容；无法确认处一律标注"字幕无法确认"或"口径失真"，不做外部补充。

---

## 一、主要主题与核心内容

### 1. 开场：SpaceX Starship 首次入轨——从"熄火"到"go for orbit"（00:00:00–00:16:01）

- 开场白（00:00:00）："**ROCKET SHIPS AND YIELDS TAKE OFF INTO OUTER SPACE.**"——开盘前 30 分钟从 Surveillance 接棒（Danny："THAT DOES IT FOR SURVEILLANCE"）。
- 意外（00:01:20，Ed Ludlow）："**AT THE BOTTOM OF STARSHIP ARE SIX RAPTOR ENGINES AND ONE OF THOSE ENGINES CUT OUT EARLY ... THEY WILL NOW NOT BE ABLE TO ATTEMPT TO GET TO AN ORBITAL ALTITUDE AND THE STOCK['S] NOW REACTING ... DOWN 1.3%.**"——股价随直播剧烈波动：-1.3% → -1.8% → -2%（00:04:18）。
- 单点故障论（00:02:05）："**IF YOU GO BACK TO THE S1, THE PROSPECTUS PRIOR TO THE IPO COULDN'T HAVE BEEN CLEARER THAT STARSHIP['S] SUCCESS IS THE SINGLE POINT OF FAILURE OF WHICH SPACEX'S WHOLE FUTURE BUSINESS IS RELYING ON.**"——IPO 发行价 $135（00:04:24），"still above that, but dropping precipitously"。
- 载荷（00:07:03）：船上 **26 颗真正可用的 Starlink 卫星**、原计划贡献 **每秒 1 太比特**网络容量；部署方式如 PEZ 糖果滑出；"卫星形态的数据中心"（轨道算力）时间表"明年"——上市前内部人士反而认为公司在此前瞻上偏保守。
- 转折（00:12:09）："**SPACE X GO FOR ORBIT. STARSHIP WILL SOON PERFORM A BURN WITH A SINGLE RAPTOR ENGINE TO ENTER A 275 KM ORBIT OF EARTH.**"——股价转涨（盘前 +0.3%~+0.6-0.7%，00:12:20、00:25:09）。
- 入轨确认（00:24:58、00:37:39）：第 14 次试飞（"the 14th test flight"）**达到约 275 km 轨道高度**——此前所有试飞均为亚轨道；随后"**ALL 26 SATELLITES ON STARSHIP ROCKET HAVE BEEN DEPLOYED INTO ORBIT**"（00:47:55）；任务全程约 9 小时 50 分绕地六圈、最终离轨溅落智利以西。
- Falcon 9 退役时钟（00:10:14）：SpaceX 已**停止接受 2029 年初之后的 Falcon 9 订单**、ISS 2030–31 退役离轨——"**THE ENTIRE SPACE ECONOMY IS KIND OF IN LIMBO**"；SpaceX 承担全球 80%+ 的入轨载荷。
- 收盘前股价（01:01:53，Nora）：入轨+部署成功后 **+1.33%**（此前一度 -1.6%~-2%）。

### 2. 英伟达：史上最大回购 + AI 代理安全系统（00:00:18、00:14:32–00:16:01、01:19:43 起）

- 双消息（00:00:18）："**NVIDIA UP 2% ... INCREASING THE SIZE OF ITS SHARE BUYBACK PLAN BY $150 BILLION ... ALSO UNVEILED A NEW SYSTEM DESIGNED TO STOP AI AGENTS THAT BREAK THE RULES.**"
- Ed 口径（00:15:02）：市场早有预期（规模受限、M&A 空间小——Hugging Face 交易"相对小额"）；同日披露订单积压（"commits"）增长，并给出案例数据——"**ANTHROPIC HAS TO DATE $180 BILLION OBLIGATION FOR NVIDIA HARDWARE ACROSS ITS DIFFERENT DEPLOYMENTS**"（00:15:40）。
- 定性（00:39:44，Seth Figerman）：对担心 AI 开支潮可持续性的投资者而言是"reassuring moment"；安全工具部分——英伟达姿态与同行不同："**THEY'VE SAID THIS IS FUNDAMENTALLY AN ENGINEERING PROBLEM WHEREAS ANTHROPIC AND OTHER AI GROUPS HAVE IMPLIED IT'S A REGULATORY CHALLENGE**"（01:40:11 段同旨）；"约百家伙伴"如何落地仍需时间检验（00:40:44）。

### 3. Tom Leighton（Akamai CEO）：$120 亿 Anthropic 协议与分布式算力模式（00:16:08–00:24:55）

- 背景（00:16:08）："**AKAMAI SHARES POPPED LAST WEEK AFTER INKING A 12 BILLION 7-YEAR CONTRACT WITH ANTHROPIC**"（AI 将向 Anthropic 供应 CPU 以拓宽 Claude 模型接入）。
- 集中度之答（00:17:22）："**COLLECTIVELY NOW 14.4 BILLION IN LONG-TERM COMMITS WE'VE SIGNED ALREADY THIS YEAR ... WHEN IT'S FULLY ON BOARD AND RAMPED UP THAT'LL BE $2.2 BILLION A YEAR OF REVENUE AND VERY PROFITABLE, REVENUE ACCRETIVE TO OUR MARGINS.**"
- 资金（00:18:09）：账上现金超 **$40 亿**，暂不需举债；"利率再升一两个点对这些交易的盈利性影响不大"（00:19:30）；capex 与机房建设先行 6–9 个月才产生收入，**Q4 起开始体现**、**2028 年初全部进入满产收入**（00:18:32）。
- 模式优势（00:20:29）：**700 城、约 4,000 个接入点、单点 10–20MW**——远小于动辄吉瓦、遭遇社区抵制与审批困境的巨型数据中心；对照上周 Oracle 大型数据中心宣布不可抗力的窘境（00:21:10）。
- 商品化之问（00:21:32）："**WE'RE PRETTY FAR FROM THAT ... MODEL AS A SERVICE, INFERENCE AS A SERVICE ... REALLY GOING TO TAKE OFF.**"
- AI 安全（00:22:13）：两侧都要做——代理护栏（Akamai 自研 agent sandbox/agent security）+ 关键基础设施网络防御（"**BEFORE THERE WAS AI, YOU NEED TO HAVE THE CYBER DEFENSES IN PLACE**"）；政府可为标准与最低防护背书（00:24:47）。

### 4. Lori Calvacina（RBC）：估值-盈利测试——"没有魔法数字"（00:27:02–00:35:08）

- 油-收益率联动（00:29:12，致谢利率策略师 Blake Win）：若油价是 10Y 上行的推手，则一旦松动，估值端可获喘息——"**IF ONE SHIFTS, THERE['S] THE POTENTIAL FOR THE OTHER TO GET SOME RELIEF**"。
- 模型（00:30:08）："**I TAKE THE CONSENSUS BOTTOM UP ... LOP 10% OFF EARNINGS JUST TO BE CONSERVATIVE**"；基础情形已计入 **5% 收益率、3 次加息、2.75% 通胀** → **标普目标 8,150**（当前高点约 7,900 附近）；新增压力测试（通胀 3%、+1 次加息、10Y 5.25%）→ "slightly up market, kind of maybe flattish"。
- 结论（00:31:17）：盈利收益率 vs 债券收益率的跨资产模型"**NOT AT THE TIPPING POINT YET ... WE ARE RUNNING OUT OF ROOM**"；"**THERE'S NO MAGIC NUMBER BECAUSE YOU HAVE TO PUT IT IN THE CONTEXT OF THESE STRONG EARNINGS**"。
- 情绪（00:32:38）：AAII 两周前跌至长期均值下方两倍标准差、恰逢加息——情绪模型反而从 +10% 前瞻回报信号升至 **+15%**（"people feeling lousy is actually good for the market long term"）；Duke CFO 调查仅小幅走软。
- 消费（00:31:57）：RBC 经济团队的 K 型消费"alive and well"——高端支出力抵消低端、中间层"squishier"。
- 结构（00:33:21）：9 月 4 日（劳动节后）以来 EPS 一致预期几乎未动——仅能源、Mag7、明年科技数字微调；"**SINCE THE END OF JULY, ENERGY AND TECH HAVE BEEN YOUR BEST PERFORMING SECTORS**"；EPFR 美股资金流放缓但未转负（00:34:48）。
- 加息周期之问（00:32:18）："**IS THIS A BABY HIKING CYCLE, WHICH IS KIND OF WHAT THE TWO TO THREE THAT['S] EMBEDDED IN FORECAST ASSUMES, OR IS IT GOING TO BE A MAJOR ONE?**"

### 5. Nora Top Calls（00:36:24–00:37:14）

- **Roblox**：Jefferies 从持有下调至跑输大盘——7 月以来 +30% 后"投资者可能过于兴奋"，新算法（优先长期留存）或拖累短期用户增长；
- **First Solar**：KeyBank 从低配上调至标配——回调后估值更有吸引力，但库存高企、项目启动放缓的挑战仍在；
- **Sweetgreen**：Wells Fargo 升至增持、目标价近乎翻倍（$6→$11）——环孢子虫疫情拖累消退、客流回暖，股价创 7 月以来新高。

### 6. Paramount $440 亿发债：媒体整合的"必须发生"（00:43:51–00:46:55）

- 结构（Steven Flynn，00:44:17）："**THEY'RE LAUNCHING DEBT INTO BOTH INVESTMENT GRADE ... AND THE HIGH YIELD BOND MARKET**"——总额约 **$440 亿**支持收购华纳兄弟探索；其中 **$124 亿等值高收益债**（美元+欧元）为史上最大级别高收益交易之一；对照上周 **SoftBank $100 亿三部分美元债**。
- 市况（00:45:04）：年内 IG 美元债发行 **+26%**、高收益 **+14%**——需求强但成本更高；交割下周完成；其后有可观股权资本垫底、但杠杆将高企。
- 定性（00:46:31）："**THE MEDIA INDUSTRY NEEDS TO CONSOLIDATE. THERE['S] TOO MANY PLAYERS ... STREAMING IS WHERE THE GROWTH IS. IT['S] REALLY A DEAL THAT HAS TO HAPPEN.**"

### 7. Michael McKe：数据周、13/19 票委讲话与曲线信号（00:49:01–00:53:31）

- 前瞻（00:49:43）：多数数据关乎就业端而 Fed"not too worried"——除非周四 ISM 制造业就业分项与周五非农大超预期，市场难有大动；
- Fed 讲话（00:50:18）："**WE GET 13 OF THE 19 ... VOTING FED OFFICIALS ON THE OPEN MARKET COMMITTEE SPEAKING THIS WEEK**"——Bowman 谈银行监管为主，Williams/Waller/Collins/Cook 等谈经济，周五 Dallas 的 Lori Logan（曾先反对不动、后随队加息）最受关注；市场已定价**10 月加息**（00:51:07）。
- 关键之问（00:52:03）："**WILL THEY BOTHER TO RAISE RATES 5 DAYS BEFORE A MIDTERM ELECTION?**"——取决于本周 PCE 与 10 月晚些的 CPI/PPI。
- 曲线（00:52:37）：前端领涨使 2s10s 收窄至 **2025 年初以来最小**；Fed 偏爱的 **3 个月–18 个月曲线在走阔**——"**IT DOESN'T LOOK LIKE WE'RE FORECASTING ANY KIND OF RECESSION THROUGH THE YIELD CURVE**"。

### 8. Christina Hooper（Man Group）：警惕"实质性股票抛售"（00:53:38–01:00:29）

- 警报（00:53:40 段引语）："**ON ALERT FOR A QUOTE 'SUBSTANTIAL STOCK SELLOFF'**"（节目预告）；核心："**SOMETHING HAS TO GIVE**"——收益率 >5% 历史上并不异常，异常的是**上行的速度**与**政府债务之高**（00:54:19）。
- 财政（00:55:04）：赤字/GDP 约 **6%**、债务突破 **$40 万亿**里程碑；上周 IIF、OECD、IMF 先后点名美国——"**MORE AND MORE BOND VIGILANTES COMING OUT**"（00:55:21）。
- 机制（00:56:06）：美国经济已成"**financing dependent economy**"——AI capex 日益依赖发债，融资成本上升推高门槛回报率；国债、AI 相关信用债、股票三方争夺资金；"**WE COULD EASILY GET TO 5 1/2% BEFORE YEAR END AND THEN WE COULD PROBABLY DRAW SOME INVESTORS OVER**"〔字幕作"5 12%"，按口径修正为 5½%——标注〕。
- 消费（00:58:30）："**IT IS P-SHAPED WHEN WE THINK ABOUT NET WORTH**"——顶层家庭握有绝大部分财富、消费韧性极强，但正因如此，**股票抛售（财富效应逆转）才是消费的最大风险**；供给冲击型通胀下加息效力有限——"**THAT'S WHERE STAGFLATION RISK INCREASES**"（00:59:58）；"**AI CAPEX AND CONSUMER SPENDING, BOTH ARE QUITE VULNERABLE**"（01:00:11）。

### 9. Mark Champion（Bloomberg Opinion）：伊朗僵局与柴油禁令的全球回声（01:02:21–01:09:26）

- 现状（01:03:36）：伊朗方案被否后本周谈判续开，"**WE'VE BEEN HERE MANY TIMES BEFORE ... BOTH SIDES SHOWED NO REAL WILLINGNESS TO COMPROMISE**"。
- 谁占上风（01:04:38）："**YOU'D HAVE TO SAY IT['S] THE US**"——美海军已能护航油轮通行、同时封锁伊朗出口，"**THAT IS NOT THE SITUATION THAT EXISTED SOME WEEKS AGO**"；伊朗要么回到桌前、要么升级以重夺海峡地位。
- 升级工具箱（01:05:30）：代理人再袭 East-West 管道、打击海湾能源基础设施（修复周期远长于油轮遇袭）、"扩大战争地理范围"（伊朗将领近期言论）、远至拉美/欧洲的恐怖手段。
- 中国变量（01:07:04）：习特会后特朗普施压北京停止支持伊朗（零部件、购油、可能情报）——"**WE DON'T KNOW ... WHAT THE CHINESE HAVE ACTUALLY AGREED TO DO, IF ANYTHING**"。
- 柴油禁令（01:08:06）：欧洲高度紧张——英国尤其脆弱、或现抢购；"**ONE POSSIBILITY IS THAT THEY'RE TRYING TO PRESSURE THE EUROPEANS INTO LEANING ON PRESIDENT ZELENSKIY ... TO STOP TARGETING RUSSIAN REFINERIES**"（01:09:06）。

### 10. Rich Steinmeier（LPL Financial CEO）：AI 不取代"人的建议"（01:10:45–01:18:20）

- 背景压力（01:11:12）：Muse 发布当日 LPL 股价曾单日 -7%——"**WHAT IS YOUR PUSH BACK TO THIS IDEA THAT WE COULD SEE FINANCIAL ADVICE BECOME COMMODITIZED?**"
- 核心答（01:11:23）："**WHEN YOU GET TO BIG LIFE EVENTS, THE BIG CHALLENGES, THE BIG QUESTIONS ... YOU NEED TO HAVE SOMEONE THAT YOU TRUST AT THE MIDDLE OF A RELATIONSHIP**"（举家阿尔茨海默照护实例）；"**IT'S ABOUT RELATIONSHIPS, TRUST, CONTEXT, EMPATHY ... WE FEEL BULLISH ABOUT THE HUMAN ADVICE**"。
- 分工（01:13:05）："**60% OF THE WORK THAT ADVISERS DO IS NOT CLIENT-FACING**"——让机器人做后台（开户、再平衡、准备/收尾），顾问做前台判断；"human in the loop"防"AI 味"侵蚀信任（01:13:57）。
- 工具（01:14:59）：LPL 同样与 **Anthropic（Claude）** 合作、数据置于自有安全环境——对照 Anthropic 与 Schwab 的财务顾问工具合作（01:14:48 提及）。
- 并购潮（01:15:52）：史上最大 Commonbwealth 收购之后——"**VANGUARD BUYING ALTRUIST, CARLYLE AND BAIN REPORTEDLY BIDDING FOR WEALTH ENHANCEMENT GROUP, $7 BILLION ... I DON'T THINK WE'RE AT THE FINAL STAGE**"〔"Carlile and Bane"拼写口径失真〕；最低可行规模持续上移。
- 财富转移（01:17:34）：代际传承与小企业主接班是顾问网络的下一战场。

### 11. Ryan Vastelica：英伟达回购的市场读法与"Meta 引力中心"（01:19:43–01:23:45）

- 回购（01:20:04）："**THE RECEPTION ... HAS BEEN PRETTY POSITIVE**"——高利润、高现金流；比"循环融资"式的对外投资"clean-cut"得多；估值处"AI 时代以来相对自身历史的低位"。
- 安全（01:21:01）："**WE ARE ALWAYS HEARING ABOUT NEW HACKS, NEW BREACHES**"；当最坏叙事已是"Bill Gates 说的十亿人死亡"级别，单一工具难完全安抚（01:21:26）。
- Meta（01:22:04）："**META IS NOW SORT OF THE CENTER OF GRAVITY IN THE MARKET ... SO MANY DIFFERENT SECTORS MOVING ON THIS PRODUCT**"——进企业软件让人想起年初"SaaS 末日"讨论；**Salesforce、Workday、Datadog、ServiceNow 全线下跌**；Meta 本身也在跌（收益率+自身消息）。
- MongoDB（01:22:33）：CEO 突然离职+明日投资者日活动——"**A CEO CHANGE WAS NOT ON THE LIST**"；有人视之为买入机会；"**YOU JUST CAN'T ENFORCE NON-COMPETES THESE DAYS**"——人才战争远未结束。

### 12. Kaylee Lines：中美"30 换 30"关税互减 + 伊朗谈判僵局（01:24:13–01:27:42）

- 协议（01:24:29）："**THIS IS A 30-FOR-30 DEAL ... APPLYING TO $60 BILLION WORTH OF GOODS IN TOTAL**"——由 5 月特朗普访京时设立的 Board of Trade 谈成；美方清单 **77 类中国产品**（玩具、日用品等），中方清单 **约 1,600 项**（小麦等农产品、煤炭、医疗设备）；中国商务部称约 **90% 商品将适用最惠国待遇**。
- 体量（01:25:26）："**$60 BILLION ... COVERS A FRACTION OF THE MORE THAN $400 BILLION WORTH OF GOODS THAT WERE TRADED BETWEEN THE US AND CHINA LAST YEAR**"——休战延长至**一月**。
- 伊朗（01:25:51）：联合国大会边缘的美伊纽约会谈中，伊朗提出**约 7 天内重开霍尔木兹**的方案遭特朗普拒绝——"**IRAN, AT LEAST ACCORDING TO AN INTERVIEW HE GAVE AXIOS, AS OVERPLAYING ITS HAND**"；伊朗总统在 UNGA 演讲：封锁与制裁不除、不放行自由通航；特朗普多次表态**中期选举（六周后）前不会有协议**。

### 13. Nikki Shields（MKS PAMP）：金价单日 -4% 与"弱手换强手"（01:27:46–01:32:05）

- 当日（01:29:00）："**GOLD IS FALLING SOME 4% THIS MORNING. IT'S HAVING A REALLY BAD DAY**"——中东紧张→能源成本高企→Fed 加息押注升温→实际利率上行。
- 短期逆风（01:28:24）："**OIL PROBING 110 ... THE MARKET PRICING IN BASICALLY 100 BASIS POINTS OF FED HIKES OVER THE NEXT YEAR WHICH — IT'S AN EXTREMELY TOUGH ENVIRONMENT FOR GOLD**"。
- 结构多头（01:28:16）：货币贬值/去美元化/多元化主题不变——"**ETF INFLOWS COMING INTO THE MARKET AGAIN AS THE YIELD CURVE INVERTS**"、央行持续分散法币敞口。
- 央行与中国的 1,000 吨（01:30:17）："**A THOUSAND TONS OF IMPORTS INTO CHINA. A LOT OF THAT IS THE PBOC BUT IT['S] JEWELERS, FUNDS, INSTITUTIONAL ... VERY LITTLE CONFIDENCE IN LOCAL ASSETS**"；央行"在今日这类陡峭回撤中仍会是买方"。
- 零售（01:31:04）：Q1"贬值交易"Google 搜索峰值后，零售兴趣已转向 AI/科技——"**I THINK IT'S HEALTHIER. IT'S A HEALTHIER TWO-WAY MARKET**"；金价正与实际利率/短端利率重新高度相关；中国黄金周+本周 NFP/通胀数据=高事件风险。

### 14. Nora Movers 收尾与全天行情读数（01:18:25 起、00:46:57、01:09:47）

- 三条个股（01:18:36）：**贵金属矿下跌**（金银价格走低：中东紧张→能源成本高→加息押注升）；**Snowflake $35 亿可转债**（部分用于偿还 2027 年到期可转债，股价 -3% 下方）；**MongoDB CEO CJ Desai 即时卸任赴 Meta**、前 CEO Dev Ittyeria（字幕"Dev Editeria"）暂行执掌——**股价 -20%+**。
- 指数（全天多时点）：标普 **-0.4%→-0.5%**（开盘即跌）；纳指 **-0.5%→-0.75%→-1%**；罗素 2000 跑输；**10Y 5.2151（+5bp 以上，2007 年以来最高）**、**30Y 2004 年以来最高**；Brent +2%（盘中高 $107）。
- 板块（00:35:39）：**能源是当天唯一绿色板块**；**材料最弱**（金银下跌）、其后依次为**可选消费、通信服务**——个股层面 Microsoft/Meta 下跌、MongoDB 因 CEO 出走"crater"。

---

## 二、与当日行情和板块相关的要点

- **指数（盘中多时点）**：
  - 标普 500：开盘约 -0.5%，全时段 -0.4%~-0.5%（"breadth decisively to the downside"）；
  - 纳指：-0.5% → -0.75% → -1%（长久期科技受收益率压制最重）；罗素 2000 同样跑输；
  - 背景上周：**收益率连涨四周后、股市上周反弹超 1% 收官**（Christina 段引述"Stocks ended the week higher by more than 1%"，00:53:49）。
- **利率**：
  - **10Y 5.2151**（+5~7bp，2007 年以来最高）；**30Y 2004 年以来最高**；2Y 前端 5bp+ 上行——"THE SAME NARRATIVE THAT WE ENDED THE WEEK WITH: OIL HIGHER, YIELDS HIGHER, THEREFORE STOCKS LOWER"（00:27:12）；
  - 高收益利差走阔、CCC 全年承压（Surveillance 档详述，本档 01:19:33 前后未展开）；Paramount $124 亿 HY 大单与上周 SoftBank $100 亿——供给压制利差（Steven Flynn）。
- **商品**：
  - **Brent +2%、盘中高 $107**（开盘档读数；Surveillance 档早盘曾 +3~4% 至 108）；伊朗外长纽约会调停人（无美方代表）消息一度抹去部分涨幅（01:03:20）；
  - **黄金 -3%~-4%、白银下跌**——实际收益率挤压；中国 1,000 吨年进口与央行买盘为结构支撑；油"probing 110"（Nikki 口径）。
- **汇率**：本档字幕未涉及具体汇率读数（字幕无法确认）。
- **板块（开盘即时图）**：
  - **唯一上涨：能源**（油价 +2%）；
  - **最弱：材料**（金、银与贵金属矿随实际利率跳水）→ **可选消费** → **通信服务**（Meta 拖累）；
  - 科技内部：**英伟达独红**（+2%~+2.5%），Microsoft/Meta/芯片普跌；软件全线走弱（Salesforce/Workday/Datadog/ServiceNow——Meta 企业级平台引发的替代恐慌）。
- **个股 Movers**：
  - **NVDA +2%~+2.5%**：+$1,500 亿回购 → 总额 $2,350 亿（史上最大）；Open Shell/Sentry 安全系统；Anthropic 累计 $1,800 亿硬件承诺；
  - **MDB -20%+**（盘中；收盘档口径 -18%+、3 月 3 日以来最差）：CEO CJ Desai 即时离任执掌 Meta 新企业 AI 平台，前 CEO 回锅；
  - **SpaceX -2% → +1.33%**：发射全程过山车后入轨+26 星部署成功；
  - **SK 海力士 -5%+**（Nora 口径；Surveillance 档早盘 -3.6%）——子公司 Solidigm 或 2027 年 IPO；
  - **Snowflake -3% 下方**：$35 亿可转债（部分偿 2027 年到期可转债）——稀释；
  - **Roblox**（Jefferies 降跑输、7 月来 +30% 后）、**First Solar**（KeyBank 升标配）、**Sweetgreen**（Wells Fargo 升增持、PT $6→$11、创 7 月以来新高）；
  - **Paramount**：$440 亿并购债启动（$124 亿 HY）；
  - **LPL Financial**：CEO 专访（Muse 发布日曾 -7%）。
- **数据与事件日历（本集口播）**：
  - 本周：**JOLTS、周三 PCE、周四 ISM 制造业（含就业分项）、周五非农**；**13/19 位 FOMC 票委讲话**（Bowman/Waller/Williams/Collins/Cook/Logan 等）；市场已定价 **10 月加息**；
  - "加息在中期选举前 5 天落地吗"之问（McKe）；明日（周二）：MongoDB 投资者日活动（CEO 突换后）；OpenAI DevDay、加拿大商品禁令生效（The Close 档预告）；
  - 事件：SpaceX 首次入轨（成功）；习特会后续"30 换 30"关税清单落地；伊朗外长纽约会调停方。
- **当日行情驱动归纳（盘中视角）**：9/28 = **"油-收益率-股指三连锁 + AI 内部分化日"**：
  - 伊朗方案被否 → 油价再涨 → 10Y/30Y 续创 2007/2004 年以来新高 → 股指小幅回落、板块仅能源独绿；
  - **贵金属矿成重灾区**：金 -3~-4% 令材料板块垫底（实际利率的镜像）；
  - AI 阵营裂解：英伟达用史上最大回购对冲"放慢论"；Meta 以挖角 MongoDB CEO 高调进企业级、软件股集体承压；MongoDB -20% 成单日最大牺牲品；
  - SpaceX 入轨成功为"AI+太空 capex"叙事提供当日唯一工程级利好对冲。

---

## 三、主要分歧

1. **收益率上行的定性：良性 vs 病理**：
   - **Lori Calvacina（RBC）**：油价若松动、估值端可得喘息；盈利强到没有"魔法数字"式的临界点；
   - vs **Christina Hooper（Man Group）**：上行速度异常+财政（赤字 6%/$40 万亿）——"something has to give"，警惕实质性股票抛售；
   - vs **Michael McKe（转述 Fed 视角）**：前端引领的收益率上行恰是"长端通胀受控"的信号、曲线不预示衰退。
2. **AI capex 的融资依赖度**：
   - **Tom Leighton（Akamai）**：$40 亿现金在手、利率升 1–2 个点无碍盈利性；
   - vs **Christina Hooper**：经济整体已成"financing dependent"，融资成本上行直接抬高 AI capex 门槛回报率；
   - vs **Nikki Shields**：散户资金从贵金属转向 AI——叙事压力测试才刚开始。
3. **Fed 与中期选举**：
   - **McKe**：13/19 票委齐发声、10 月加息已定价——但"选前 5 天加息"取决于通胀数据；
   - vs **Lori Calvacina**：baby cycle（2–3 次）vs major cycle 之辩仍在；
   - vs **Mark Champion**：政治时钟或逼总统在升级与妥协间二选一。
4. **金融建议会否被 AI 商品化**：
   - **Rich Steinmeier（LPL）**：大事决策需要信任与共情，AI 做后台、人做前台；
   - vs 市场投票：Muse 发布日 LPL -7%——投资者的怀疑写在价格里。
5. **MongoDB 人才地震的读法**：
   - **Ryan Vastelica**：有人视为买入机会、"竞业禁止已无法执行"；
   - vs 盘面：-20% 单日重挫、明日投资者日蒙阴影。
6. **黄金的多空时窗**：
   - **Nikki Shields**：短期极难（油价逼 110、100bp 加息定价），但弱手→强手（央行/ETF）是健康换手；
   - vs 当日盘面：金 -3~-4%、贵金属矿领跌全市场——结构性买盘尚未托底日内价格。
7. **柴油禁令与欧洲**：
   - **Mark Champion**：欧洲（尤其英国）将现短缺与抢购，甚至可能是施压欧洲劝泽连斯基停打俄炼厂的筹码；
   - vs Surveillance 档 CSIS：禁令反噬美国国内价格——两个大洲各自买单。
8. **信用大单供给是好是坏**：
   - **Steven Flynn（Bloomberg Intelligence）**：Paramount $440 亿是"必须发生的交易"、需求端年内 IG +26%/HY +14% 证明胃口仍在；
   - vs **Christina Hooper**：国债、AI 信用债、股票三方争钱——融资依赖型经济的裂缝正在此处最先显现；
   - vs Surveillance 档 Goldman：走阔是"供给消化"而非信用事件——三方对同一利差读数给出三种温度计。
9. **媒体整合的杠杆容忍度**：
   - **Flynn**："significant equity capital behind"——债券持有人乐见厚股本垫底；
   - vs 本档主持追问："DOESN'T THIS JUST INCREASE THE STAKES ... CONSIDERING HOW MUCH LEVERAGE THEY'RE PUTTING ON FROM DAY ONE?"——生而高杠杆的并购在 5%+ 利率世界的容错率之问。

---

## 四、个股与 ETF 汇总表

| 代码/名称 | 方向 | 幅度（字幕原始口径） | 原因/引语 |
|---|---|---|---|
| 标普 500 | 下 | **-0.4%~-0.5%（全天）** | 油价+收益率双升；宽度单边向下 |
| 纳指 | 下 | **-0.5%→-0.75%→-1%** | 长久期科技承压；罗素 2000 同步跑输 |
| 10Y/30Y 收益率 | 上 | **10Y 5.2151（+5bp+，2007 年来最高）；30Y 2004 年来最高** | 与上周同一叙事：油高→收益率高→股低 |
| Brent | 上 | **+2%、盘中高 $107**（另档口径 +3~4% 至 108） | 特朗普否决伊朗 7 天重开方案；外长会调停人略降温 |
| 黄金/贵金属矿 | 下 | **金 -3%~-4%；矿企板块领跌** | 实际利率上行；油价逼 110；市场定价未来一年约 100bp 加息 |
| NVDA（英伟达） | 上 | **+2%~+2.5%** | +$1,500 亿回购→总额 $2,350 亿史上最大；AI 代理安全系统；Anthropic $1,800 亿承诺 |
| MDB（MongoDB） | 下 | **盘中 -20%+（收盘档 -18%+）** | CEO CJ Desai 即时卸任赴 Meta 执掌企业级 AI 平台；前 CEO Dev Ittyeria 回任；明日投资者日 |
| SpaceX | 剧烈波动→上 | **-2%（熄火）→+0.3~0.7%（go for orbit）→+1.33%（入轨+部署）** | Starship 第 14 次试飞首次入轨（275 km×6 圈）、26 颗 Starlink 实星全部署；IPO 价 $135 之上 |
| SK 海力士 ADR | 下 | **-5%+**〔Surveillance 档早盘 -3.6% 并存〕 | 子公司 Solidigm 或 2027 年 IPO——股权与结构之忧 |
| SNOW（Snowflake） | 下 | **-3% 下方** | $35 亿可转债（部分偿 2027 年到期券）——稀释 |
| META | 下 | 无具体读数（"也在跌"） | 高收益率+企业级新战线；挖角 MongoDB CEO；软件股替代恐慌（Salesforce/Workday/Datadog/ServiceNow 齐跌） |
| RBLX（Roblox） | 下（评级） | 7 月以来 +30% 后 | Jefferies 降至跑输：新算法拖累短期用户增长 |
| FSLR（First Solar） | 上（评级） | 无幅度 | KeyBank 低配→标配：回调后吸引力回升；库存与项目启动仍为挑战 |
| SG（Sweetgreen） | 上 | PT $6→$11；股价创 7 月以来新高 | Wells Fargo 升增持：环孢子虫阴影消退、客流回暖 |
| PSKY/WBD（Paramount 并购债） | 事件 | **$440 亿总盘子、$124 亿 HY（美元+欧元）** | 收购华纳兄弟探索；下周交割；对照上周 SoftBank $100 亿三部分美元债 |
| LPLA（LPL Financial） | 事件 | Muse 发布日曾单日 -7% | CEO：AI 增强而非取代顾问；与 Anthropic/Claude 合作；并购潮未到终局（Vanguard-Altruist、Carlyle/Bain-$70 亿 Wealth Enhancement 传闻） |
| Akamai | 事件 | 无当日幅度 | $120 亿/7 年 Anthropic CPU 协议；年内累计长期承诺 $144 亿、满产年化 $22 亿收入；$40 亿现金 |
| 中美贸易（宏观） | 事件 | **$600 亿双边、休战延至 1 月** | 30 换 30：77 类/1,600 项清单；90% 最惠国待遇（中方口径） |

---

## 五、转写失真备查与其他值得记录的细节

- **转写失真备查（本集）**：
  - "DANNY BER/DANNY BERGER"＝主持人 Danny Berger；"MATT MILLER STILL OUT ON PATERNITY LEAVE"＝常态搭档缺席原因；
  - "ED LEDLLO/LLLO"＝Bloomberg Tech 主持 Ed Ludlow；"NOR MELINDA/NORINDA/NORA"＝记者 Nora（Melinda，姓氏拼写反复）；
  - "SETH FIGERMAN"＝Bloomberg Tech 编辑（按字幕，拼写疑失真）；"RYAN VASTELICA/VISTELLA"＝Bloomberg 科技记者（拼写失真）；
  - "MICHAEL MCKE"＝Bloomberg 经济记者（按字幕）；"KAYLEE LINES"＝Balance of Power 联合主持（按字幕）；
  - "LORI CALVACINA"＝RBC 资本市场美股策略主管（按字幕）；"BLAKE WIN"＝其利率策略师（拼写疑失真）；"STEVEN FLYNN"＝Bloomberg Intelligence 信用分析师（按字幕）；
  - "CHRISTINA HOOPER ... MAN GRIEVE"＝Man Group 首席市场策略师（机构名口径失真）；"MARK CHAMPION"＝Bloomberg Opinion 专栏作家（按字幕）；
  - "RICH STEINMEIER/STEINMEER"＝LPL Financial CEO（按字幕，拼写反复）；"CARLILE AND BANE"＝Carlyle 与 Bain（拼写失真）；"COMMONBWEALTH"＝Commonwealth（LPL 收购标的）；
  - "NIKKI SHIELDS ... MKS PAMP/MKS S PAMP"＝MKS PAMP 研究主管（按字幕）；"DEV EDITERIA"＝MongoDB 前 CEO（Dev Ittyeria——拼写口径失真）；"CJ DESAI"＝MongoDB 即将离任 CEO（按字幕）；
  - "AI WILL SUPPLY ANTHROPIC WITH CPUS"＝Akamai（"AI"为 Akamai 之误写）；"OKAMI/AAMI/AKAMI"＝Akamai（多处失真）；
  - "SOLID DIME/SOLID"＝Solidigm（SK 海力士美国子公司）；"SKH HIGHIX/SK HEINIX/SKH"＝SK Hynix（多处失真）；
  - "5 12%"＝5½%（Christina Hooper 年末 10Y 目标——按上下文口径修正并标注）；"5.2151"＝5.2151%（10Y 读数连写）；"610/7/10EN OF 1%"＝0.6~0.7% 连读失真；
  - "MICKEY/MIKE"＝Michael McKe（00:50:15 处人称混用）；"ANTHROPIC ANTHROPIC"＝重复连写；"STARLING SATELLITES"＝Starlink（口误型失真）；
  - "10-YEAR YIELD ... CALLED 5 A HALF"＝口播含混（上下文为 5.2% 一档——标注）。
- **字幕无法确认项**：Nora/Nor Melinda 的标准全名；Seth Figerman、Ryan Vastelica 的标准拼写；Steven Flynn 全名；"Solidigm IPO 估值"（本档未提金额，Surveillance 档作 $1,000 亿——两档口径不一）；Meta 当日具体跌幅读数（本档仅"下跌"）。
- **数据花絮（本集全部读数索引）**：
  - 股：标普 -0.4~-0.5%、纳指 -0.5→-1%、罗素跑输；能源唯一绿板块、材料/可选消费/通信服务居末；NVDA +2~2.5%、MDB -20%+、SpaceX -2%→+1.33%、SK 海力士 -5%+、SNOW -3% 下方、Sweetgreen 创 7 月新高；
  - 债：10Y 5.2151（2007 高）、30Y（2004 高）；IG 发行 +26% YTD、HY +14% YTD；Paramount $440 亿/$124 亿 HY；SoftBank 上周 $100 亿；
  - 商品：Brent +2%（高 $107）、油"probing 110"、金 -3~-4%、中国年进口黄金 1,000 吨；
  - 宏观：非农前值/预期（本档未展开——Surveillance 档 +9 万/16.2 万/4.1%）；10 月加息已定价；13/19 票委讲话；2s10s 至 2025 年初以来最窄、3mo–18mo 走阔；赤字 6% GDP、债务 $40 万亿；中美 $600 亿清单（77/1,600 项、90% MFN、休战至 1 月）；
  - AI/公司：NVDA $150B/$235B 回购、Anthropic $180 亿→英伟达承诺（本档口径 $1,800 亿）；Akamai $120 亿/7 年、$144 亿累计、$22 亿/年满产、$40 亿现金、700 城/4,000 PoP/10–20MW；LPL"60% 顾问工作非面向客户"；Gates"十亿人死亡"级叙事（转述）；
  - SpaceX：第 14 次试飞、6 台 Raptor 一台早熄、275 km、9h50m/6 圈、26 星、IPO $135、Falcon 9 停单 2029 初、全球载荷份额 80%+。
- **轻松一刻**：Ed Ludlow 的"PEZ 糖果"卫星部署比喻与"我看到他们在鼓掌，也许是因为还能把它推进轨道"；Danny 的"Braco——他们是化学品公司，我不够聪明看不懂他们的生意，但人家在纽交所上市 40 周年"（NYSE 敲钟段）；主持人对"发射刚成功股票还跌"的错愕；"你不能再去执行竞业禁止条款了"的人才战争吐槽。
- **与前后档口衔接**：
  - 承接同日 **Surveillance**（02:27 收束交棒）——油价/收益率/非农周一贯，本档新增：Akamai CEO 首访、Paramount 发债、Man Group 抛售警报、LPL CEO、贵金属聚焦、中美关税清单细节；
  - 交给同日 **The Close**（收盘口径）：标普收 -0.8%、MongoDB 收 -18%+（盘中 -20%+ 的收敛）、Meta 两日 -8%、板块仅必需消费/医疗/能源三绿——与开盘档"能源独绿"相比，收盘前防御性板块补位；
  - 明日预告（本档 01:32:08）：Gabriela Santos（JPMAM）、前 SEC 主席 Gary Gensler（字幕"Gendler"——口径失真）、Meredith Whitney、Lightseed CEO。

---

## 六、SpaceX Starship 首次入轨时间线（本档独有直播线）

- **[00:00:29]** 开播即切直播画面：Starship 已升空，"你正在看实时画面"；
- **[00:01:20]** Ed Ludlow：飞船段 6 台 Raptor 中**1 台提前熄火**——"将无法尝试进入轨道高度"，股价盘前 **-1.3%**；
- **[00:02:55]** "火箭科学"现实版：SpaceX 原文"ON THE WAY UPHILL"（上行途中）；对照第 13 次试飞（Test 13）周四夜首试在归零前 hold、股价盘后跳水的先例；
- **[00:03:33]** 商业版图再梳理：Falcon 9（现役主力、全球载荷 80%+）→ Starship（未来：Starlink 星座、**轨道数据中心**、NASA 登月、火星）；S1 招股书明示 Starship="**single point of failure**"；
- **[00:04:24]** IPO 发行价 **$135**，"still above that, but dropping precipitously"——盘前 **-1.8%**；
- **[00:06:46]** 轨道算力之问："卫星形态的数据中心"载荷部署方式与 Starlink 相同（PEZ 式滑出）；时间表"明年"、上市前内部认为公司前瞻偏保守；
- **[00:08:20]** 最新头条："**SPACE X CONSIDERING STARSHIP ORBIT ATTEMPT AFTER ENGINE WENT OUT**"——是否补做单引擎入轨点火仍在评估；原计划第 25 分钟执行；
- **[00:12:09]** 定音："**SPACE X GO FOR ORBIT. STARSHIP WILL SOON PERFORM A BURN WITH A SINGLE RAPTOR ENGINE TO ENTER A 275 KM ORBIT OF EARTH**"——股价转涨（盘前 +0.3%）；
- **[00:14:27]** 任务参数复述：275 km、约 10 小时（9h50m）绕地六圈、离轨溅落智利以西、海上不尝试回收——"可复用"前提是先能回得来；
- **[00:24:58]** 快讯：**Starship 已入轨**——"FIRST SHARES WERE FALLING. THAT FLIPS NOW UP [0.6–0.7]% WITH THIS MILESTONE PASSED"；同时开始部署 Starlink 卫星；
- **[00:37:39]** Ed 确认（第 14 次试飞）：**达到约 275 km 轨道高度**、正在部署 26 颗实星；"IT MATTERS THAT THEY'RE MAKING PROGRESS AND THE STOCK RESPONDING ACCORDINGLY"；
- **[00:47:55]** 终章："**ALL 26 SATELLITES ON STARSHIP ROCKET HAVE BEEN DEPLOYED INTO ORBIT**"——股价 **+1.33%**（自晨间 -2% 低点全程反转）；
- 本档未及（收盘后）：溅落结果与再入数据——字幕无法确认。

---

## 七、本集未展开但同日其他档口覆盖的事项（交叉索引）

- **波音 737 Max 10 认证延迟（-6~7%）**：The Close Stock of the Hour + Closing Bell Movers；
- **Kodiak Sciences +177%**：Closing Bell/The Close（医疗保健板块收绿的引擎）；
- **Palo Alto Networks +4.6%（BTIG 升 PT）**：Closing Bell/The Close（网络安全当日第一赢家）；
- **AMD $82 亿全股票收购 World Labs（盘后）**：The Close（Ed Ludlow 专访 Lisa Su/李飞飞）；
- **收盘指数全读数与板块三绿**：The Close/Closing Bell（标普 -0.8%、必需消费/医疗/能源独绿）；
- **住宅建筑商 -8%**：The Close 收盘后段；
- **MongoDB 收 -18%+（较盘中 -20%+ 收敛）与 $61 亿市值蒸发**：The Close/Closing Bell；
- **10Y 绝对水平读数**：本档为 5.2151，Surveillance 档 5.20–5.23 并列——收盘档未再复述（The Close 仅 +7bp 变动口径）；
- **Morningstar 耐克 $94 公允价值、25 年低点**：The Close（周四盘后财报前瞻）。

---

## 八、嘉宾观点速览表

| 嘉宾（字幕口径） | 机构/身份 | 核心观点（一句话） | 关键数字 |
|---|---|---|---|
| Ed Ludlow | Bloomberg Tech 主持 | Starship 是 SpaceX"单一故障点"——入轨即商业叙事兑现 | 275 km/6 圈/26 星；IPO $135 |
| Tom Leighton | Akamai 联合创始人/CEO | 分布式小节点（10–20MW）模式避开社区抵制与审批陷阱；AI 安全=护栏+网防两侧 | $120 亿/7 年协议；年内承诺 $144 亿；满产 $22 亿/年 |
| Lori Calvacina | RBC 美股策略主管 | 没有魔法数字——强盈利对冲高收益率，但"余地在耗尽" | 目标 8,150；压力测试 5.25% 仍平盘；情绪信号 +15% |
| Steven Flynn | Bloomberg Intelligence 信用分析师 | Paramount 大单是"必须发生的媒体整合"，需求端足以消化 | $440 亿/$124 亿 HY；IG +26%/HY +14% YTD |
| Michael McKe | Bloomberg 经济记者 | 13/19 票委齐发声；曲线不预示衰退；关键在"选前 5 天敢否加息" | 10 月加息已定价；2s10s 至 2025 年来最窄 |
| Christina Hooper | Man Group 首席市场策略师 | "总得有什么让步"——收益率速度+财政是异常项，滞胀风险显著 | 赤字 6% GDP；$40 万亿债务；年末或见 5½% |
| Mark Champion | Bloomberg Opinion | 美国握上风；伊朗要么回桌要么升级；柴油禁令是欧洲的噩梦 | 升级路径：管道/海湾设施/地理外扩 |
| Rich Steinmeier | LPL Financial CEO | AI 做后台、人做前台——"human in the loop"是信任的护城河 | 顾问 60% 工作非面向客户；并购潮未到终局 |
| Ryan Vastelica | Bloomberg 科技记者 | 英伟达回购比"循环融资"干净；Meta 成市场引力中心 | MongoDB 盘中 -20%+；软件股集体承压 |
| Kaylee Lines | Balance of Power 联合主持 | "30 换 30"只是 $4,000 亿贸易的小切口；休战延至 1 月 | $600 亿/77 类 vs 1,600 项；90% MFN |
| Nikki Shields | MKS PAMP 研究主管 | 短期极难（100bp 加息定价）、结构多头（央行/ETF 换手） | 金 -3~-4%；中国年进口 1,000 吨 |
