# Bloomberg Surveillance 节目内部研究（2026-09-29 周二）

## 元信息

| 项目 | 内容 |
|---|---|
| 本地字幕绝对路径 | `E:\Skill\finviz-us-sector-rotation - Zcode\finviz-us-sector-rotation-v0.2\script\bloomberg surveillance-2026-09-29.txt` |
| 字幕 SHA-256 | `9d50d096af3be07b14c982fc7de8ffd01201c92d29ab9fab108997d1116ba00f`（python hashlib 本地计算，完整 64 位十六进制） |
| 节目日期 | 2026-09-29（周二）——**周一（9/28）股债双杀后的第二个交易日晨间档**。盘前定调："Coming into Tuesday on Shaky Ground"——AI 交易仍在为股指"隔热"，但收益率处数十年高位（**2Y 4.90–4.94、10Y 5.20–5.22（2007 年以来最高区）、30Y 5.53–5.55（2004 年以来最高）、3 年期以上全线 ≥5%**）；Brent 自 ~$105 回落至 ~$103；**Anthropic 招股书泄露（Reuters）：自曝"灾难性或生存性风险"、未来数年计划支出 $5,180 亿**；Oura 推迟 IPO；**总统今午白宫宴请 AI 巨头（监管议题）**；今日 6 位联储官员讲话 + JOLTS/消费者信心开局数据周（周三 PCE〔新算法〕、周四初请、周五非农） |
| 节目名称与主持人 | Bloomberg Surveillance（晨间 3 小时档，纽约）。**Jonathan Ferro**（字幕作"JONATHAN PHARAOH"）、**Lisa Abramowicz**（"LISA ABRAMOWITZ"）、**Annmarie Hordern**（"AN MARIE HORDERN"）三人主持；Bloomberg Brief 由 **Vonnie Quinn** 负责；华盛顿记者 **Tyler Kendall**、**Andrew Curren**（字幕作"ANDER CURRAN"）；盘前 Movers 由 **Yahaira** 负责（字幕拼写作 Yahara/Yhara/Yara/Johanna/Yahhira——姓氏字幕未给出） |
| 字幕全文读取状态 | 已完整读取：全文 4,389 个换行行（wc -l 计 4,389 个换行符，行尾 CRLF、末行带尾换行），Read 分 3 段读至 EOF：1–1500、1500–2999、3000–末行 [02:24:00] 'This was Bloomberg surveillance.'，无遗漏、无明显时段空档 |
| 时长/结构 | 00:00:05–02:24:00（约 144 分钟，3 小时）。嘉宾出场序：开场三人组（Anthropic 招股书/白宫 AI 午宴/Oura 推迟 IPO/六位联储讲话）→ **Ed Yardeni（Yardeni Research）**（"债券义勇军算法"、5.5% vs 6%）→ Vonnie Brief（高盛接班/英国恐袭嫌犯保释/Oura）→ **Tyler Kendall**（伊朗：中期选举前无协议的基准情形）→ **Tobin Marcus（Wolfe Research）**（"war/worse/deficits/data"四因子、柴油出口禁令 skepticism）→ 盘前 Movers（Yahaira：Summit/FICO/Navitas）→ **Dan Ives（Wedbush，字幕"YORK FOR LIVES"）**（Anthropic IPO：第三次局、$4–5 万亿资本开支）→ Vonnie Brief（中国 AI 人才出境限制/Shein 财报）→ **Anders Persson（字幕"ANDIS PERSON OF NEW"——机构名口径失真，疑为 Nordea，标注）**（core PCE 见顶回 3%、perfect storm、久期转中性）→ **Eric Johnston（字幕"ERIC JOHNSON OF CANCER"——疑为 Cantor，标注）**（实际收益率 2.9%、银行股=科技颠覆）→ Vonnie Brief（加拿大禁令生效/RTX $207 亿合同）→ **Joyce Chang（J.P. Morgan 全球研究主席）**（中期选举被低估、AI 监管是 2028 议题）→ **Jill Carey Hall（BofA）**（小盘质量+价值、S&P 年底 7,400）→ **Karen Manna（Federated Hermes，字幕多作 CARAMANA/KAREN MANAB——拼写无法确认）**（前端为王、EM 优于 DM 主权）→ **Mona Mahajan（Edward Jones）**（AI 基建成熟、下一阶段是普及）→ Morning Calls + **Jonathan Krinsky（BTIG）**（2000 年式宽度背离、公用事业 RSI<22）→ **Andrew Curren**（数据周前瞻：周五非农预期 +9 万、失业率 4.1%、10 月加息概率 >70%）→ **Greg Daco（EY Parthenon，字幕"EY PATHON"）**（12 月再加息一次、供给冲击悖论、Target 降价）→ **Blake Gwinn（RBC，字幕多作 BLAKE QUINN/W）**（对收益率"建设性看多"、cathartic puke 未现）→ 交易日历收尾 |

> 说明：字幕为机器转写，存在拼写失真（人名/机构名/数字）。本文为内部研究文件，仅使用该字幕文件内容；无法确认处一律标注"字幕无法确认"或"口径失真"，不做外部补充。当日客观背景（任务给定）仅用于对照：周二能源商品大跌、公用事业领涨、工业与半导体偏强、必需消费与金融偏弱、AMD 收购 World Labs 后首个交易日、本周 PCE+美光+非农连测——本档字幕对 ETF 层面细节多数未覆盖（见第二节末尾对照）。

---

## 一、主要主题与核心内容

### 1. 开场：Anthropic 招股书泄露、白宫 AI 午宴与 IPO 窗口收窄（三人组，00:00:19–00:05:14）

- 定调（00:00:19）："**COMING INTO TUESDAY ON SHAKY GROUND, THE AI TRADE HELPING TO INSULATE EQUITIES FROM BOND YIELDS AT MULTI-DECADE HIGHS AS THE PRESIDENT IS CONVENING TECH LEADERS WITH REGULATION TOP OF MIND.**"
- Anthropic 招股书（00:00:44）：Reuters 报道其警告自研技术"**POSES THE RISK OF CATASTROPHIC ... OR EXISTENTIAL RISKS TO HUMANITY**"；同时计划未来数年支出"**$518 BILLION IN CLOUD COMPUTING AND INFRASTRUCTURE APPLICATIONS**"（00:01:02）。
- 结构性反差（00:01:21）：261 页主体中约 **80 页**为风险因素——"**NEARLY TWICE THE 48 PAGES IT ACTUALLY USED TO DESCRIBE ITS BUSINESS**"；主持人调侃："**IF YOU CAN'T STOP THE PROSPECTUS FROM LEAKING, HOW CAN YOU SELF-REGULATE?**"（00:01:42）。
- 午宴阵容之争（00:01:52）：OpenAI/Anthropic 领导层 vs Jensen 黄的立场——"**THIS IS AN ISSUE OF YOU GUYS NOT HAVING RESPONSIBLE BUSINESS MODELS**"；OpenAI 曾因安全顾虑推迟部分先进模型（00:02:07）。
- IPO 窗口（00:02:20）：OpenAI IPO 推迟到明年"**MAYBE EVEN LONGER**"；**Oura（字幕作 ORA/OURORA/MORORA——智能戒指商）宣布推迟 IPO**，理由是市场不确定性——"**THIS IS NOT THE IPO WINDOW THE BANKERS WERE HOPING FOR COMING INTO FALL**"（00:02:31）；银行家们此前的管线"**AS FULL AS THEY HAVE EVER SEEN IT**"（00:02:39）；主持人猜测这"**MAY BE WHAT THE FEDERAL RESERVE IS TRYING TO ACCOMPLISH**"——给牛市去沫（00:02:46）。Oura 今年收入增长 **90%**（00:07:53）。
- 联储讲话日（00:03:06）：今日六位官员——Bowman 开场、Governor Barr（字幕"GOVERNOR BAR"）、Goolsbee（"AUSTIN GBY"）、**Williams 下午 2 点**、**Waller 下午 3 点**；Bob Michele（JPM，字幕"BOB MICHAEL"）昨日称 Williams 是当下最重要的讲话人——"**WHERE ARE THE DOVES? THERE IS NO DOVISH MODERATING VOICE ON THE FOMC**"（00:03:57）。
- 数据周（00:04:10）：今日 JOLTS（10 点）+消费者信心；本周 ADP、初请；**周三 PCE**（"核心 PC 是关键"）、**周五非农**；中期选举前数周（00:04:25）。
- 农业带与柴油（00:04:30）：Axios 头版——共和党策略师称"**FARM COUNTRY IS STRUGGLING**"，爱荷华或翻转；政府仍在辩论**柴油出口禁令**——"**THE ISSUE IS UNDERNEATH THE SURFACE ... IT'S IN THE PRODUCT**"（00:04:52）。

### 2. Ed Yardeni：债券义勇军的复仇——算法放大器（00:05:14–00:12:00）

- 引言（00:05:19）："**WE SUSPECT THAT THE BOND MARKET HAS BEEN HACKED BY BOND VIGILANTE ALGORITHMS. THEY RESPOND TO NEWS HEADLINES WITH HUGE TRADES THAT EXACERBATE VOLATILITY.**"
- 我们已在负反馈循环中（00:05:41）："**WE AREN'T ON THE BRINK OF IT. WE'RE SORT OF IN THE MIDST OF IT.**"——年初以来（或始于去年）全球收益率同步上行；**日本央行加息 → 全球套息交易平仓**是"膝跳式机械因素"（00:06:00）；算法再把任何新闻放大。
- 自限机制（00:06:31）：观察"**BOND YIELDS GOING UP LESS THAN SHORT-TERM RATES**"——2 年期是全球央行的领先指标，目前"**THE TWO-YEAR TREASURIES IN ALL THE MAJOR COUNTRIES ARE POINTING TOWARDS MORE TIGHTENING**"（00:07:16）；9 月 15 日他已转向"谨慎"（"PROCEED WITH CAUTION"，00:07:29）。
- AI 侧的应力（00:08:07）：盯 **Oracle/Stargate**（与 OpenAI、SoftBank 合计承诺 **$5,000 亿**）——其中一座数据中心因**新墨西哥州否决 19 英里天然气管道**而显著推迟（00:08:26）——"**THERE'S STARTING TO BE SOME STRESSES IN THE AI TRADE AS WELL**"。
- 债券 5.25% 有吸引力但未必是顶（00:09:12）："**BONDS YIELDING 5.25% ARE VERY ATTRACTIVE ... IT DOESN'T FEEL LIKE THIS IS NECESSARILY THE PEAK**"；Jim Bianco（字幕"JIM BIANO"）昨日转多——"**5.2% IS GOING TO COMPENSATE HIM**"（01:29:32 复述）。
- 义勇军复仇论（00:10:06）："**THIS MIGHT BE THE REVENGE OF THE BOND VIGILANTE[S] ... THEY WERE SUPPRESSED FROM THE GREAT FINANCIAL CRISIS TO THE GREAT VIRUS CRISIS WITH QE AND ZERO INTEREST RATES ... YOU ACCUMULATED ALL THAT DEBT AT NEAR ZERO INTEREST RATES BACK THEN. NOW YOU'RE GOING TO HAVE TO REFINANCE IT AT THESE YIELDS.**"
- 高度（00:10:44）："**MORE AND MORE PEOPLE ARE THINKING ABOUT GETTING CLOSER TO 6%. I WOULD SAY 5.5%. I'M NOT GETTING INTO THE ALARM STAGE ... WE ARE GOING TO FIND LOTS OF BUYERS**"——2023 年 5% 时拍卖转好、收益率因通胀回落而下行的先例；但这次**中东**不同：油价 higher-for-longer → 通胀更粘 → 央行非"一次完事"而是收紧模式（00:11:19）。**澳大利亚隔夜再加息**（00:11:57）。
- 中国例外（00:12:13）：中国国债收益率年初以来反而更低——**PBOC 将为首购家庭补贴房贷利息**（00:12:21）；中国是**通缩螺旋**、居民不愿消费、5% GDP 目标难以达成的另一类问题（00:12:35）。

### 3. Vonnie Brief 一：高盛接班与 Oura（00:13:10–00:14:09）

- **高盛**：董事会正安排 **COO John Waldron 接替 David Solomon**，WSJ 称最早明年、或 27 年底/28 年，Solomon 转任执行主席（00:13:32）。
- **英国**：Trump 批评英国对 RAF 基地涉伊恐袭案五名嫌犯保释释放（现场未发现可用爆炸物）（00:13:12）。
- **Oura**：推迟上市；公司自称盈利且IPO 过程开始以来"进一步强化"，"**WE AIM TO DELIVER AN EXTRAORDINARY IPO ... WE HAVE THE LUXURY OF CHOOSING OUR MOMENT**"（00:13:53）。

### 4. 伊朗-美国：中期选举前的"无协议"基准（Tyler Kendall + Tobin Marcus，00:16:25–00:24:03）

- Trump 剪辑（00:16:28）："**IRAN WILL NEVER HAVE A NUCLEAR WEAPON. WE'RE GOING TO WIN THAT WAR VERY SOON ... AS SOON AS THAT WAR ENDS, INFLATION'S GOING TO BE ERADICATED TOTALLY.**"
- Tyler Kendall（00:17:01）：伊朗官员私下对协议**悲观**，上周 UGA 间隙几乎无进展；白宫要求**重开霍尔木兹海峡的坚定承诺+核让步**；伊朗外长留在纽约、隔夜未晤卡塔尔调解人；伊方"**STRONGLY DENY ... ANY FLEXIBILITY REGARDING NUCLEAR**"；伊朗要求**解除其港口军事封锁**（美方视为不可谈）+金融救济；Trump 否认 Axios 的"放松制裁换协议"报道（00:18:12）；**财长 Bessent：伊朗待交付原油仅剩约 1,500 万桶、出口即将枯竭**（00:18:07）；伊朗 awaiting 美方对最新提议的最终答复（00:18:24）。
- **Tobin Marcus（Wolfe Research）**（00:18:29）：基准情形"**NO DEAL BEFORE THE MIDTERMS**"（00:18:31）——双方红线与**协议概念/结构本身**都有巨大分歧，"**DETERIORATION RELATIVE TO WHERE WE WERE IN MAY AND JUNE**"（00:19:23）。
- 轰炸重启威胁（00:19:29）："**A FAIRLY EMPTY THREAT**"——美军**防空拦截弹库存耗损**、基地存活率、区域能源资产保护构成硬约束；军方的谨慎意见正在传导（00:19:37）。
- 柴油出口禁令（00:20:22）：Axios 引爱荷华共和党竞选顾问"**IN IOWA WE SHOULD BRACE FOR LOSING EVERYTHING**"；Tobin 判断**不会推出**——Cruz 参议员获白宫保证、能源部长 Wright 称"**IT WOULDN'T EVEN HELP**"（00:21:24）。
- 可负担性排序（00:21:43）：**房贷利率是可负担危机中最显著的单项**——"**BUYING A HOME IS THIS VERY CORE ASPIRATIONAL IDEA ... IT LOOKS REALLY FAR OUT OF REACH**"；历史上**解放日关税退让与 6 月对伊谈判推进都被收益率触发**（5 月中 10Y 冲 4.66——"A PRACTICALLY QUAINT LEVEL AT THIS POINT"）（00:22:07）。
- 四因子（00:22:28，主持人复述）："**WAR, WORSE, DEFICITS, AND DATA**"〔"worse"疑为转写失真，按字幕保留〕——**赤字无解**："**DEFICIT PROJECTIONS ARE STUCK IN THE 6% OF GDP RANGE**"，国会明年任何动作大概率增赤（国防、医保）；**CBO 假设的债务平均利息成本终值 3.9%——而当前整条曲线都高于此**（00:23:24）。
- 政治注脚（00:23:43）：Trump 当选三支柱——通胀、移民、"反 woke 1.0"；移民已兑现、通胀被战争拖累。

### 5. 盘面与宽度：指数近高点下的"鸭子市场"（00:24:33–00:27:36）

- 数据与 PMI 之辩（00:24:51）：上周 S&P 综合 PMI 为**五年最快**——"**ARE YOU SUGGESTING THE S&P PMI IS TO THE ISM WHAT ADP IS TO PAYROLLS?**"（笑谈，00:25:16）；本周 ISM 制造业将验证。
- Mike Wilson（Morgan Stanley，转述 00:25:49）："**EQUITY MARKETS AREN'T MADE FROM TEFLON. THEY ARE READJUSTING. THE EQUITY MARKET IS NOT COMPLACENT AROUND THE RISK.**"——**Russell 3000 中逾 50% 个股自 6 月以来回撤 ≥20%**；**S&P 估值回到约 19 倍、接近 3 月低点**；**Russell 2000 9 月至今 -4.5%**（00:26:11）；**公用事业、地产、工业**等周期板块被打压（00:26:16）；银行入财报季表现不佳（00:26:33）。
- Kevin Gordon（Schwab 系，字幕未给机构，00:02:54 段）："**THE LAST TIME THE PERCENTAGE OF THE S&P 500 MEMBERS ABOVE THEIR 200-DAY MOVING AVERAGE WAS THIS LOW, THE S&P WAS DOWN IN CORRECTION TERRITORY. TODAY, THE INDEX IS BARELY OFF ITS HIGH**"——他称之为"**COMBATIVE DUCK MARKET**"（划水的鸭子）（00:02:55）。
- 商品（00:26:41）：**East-West 管道（沙特）产能利用率升至 50%**；WSJ/Kpler 报道**更多原油正在通过霍尔木兹海峡**（封锁仍屏蔽伊朗出口）；但外交停滞——"**NO DEAL IN SIGHT HEADING INTO THE MIDTERMS**"。

### 6. 盘前 Movers：Summit、FICO、Navitas（Yahaira，00:27:36–00:28:56）

- **Summit Therapeutics**：盘前飙涨 **20%+**——**AstraZeneca（字幕"ASTROENICA"）投资 $20 亿**、共同开发其在研抗癌药；行业正面临**专利到期潮**前寻找新增长（00:27:38）。
- **Fair Isaac（FICO）**：大跌 **13%+**——房市监管者（FHFA，字幕"BILL PY"）宣布 **VantageScore 将与 FICO 并入 Fannie Mae/Freddie Mac 抵押定价网格**，FICO 在抵押市场的长期垄断承压、或降低部分新发放房贷费用（00:28:03）。
- **Navitas（字幕"NVITAS/NVIDITA"——拼写无法确认）**：盘前涨近 **12%**——赢得**美军下一代国防功率芯片合同**；合同金额与时限未披露，"**A MASSIVE POP FOR A DEAL WE KNOW VERY LITTLE ABOUT**"（00:28:33）。

### 7. AI 议程：招股书、撤回模型与白宫午宴（00:29:00–00:31:27）

- 三条雷达（00:29:00）：**Anthropic IPO 估值近 $2 万亿**、招股书自曝生存风险；**OpenAI 撤回最新 Astra 模型版本**并暂停最强版本训练——"**AFTER ROGUE AGENTS BREACH GOVERNMENT WEBSITES IN THE US AND AUSTRALIA**"（00:29:21）；**Trump 今日宴请科技巨头**（Politico：黄仁勋、扎克伯格、Dario Amodei 出席）（00:29:28）。
- 自递归恐惧（00:29:55）："**THE IDEA THAT AI SYSTEMS CAN IMPROVE UPON THEMSELVES ... CREATE SOMETHING THAT CANNOT BE UNPLUGGED**"；议长 Johnson："**THEY DON'T WANT A MORATORIUM. THEY WANT TO MAKE SURE THEY WIN THIS RACE AGAINST CHINA**"（00:30:22）；总统日程表上写的是"**SUPER INTELLIGENCE MEETING**"——Lisa 建议改名"**AMERICAN INTELLIGENCE**"（00:31:21，玩笑）。

### 8. Dan Ives（Wedbush，字幕"YORK FOR LIVES"）：第三次局、$4–5 万亿（00:31:31–00:37:30）

- 客户集中度不是问题（00:31:58）：GPU 与超大规模客户注定集中，"**WE'RE STILL THIRD INNING OF THE AI REVOLUTION**"；Anthropic IPO 是"**A WATERSHED EVENT FOR THE TECH SECTOR AND THE MARKET**"（00:31:41）。
- 生存风险条款（00:32:40）："**IS THAT A SALES PITCH OR A WARNING? ... A HEADSCRATCHER ... TO SATURDAY NIGHT LIVE SKIT**"；核心逻辑："**IF THEY SLOW DOWN, CHINA WINS. THE GENIE'S ALREADY OUT THE BOTTLE**"（00:32:57）；"**YOU CAN'T GET TO THE TOP FLOOR AND THEN PULL THE LADDER UP**"——监管捕获亦是问题（00:33:11）。
- 中美位势（00:33:59）："**FOR THE FIRST TIME IN 30 YEARS, THE US IS AHEAD OF CHINA WHEN IT COMES TO TECH**"；焦点应是**主权 AI 与企业数据控制**（00:34:18）。
- 支出量级（00:35:16）："**WE'RE GOING TO HAVE CALL IT FOUR TO FIVE TRILLION BEING SPENT IN THE NEXT THREE TO FOUR YEARS. BUT YOU'RE BUILDING THE VEGAS STRIP IN 1955**"——投资者终将追问回报时点；上市带来的**透明度（如 SpaceX）对行业健康**（00:35:46）。
- 午宴动机（00:36:29）：总统要行业统一口径——"**TECH INDUSTRIES CREATED THE PR[] NIGHTMARE THEMSELVES**"；每关停一座数据中心，"**THE WINNER ... IS CHINA**"（00:37:11）。

### 9. Vonnie Brief 二：中国出境限制与 Shein（00:37:55–00:38:46）

- **中国扩大对顶尖 AI 人才出境限制**至私企核心人员**家属**——配偶子女出境需北京批准（00:37:58）。
- Trump 在 Truth Social 否认 Axios 报道："**THIS IS UNTRUE. I OFFERED THEM NOTHING**"（00:38:14）。
- **Shein 港股首份财报后大跌**：**经营利润 -53%、净收入几近持平**，并警示下半年不确定性（00:38:30）。

### 10. Anders Persson（字幕"OF NEW"，疑 Nordea——机构口径失真）：core PCE 见顶、完美风暴（00:40:44–00:47:27）

- 核心观点（00:41:11）：**core PCE 正见顶、年底回落至约 3%**、对消费仅温和拖累；本周**周五非农比 PCE 更关键**——PMI 之后需要确认经济真实强度（00:41:34）；明日 PCE 附带**修正+新算法**（00:41:42）。
- 完美风暴（00:42:31）："**A BIT OF A PERFECT STORM**"——联储加息+会后密集鹰派言论、火热的 PMI、**中东僵局（第一大驱动）**、油价的第一导数传导为**柴油等第二导数**、拍卖担忧、**AI 超大规模发行人供给**——"**A TOXIC KIND OF TYPE MIX**"，趋势仍向上。
- 仓位（00:43:25）：久期**由长期做空转向中性**——"**NOT QUITE COMFORTABLE GOING LONG DURATION YET**"；转而**分散至利差板块**：信用、证券化、**CLO**、市政债与优先股；**杠杆贷款/高级贷款收益率约 9%**、为其偏好资产（00:45:49）。
- 系统性视角（00:44:01）："**PEOPLE HAVE MORE CONFIDENCE IN THE CORPORATE CREDITWORTHINESS OF US COMPANIES THAN THE US GOVERNMENT**"；收益率压力是**全球现象**、财政担忧四处蔓延——这正是难以做多久期的原因（00:44:38）。
- 信用未裂（00:46:21）：利差近几日仅温和走阔，"**WE'RE NOT SEEING CRACKING JUST YET**"；对 Goldman 的 Amanda Lynam"上质量=撞上供给负技术"论，他**部分同意**但更愿下沉：**单 B/双 B 仍具吸引力**（00:47:00）。
- 尾注（00:47:42）：卡塔尔外长称正与美伊"交换信息与可能的方案"——但自 2 月以来调解从未有真正突破；**Brent ~105、WTI ~92**（00:47:56）。

### 11. Eric Johnston（字幕"OF CANCER"，疑 Cantor——机构口径失真）：实际收益率 2.9%、银行的科技颠覆（00:53:03–01:00:06）

- 实际收益率（00:53:19）："**THE REAL YIELD ON THE 30-YEAR RIGHT NOW IS 3.3%. ON THE 10-YEAR IT'S ABOUT 2.9%**"——"**YOU CAN OWN INFLATION PLUS 2.9% FOR 10 YEARS**"对养老金开始有吸引力；但对经济的驱动力已不如从前——超大规模举债者**净债务/净现金仓位很小**，ROI 对融资成本不敏感（00:53:52）。
- 指数之下（00:54:39）：科技大幅跑赢、**其余市场成为资金来源**；**个人 AI 代理**是部分原因——订阅类股票承压。
- 银行定性（00:55:10，主持人问及）："**TECH. TECH DISRUPTION.**"——存款是银行最便宜的资金；若个人代理把支票账户缓冲压到最低、把余额扫入**收益率 3.75% 且上行**的货币基金，廉价存款被侵蚀（00:55:52）；节奏判断："**MORE THE LATTER（慢出血）**"——银行会自我保护并适应（佣金从 $20→$10→$5→免费的历史）（00:56:48、00:57:15）。
- 消费结构（00:57:54）：油价占钱包比例远小于 10–30 年前；高收入消费者（消费主力）**净现金**状态下反而受益于高收益率——"**THE ECONOMY CAN ABSOLUTELY HANDLE THAT**"（00:58:43）。
- 通胀锚（00:58:56）：**柴油创纪录**将渗入核心通胀，但基数有利——"**LAST FOUR MONTHS, CORE CPI MONTH-OVER-MONTH ANNUALIZED HAS BEEN 2.1%. SUPER CORE HAS BEEN 1.7%**"（00:59:12）；对冲项：**关税的同比基数滚落**与需求端（00:59:26）。
- 收尾（01:00:28）：银行自 8 月中高点**近 -10%**——"**IT IS NOT JUST ABOUT EXISTENTIAL RISK. IT'S MORE ABOUT PROFIT RISK DRIVEN BY TECH DISRUPTION**"；10 月 13 日 JPM 财报电话会上"代理会吸走廉价存款吗"将成为必问题（01:00:02）。

### 12. Vonnie Brief 三：加拿大禁令生效与 RTX（01:00:45–01:01:47）

- **美对部分加拿大产品进口禁令今日生效**：摩托车、酒类、乳清制品；Trump 预计加拿大将在 **3–4 周内**下调对美关税并"道歉"（01:00:48）。
- 总统与议长 Mike Johnson 宴请 AI 公司 CEO（Nvidia/Anthropic/OpenAI/Meta）（01:01:04）。
- **五角大楼授予 RTX $207 亿、五年期合同**——将空空导弹产能近翻倍（Raytheon 部门），补充对伊战争消耗的弹药（01:01:26）。

### 13. Joyce Chang（J.P. Morgan）：中期选举是被低估的风险（01:06:44–01:12:00）

- 核心判断（01:07:05）："**THE MIDTERM ELECTIONS ARE UNDERESTIMATED AS A RISK RIGHT NOW**"——三大看点：**可负担性、AI、更高关税+伊朗再升级**；前两者"**IRRESPECTIVE OF THE OUTCOME**"都会持续（01:07:12）。
- 油价的政治经济学（01:07:44）：若加油站的油价停在 **$4.50**，"**YOU WIPE AWAY ALL THE BENEFITS OF THE ONE BIG BEAUTIFUL BILL**"——两党都没赚到经济信任；民调情绪近月明显转变（01:08:03）。
- 出口禁令（01:08:19）："**VERY MUCH ON THE TABLE**"但只管 30 天——随后炼厂压缩等扭曲接踵，"**NOT A POLICY THAT REALLY MAKES MUCH SENSE**"。
- 税项与监管（01:08:59）：个税红利已兑现、企业税优惠分阶段保留；**AI 监管"更像是 2028 年议题"**——本届政府不会有实质动作；公私合营模式"在新兴市场 rarely last"（01:10:04）。
- 增长面（01:10:34）：**科技资本开支明年仍很好**； crunch 点在**明年 8 月财政部上调融资规模**与 2028 大选年；当前是"**ONE OF THE BROADBASED GROWTH RECOVERIES**"——日本、欧洲（1.5%）高于潜在增长、美国亦然、中国做刺激（01:11:24）；"**HIGHER RATES ARE GOING TO STAY HERE, BUT THE HIGHER FISCAL IS ALSO GOING TO STAY HERE**"（01:11:43）。

### 14. Jill Carey Hall（BofA）：小盘的质量与价值、S&P 年底 7,400（01:19:27–01:26:38）

- 背景板（01:19:31）：**Russell 2000 自联储最近一次加息以来下跌、但年内仍 +13%**；上半场 +20%+ 的领涨者多为**AI 基建主题**而非经济敏感制造类（01:20:00）。
- 利率敏感性（01:20:29）：小盘与利率/联储预期的相关性近年显著抬升——**无盈利股占比高**（长端）+ **BofA 经济学家预计还有两次加息**（短端）；小盘**仅约一半债务为长期**（01:21:02）——再融资风险是最大尾部。
- 风格处方（01:21:09）：**质量**（盈利稳定）+**价值**——"**VALUE ... DOES WELL IN PROFITS RECOVERIES, FED HIKING CYCLES, AND MID-CYCLE ENVIRONMENTS（BofA 商业周期指标显示当前为中周期）**"；今春前的微盘/低质量热潮已充分伸展。
- AI 是上行而非风险（01:22:03）：小盘更劳动密集，AI 带来的**利润率上行空间未被定价**；财报电话会提及 AI 的比例仍低于大盘但快速上升（01:23:16）；医疗保健（小盘大板块）是用例富矿（01:22:35）。
- 通胀与能源（01:24:15）：1970 年代先例——小盘在通胀环境中历史上跑赢、利润率反而更有韧性；当前小盘在**能源与资本品**的敞口受益于商品上行 vs 消费受损（01:24:34）；最大成本是**劳动**而非能源（01:25:00）。
- 大盘点位（01:25:28）：**BofA S&P 500 年底目标 7,400**——距周一收盘约 5–6%；理由：季节性弱期+回调逾期（**5% 回调年均 3 次、10% 年均 1 次**）、利率/通胀/联储风险、流动性更差（回购更少、发行更多）（01:25:36）；"**THE EQUAL WEIGHTED S&P 500 [HAS] MORE UPSIDE THAN THE CAP WEIGHTED INDEX**"（01:26:13）；等权至今 **-4.5%**（01:26:22）。

### 15. Karen Manna（Federated Hermes，拼写无法确认）：前端为王、EM 优于 DM（01:30:11–01:35:03）

- 2022 创伤（01:30:43）："**YOUR STARTING POINT ON YIELDS IS A REALLY GOOD INDICATOR OF WHERE YOU'LL END UP FROM A TOTAL RETURN PERSPECTIVE**"——但 2022 的体验让投资者裹足。
- 处方（01:31:20）："**LEAN INTO MORE KNOWNS THAN UNKNOWNS AND BUY THE FRONT END OF THE CURVE. PROTECT THE PRINCIPAL, GET A LITTLE BIT OF INCOME**"；能忍受波动者可开始进入**以 10 年期国债为核心的核心固收**（公司债+EM 债+选择性 MBS）（01:32:08）。
- EM 偏好（01:32:56）："**WOULD YOU RATHER BUY EMERGING MARKETS DEBT THAN DEVELOPED MARKET SOVEREIGN DEBT?——YES**"；EM 三分法：developed/developing/continuing emerging；**韩国是起点**——区分油出口/进口国、看外资与政治支持广度（01:33:41）。
- DM 的 EM 化（01:34:17）："**BY YIELDS AT TIMES ... AND BY DEBT LEVELS**"——美国债务水平爬升后很难走出来；"**NEITHER SIDE REALLY HAS THE WILL RIGHT NOW TO CORRECT THE DEBT SITUATION**"（01:34:48）。
- 花絮（01:35:33）：Liz Truss 在 X 上频繁晒收益率对比——主持人：人数不多但"我确实同情 Liz Truss"。

### 16. Mona Mahajan（Edward Jones）：AI 基建成熟、下一阶段是普及（01:41:24–01:47:41）

- 速度与水平（01:41:46）："**IT'S NOT ONLY THE LEVEL OF YIELDS, IT'S THE SPEED ... THE 10-YEAR YIELD HAS RISEN 50 BASIS POINTS [IN A MONTH]**"——破坏不发生在指数层面，而在**小盘、金融、公用事业等债券代理**（01:42:09）。
- 周期减速情景（01:42:36）：未来 6–12 个月可能出现**温和周期性放缓**（自强势起点）；高现金流、强资产负债表公司继续受益。
- 盈利权重（01:43:17）：下一季度 S&P 盈利增速 **28%、全年 30%+**——"**NOT LEVELS WE HAVE SEEN HISTORICALLY UNLESS EMERGING FROM A DOWNTURN**"；估值已收缩 10–15%；明年盈利增速 10–15%（01:43:58）；"**YEAR FOUR OF DOUBLE-DIGIT S&P 500 RETURNS**"（01:44:32）——盈利持平估值即可再造 10–15% 涨幅；**尚无 2022 式全面熊市条件**（衰退或激进加息）（01:46:00）。
- AI 换挡（01:46:35）："**THE INFRASTRUCTURE PART OF AI HAS MATURED ... WHAT WE WOULD REALLY WANT TO SEE IS THE NEXT PHASE, WHICH IS AI ADOPTION**"——医疗、工业、金融的**生产力兑现**尚未体现；等待"**HANDOFF**"（01:47:22）。

### 17. Morning Calls + Jonathan Krinsky（BTIG）：2000 年式宽度背离（01:49:35–01:59:08）

- Morning Calls（01:51:35）：**德银升 Netflix 至买入**（估值具吸引力入场点）；**瑞穗下调沃尔玛目标价**（AI 改变购物习惯之潜在影响）；**TD Cowen 首予 SpaceX 买入**（"massive AI opportunity over the long term"，该名字盘前 +1%）。
- 两项 2000 年以来未见（01:52:33）："**10 STRAIGHT DAYS WITH MORE 52-WEEK LOWS THAN 52-WEEK HIGHS IN THE S&P WITH THE INDEX ITSELF WITHIN 2% OF A 52-WEEK HIGH. THAT HASN'T HAPPENED SINCE 2000**"；以及"**LESS THAN 50% OF THE S&P ABOVE THE 200-DAY MOVING AVERAGE** [WITH THE MARKET NEAR HIGHS]——NOT SINCE THE 1990–2000 PERIOD"（01:52:53）。
- 1998/2000 类比（01:53:25）：1998 信号出现在 20% 回撤之后、不可比；真正可比的是**1999 底–2000 初**——纳指见顶时**等权 S&P 已自高点回落 15–20% 并率先见底**，随后宽度全年改善而指数下行——"**WE COULD HAVE A MINI VERSION OF THAT**"（中东若解局、油与收益率回落利好宽度但不利好 AI/科技）（01:54:06）。
- AI 交易解剖（01:54:42）：**SOX 自高点 -15%、中位半导体个股 -30%**、仅少数回到 52 周高；资金回流 **Mag 7/超大规模**；Oracle（非 Mag 7）挣扎——"**WE STILL THINK THE AI TRADE IS VULNERABLE AND HAS ANOTHER LEG LOWER**"（01:55:20）。
- 公用事业战术机会（01:55:31）：上周四公用事业 **RSI<22**——2003 年以来仅 10 次，**10 日后全部上涨、平均约 +7%**；与国债的看涨背离："**TREASURIES MOVED LOWER SINCE LAST THURSDAY BY ABOUT A PERCENT WHEREAS UTILITIES HAVE NOT**"（01:56:39）；年内同日定律：**公用事业年内顶部与 10Y 收益率年内底部同为 2 月 27 日——战争开始前一天**（01:59:14，主持人补充）。
- 结构 vs 战术（01:56:10）："**STRUCTURALLY, WE STILL THINK YIELDS ARE GOING HIGHER. THEY JUST BROKE OUT OF A THREE-YEAR TRADING RANGE ... THAT PROBABLY SUGGESTS A MOVE UP TOWARDS THE 6% [LEVEL] FOR THE 10-YEAR OVER TIME**"；战术上情绪已极差、仓位拉伸。
- 政治催化（01:57:51）：**蓝营横扫概率上升 = AI 交易逆风**（数据中心反弹的民意压力）；**Anthropic 巨型 IPO = 潜在供给冲击**（基金需卖其他 AI 筹码腾仓）（01:58:39）。

### 18. Andrew Curren + Greg Daco（EY Parthenon）：数据周与"12 月再加息"（02:00:23–02:13:27）

- Andrew Curren（02:03:11）：活动面稳健——**明日 8 月实际消费支出料为年内最强单月**；**周五非农预期 +9 万左右、失业率维持 4.1% 低位**（02:03:48）；PMI"**LESS OF AN OUTLIER**"；六位官员讲话的主旋律：**不担心就业与经济、只盯通胀**（02:04:05）。
- PCE 新算法（02:04:40）：明日 PCE 为联储偏好的通胀计——**同比口径将显示改善，但核心环比约 0.3%"probably not where the Fed wants it to be"**。
- 定价（02:05:49）：**10 月加息概率 >70%**——"**THE BAR IS PRETTY HIGH TO NOT HIKE**"；下一份 CPI 在 **10 月 14 日**（02:06:18）。
- Greg Daco（02:06:23）：**预计联储 12 月再加息一次**；紧缩对**供给冲击**无效——当下是"**SUPPLY SHOCKS LAYING ONE ON TOP OF THE OTHER**"+ AI 投资潮对**弹性极低的资源集合**施压（02:06:42）；AI 既 是需求冲击也是（未来的）供给冲击——**生产力红利的通缩目前只是"希望"**，采用成本反而在上升（02:07:10）。
- 央行沟通学（02:08:44）：需要"**ACTIVIST**"的央行——多讲情景与反应函数、沟通更多而非更少；"**IT NEED NOT MEAN BEING HAWKISH FOR THE SAKE OF BEING HAWKISH**"。
- Aura 之问（02:08:53）：主持人质疑——IPO 推迟难道不正是收紧在"**TAKING SOME FROTH OUT OF THE MARKET**"的证据？Daco：加息本身不至、但**整条曲线抬高=资本成本持续高企**（02:09:03）。
- 悖论（02:09:51）："**WE'RE IN THIS PARADOX WHERE YES THE ECONOMY IS SHOWING SIGNS OF BEING ROBUST BUT AT THE SAME TIME RECESSION RISKS AND DOWNTURN RISK ARE ACTUALLY RISING, NOT FALLING.**"
- CarMax 解读（02:10:02）：最利率敏感的汽车板块——**信用卡与汽车拖欠率开始上行**（02:10:34）；买车"前几年只还利息"的负担结构（02:10:57）；"**THAT ON TOP OF 7% MORTGAGES**"（02:11:06）。
- 零售价格战（02:11:57）：**Target 对约 2,000 种商品降价**（家居与服装）——"**THEY'RE JUST NOT THE KIND OF HEADLINES YOU'D READ IF THE CONSUMER PRICE TOLERANCE WAS HIGH**"；沃尔玛同步、**Lindt 下调圣诞巧克力价格**（02:12:35）；对照**迪士尼凭定价权提价**——"lazy subscriptions"插科打诨（02:12:50）。

### 19. Blake Gwinn（RBC，字幕多作 QUINN）：建设性看多收益率、"cathartic puke"未现（02:15:22–02:23:39）

- 引言（02:17:33）："**WE'RE CONSTRUCTIVE ON YIELDS AT THESE LEVELS, BUT LIKE EVERYONE ELSE, IT'S VERY SCARY TO GET LONG UNTIL THE BLEEDING STOPS.**"
- 失序的定义（02:17:50）：**挤仓+止损连锁**才算失序——本轮**欧洲比美国更剧烈**（美国是被拖着走）；**互换利差等压力信号缺席**；收益率上行与**油价高度同步**（02:18:18）。
- 欧美之别（02:19:06）：欧洲此前堆积了大量**正利差仓位**，美国从未有同等规模——"**THERE WASN'T AS MUCH MATERIAL TO BE PUKING**"（02:22:00，名句）；上周五/本周初美国开始出现些许止损压力。
- 赤字怀疑论（02:19:22）："**I'M GENERALLY A SELLER OF THE DEFICIT CONCERNS**"——3 月以来收益率 = **全球政策预期重定价 + 油价**；若真是财政担忧，**互换利差（尤其长端）应显著走低——但没有**；财政赤字大的预期"已伴随我们多年"，长端利率对利息负担的影响要到 **8–10 年后**才显现（02:20:25）。
- 联储 7 月 vs 9 月（02:20:52）：最大区别就是**伊朗与油价**——7 月时油价远期曲线仍预期解局，9 月已消失、油价回上 $100。
- 什么能让利率下来（02:21:36）："**IT IS A RESOLUTION IN IRAN. IT'S OIL PRICES COMING BACK DOWN OR SOMETHING TO HAPPEN TO THE AI STORY. BUT CAN WE REALLY COUNT ON EITHER ... IN THE NEXT MONTH OR TWO? NOT REALLY.**"
- 仓位伤痕（02:22:20）：抄底者已被割两三次——"**WHEN YOU CATCH A FALLING KNIFE THREE TIMES, YOU NO LONGER WANT TO PUT YOUR HAND OUT**"（主持人）；Blake："**AT TIMES IT'S FELT LIKE A FALLING CHAINSAW**"（02:23:39）。
- 前端（02:22:56）：**2Y 与政策利率之间利差舒适**——需要很大冲击才能让联储超出曲线已定价的幅度；但冲击可能来自"**DIESEL PRICES GOING MUCH HIGHER AND THE ECONOMY NOT ROLLING OVER**"（02:23:07）。

### 20. 交易日历收尾（02:14:49–02:23:56）

- 10:00 JOLTS；11:00 起联储讲话（Barr 等）；下午 Williams、Waller；**明日 PCE + ISM 制造业 + 美光（盘后）**；周四初请；**周五非农**（02:16:35）；下周财报表：**10 月 13 日 JPM 开局**（01:48:09）。
- 明日嘉宾预告（02:23:49）：BofA 的 Francisco Blanch、Alpine 的 Sarah Hunt（字幕"ALPINE SAX AND WOODS"——机构口径失真）、Barclays 的 Alex Goldman（"BARKCLAY"）、Wolfe 的 Stephanie Roth。

---

## 二、与当日行情和板块相关的要点

- **指数（盘前期货口径，本档为晨间节目）**：
  - **S&P 500 期货**：开盘持平 → +0.1% → +0.15% → +0.2%（第三小时）；**纳指期货 +0.15% → +0.4% → +0.5%**；Russell 持平（00:25:33、01:12:47、01:28:48、02:14:49）；
  - **背景板（周一收盘，转述）**：昨日 broad-based losses、等权 S&P **连跌六周**、标普距历史高点**约 2%** 以内（00:39:42、00:15:44、01:12:52）；
  - 宽度结构：**Russell 3000 逾 50% 成分自 6 月回撤 ≥20%**（Mike Wilson 口径）；**<50% 成分高于 200 日均线**（Krinsky/Gordon 口径）；**10 个交易日 52 周新低多于新高**（2000 年以来首次）；S&P 估值 ~19x、近 3 月低点；
  - 风格与市值：**Russell 2000 9 月 -4.5%、自 8 月中高点银行 -10%、自上月中小盘 -8%**；等权 YTD -4.5%；价值 YTD +22% vs 成长 +6%（Gabriella Santos 口径为同日 OI 档，本档未现——字幕无法确认，标注）。
- **利率（晨间读数）**：
  - **10Y：5.20–5.22**（盘中 -1~-3bp；2007 年以来最高区）；**2Y：4.90–4.94**；**30Y：5.53–5.55，2004 年以来最高**；**3 年期以上全线 ≥5%**（00:15:29、00:40:02、01:13:19、01:28:54、02:16:01）；
  - 月度变幅：**本月 2Y/10Y 各 +约 50bp**；实际收益率 **30Y 3.3%、10Y 2.9%**（Eric Johnston）；
  - 定价：**10 月加息概率 >70%**（Andrew Curren）；市场此前定价"再加息四次"预期（01:16:19，"THE FED POTENTIALLY HIJKING FOUR MORE TIMES"——字幕原文如此）；BofA 经济学家预计还有两次（Jill）；
  - 曲线：**陡峭化**——与"再加息四次+走平"的共识预期相反（02:16:19）；
  - 观点谱系：Yardeni 5.5%（买家会出现）vs Krinsky 结构性 6% vs Bianco 5.2% 补偿已够（转多）vs Karen Manna 只买前端。
- **商品**：
  - **Brent：105 → 104 → 103（-0.25% → -0.6% → -1%+）**；**WTI：92 → 91（守住 90 关口）**；驱动：**East-West 管道利用率 50%**、Kpler 显示更多油通过海峡、但外交僵局（00:16:16、00:26:41、00:48:44、01:37:21）；
  - **柴油创纪录价格**——渗入核心通胀的"第二导数"（Anders Persson/Eric Johnston/Ed Yardeni 多位引用）；加油站 **$4.50/加仑**是政治阈值（Joyce Chang）；伊利诺伊中部 **$4.59/加仑**（同日 OI 档 Mike McKee 口径，本档未现——字幕无法确认）；
  - 中东：Bessent 称伊朗待交付原油仅 ~1,500 万桶；Trump 称"海峡近两日石油流出量史上最高"（同日 The Close 档口径，本档未现——字幕无法确认）。
- **汇率**：本档字幕未涉及具体汇率读数（字幕无法确认）。
- **板块（晨间讨论口径）**：
  - 9 月以来被打压：**公用事业、房地产、工业**（00:26:16）；**金融/银行：自 8 月中 -10%**（00:51:51）——Eric Johnston 定性为**科技颠覆（存款被代理吸走）而非周期走弱**；
  - 公用事业：**上周四 RSI<22**（2003 年以来第 10 次、其后 10 日平均 +7%）——战术反弹候选（Krinsky）；
  - AI/半导体：SOX 自高点 -15%、中位个股 -30%（Krinsky）；Mag 7/超大规模为资金避风港；
  - 小盘：利率敏感 + 无盈利占比 + 半数债务为浮动/短端（Jill）；
  - 等权 S&P：六周连跌后 YTD -4.5%——BofA 认为比市值加权更具上行（Jill）。
- **个股 Movers（盘前）**：
  - **SMMT（Summit Therapeutics）+18%~+20%+**：AstraZeneca 投资 $20 亿、共同开发在研抗癌药；
  - **FICO（Fair Isaac）-13% → -22%**：FHFA 负责人宣布 VantageScore 并入 Fannie/Freddie 抵押定价网格——垄断溢价遭削（同日收盘档口径最终 -27~28%）；
  - **Navitas（字幕口径）+12%**：美军下一代功率芯片合同（金额未披露）；
  - **KMX（CarMax）+7.5%/+5%**：同店销售 +13%（预期两倍以上）、终结四连跌、YTD 已涨 45%；但公司称**依赖降价**引流（00:15:02、02:01:35）；
  - **Wyndham 酒店（字幕"WINDHAM"）+2.3%**：回购追加 $4 亿（01:15:41）；
  - **Jefferies -1.75%**：资管收入腰斩（First Brands/Radiant World 拖累）、固收疲弱，投行与股票交易创纪录（02:01:35）；
  - **Shein（港股）**：经营利润 -53%（Vonnie Brief）；
  - **Netflix**：德银升至买入；**Walmart**：瑞穗降目标价；**SpaceX**：TD Cowen 首予买入、+1%；
  - **RTX**：$207 亿五年期导弹合同（五角大楼）；
  - **Goldman Sachs**：Waldron 接班 Solomon 最早明年（WSJ；Solomon 64 岁、Waldron 57 岁）；
  - **Oracle**：Stargate $5,000 亿承诺下、新墨西哥管道被否致数据中心推迟（Yardeni 关注点）。
- **数据与事件日历（本集口播）**：
  - 今日：**JOLTS（10am）+消费者信心**；6 位联储讲话（Barr、Goolsbee、Williams 2pm、Waller 3pm、Bowman 等）；**白宫 AI 午宴 + america.gov 发布**（Tyler Kendall 段）；
  - 明日：**PCE（新算法+修正）+ ISM 制造业 + 美光盘后财报**；
  - 周四：初请；**周五：非农（预期 +9 万左右、失业率 4.1%）**；
  - 后续：**10 月 14 日 CPI**；**10 月 13 日 JPM 财报开局**；
  - 政策/地缘：**加拿大禁令今日生效**（摩托车/酒类/乳清）；柴油出口禁令辩论未死；中期选举 **35 天**（字幕口径；同日 The Close 档 Tim Adams 称 39 天——口径冲突，标注）。
- **当日行情驱动归纳（晨间视角）**：9/29 晨间 = **"收益率高位喘息 + AI 叙事自我审视"** 日：
  - 长端连涨后的第一次小幅回落（10Y -1~-3bp）叠加油价回落（Brent -1%+）——期货微涨、纳指领涨；
  - 债市多头在"5.2% 已够补偿"（Bianco）与"结构上 6%"（Krinsky）之间拉锯；**互换利差无压力**成为"非财政危机"的主要证据（Blake Gwinn）；
  - AI 阵营进入**治理时刻**：Anthropic 招股书自曝生存风险 + OpenAI 撤回 Astra + 白宫午宴 + 中国限制 AI 人才出境——监管从抽象风险变为当日议程；
  - IPO 窗口实质性收窄（Oura 推迟），但 Anthropic $2 万亿 IPO 仍被银行家视为"**会被追逐**"的例外；
  - 宽度恶化（52 周新低 10 连、<50% 高于 200DMA）与指数近高点的组合，被 Krinsky 定格为 2000 年式背离——**公用事业超卖反弹**与**AI 再下台阶**是其战术配对。
- **字幕未覆盖项对照（当日背景口径仅作参照，本档字幕无法确认）**：WTI 原油期货 ETF 约 -4.4%、天然气 -4.1%、油服 -2.9%、韩国 ETF 约 +1.9%、金矿 ETF 反弹约 +1.5%、公用事业多范围领涨、必需消费与金融偏弱等 **ETF/收盘层面** 读数未在本晨间档字幕出现——本档油价口径为期货（Brent -1%~-2.5% 区间、WTI ~91–92），与背景口径的 ETF 跌幅存在口径差（期货 vs ETF），按各自原始口径保留并标注。

---

## 三、主要分歧

1. **收益率还能走多高**：
   - **Ed Yardeni**：5.5% 为其上限判断、买家将在当前水平涌现（2023 年 5% 先例），"NOT GETTING INTO THE ALARM STAGE"；
   - vs **Jonathan Krinsky（BTIG）**：10Y 突破三年区间后**结构上指向 6%**，只是战术上已拉伸；
   - vs **Jim Bianco（转述）**：5.2% 已足以补偿——技术性回撤即转多；
   - vs **Karen Manna**：不做久期判断，"KNOWN over UNKNOWNS"——只买前端。
2. **赤字是否已是收益率的驱动**：
   - **Tobin Marcus/主持人**：赤字无解（6% of GDP 锁死、CBO 3.9% 利息假设被整条曲线击穿）、负反馈循环或在酝酿；
   - vs **Blake Gwinn**："I'M GENERALLY A SELLER OF THE DEFICIT CONCERNS"——**互换利差无压力**、财政担忧无新信息；3 月以来就是政策预期重定价+油价；
   - vs **Joyce Chang**：财政赤字比科技数字更占空间——但这是**持续性背景**而非当日催化。
3. **经济是"再加速"还是"见顶前的悖论"**：
   - **Andrew Curren/数据面**：PMI 非异常值、消费与就业稳健、非农 +9 万预期；
   - vs **Greg Daco**："**ROBUST BUT RECESSION RISKS RISING**"——资本成本持续高企 + 拖欠率上行；
   - vs **Anders Persson**：core PCE 见顶回落至 3%、信用未裂——周期"可管理"；
   - vs **Eric Johnston**：高收入净现金消费者**受益于**高收益率——消费韧性有微观基础。
4. **银行股 -10% 的定性**：
   - **Eric Johnston**：**科技颠覆**（个人代理侵蚀廉价存款）——慢出血而非挤兑；
   - vs 主持人与多数市场声音（"A LOT OF PEOPLE SAY IT'S THE LATTER [CYCLE]"，01:03:30）——周期性回落；
   - 公共检验点：10 月 13 日开始的银行财报电话会。
5. **AI 监管与"放慢"的代价**：
   - **Dan Ives**：不能慢——"IF THEY SLOW DOWN, CHINA WINS"；午宴应为行业统一口径服务；
   - vs **Anthropic 招股书/OPENAI 撤回 Astra**：把生存风险写进法律文件、以行动示慎；
   - vs **议长 Johnson/白宫**：不要暂停条款、赢下对华竞赛优先——监管 deferred 到 2028（Joyce Chang）。
6. **IPO 窗口的宽窄**：
   - **Anthony Hughes（同日 OI 档）**：窗口只对最大者开——Anthropic 例外、会被追逐；
   - vs **本档主持人**：Oura（收入 +90% 的盈利公司）都要推迟——"这或许正是联储想看到的去沫"；
   - vs **Greg Daco**：推迟是资本成本抬升的开始而非终点——若更多交易回撤将动摇信心。
7. **小盘股的多空**：
   - **Jill Carey Hall**：质量+价值在加息周期与小周期复苏中占优、AI 提供未定价的利润率期权；
   - vs **Krinsky/宽度证据**：无盈利微盘已伸展过度、7 月动量平仓的"AI tantrum"尚未走完；
   - vs **Mona Mahajan**：小盘是利率压力的震中——6–12 个月内或现温和周期放缓。
8. **公用事业反弹的条件**：
   - **Krinsky**：RSI<22 的统计升幅（10 日平均 +7%）+ 与国债的看涨背离——不需要收益率大幅下行也能涨；
   - vs **主持人**：公用事业与国债直接相关——**若国债因"错误原因"（数据恶化）上涨，成长配齐的公用事业未必受益**（01:59:30）。

---

## 四、个股与 ETF 汇总表

| 代码/名称 | 方向 | 幅度（字幕原始口径） | 原因/引语 |
|---|---|---|---|
| S&P 500 期货 | 上（盘前） | **+0.1%→+0.2%** | 收益率/油价小幅回落后的喘息；指数距历史高点 ~2% |
| 纳指期货 | 上（盘前） | **+0.15%→+0.5%** | AI 交易"隔热"延续；半导体盘中偏强（同日其他档） |
| Russell 2000 | 下（9 月） | **9 月 -4.5%；自上月中期 -8%；YTD +13%** | 利率敏感+无盈利占比；半数债务为短端/浮动 |
| 等权 S&P 500 | 下 | **连跌六周；YTD -4.5%** | 宽度恶化；BofA 认为后续上行大于市值加权 |
| 银行股（S&P 上市银行） | 下 | **自 8 月中 -10%** | Eric Johnston：科技颠覆（代理吸存款）而非周期；10/13 JPM 财报为检验 |
| 10Y 收益率 | 高位回落 | **5.20–5.22（-1~-3bp）；2007 年以来最高** | 本月 +50bp；互换利差无压力；10 月加息概率 >70% |
| 2Y / 30Y | 高位 | **2Y 4.90–4.94；30Y 5.53–5.55（2004 年以来最高）** | 3 年以上全线 ≥5%；曲线陡峭化 |
| Brent / WTI | 下 | **Brent 105→103（-1%+）；WTI 92→91** | East-West 管道 50%、海峡过油增加；但无协议僵局 |
| 柴油 | 上（背景） | **创纪录价格** | "第二导数"渗入核心通胀；出口禁令辩论的动因 |
| SMMT（Summit Therapeutics） | 上 | **+18%~+20%+（盘前）** | AstraZeneca 投资 $20 亿共同开发在研抗癌药；专利悬崖前的增长渴求 |
| FICO（Fair Isaac） | 下 | **-13%→-22%（盘前两读数）** | FHFA：VantageScore 并入 Fannie/Freddie 抵押定价网格——垄断被破 |
| Navitas（字幕口径） | 上 | **+12%（盘前）** | 美军下一代功率芯片合同（金额/时限未披露） |
| KMX（CarMax） | 上 | **+7.5%/+5%（盘前）；YTD +45%** | 同店 +13%（超预期两倍）、终结四连跌、重启回购在即；但靠降价引流 |
| Wyndham（字幕"WINDHAM"） | 上 | **+2.3%** | 回购追加 $4 亿——"英伟达 $1,500 亿之后回到地球" |
| JEF（Jefferies） | 下 | **-1.75%（盘前）** | 资管收入腰斩（First Brands/Radiant World）；IB 与股票交易创纪录、固收弱 |
| Shein（港股） | 下 | **经营利润 -53%** | 上市后首份财报：净收入近持平、警示下半年不确定性 |
| NFLX（Netflix） | 事件 | 德银升至**买入** | 估值具吸引力入场点 |
| WMT（沃尔玛） | 事件 | 瑞穗**下调目标价** | AI 改变购物习惯的潜在影响 |
| SpaceX（非上市） | 事件 | **TD Cowen 首予买入**；名字 +1% | "MASSIVE AI OPPORTUNITY OVER THE LONG TERM" |
| ORCL（Oracle） | 关注 | — | Stargate $5,000 亿承诺；新墨西哥气管道被否、数据中心推迟（Yardeni 的"应力"样本） |
| GS（高盛） | 事件 | — | Waldron 接班 Solomon 最早明年（WSJ）；Solomon 转执行主席 |
| RTX | 事件 | — | 五角大楼 $207 亿五年合同、空空导弹产能近翻倍 |
| Oura（未上市） | 事件 | **推迟 IPO** | "WE HAVE THE LUXURY OF CHOOSING OUR MOMENT"；今年收入 +90% |
| Anthropic（未上市） | 事件 | **IPO 估值近 $2 万亿** | 招股书：生存风险 ~80 页 vs 业务 48 页；未来数年支出 $5,180 亿 |
| OpenAI（未上市） | 事件 | **IPO 推迟至明年或更晚** | 撤回 GPT-6.1 Astra、暂停最强模型训练（代理入侵政府网站事件后） |
| Target / Lindt / Disney | 定价权光谱 | — | Target 2,000 种商品降价、Lindt 降价 vs 迪士尼提价——"定价能力"的三个样本 |
| NVDA（英伟达，背景） | 背景 | 昨日 +$1,500 亿回购后 | 本档作参照系（"BACK ON EARTH WITH WINDHAM"）；未给当日读数 |

---

## 五、转写失真备查与其他值得记录的细节

- **转写失真备查（本集）**：
  - "JONATHAN PHARAOH"＝Jonathan Ferro；"LISA ABRAMOWITZ"＝Lisa Abramowicz；"AN MARIE HORDERN"＝Annmarie Hordern；
  - "ED YARDENI/YADENI/YENNI/JADENI OF YARD DENNY RESEARCHERS"＝Ed Yardeni（Yardeni Research）；
  - "TOBIN MARCUS OF WOLF RESEARCH"＝Wolfe Research（按字幕）；
  - "DAN IES OF YORK FOR LIVES"＝Dan Ives（Wedbush Securities——机构名转写严重失真，按字幕标注）；
  - "ANDIS PERSON OF NEW"＝Anders Persson，机构名残缺（疑 Nordea——字幕无法确认）；
  - "ERIC JOHNSON OF CANCER"＝Eric Johnston（疑 Cantor Fitzgerald——字幕无法确认）；
  - "CARAMANA/KAREN MANA/KAREN MANAB OF FEDERATED HERMES"＝Federated Hermes 某策略师（标准拼写无法确认）；
  - "BLAKE QUINN/BLAKE W/BLAKE GWYN OF RBC"＝Blake Gwinn（RBC——本档三处拼写不一）；
  - "GREG ECHO/GREG DEKO/GREG AKO OF EY PATHON"＝Greg Daco（EY Parthenon）；
  - "JILL CARRIE HALL/JOE"＝Jill Carey Hall（BofA——转写两处把 Jill 作 Joe）；
  - "MONA MAHAJAD/MANA MAHAJAN/MANAH EDWARD JONES"＝Mona Mahajan；
  - "JOYCE CHANG OF JP MORGAN, CHAIR OF GLOBAL RESEARCH"＝按字幕；
  - "VONNIE QUINN/BONNIE QUINN/VONYIE"＝Vonnie Quinn（Bloomberg Brief）；
  - "TYLER KENDALL"＝华盛顿记者（按字幕）；"ANDER CURRAN/AND THE KAREN THERE OF BLOOMBERG"＝Andrew Curren（拼写无法确认）；
  - "YAHARA/YHARA/YARA/JOHANNA/YAHHIRA"＝盘前 Movers 记者（姓氏字幕未给出——字幕无法确认）；
  - "GOVERNOR BAR"＝联储理事（姓名残缺——字幕无法确认）；"AUSTIN GBY"＝Austan Goolsbee；"KEVIN WORSH/WARS"＝Kevin Warsh（联储主席，同日 The Close 档另作"WARSH"）；"BOB MICHAEL"＝Bob Michele；"JIM BIANO"＝Jim Bianco；"MICHAEL WILSON AND MORGAN STANLEY"＝Mike Wilson（Morgan Stanley）；
  - "ANDREW HOLLENHORST OF CITY GROUP"＝Citi 的 Andrew Hollenhorst（按字幕）；
  - "KEVIN GORDON"（00:02:54 段）＝策略师（机构字幕未给——字幕无法确认）；
  - "TORSSON SLOCK/TORSTON/TORSON SLO"＝Torsten Sløk（Apollo）——其"AI 银行挤兑"与"供需错配"笔记两度被引用；
  - "AMANDA LYNAMAN"＝Goldman 的 Amanda Lynam（按字幕，拼写存疑）；
  - "ASTROENICA"＝AstraZeneca；"BILL PY"＝FHFA 负责人（姓名拼写无法确认）；"FANNY MAY/FREDDY MACK"＝Fannie Mae/Freddie Mac；
  - "NVITAS/NVIDITA"＝某功率芯片商（疑 Navitas——字幕无法确认）；
  - "ORA/OURORA/MORAURA"＝Oura（智能戒指商）；"SHIEN"＝Shein；"WINDHAM HOTEL"＝Wyndham 酒店（按字幕保留）；
  - "ALPINE SAX AND WOODS"＝Sarah Hunt 所属机构（转写失真——字幕无法确认）；"ALEX GOLDMAN OF BARKCLAY"＝Barclays 某分析师（拼写无法确认）；
  - "SCOTT BESSON"＝Scott Bessent；"SENATOR CRUZ"＝按字幕；"SECRETARY WRIGHT"＝能源部长 Wright；
  - 数字类：'"WAR, WORSE, DEFICITS, AND DATA"'（00:22:28）——"worse"疑为"words"或其他，按字幕保留并标注。
- **字幕无法确认项**：Yahaira 的姓氏；Anders Persson 的机构；Eric Johnston 的机构；Karen Manna 的标准拼写；Governor "Bar" 的全名；Alpine/Barclays 两位明日嘉宾的标准姓名；Navitas 的确切代码；CarMax "重启回购"的时点细节（本档说"in the third quarter"为同日 OI 档口径，本档未给）。
- **数据花絮（本集全部读数索引）**：
  - 债：2Y 4.90–4.94、10Y 5.20–5.22、30Y 5.53–5.55；本月 2s/10s 各 +50bp；实际 30Y 3.3%/10Y 2.9%；杠杆贷款 ~9%；货币基金 ~3.75% 上行；CBO 利息假设 3.9%；5 月中 10Y 4.66；
  - 股：标普距高点 ~2%；Russell 3000 >50% 成分 -20%+；S&P ~19x；Russell 2000 9 月 -4.5%、YTD +13%；银行 -10%；等权 -4.5% YTD；SOX 距高点 -15%、中位半导体 -30%；BofA 目标 7,400（距收盘 5–6%）；公用事业 RSI<22（2003 年来第 10 次、10 日平均 +7%）；
  - 油与地缘：Brent 103–105、WTI 91–92；East-West 管道 50%；伊朗待交付原油 ~1,500 万桶；中期选举 35 天（本档）；
  - 公司/事件：Anthropic $2 万亿估值、$5,180 亿支出计划、招股书 261 页/80 页风险/48 页业务；OpenAI ARR 与 Oura +90%；AstraZeneca–Summit $20 亿；RTX $207 亿；Wyndham +$4 亿；Oracle–Stargate $5,000 亿；McKinsey（同日 OI 档）1,100 万岗位；Target 2,000 种商品；
  - 数据周：非农 +9 万/失业率 4.1%；10 月加息概率 >70%；CPI 10/14；JPM 财报 10/13。
- **轻松一刻**："S&P PMI 之于 ISM，就像 ADP 之于非农"的类比梗；"American Intelligence"改名建议；John Gray 的 LinkedIn 视频与"lazy subscriptions"拉扯；Liz Truss 的"生菜时刻"之辩；"falling knife → falling chainsaw"收官。
- **与前后日衔接**：
  - 承接 9/28（周一）双杀日：本档开场即定调"周二站上摇晃地面"；Bob Michele 剪辑（390→5%→"FIVE-TWENTY-THREE IS A MUCH HAPPIER PLACE"）为 9/28 档回放；
  - 本日新增变量：**Anthropic 招股书泄露、OpenAI 撤回 Astra、白宫 AI 午宴、Oura 推迟 IPO、高盛接班、RTX 大单、Target 降价**；
  - 面向当日盘后与周三：JOLTS/信心（同日 OI 档公布）、PCE 新算法、ISM、**美光财报**——"EARNINGS, EARNINGS, EARNINGS"的检验周开启。

---

## 六、嘉宾观点速览表

| 嘉宾（字幕口径） | 机构/身份 | 核心观点（一句话） | 关键数字 |
|---|---|---|---|
| Ed Yardeni | Yardeni Research | 债市被"义勇军算法"劫持、负反馈已在途中，但 5.5% 附近将有买家 | 10Y 上限 5.5%（市场传 6%）；2Y 为央行领先指标；Oracle–Stargate $500B |
| Tobin Marcus | Wolfe Research | 中期选举前无协议；赤字无解、数据是收益率下行唯一指望 | 赤字 ~6% of GDP；CBO 利息假设 3.9%；中期选举 35 天 |
| Dan Ives | Wedbush（字幕失真） | AI 第三局、Anthropic IPO 是分水岭；慢下来中国就赢 | 3–4 年 $4–5 万亿开支；美国 30 年来首度对华领先 |
| Anders Persson | 机构失真（疑 Nordea） | core PCE 见顶年底回 3%；久期转中性、下沉利差板块 | 本月 +50bp；杠杆贷款 ~9%；单 B/双 B 有吸引力 |
| Eric Johnston | 机构失真（疑 Cantor） | 银行 -10% 是科技颠覆不是周期；实际收益率 2.9% 已吸引养老金 | 货币基金 3.75%+；核心 CPI 近 4 月年化 2.1%、超级核心 1.7% |
| Joyce Chang | J.P. Morgan 全球研究主席 | 中期选举被低估；AI 监管是 2028 议题；高利率+高财政并存 | 加油站 $4.50 抹平 OBBBA 红利；出口禁令只管 30 天 |
| Jill Carey Hall | Bank of America | 小盘买质量与价值；等权比市值加权更优；S&P 年底 7,400 | BofA 再加息两次预期；小盘半数债务为短端；5% 回调年均 3 次 |
| Karen Manna | Federated Hermes（拼写失真） | 前端为王；EM 债优于 DM 主权；DM 正在"EM 化" | 10Y 为核心的核心固收载体；韩国为 EM 起点 |
| Mona Mahajan | Edward Jones | 盈利是唯一引擎（全年 30%+）；AI 从基建换挡到普及的 handoff 是关键 | 估值已缩 10–15%；明年盈利 +10–15%；连续第四年双位数回报 |
| Jonathan Krinsky | BTIG | 2000 年式宽度背离；AI 还有下一台阶、公用事业有战术反弹 | 10 日新低连发；<50% 高于 200DMA；SOX -15%；10Y 结构性看 6% |
| Greg Daco | EY Parthenon（字幕失真） | 12 月再加息一次；紧缩治不了供给冲击；稳健表象下衰退风险在升 | AI 建设占 GDP 2.5%（约为互联网泡沫 2 倍——同日 OI 档 Gensler 口径） |
| Blake Gwinn | RBC（字幕作 Quinn） | 对收益率建设性看多但"血未止不敢做多"；财政担忧被高估 | 互换利差无压力；长端利息影响滞后 8–10 年；抄底被割三次 |
