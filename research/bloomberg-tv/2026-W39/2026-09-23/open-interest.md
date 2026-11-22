# Open Interest 节目内部研究（2026-09-23 周三）

## 元信息

| 项目 | 内容 |
|---|---|
| 本地字幕绝对路径 | `E:\Skill\finviz-us-sector-rotation - Zcode\finviz-us-sector-rotation-v0.2\script\open interest-2026-09-23.txt` |
| 字幕 SHA-256 | `b1c166d067c0a3fee097d7d769460f1c4cab86ae571c07320fd53c2c3cbc3880`（python hashlib 本地计算，完整 64 位十六进制） |
| 节目日期 | 2026-09-23（周三）——**习特会前一日（今晚特朗普迎接习近平、明日会谈，AI 为核心议题）；美伊 6 月中以来首次会谈次日；油价五连跌后的反弹日；PMI 超预期触发的债券抛售日**。当日盘中主线：①**S&P Global PMI（制造/服务均强、"5 年高位"口径）→2Y 收益率 +10~12bp 至 4.85-4.86%（2024 年 6 月以来最高）、10Y 重上 5.05%（2007 年高位）、纳指 -1% 自纪录回落**；②**"Catrini 交易"第二日**（昨日 Catrini 报告点名金融/在线预订被砸 → 今晨 Schwab/万事达/Visa 等反弹，Meta 续涨）；③**SoftBank 逾 $110 亿垃圾债（近 10% 票息、$300 亿+订单、仅 3 倍认购）**与 CCC-B 利差（疫情以来最阔）；④**中国监管调查 DeepSeek/Moonshot（Anthropic 指其经 Claude 路由敏感数据）→阿里 -3.7%**；⑤**柴油禁令政治**（柴油纪录 $6.53、气 $4.47；出口禁令"战术性缓解但解决不了问题"） |
| 节目名称与主持人 | Bloomberg Open Interest（开盘档，纽约）。**Danny Berger**（字幕作 Danny Burgerer/Danny Berer，口径失真）全程主持；**Michael Ball**（字幕一处作 Mike Ball；Matt Miller 本周缺席）联袂第一小时（00:00–00:43，小时切换时道别）。常驻：Nora（姓氏口径作 Melinda、无法确认）担纲 Movers×2+Top Calls；连线记者 Tyler Kendall（华盛顿，×2）；编辑嘉宾 Sarah Frier（科技）、Emily Conan 型（消费）、James Crombie（信用/Credit Edge）、Bailey Lip Schultz 型（IPO）、Shri Natarajan（华尔街）、Lyanna Baker 型（并购） |
| 字幕全文读取状态 | 已完整读取：全文 2,551 行（wc -l 计 2,550 个换行符、末行无尾换行，Read 分 3 段读至 EOF：1–880、881–1760、1761–2551，末行 [01:27:26] "…This is Bloomberg."），无遗漏、无明显时段空档 |
| 时长/结构 | 00:00:00–01:27:26（约 87 分钟；00:00:03"距现金开盘 30 分钟"=9:00 ET 起、00:43:50"开盘 30 分钟"进入第二小时、收于约 10:30 ET）。嘉宾出场序：**Tyler Kendall①**（美伊会谈/柴油禁令/中期风向）→ 棚内 Mike 论"战术性缓解"→ **Sarah Frier**（习特会名单/稀土反制/distillation 调查/Muse 信任）→ **Emily Conan 型**（通用磨坊/饼干桶财报）→ Nora Movers①（IonQ/阿里/RCL）→ High Interest（**Morgan Stanley 邮件泄密/UBS +$17B 资本/SoftBank 债**）→ **James Crombie**（高收益认购结构/CCC 分化）→ **Bailey Lip Schultz 型**（诺和直接上市传闻/IPO 推迟潮）→ 开盘铃（第一夫人+Lisa Su 于 NYSE"Imperia 峰会"；**Nucleio 型核电公司 IPO** 仅超 $20 亿）→ **Botta Kerr 型（Northern Trust 家族办公室 CIO，姓名口径严重失真）**（税务亏损收割/宏观对冲基金/China 极化/Apollo gate/二级份额/$5 亿门槛/dry powder）→ 盘面（Catrini 反弹名单）→ Nora Top Calls（微软/诺和/PG&E）→ **Kate McShane（高盛零售）**（第 33 届全球消费零售大会/K 形/沃尔玛 agentic）→ **Shri Natarajan**（MS 泄密深度）→ 小时2（Danny 单人）：**Emily Bowersock Hill（Bowers Capital Partners）**（标普目标降至 7,800/三次加息/实资产/荷兰央行搬金）→ 收益率读数 → Nora Movers②（通用磨坊/麦当劳 $85 亿/RCL -5%）→ **Lyanna Baker 型**（RCL×Sandals 并购拆解）→ **Martin Whitaker（Just Capital，Paul Tudor Jones 创立）**（21% 知美领先/87% 担忧安全/30% 选民或换票）→ **PG&E CEO（字幕作 Patty Poppy，口径失真）**（山火责任改革/战略评估/$20 亿资本开支推迟/Diablo Canyon）→ **Ben & Jerry's CEO（字幕作 Yokan Sen/Yukan Semph，口径失真）**（价值观商业/Q2 +9.2%）→ **Tyler Kendall②**（习特会 preview：农产品采购/能源商品/$300 亿对等降税/AI 热线）→ 收尾（Bloomberg Deals 今日 12:00：Blackstone 副主席 Tom Nides；明日嘉宾 Kosla Ventures 创始人〔字幕作 Venode Kosa，口径失真〕） |

> 说明：字幕为机器转写，存在拼写失真（人名/机构名/数字）。本文为内部研究文件，仅使用字幕文件内容；无法确认处一律标注"字幕无法确认"或"口径失真"，不做外部补充。

---

## 一、主要主题与核心内容

### 1. 开局定调：昨日"零波动"与"Catrini 交易"的第二日

- 开场（00:00:00）："**S&P yesterday finished down 0.0001%. Will we get any movement today? 30 minutes until the start of your cash equity trade.**"
  - （标普昨日 -0.0001%——今天会有波动吗？距现金开盘 30 分钟。）
- 更正（00:12:36）："**I mentioned that the equity market, the S&P, fell by 0.1% yesterday. That's actually incorrect. It was 0.0077% if we're being precise. So, barely a move there.**"
  - （精确口径 -0.0077%——几乎没有变动。）
- Catrini 交易框架（00:00:41）："**We're back in this world where... every now and then we just do the Catrini trade. Catrini had a note out yesterday. Basically, everything he talked about got slammed — everything from financial services to online booking platforms. Meta... continues to gain about a quarter of a percent. It's basically making investors think about what happens when AI takes some of the hassle out of shopping.**"
  - （"隔天做一笔 Catrini 交易"的世界：昨日报告点名的一切都被砸——从金融服务到在线预订平台。）
- 昨日受害与今日反弹（00:01:03）："**You had Schwab, for example, that ended sharply lower. And if an agent can quickly compare prices, cancel service, or switch providers for you, that could be a real problem for banks and insurers and others that benefit when you as customers simply stay put. So, we're getting a little bit of a rebound in these stocks so far this morning.**"
- Mike 的怀疑（00:13:01）："**They do have an impact, but will it last? To your point [it] is still TBD... how's it going to [percolate] down and where does the line draw where people are going to have to accept that yes I have to be more competitive with my pricing and more transparent and that's going to cause my margins problems — I don't know... we might have had this great kind of ramp up because it hit the headlines and everyone got excited, then we don't actually get sort of maybe the returns you want and people get more nervous about giving AI all their information — and here we go. It's just sort of a head fake.**"
  - （影响有、持续性 TBD；采用率不足+信任迟疑=可能只是假动作〔head fake〕。）
- Sarah Frier 的证词（00:08:58）："**What have been called human inertia brands — your insurers, the price comparison, the gym membership, the travel search — those things will be able to be optimized by AI, not just by assistants with access to all of your data... but by AI in general... the subscription businesses may lose out in that situation. However, Muse itself... has had a breakout success — which, trust me, after years covering Meta, when I see Meta have a breakout consumer product success, that is surprising to me and good for them. It still is going to require Meta to build some trust with the public over sharing access to their email accounts, to their medical history... their financial information... it could be that it's worth it, but it has to be really worth it.**"
- Danny 的观察（00:13:44）："**I'm convinced the downloads were really good off the bat just because they have this WhatsApp community... on WhatsApp I immediately got a text being like 'download Muse'. I was curious. I did not download it, I will say.**"
  - （WhatsApp 社群裂变推高下载；Danny 本人"没下"。）

### 2. 美伊会谈次日：条件、拖延与"更高油价地板"

- Tyler Kendall①（00:01:35）：
  - "**The optimism was coming from President Trump confirming that as the US issued these rare visas for Iranian officials to come to the United Nations General Assembly, a meeting did happen. The US side characterized it as going very well. They confirmed that there is going to be another meeting.**"
  - （美签发罕见签证→会谈确实发生；美方称"很好"；确认将有下一场。）
- 伊朗要价不变（00:02:15）："**Iranian state media saying that essentially the country's positions have not changed. We're seeing a lot of the same demands that at this point we've been tracking for months, including that the US would need to lift its own naval blockade. And repeatedly we hear from White House officials that that's going to be a non-starter.**"
- 选举与拖延（00:02:49）："**President Trump seems to think that Iran is trying to delay this until after the midterm elections. He himself says that he doesn't take the election into account when he's thinking about weighing the next steps with Iran. But clearly the higher energy prices are weighing on American consumers.**"
- 中期风向（Danny 提问口径，00:02:33）："**The midterm elections now are starting to skew more towards the Democrats.**"（中期选举天平开始向民主党倾斜。）
- 价格读数（00:03:04）："**Today the national average for a gallon of gas $4.47. We had another record on diesel — $6.53 yesterday. In part prompting President Trump to say that he has encouraged advisers that they should seriously consider this export ban. The US Treasury Secretary Scott Bessent saying they're weighing whether a full or partial ban would be feasible.**"
- 共和党推动（00:03:25）："**You have some Republicans now calling on some sort of suspension or end to the war as they continue to hear from their own constituencies and voters that this is going to be a top issue... energy analysts say... over the long term we could actually see higher prices if refiners have to curb their own output.**"
- Mike 的"战术性缓解"论（00:03:59）："**It's a little bit of a desperation — we saw this again with the yen intervention. We saw this sort of with the buybacks in Treasury. They're really just trying to get to the midterms without anything blowing up... maybe we get a tactical sort of relief trade and we've seen diesel sort of come off in the futures market... you want to take profit ahead of this, you just don't know. But ultimately, it's not going to really solve anything.**"
  - （像日元干预、像财政部回购：撑到中期选举别爆就行；**柴油期货已自高位回落**=战术性缓解，但解决不了任何事。）
- 油价地板（00:04:44）："**There's still some kinetic activity going on in the strait. We don't know where the Houthis are... it was interesting to think about that... Iran doesn't control these guys. They obviously have influence on them, but there's some other micro stories going on there that are kind of almost outside of the US and Iran's control. Like if the Houthis want to continue to press the Saudis, that will put pressure on even if the East-West pipeline goes back into full capacity... the threat is there and therefore maybe a higher floor on the price of oil.**"
- Danny 的对照（00:04:29）："**It's incredibly difficult for this market... to deal with the chop... whether you can trust the signal from Trump saying... that he's given visas for the Iranians — it doesn't seem like enough for this market to keep crude below $100 a barrel.**"

### 3. 习特会 preview：名单、稀土与"AI 安全"议题

- Tyler Kendall②（01:23:52）："**President Trump welcoming Xi Jinping to Washington this evening ahead of talks tomorrow with AI set to be a central topic.**"
- 名单之问（Danny，00:05:28）："**It does seem that they rolled out the carpet for all the American CEOs... China's not doing the same for Chinese tech companies. Is there any signal in that?**"
- Sarah Frier 答背景（00:05:40）："**The backdrop of this conversation is that we need to come to a sort of arrangement with China. There's no guarantees here... but there is talk of we need to come to an agreement — a global agreement on what kind of curbs we need for AI, what we do about the safety threats... the Chinese side of the equation — they already feel like they've been held back by the US with export curbs, with limits on chips... at the same time, they have some concerns about regime security... there are sort of joint incentives on trying to come up with a path forward that doesn't get us to anything catastrophic. But... it may end up being more of a meet and greet.**"
- 稀土/精炼反制（Danny，00:06:53）："**The Chinese wanted to flex back. They bring some of these rare earth refiners, some of these copper and lithium refiners — as we know they have that market monopoly there and we need that greatly... that's what changed the tide last year when we started to realize that... our leverage is a little less.**"
- Distillation 调查（Sarah，00:06:19）："**There was a report from the Information yesterday about looking into some of these distillation concerns — some concerns that some Chinese models have used Claude to come up with answers for their users and train their models.**"
- 能力差距与开源（Sarah，00:07:19）："**We were talking about Nvidia's most advanced chips and limiting China's access to them. Now we're in a different situation where the gap between China's capabilities and the US capabilities does seem like it's starting to close. There's a little bit of anxiety about open-source models in particular — none of the curbs on AI that US leading labs have discussed are going to be possible without some curbs on open-source technology. At the same time that [open source] is really important to China and is very popular among US startups... turning to Chinese open source models in order to build AI internally more cheaply, more customizably. It is a really complex set of issues that I don't think will be resolved at this meeting.**"
- Bloomberg Economics 预期（Tyler Kendall②，01:25:26）："**Expect some tactical developments around trade. We've gotten a preview of some of them. We are expecting the administration to push for China to announce agricultural purchase commitments — maybe something related to energy goods as well. The two sides have also already previously announced that they are working to lower tariffs on a reciprocal basis for up to 30 billion dollars worth of goods. We're tracking closely the AI conversation. There's been some reporting that maybe we'll see a so-called hotline established between the two countries, though sourcing has been downplaying this, saying that it's more an open line of communication... may not address some of those core issues like allegations by the US government that China is stealing American IP... Chinese purchases of Iranian crude.**"
- 后续观察点（01:26:15）："**Watch out for anything related to another meeting... if the two sides commit to President Trump going to APEC in China later this fall, Xi Jinping coming back for the G20. The stability seems to be the line and maintaining that.**"

### 4. SoftBank 垃圾债与信用市场分化

- High Interest（00:16:09）："**SoftBank raising over 11 billion in bonds to help fund its big push into AI. It's offering investors yields of nearly 10% — the highest ever for some of its own bonds. Demand is strong though, with more than $30 billion in orders.**"
- James Crombie 的拆解（00:16:33）：
  - 认购对照："**Well, there isn't that much demand if you look at it in the context of an IG deal that gets over hundred billion dollars in orders. This is risky... you can tell by the level — it's only three times oversubscribed, which in the context of all the other stuff that's 10 times oversubscribed... there is some caution here.**"
  - 资负错配之问（Mike 提问）："**SoftBank's kind of got a little bit of an asset-liability mismatch now... there's a lot of paper that needs to be rolled [at] higher levels... when can we start thinking about that?**"
  - 到期墙："**There's a big maturity wall coming up for lower-rated credit, which you can definitely see in the spreads on triple-C rated bonds — the gap between triple-C and single-B... is the highest since the pandemic. So there's definitely a lot of concern that that cohort of borrowers won't be able to pay the money back.**"
  - 传染警告（00:17:49）："**It's only that lower-rated tranche... which is kind of misleading for people... there is such a thing in credit markets as contagion and I think people are underestimating the risk on the single-B, particularly the single-B minus — which, interestingly, the SoftBank deal today: they're rated double-B but they're actually pricing closer to a single-B minus, which shows that the market is very concerned about the level of risk in that deal.**"
  - 两极化结论（00:18:37）："**It's just this broader winners and losers... it's just going to be more pickiness where people feel safe with capital or a giant kind of concession where you need to just pay more... when you look at the SoftBank deal in particular: if you think you're going to succeed in the AI race and everything's going to work out, then it's actually a cheap deal. If you're worried about it... stay away.**"

### 5. IPO 市场："vibes are off"与诺和直接上市传闻

- Bailey Lip Schultz 型（00:19:10）——诺和线：
  - "**The FT reporting that Novo is considering replacing its ADRs with a direct NYC listing to boost its profile in the US. The CEO there apparently telling the FT there are no active discussions about such a move.**"
  - 动机框架："**You have to think about what mission would they want to accomplish. Is it easier access to investors who maybe can't invest in ADRs, or is the long game ultimately making a primary listing here in New York? The whole pitch from US bankers going back the last decade is you can get greater valuations here than you can elsewhere. And then also once you're formally listed here... that opens up ETFs, more passive funds.**"
  - 实质："**There already are ADRs listed here. So you wouldn't be doing an IPO. You wouldn't be raising capital. You would just be kind of transitioning — which we've seen a number of companies do and we've seen them typically perform better than their peers.**"
- IPO 推迟潮（00:20:43）："**It feels like IPO sentiment elsewhere is different than we expected... The vibes are off depending who you talk to... yes, we have the Nasdaq 100 at the all-time high. Yes, the Nasdaq composite [is] at an all-time high. But if you look under the surface: deals in Bamboo, an insurance-related company, which postponed its IPO; and [a] nuclear company, which postponed its IPO last week. These are in industries that have been challenged. So their comparables are trading down relative to maybe what they were expecting. And even when I talk to folks on the buy side — outside of an Anthropic, these are seen as kind of B or C rated assets. So it's not something that they need to buy and that's where you're seeing investors push back a bit.**"
  - 〔Bamboo 与该核电公司名口径失真、无法确认。〕
- 今日 IPO（00:22:36）："**Down at the NASDAQ we have Nucleio. They are a nuclear power company and they are IPOing today. We're just talking about the lack of IPOs... This one's only just over $2 billion. And considering in today's context, that's peanuts. That's nothing. Tiny company.**"
- 开盘仪式（00:22:20）："**Down at the New York Stock Exchange, it's the first lady... she is celebrating the Imperia Summit — an economic event for women in power. Looks like we have Lisa Su there as well.**"
  - 〔"Imperia Summit"与"Lisa Su"口径均无法确认、按字幕。〕

### 6. 家族办公室视角（Botta Kerr 型，Northern Trust Family Office CIO）

- 税先于战术（00:23:42）："**For family offices, they're really investing for generations and they're triple bottom line investors. So they think about return potential, but they also think about taxes... the daily movements of the market actually provide lots of opportunity for tax loss harvesting, more so than tactical trading on individual securities.**"
- 对冲基金再受宠（00:24:20）："**Hedge funds for many years were not a popular asset class for family offices — disappointing returns overall... but given the geopolitical climate, given how big the moves are on macro trends, we're really seeing strong performance out of some of those macro players and long-short... family offices often have private foundations as well that can be tax-deferred assets, and so the hedge fund allocation does tend to live there... it is a talent war... the larger, bigger hedge funds [have] been able to retain that talent and also demonstrate substantial outperformance.**"
- AI 是唯一横贯因子（00:25:10）："**A lot of allocators are pivoting to a total return allocation approach where you're thinking about factors and not just asset classes. And if you were going to say what's the one factor that's across every asset class today, it's AI. It's in the private markets. It's in the taxable bond markets. It's in the equity markets... in venture, over 80% of deals recently.**"
- 非 AI 的配置（00:25:44）："**In core buyout and middle market, that's not the case. We're also seeing increases in infrastructure as an allocation. So when you think about the picks and shovels trade, that's important.**"
- 中国极化（00:26:24）："**If you've met one family office, you've met one family office... China's been polarizing. So there's been a lot of families that have excluded China allocations in emerging markets and that's played to their favor in recent years. But... China is speeding up in the AI race and in many ways has actually exceeded our capabilities — to your point around energy production and their ability to really power data centers. They don't have a NIMBY movement in China. Today we've got about 70% of the population opposing data center construction. So we have to be very thoughtful with our clients around the push and pull of geopolitical concerns and governance concerns with real exposure to profits... we view it as important to have exposure to the market. It's a market that can't be ignored.**"
- 私募信贷与 Apollo gate（00:27:20）："**Apollo gating another one of their funds. The noise around it certainly has settled down... our family office clients aren't seeing as much of pulling from private credit. In fact, I think it's the opposite. There's opportunity to drive secondary allocations... secondaries in terms of continuation vehicles led by GPs seeking liquidity is a real opportunity... private credit dislocation really bringing up secondary opportunity... secondaries were historically viewed as a niche asset class and today as those offices are deploying, privates are often the first sub-asset class that they're deploying to, including in credit.**"
- BDC 之问（00:28:20）："**A BDC was sold to a family office with the idea being like this is a great cash management tool because you earn more yield and it's a semi-liquid product — which essentially we learned it's not: when you want your money back it becomes incredibly illiquid when everyone's doing the same thing at the same time.**"
  - 答复："**The biggest mistakes in investing often happen with a mismatch of liquidity and the underlying instrument... the mismatch of long-dated debt with regular liquidity was always concerning to me... for many of our family office clients, they didn't buy it. In fact, they can tolerate the illiquidity premium... private equity and venture represents a much larger piece of their allocation on average. So we're not seeing a lot of stress or really even distress in that space with our clients.**"
- Dry powder 与新财富（00:29:44）："**There is dry powder because there's a lot of new wealth being created... to truly staff up with a chief investment officer and a CFO, it does take [around] the $500 million level... obviously the IPO chatter this morning — maybe some of them are delayed, but a lot of them are going to go forward... there are real catalysts to new cash being deployed. The problem is once it's deployed, the taxes get in the way of being true tactical allocators... they really tend to stick to that strategic asset allocation with some marginal changes around the edges.**"
- 财富源头（00:30:45）："**All the wealth being created from like a SpaceX IPO, like VC — all of a sudden everybody having AI bets and having Anthropic salaries that are paying off hugely. It's been such an interesting trend to watch... it's an explosion of wealth in the world truly because of all the liquidity that's being created.**"

### 7. 零售与消费（高盛 Kate McShane，第 33 届全球消费与零售大会）

- 大会基调（00:33:55）："**Divergence is probably fair, but at the same time there wasn't any kind of real panic about the health of the consumer. If we had to really juxtapose what we heard at our conference this year versus last year, I think the biggest difference is just the war. There is a lot more inflation because of that. Gas prices are obviously higher. All consumers have to contend with that, but especially the lower income consumer that's been dealing with a lot of inflation in general now has the added inflation of gas.**"
- 供应链与运费（00:34:52）："**Last year they were contending with tariffs — there was some sourcing that had to be changed as a result of that. This year seems a little bit easier... in terms of being able to get your hands on the goods that you want on the shelves... we do expect a slightly better holiday in that regard... obviously the cost of everything is going to be higher on the freight side. A lot of the retailers are locked in right now with ocean freight. Those will come up for negotiations come the spring... diesel obviously is a little bit of an issue on the trucking side.**"
- Macy's 上行赌注（00:35:43）："**There are companies like Macy's, for example, that are trying to bring in a higher income consumer and bringing in those higher-end, closer to luxury type products.**"
- K 形与下沉（00:36:00）："**The K-shaped economy is real, and I think even the discounters we cover — Dollar General, Dollar Tree — they are seeing more trade in from that $100,000-income consumer than they have previously. I think it's a testament to... no matter what income demographic you are in, you are looking for more value.**"
- Agentic commerce（00:36:47）："**This week's big theme is this Meta Muse development which empowers the consumer... we covered Walmart and they probably have been the most prolific in terms of what they have talked about with regards to agentic commerce... what these platforms are built for are to offer the best prices, the speediest, the most value — and so for someone like Walmart, that speaks very well to what their proposition is. But we haven't really heard as much on the agentic commerce front from other retailers. It's been more on the efficiency side, on the cost side where they're trying to find more efficiencies.**"
- 大者恒大（00:37:40）："**If you are a Walmart or even an Amazon and you have the financial firepower to invest in these things versus smaller companies... the size and scale of your business, your ability to invest in things is going to differentiate you from some of the smaller players... the supply chain was a big differentiator — the bigger you were, the more scale you had, the more negotiation you had. This is a continuation of what the tariff situation showed us: might makes right... ultimately it's about the execution. And the Walmarts of the world are exceptionally good at this.**"
- 创新与 Best Buy（00:38:17）："**Innovation still is very much at the forefront of what the consumer is willing to pay for — newness, innovation... that can come in consumer electronics, that can come in fashion... For Best Buy, I think so. It is better execution at Best Buy. Appliances has been a drag on their comp for a while — it seems to have stabilized now. You might have a better product cycle coming up with RGB TVs. Computing continues to drive their results.**"

### 8. Morgan Stanley 邮件泄密事件（Shri Natarajan）

- 事实（00:39:16）："**Morgan Stanley is dealing with an embarrassing email misfire after a staffer accidentally shared an internal list of over 100 investment banking deals the firm is pitching across Asia. The document included potential IPOs, private equity backers, and paused projects. In a statement to Bloomberg News, Morgan Stanley wrote: 'We promptly took steps to address this inadvertent sharing of information and we continue to engage with relevant parties.'**"
- 定性（00:39:55）："**Let he who has never [sent] out a misfired email throw the first stone... the prominent word across Wall Street today... is schadenfreude. There will be a lot of people taking joy in Morgan Stanley's misfortune. But honestly, truly, this could happen to anyone... when you're at the very top end of it — especially in a place like Asia where Morgan Stanley is a dominant bank... one of the top banks when it comes to IPOs... one of the top banks when it comes to Asia mergers — for them to accidentally send out a list like this, that is a pipeline of some of the most important deals taking place in Asia.**"
- 边际缓和（00:40:57）："**If you leak a deal or two, perhaps you will have a furious counterparty or two. When you leak a hundred deals, hopefully you just get a collective shoulder shrug.**"
- 内幕交易之问（00:41:34）："**Some of the most sophisticated insider trading crime syndicates spend years trying to build up infrastructure trying to get information on a pipeline of three, four, five, a dozen deals — and suddenly you have an accidental email... this is bad for the insider traders.**"
- 后果评估（00:42:20）："**There will certainly be real world consequences. It is clear... our reporters have already seen the document. There are people who are posting blurred accounts of it on Instagram and social media. The fact that an investment banking deal pipeline is going viral on social media — that tells you everything... I can't imagine this having a serious hit on bottom line... Morgan Stanley is best in the business when it comes to Asia — hopefully people are able to look the other way and realize this was just a mistake.**"
- 交易成本之问（Danny，00:42:21）："**If something in this... let's say you're targeting a public company and shares rally because of this, all of a sudden that deal is a lot more expensive.**"

### 9. Emily Bowersock Hill：标普目标 7,800 与"利率太低"论

- 目标下调（00:44:26）："**We believe the stock market's gains for the year are in and we have reduced our S&P 500 target to 7,800 due to rising rates which are a drag on stocks.**"
- 估值机制（00:44:46）："**When the Treasury is yielding 4%, investors can pretty easily justify paying a 20-times multiple. When that yield is 5%, those multiples are much less attractive. So not only does the market discount future rates at a higher rate, but a 5% Treasury yield poses significant competition [to equities].**"
- 盈利与指引（00:45:07）："**We are definitely optimistic about earnings — we're expecting 20% at least year-over-year earnings growth — but we are... significantly more cautious about what we're going to hear in terms of company forward guidance.**"
- 消费者压力清单（00:45:42）："**The American consumer has a reputation for continuing to spend even under duress. But spiking gas prices, higher mortgage rates, increasing payments on lines of credit are putting already stressed and overleveraged consumers in a bad position... the inflation has really spread far beyond food, energy, and shelter... the cost of car ownership, which came out in the most recent CPI data, has gotten significantly more expensive — and American consumers love their cars... consumer sentiment has dropped very significantly from last September — 13%... those are preliminary numbers... consumers have really spent down their savings buffer. So I do think you're going to hear from companies that depend on the American consumer that they're worried about consumer spending through the end of the holiday season.**"
- 当日叙事（Danny，00:46:49）："**About 15 minutes or so, we got global S&P figures rising to a 5-year high. And at the same time, as almost as if on cue, 10-year yields go back above 5% to reach the highest level since 2007... there's more odds that the Fed is going to be tightening rates.**"
- 结构性通胀（00:47:30）："**The Fed is going to have a very difficult time reaching its 2% target. There are a number of broad structural reasons for that — climate change, [deglobalization], geopolitical disruption. All these are inflationary forces and monetary policy is a blunt tool that may not be able to address those. It's possible that AI innovation will boost productivity enough to offset some of those forces. But what that idea is not factoring in... is the strong possibility that AI innovation would actually inflame societal division, widen the disparity of wealth even further and lead to the deterioration of democracies around the world. And those things would harden those structural inflationary forces... if you look at our expectations for economic growth and our expectations for inflation which are strong, interest rates now are actually too low. So we are going to need to see higher interest rates over the next year or two... It's not an issue with economic growth, not an issue with earnings. It's an issue with inflation.**"
- 加息路径（00:49:06）："**A market that's pricing in three [to] four — somewhere in, more towards the three side — hikes through 2027. Is that about in line with what you're expecting? — Yes, we're expecting three hikes. Probably one in December. I don't see October, but it's certainly possible. And I think the Fed will end up pausing next April, about 75 basis points higher than this... we're pretty much consensus with three more 25 basis point hikes.**"
- 藏身处（00:49:48）："**The benefits of AI are going to accrue to the people who already have capital invested. So we are recommending... that our clients hold their positions in private and public equity. And... you need exposure to real assets that are a good inflation hedge — so private infrastructure and timber, for example. The second thing is: witness the Dutch central bank's decision to move a substantial percentage of its gold reserves from New York to London... they initially moved that gold to London in the early years of World War II because they... were concerned about confiscation by the German government... what we're seeing is central banks around the world act on this diminished trust in the US government. China has imported a record amount of bullion this year... I would make sure that [the portfolio] is diversified internationally and outside the US dollar... portfolio construction should be informed by that diminished [trust].**"

### 10. Just Capital 调查：美国公众与 AI 竞赛（Martin Whitaker）

- 调查背景（00:58:46）："**Just Capital, the nonprofit formed by Paul Tudor Jones, released a new study, finding that most Americans do not know that the US is currently leading the world in AI development — with just 21% of respondents saying that the US has a leg up.**"
- 安全共识（00:59:25）："**I was most surprised by the overwhelming support for AI safety. We've been doing a huge amount of surveying of not just the public, but investors, business leaders, and you see agreement across the board: 87% of Americans are concerned about AI safety and want the president to take action on that — but they don't want to slow down.**"
- National AI Monitor（00:59:47）："**We just released something called the National AI Monitor, which tracks how ordinary Americans are kind of experiencing AI in their lives. People are net positive on that, especially at work... positive as consumers... positive about the impact of AI in their communities — but negative on the environment. Another interesting finding was: the more people use AI, the more they're trained in AI, the more comfortable they get and the more optimistic they get about the future.**"
- 数据中心张力（01:00:17）："**The data centers are a kind of manifestation of what AI could do... but if you ask about people's experience of AI right now — positive in the workplace, that's in fact where people are most positive.**"
- 选票弹性（01:00:58）："**Up to 30% of voters said that they would switch their vote to a candidate who aligns with their AI views.**"
  - Danny 注："**I had a conversation roughly about a year ago with the historian Neil Ferguson who basically said [in] 2028 the main issue was going to be AI — and I thought it sounded crazy then. It's feeling increasingly less crazy.**"
  - Whitaker："**I do think that 30% is going to go up over time.**"
- 党派裂口（01:02:08）："**The biggest political split was on whether America should be an AI leader — that was a 20-something percent split. But for the most part, Republicans, Democrats aligned within a few points on prioritization of safety... certainly aligned on how two-thirds of Americans would like the president to get a deal done with China. But even if he doesn't, they don't want no action on guardrails.**"
  - 〔Danny 口径为"28 点差距"、Whitaker 口径"20 多个百分点"——两口径并存、分别保留。〕
- 波音/空客类比（01:01:34）："**Most of the world's airplanes are made by two companies — Airbus and Boeing. When you get on a plane, you expect it to not fall out of the sky... it's the same with AI... certainly the AI developers and the AI deployers — who by the way are held equally responsible by the public if things go wrong.**"
- 系统性风险（01:03:13）："**The big risk here honestly is if people lose trust and lose faith that AI is working for them and their family... if they see fewer and fewer people getting wealthier and wealthier from AI, but their lives are worse — that's a real problem with our system of capitalism [and] democracy, and if people don't like the system, they're apt to want to change it.**"
- Muse 信任注脚（01:03:54）："**It got millions rather [than billions] — 2.5 million downloads in the space of something like a couple of days... there is a cohort out there that clearly trusts this AI agent enough to give it its credit card data and its login information.**"
  - Gallup 对照："**People are very worried about an AI doomer future — we don't see that in terms of individual experience... people prefer their AI. Like, I like my AI, but I don't — I'm worried about AI's future impact on society.**"

### 11. PG&E：山火责任、战略评估与电网（CEO，字幕作 Patty Poppy）

- 处境（00:05:40 段/01:05:40）："**PG&E shares have been under pressure in recent weeks after California lawmakers failed to deliver the wildfire liability reforms investors were hoping for. The utility has since launched a strategic review of its business and at the same time the AI boom creating a huge new source of electricity demand from data centers — putting even more focus on how PG&E plans to build out the grid.**"
- 改革现状（01:06:36）："**There's no doubt that waiting is not an option. Kicking this can down another year is just not an option. Our customers are waiting and suffering for the lack of action. I'm grateful for the governor and speaker Rivas stating there's more work to be done yet this year — and we agree... we can power it, but not without policy reform.**"
- 信用后果（01:07:40）："**The credit agencies — in fact Fitch put us on negative outlook last week. We continue to be sub-investment grade at Moody's and S&P and that costs our customers real money... in addition to the equity holders who... pulled their money out of PG&E when this bill didn't get voted on... our customers are paying for all of that inaction.**"
- 资本开支反制（01:09:10）："**After the inaction of the legislature during the regular session, we went ahead and announced that we were going to be pulling back on capital because our customers cannot afford for us to borrow that money at those rates... things like new housing starts will slow in California. It's the number one problem in California and we're going to be unfortunately a negative impact on that. People will definitely feel it... the slowing down of interconnections of new clean energy resources that were going to be added to the grid in 2027 will be slowed. Our ability to power AI will be slowed as a result of our necessary pullback.**"
- 规模与药方（01:10:30-01:10:56）："**We power two-thirds of... the state of California. It's the fourth largest economy in the world... there is a fix. It's about a paragraph of text... the governor sent the CPUC a letter and asked them to provide a report by November 1st to indicate what regulatory fixes could be made.**"
- 责任逻辑（01:11:22）："**Consumers recoup compensation from my customers, not from me the company, when we are prudent operators... some externality — whether it's a bird nest or a tree that looks healthy but falls on a line or somebody runs into a pole — our customers pay. That's bad policy... Insurance should pay for insured risk. They know how to insure that risk and they should charge the appropriate price for that risk. But my customer should not be the insurer of last resort... the legislature's own report suggested that it was untenable to maintain the status quo.**"
- 费率 vs 账单（01:12:32）："**We do not have the highest bills. We have the highest rates, but we have low usage... we've lowered rates five times in the last two years... new large demand from both AI and manufacturing and electrification of vehicles and buildings are all sources of ways that we can... even lower rates further.**"
- 战略评估范围（01:13:58）："**First, it is policy reform... but in the absence of it, there are a range of options including regulatory fixes... we could reconsider our capital allocation and maybe slow capital further over a longer period of time. We could ring fence particular assets... my gas customers — 5 million of them — are paying for wildfire risk and it has nothing to do with wildfire risk. My generation assets — I have 8 gigawatts of clean energy, the most beautiful hydro system in the world, one of the best nuclear power plants in the world, Diablo Canyon nuclear power plant... we're going to try and figure out how to unlock the value in these incredible assets... everything's on the table.**"
- 推迟金额（01:13:47）：**已推迟约 $20 亿基建开支**（"you've already deferred some of the $2 billion worth of infrastructure spending"）。

### 12. Ben & Jerry's：价值观商业的样本（CEO，字幕作 Yokan Sen）

- 业绩（01:16:42）："**We are a values-based company... one of the reasons why I love this job... a three-part mission: product making it in the nicest possible way, a social mission which comes through the things we stand for and how we source, and then it all sits in a business model — and that model actually really works... we grew in quarter 2, 9.2%.**"
  - 〔字幕一处"9.2% 2%"口径混乱、按 9.2% 记录。〕
- ESG 逆风（01:17:39）："**A lot of companies quietly dismantled their ESG and DEI programs because of that pressure. Are you not facing some of the same constraints...? — It's baked into our model. We wouldn't change this now... that would be a thing that people would say like I wouldn't recognize Ben and Jerry's.**"
- 创始人张力（01:18:20）："**There has been this real intense pushback... from the founders themselves... concerns about dismantling the independent board... maybe Unilever forced out your [processor]... what do you respond to people that say you're trying to sanitize what was the core? — Ben is a great campaigner. Ben is an activist. He's the founder of the company... he's been part of our history as well, trying to push us, raise the bar.**"
  - 回购之问（01:21:00）："**Is it made difficult by having the co-founder out there doing things like trying to campaign to buy back the company himself?**"
- 选举动员（01:19:31）："**We've just launched the flavor [Rock the Vote 型]... all about bringing people out to vote — the suppressed voters, the minority voters, the voters that are coming for the first time... that's our focus now for the midterms because if you vote, democracy works... we've... donated about 3 million to People's Action to help them... do community organizing and getting people to come out to vote.**"
- 加沙之问（01:19:58）：被问及为何不选加沙议题——"**If you're in the space... of social justice and the work that we do based on our values, you got to be also out there to say: this is now the campaign we focus on. And the most relevant thing now for the second half of the year is people voting and getting out for the midterms.**"
- 产品逻辑（01:21:42）："**We make... the best product in the nicest possible way. And we've been doing that for 48 years... rich chunks and swirls, chocolate chip cookie dough, fudge brownie — real all-time favorites — and they give you that affordable indulgent treat... we use fair trade sugar and cocoa... we're bringing these classic favorites... on a stick as well.**"
- 品牌里程碑（01:19:01）："**We're going to be 50 years in 2028.**"

### 13. 收益率与盘面全日读数（多时点）

- 盘前（00:12:34）：**标普微跌、纳指期货 -0.2%**。
- 开盘后（00:31:09）："**Meta has another good day — it is now trading at the highest level since September of last year. Microsoft doing well too. Palantir up 2%... Mastercard, Berkshire Hathaway, Tesla, Visa — some of the stocks that have been hit by the Catrini trade... bounced back this morning. On the downside: Broadcom, Amazon, Alphabet, Nvidia, Intel... tech... ends down about 2% here in the opening hours... Energy the best performer as the price of oil goes up. Utilities fall by 1% alongside consumer discretionary.**"
  - 〔"tech ends down about 2%"口径疑失真（或为 -0.2%）、按字幕记录。〕
- 收益率第一读（00:51:18）："**On the front end of the curve, they are higher by more than 10 and a half basis points — the highest level since June of 2024. A couple of factors: stronger PMIs and a stronger economy... the price of oil back on the move higher... more hawkish Fed speak — we had Goolsbee earlier in the week... 10-year yields up seven basis points. 30 years up four and a half basis points... We are down 4/10 of a percent for the S&P.**"
- 收益率第二读（00:57:30）："**The bond selling continues at pace... nearing 11 basis points for your two-year yields at the highest level since the summer of 2024... two-year yields again up at 4.8620... 10-year yields back at their 2007 high, back above 5%... [the Nasdaq] drops by about 1%.**"
- PMI 触发（00:46:59）："**We got global S&P figures rising to a 5-year high... as almost as if on cue, 10-year yields go back above 5% to reach the highest level since 2007.**"
- 收盘读（01:04:53/01:26:36）："**We're up nearly 12 basis points for your 2-year yields as we price in more hikes from this Fed after stronger than expected PMI data that also suggested the labor component was quite strong... we're now higher by nearly 10 basis points for the 10-year yield — that's back above 5%... the front end higher by 10 basis points, trading at the highest level since June of 2024 at 4.8516... 10-year yields back at a 2007 level at 5.05. 30-year yields up six basis points.**"
  - 〔2Y 两读 4.8620/4.8516 并存、按区间记录。〕
- UBS 资本线（00:15:53）："**Swiss lawmakers... want UBS to keep a lot more cash on hand in case another banking crisis hits. The new rules could force UBS to add about 17 billion dollars in capital. UBS says the plan goes too far and plans to keep fighting as the proposal moves through parliament.**"
- 收尾预告（01:27:12）："**Catch me on Bloomberg Deals today, 12:00 p.m. New York time. In about 1 hour's time, I'll have an exclusive interview with Blackstone vice chairman — that is Tom Nides. And tomorrow on the show... Kosla Ventures founder [will] be joining us.**"

### 14. RCL×Sandals 并购拆解（Lyanna Baker 型，Bloomberg US Deals 执行主编，00:54:38–00:57:20）

- 交易定位（00:54:38）："**Royal Caribbean is checking into the resort business. The cruise giant is buying half of Sandals Resort for about $3 billion, giving it a major foothold on land across the Caribbean. The deal is expected to close early next year and shares are falling about 5% this morning.**"
- "史上最大"（00:54:42）："**You were just telling me in the break that this is their biggest deal ever. — It is. And investors don't love surprises like that when you suddenly see a company that maybe was doing buybacks and other things just make a big bold move into M&A.**"
- 标的背景（00:54:53）："**Sandals had been for sale for many years. The founder had passed away in 2021 and it had been in sort of legal turmoil for a while, and the pandemic sort of slowed things down. Clearly, Royal Caribbean here is making a big statement purchase in the Caribbean. Sandals is apparently the biggest private employer in the Caribbean.**"
- 商业逻辑（00:55:15）："**It really is a way to cater to tourists who just want everything taken care of — they want all-inclusive, they don't want to have to decide what time they're going for dinner and where they're going for dinner every night. So that's something that's in common even though these are very different vacation experiences.**"
  - Danny 补充："**You're on our cruise and then we're going to take you to an island and then you can spend money and also that money is coming to us versus somebody else.**"（船+岛闭环、钱留自家。）
- 分析师疑虑（00:55:40）："**Analysts are scratching their heads a little bit. Not just because Royal Caribbean hasn't done mergers and acquisitions before like as big as this, but it's a different audience even if the mentality is similar. Sandals is all about the couple — there's no kids allowed. There is something called the Beaches brand that families are allowed at, but those are only two resorts.**"
- 协同展望（00:56:22）："**Both sides have a chance to kind of diversify and we should see things like the loyalty programs combining and other synergies like that.**"
- 行业注脚（00:56:46）："**Cruise lines have done well except [they] have kind of faced the impact of higher fuel prices... the stocks of a lot of these companies have lagged. Royal Caribbean has done better than its competitors, but I wouldn't say the cruise industry is doing amazing right now for the reasons you mentioned — like fuel prices.**"

---

## 二、与当日行情和板块相关的要点

- **重要限定**：本档覆盖 9:00–10:30 ET（开盘前后 90 分钟），为盘中段；收盘兑现见同日 The Close（S&P -0.8%、纳指 -1%、道指 -370、能源 +1.1% 唯一收涨、VIX>15）。
- **指数/盘面（盘中读数）**：
  - 昨日标普 **-0.0077%**（精确口径）；
  - 今日**标普 -0.1% → -0.4%（10:00 前后）**；
  - **纳指期货 -0.2% → 纳指盘中 -1%**；
  - **科技开盘时段约 -2%〔口径疑失真〕**；
  - **Meta 创去年 9 月以来盘中新高**。
- **利率（当日核心驱动）**：
  - **2Y +10.5bp→近 +12bp、4.8516-4.8620 区间＝2024 年 6 月/夏季以来最高**；
  - **10Y +7→+10bp 至 5.05%＝2007 年高位**；
  - **30Y +4.5→+6bp**；
  - 触发器=**S&P Global PMI（制造+服务均超预期、升至"5 年高位"、就业分项强）+油价反弹+Goolsbee 以来的鹰派 Fed speak**。
- **Fed 定价**：
  - Bowersock Hill——**市场定价 3-4 次之间（偏 3 次、至 2027）**；她预期**三次 25bp：12 月一次〔10 月不见〕、明年 4 月暂停（累计再 +75bp）**；
  - "利率现在其实太低"论（结构性通胀：气候/去全球化/地缘+AI 的社会撕裂反噬）；
  - 〔同日 Surveillance：DB 基准 +50bp〔12 月+3 月〕、75 下限；JPM PB 今年+1/明年上半年+1。〕
- **商品/油品**：
  - **原油回到 $100 上方拉锯**（"不足以把原油压在 $100 下方"；"油价有更高地板"）；
  - **柴油期货已自高位回落（战术性缓解）**；
  - **柴油昨日纪录 $6.53、汽油 $4.47**；
  - 出口禁令=**战术 relief 但不解决任何事**（Mike）。
- **信用**：
  - **SoftBank $110 亿+ 发债、近 10% 票息（其部分债券史上最高）、$300 亿+ 订单、仅 3 倍认购**；
  - **评级双 B、按 B- 定价**；
  - **CCC-B 利差＝疫情以来最阔、到期墙**；
  - **数据中心/AI 债的两极化**（"信 AI 赢=便宜、怕爆雷=远离"）。
- **板块信号（盘中，供轮动报告）**：
  - **强=能源**（"energy the best performer as the price of oil goes up"）；
  - **强=Catrini 受害组反弹**（Schwab/万事达/Visa/Berkshire/Tesla——昨日被砸的金融与支付反弹）；
  - **强=Meta 生态**（Meta 盘中新高；Muse 数日 250 万下载）；
  - **强=微软**（Stifel 上调至买入）；
  - **弱=大科技硬件**（Broadcom/Amazon/Alphabet/Nvidia/Intel 领跌——AI 交易获利了结+利率）；
  - **弱=公用事业 -1%、可选消费 -1%**（利率敏感；PG&E 另有公司层面利空）；
  - **弱=中概 AI**（阿里 -3.7%：中国调查 DeepSeek/Moonshot）；
  - **弱=食品龙头个股**（通用磨坊销售超预期仍 -2%）；
  - **弱=快餐个股**（麦当劳 -4.3%、近四年最低：$85 亿加盟商计划被视为利空）；
  - **弱=邮轮个股**（RCL 由盘前 +1% 转跌、盘中 -5%：$30 亿 Sandals 并购）；
  - **强=量子**（IonQ 盘前双位数：CPU 实时纠错解码器）。
- **IPO/一级市场**：
  - **Nucleio 型核电公司今日 IPO（仅超 $20 亿）**；
  - **Bamboo（保险）与某核电公司推迟 IPO**；"**除 Anthropic 外多为 B/C 级资产**"；
  - **诺和诺德考虑 ADR→纽约直接上市（FT；CEO 称无积极讨论）**；
  - **SpaceX IPO 预期催生家族办公室新财富**。
- **数据与事件日历（本集口播）**：
  - 今日：**习特晚宴+明日会谈（农产品采购承诺、能源商品、$300 亿对等降税落地、AI 热线）**；**Bloomberg Deals 12:00（Blackstone 副主席 Tom Nides）**；**Bloomberg Green 气候周活动（Ben & Jerry's/IKEA CEO 同场）**；
  - 明日：**Kosla Ventures 创始人（字幕 Venode Kosa，口径失真）上节目**；习特会谈日（见 The Close 明日展望：餐馆+Costco 财报、初请+建筑许可）；
  - 远期：**中期选举（"skew more towards the Democrats"）；APEC（特朗普或赴华）/G20（习近平或回访）**。
- **当日行情驱动归纳（盘中视角）**：9/23 盘中=**"PMI 强→利率杀估值→AI 动能获利回吐"的三段式**：
  - ①2Y/10Y 双双突破关键关口（2024/6 与 2007 高位）直接压制纳指与高倍数科技；
  - ②昨日 Catrini 交易的"put on"今晨部分"take off"（金融支付反弹、大科技回吐）——隔日反转结构；
  - ③能源因油价反弹+柴油禁令预期走强、炼厂背离（The Close 收盘口径）；
  - 信用端的 SoftBank 认购倍数（3x）与 CCC-B 利差给出"AI 信仰溢价 vs 信用分层"的仓位注脚。
- **与同日两档节目的读数接力（供轮动报告直接引用）**：
  - 利率：盘前（Surveillance）**2Y 4.80 年内高点**→盘中（本集）**2Y 4.85-4.86（2024/6 以来最高）、10Y 5.05**→收盘（The Close）**10Y +14bp、30Y +9bp 测 5%、5Y 2007 以来最高**；
  - 股指：盘前**标普期指 +0.1%→-0.1%**→盘中（本集）**标普 -0.4%、纳指 -1%**→收盘**标普 -0.8%、道指 -370**；
  - 板块：盘中（本集）"**能源最强、公用/可选 -1%、科技领跌、Catrini 受害组反弹**"→收盘"**能源 +1.1% 唯一收涨、通信服务/公用/可选/REITs >-1%**"；
  - RCL 三段式：盘前 +1%→盘中（本集）-5%→收盘 -2%；
  - 麦当劳：本集两轮口播（$85 亿计划、-4.3%、近四年最低）。

---

## 三、主要分歧

1. **Muse/Catrini 交易的持续性**：
   - **Danny**（WhatsApp 裂变=真实采用）+ **Sarah Frier**（"惰性品牌"确会被优化）；
   - vs **Mike**（采用率与信任存疑、"可能只是 head fake"）；
   - vs **Kate McShane**（零售业仅沃尔玛真谈 agentic、其余还在降本侧——产业落地远慢于市场叙事）。
2. **油价与柴油禁令**：
   - **Mike**（战术性缓解、禁令解决不了问题、油价有更高地板）；
   - vs **Tyler Kendall 引能源分析师**（炼厂减产→长期更贵）；
   - vs **白宫/Bessent**（研究全面/部分可行性）；
   - vs 盘前 Hochstein/Short 的"政策反噬论"（Surveillance）。
3. **SoftBank 债与 AI 信用**：
   - 表面（**$300 亿订单=需求强**）；
   - vs **Crombie**（仅 3 倍认购、双 B 按 B- 定价、CCC-B 利差疫情以来最阔——市场实际很挑剔）；
   - vs **"信 AI 赢=便宜、怕爆雷=远离"的二元结论**。
4. **Fed 路径**：
   - **Bowersock Hill**（三次 25bp、明年 4 月暂停；"利率其实太低"）；
   - vs **市场定价**（3-4 次之间）；
   - vs 同日 **DB**（12 月+3 月各一次为基准、75 是下限）与 **JPM PB**（合计再两次）——共识方向（还要加）、分歧节奏与终点。
5. **中国配置**：
   - **家族办公室**（极化：剔除者近年占优 vs "不能忽视的市场"）+ **中国 AI"多方面已超我们"**（含能源/数据中心执行力、美国 70% 反数据中心）；
   - vs **调查 DeepSeek/Moonshot 的监管风险**（阿里 -3.7%）；
   - vs **习特会"战术性成果"预期**（农产品/能源/$300 亿降税）。
6. **IPO 窗口**：
   - **指数新高**（纳指 100/综合均历史高位）；
   - vs **"vibes are off"**（Bamboo/核电推迟、除 Anthropic 外 B/C 级资产）；
   - vs **诺和直接上市传闻与 SpaceX 财富效应**。
7. **AI 的社会-政治定价**：
   - **Just Capital**（21% 知美领先、87% 要安全但别减速、30% 或换票、三分之二要中美协议）；
   - vs **Bowersock Hill**（AI 或加剧撕裂、固化结构通胀）；
   - vs **Whitaker**（最大风险=民众失去"AI 为我工作"的信任）。
8. **PG&E/加州模式**：
   - **CEO**（费率最高≠账单最高、两年五次降费、资产价值待解锁、"一段文字"可解）；
   - vs **UBS 下调逻辑**（山火责任改革风险、战略评估、撤长期指引）与 **Fitch 负面展望、低于投资级**；
   - vs **"加州公用事业模式是否辜负了人民"的体制之问**（Danny）。

---

## 四、个股与 ETF 汇总表

| 代码/名称 | 方向 | 幅度（字幕原始口径） | 原因/引语 |
|---|---|---|---|
| META | 上 | 盘中**创去年 9 月以来新高**（盘前 +0.25%） | Muse 延续："what happens when AI takes some of the hassle out of shopping"；数日 **250 万下载** |
| SCHW（嘉信） | 下→反弹 | 昨"sharply lower"、今晨随 Catrini 受害组反弹（无当日幅度） | Catrini 报告点名：agent 比价/换服务商冲击"吃惰性"的金融服务商 |
| MA / V / BRK.B / TSLA | 上（反弹） | 无当日幅度 | "Some of the stocks that have been hit by the Catrini trade... bounced back this morning" |
| MSFT | 上 | 无幅度（Top Call：Stifel 上调至买入） | "Finally getting back on track... strong cash flow... shouldn't need to rely as much on outside financing" |
| PLTR（Palantir） | 上 | **+2%** | AI 交易延续（无单独理由口播） |
| AVGO / AMZN / GOOGL / NVDA / INTC | 下 | 无单独幅度（科技开盘时段约 -2%〔口径疑失真〕） | 大科技获利回吐+利率上行；"part of the reason this equity market is struggling to add on any gains" |
| IONQ | 上 | 盘前**双位数**（同日 Surveillance 口径 +14%） | 实时纠错解码器、仅需一颗标准 CPU——"removing a big hurdle to making quantum computers much larger" |
| BABA | 下 | **-3.7%** | 中国网信部门对 DeepSeek/Moonshot 发起数据安全调查（继 Anthropic 指其经 Claude 路由敏感数据） |
| GIS（通用磨坊） | 下 | **-2%**（Q1 销售超预期但 YTD 大跌） | 国际业务助力+新品（Honey Nut Cheerios 蛋白版）；成本上升与零售商拒绝涨价挤压 |
| MCD（麦当劳） | 下 | **-4.3%**、**近四年最低** | 承诺 **$85 亿**帮加盟商执行多年计划（更好食品/服务/更易运营）——市场读为利空 |
| RCL（皇家加勒比） | 先上后下 | 盘前 **+1%** → 盘中 **-5%** | **$30 亿**收购 Sandals **50%**（其史上最大并购；获加勒比私岛/全包度假入口；分析师"挠头"） |
| NVO（诺和诺德） | 事件 | 无当日幅度 | FT：考虑以**纽约直接上市**替换 ADR（CEO 称无积极讨论）；Top Call：**CFRA 下调至卖出**——"GLP-1〔Ozempic 型〕峰值盈利已过、进入转型期" |
| PCG（PG&E） | 下（背景） | 无当日幅度（"under pressure in recent weeks"） | **UBS 下调至中性**：山火责任改革风险、战略评估、撤回长期盈利指引；Fitch 负面展望、穆迪/标普低于投资级；$20 亿资本开支推迟 |
| NUCLEIO 型（核电 IPO） | 事件 | IPO 规模**仅超 $20 亿** | 纳斯达克今日挂牌；对照：另一家核电公司上周推迟 IPO |
| BAMBOO 型（保险 IPO） | 事件（推迟） | — | 推迟 IPO；行业可比公司走弱 |
| SFTBY（SoftBank，信用端） | —（信用事件） | **$110 亿+**发债、票息**近 10%**（其部分债券史上最高）、订单**$300 亿+**、**3 倍**认购；评级**双 B**、按 **B-** 定价 | 募资投 AI；"if you think you're going to succeed in the AI race... it's actually a cheap deal" |
| UBS | 事件 | 或需增补约 **$170 亿**资本 | 瑞士议会新资本规则；UBS 称"过分"、将继续抗争 |
| MS（摩根士丹利） | 事件 | 无股价读数 | 误发逾 **100 单**亚洲投行推介管线（IPO/PE 出资人/暂停项目）；"real world consequences" 但底线冲击有限 |
| APO（Apollo，私募信贷） | 事件 | 无读数 | "Apollo gating another one of their funds"——噪音已淡、二级份额反而成家族办公室机会 |
| 能源板块（XLE 型） | 上 | "best performer"（The Close 收盘 **+1.1%** 唯一收涨） | 油价回 $100 上方+柴油禁令预期 |
| 公用事业（XLU 型）/可选消费（XLY 型） | 下 | 各约 **-1%** | 利率上行+PG&E 公司利空；消费谨慎 |
| SPX/纳指（指数） | 下 | 标普 **-0.1%→-0.4%**、纳指 **-1%**（昨 -0.0077%/新高后首日回撤） | PMI 强→2Y 4.86/10Y 5.05→估值压力 |

---

## 五、转写失真备查与其他值得记录的细节

- **转写失真备查（本集）**：
  - "DANNY BURGERER/DANNY BERER"=**Danny Berger**（主持人口径失真）；"MIKE BALL/MICHAEL BALL"（按字幕；Matt Miller 本周缺席）；
  - "NOR MEINDA/NORA MELINDA"=Movers/Top Calls 记者（姓氏口径失真、无法确认）；
  - "EMILY CON/EMILY CONAN"=Bloomberg 消费编辑（口径失真）；
  - "BAILEY LIP SCHULTZ"=Bloomberg 资深记者（口径失真、标准拼写无法确认）；
  - "BOTTA KERR/BATA KURB"=Northern Trust Family Office CIO（姓名口径严重失真、无法确认——"XX型"处理）；
  - "PATTY POPPY"=PG&E CEO（口径失真；标准拼写无法确认——"XX型"处理）；
  - "YOKAN SEN/YUKAN SEMPH"=Ben & Jerry's CEO（口径失真；标准拼写无法确认——"XX型"处理）；
  - "NUCLEIO"=今日 IPO 核电公司（口径失真、无法确认）；"BAMBOO"=推迟 IPO 的保险类公司（口径失真、无法确认）；"who a nuclear company"=上周推迟 IPO 的核电公司（无法确认）；
  - "VENODE KOSA/KOSA VENTURES"=明日嘉宾（口径失真；疑 Khosla Ventures 创始人型、无法确认）；
  - "CATRINI/SATRINI"=卖方分析师（报告点名金融/预订平台——姓氏拼写无法确认，按"Catrini 型"记录）；
  - "SCOTT BESANT/BESSANT"=财长 Bessent；"THRRAN/TEHRAN"、"HORMUSE/ORMUSE"=德黑兰/霍尔木兹（口径失真）；
  - "IMPERIA SUMMIT"=NYSE 开盘仪式活动名（口径失真、无法确认）；"LISA SUE"=疑 AMD CEO（按字幕、无法确认）；
  - "RGB TVs"（Best Buy 产品周期，口径疑失真）；"9.2% 2%"（Ben & Jerry's Q2 增速、按 9.2% 记录）；"flavor raz up"（投票主题口味名失真）；
  - "48620/48516"（2Y 收益率 4.8620%/4.8516%）；"505"（10Y 5.05%）；"falling by about 4 and a.5% 4.3%"（麦当劳 -4.3%）；"ends down about 2%"（科技板块、疑 -0.2% 或 -2% 口径失真）；
  - "SHRI RAJ"=Shri Natarajan（一处口径失真）；"LYANNA BAKER"（按字幕）；"JAMES CROMBIE"（按字幕）；
  - "GLOBAL S&P FIGURES"=S&P Global PMI（口径失真）；"DELOBIZATION"=deglobalization（Bowersock 段）。
- **字幕无法确认项**：Catrini 报告原文机构与完整名单；Botta Kerr 型、Patty Poppy 型、Yokan Sen 型的标准姓名；Nucleio/Bamboo/核电推迟 IPO 三家公司身份；"Imperia 峰会"正式名称；明日嘉宾确切身份；"global S&P figures"具体 PMI 数值（仅"5 年高位"口径）。
- **衍生品/波动率/仓位角度（本集相关口播汇总）**：
  - 本集**无 VIX/期权/Gamma 直接读数**（The Close 收盘口径 VIX>15）；
  - 仓位类信息：**柴油期货自高位回落（战术性缓解交易）**、**Catrini 交易的"隔日 put on/take off"结构**、**家族办公室的税务亏损收割与宏观/多空对冲基金回流**、**私募二级份额（continuation vehicle）机会**、**SoftBank 债 3 倍认购 vs IG 千亿订单的认购结构对比**、**IPO 申购分层（B/C 级资产被买方嫌弃）**、**荷兰央行搬金/中国创纪录购金（央行仓位信号）**。
- **轻松一刻**：Danny"我很想现在就在沙滩上"（Nora 报 RCL 时）；"夏天结束了"提醒；Mike"Danny 我明天见，same time same place"；Shri 段"千年谚语：谁没误发过邮件，先扔石头"；Ben & Jerry's 段"花生酱杯是挚爱""一天一勺、一桶吃四天"；Danny 对 CEO 身材"从没见过这么健壮的冰淇淋掌门""我在酿酒厂拿过一顶帽子：'永远别相信瘦的酿酒师'"。
- **数据花絮（本集全部读数索引）**：
  - 股指：昨标普 -0.0077%（精确）；今标普 -0.1%→-0.4%、纳指期货 -0.2%→纳指 -1%；科技开盘时段约 -2%〔口径疑失真〕；Meta 创去年 9 月以来新高；Palantir +2%。
  - 利率：2Y +10.5bp→近 +12bp、4.8516-4.8620（2024/6 以来最高）；10Y +7→+10bp 至 5.05（2007 高位）；30Y +4.5→+6bp；PMI"5 年高位"。
  - 个股：IonQ 盘前双位数（+14% 同日口径）；BABA -3.7%；GIS -2%；MCD -4.3%（近四年最低）；RCL 盘前 +1%→盘中 -5%；PG&E "under pressure in recent weeks"。
  - 信用/并购：SoftBank $110 亿+、近 10% 票息、$300 亿+订单、3 倍认购、双 B 按 B- 定价；CCC-B 利差疫情以来最阔；RCL×Sandals 50%/$30 亿（明年初交割）；MS 泄密 100+ 单；UBS +$170 亿资本。
  - IPO：Nucleio 型核电 >$20 亿今日挂牌；Bamboo（保险）+另一核电上周推迟；诺和考虑直接上市（FT）。
  - 调查（Just Capital）：21% 知美领先；87% 担忧安全；30% 或换票；三分之二望中美协议；Muse 数日 250 万下载；美国 70% 民众反数据中心（家族办公室 CIO 引述）。
  - PG&E：Fitch 负面展望；穆迪/标普低于投资级；$20 亿资本推迟；500 万燃气客户；8GW 清洁能源；两年五次降费率；CPUC 报告 11/1 期限。
  - 家办：$5 亿组建门槛；创投 80%+ 交易涉 AI；Ben & Jerry's Q2 +9.2%、向 People's Action 捐 ~$300 万。
- **本集未出现但背景关注的事项**：
  - VIX/期权/波动率读数（零口播；The Close 收盘口径 VIX>15）；
  - 黄金现货价格读数（仅有央行购金行为口径：荷兰央行搬金、中国创纪录进口金条）；
  - 习特晚宴名单（Zuckerberg/黄仁勋/Musk——见同日 Surveillance Brief②）；
  - PIMCO 三次加息观点（见同日 Surveillance 片间回放引语）；
  - 天然气 ETF、金矿（GDXJ 型）、基础材料板块读数（零口播）；
  - 金融板块指数读数（S&P 金融指数 7 月以来最低、KBW 6 月以来最低——见同日 Surveillance）。
- **时区与播出信息**：本档为开盘档，9:00–10:30 ET 播出（00:00:03"距现金开盘 30 分钟"、00:43:50"开盘 30 分钟"两个锚点）；主持人 Danny Berger 全程、Michael Ball 联袂首小时；当日 12:00 ET 主持人另主持 Bloomberg Deals（嘉宾 Blackstone 副主席 Tom Nides）。
- **本集金句摘录（英文原文+中文）**：
  - Mike（柴油禁令）："**They're really just trying to get to the midterms without anything blowing up.**"——"他们真的只是想撑到中期选举、别爆就行。"
  - Sarah Frier："**It has to be really worth it.**"——"把邮箱/病史/财务交给 Meta——必须真的值得才行。"
  - James Crombie："**If you think you're going to succeed in the AI race... it's actually a cheap deal.**"——"若你信 AI 竞赛会赢，SoftBank 这债其实便宜。"
  - Bowersock Hill："**Interest rates now are actually too low.**"——"按我们的增长与通胀预期，现在的利率其实太低。"
  - Whitaker："**I like my AI, but I'm worried about AI's future impact on society.**"——"我喜欢我的 AI、但担忧 AI 对社会的未来影响。"
  - PG&E CEO："**My customer should not be the insurer of last resort.**"——"我的客户不该是最后的保险人。"
  - Shri Natarajan："**When you leak a hundred deals, hopefully you just get a collective shoulder shrug.**"——"泄一两单会有人暴怒；泄一百单，大家只好耸耸肩。"
- **时段结构备注**：
  - 第一小时（00:00–00:43）：Danny+Mike 双主持，节奏=伊朗/习特会→Catrini→消费财报→信用→IPO→开盘铃→家办 CIO→盘面→Top Calls→零售→MS 泄密；
  - 第二小时（00:43–01:27）：Danny 单人，节奏=标普目标下调→收益率三连读→Movers→并购拆解→AI 民调→PG&E→Ben & Jerry's→习特会 preview→收尾预告；
  - 本集无 VIX/期权读数、无外汇读数；"Open Interest"之名下的仓位视角以**信用认购结构、IPO 申购分层、家办配置、央行购金**为主；
  - 读数口径冲突说明：2Y 收益率两读 **4.8620%（00:57:30）/4.8516%（01:26:36）**——按盘中区间记录；科技板块"about -2%"疑为 -0.2%~-2% 口径失真、引用时注明；
  - 全集收尾一句（01:27:26）："**This is Bloomberg.**"；
  - 本集自校准注：开场"标普昨 -0.0001%"在 00:12:36 自纠为 **-0.0077%**——引用昨日基准时以后者为准。
- **嘉宾观点速查（一句话版）**：
  - **Tyler Kendall（记者×2）**：美伊"再谈=积极信号"但要求未变；习特会看农产品采购/能源商品/$300 亿降税与 AI 热线。
  - **Sarah Frier（科技编辑）**：中方带稀土/铜/锂精炼商反秀肌肉；distillation 调查；Muse 爆红但信任是坎。
  - **Emily Conan 型（消费编辑）**：通用磨坊靠国际业务与新品（蛋白麦片）撑住、但成本与零售商压价两难。
  - **James Crombie（信用）**：SoftBank 仅 3 倍认购、双 B 按 B- 定价；CCC-B 利差疫情以来最阔。
  - **Bailey Lip Schultz 型（IPO）**：诺和直接上市传闻；除 Anthropic 外一级资产多被视为 B/C 级。
  - **Botta Kerr 型（Northern Trust 家办 CIO）**：税务收割>战术；宏观/多空对冲翻身；China 极化但"不能忽视"；Apollo gate 反催二级份额机会。
  - **Kate McShane（高盛零售）**：无恐慌但 K 形真实；沃尔玛是 agentic 唯一积极者；Best Buy 靠执行力+产品周期。
  - **Shri Natarajan（华尔街）**：MS 泄密"尴尬但有限"——亚洲头部地位难被替代。
  - **Emily Bowersock Hill（Bowers Capital）**：标普目标 7,800；三次 25bp（12 月起、明年 4 月暂停）；实资产+国际分散（荷兰央行搬金）。
  - **Martin Whitaker（Just Capital）**：21% 知美领先、87% 要安全、30% 或换票、三分之二望中美协议。
  - **PG&E CEO（Patty Poppy 型）**："一段文字"的政策修补+战略评估解锁资产；给 AI 供电的能力已被资本收缩拖慢。
  - **Ben & Jerry's CEO（Yokan Sen 型）**：价值观商业"焊在模式里"、Q2 +9.2%。
- **与前后日（9/22→9/24）的衔接**：
  - 承接 9/22（周二）：标普收平（-0.0077%）、纳指新高、Catrini 报告砸金融/预订、油价五连跌——本集为**盘中兑现与反转日**。
  - 本日新增变量：**PMI 5 年高位**、**2Y 4.86/10Y 5.05 关口突破**、**SoftBank 3 倍认购的信用分层信号**、**中国调查 DeepSeek/Moonshot**、**麦当劳 $85 亿计划**。
  - 面向 9/24（周四）：习特会谈日（农产品/能源/AI 热线观察点）；Kosla Ventures 创始人上节目；The Close 预告的财报/数据日。
- **与前后节目互证**：
  - 本集上承同日 Surveillance（盘前：2Y 4.80 年内高、Brent 回 100、Catrini 第二日、SoftBank 债、习特晚宴名单）并给出盘中兑现（2Y 4.86、10Y 5.05、纳指 -1、能源最强）；
  - 下接 The Close（S&P -0.8%、能源 +1.1% 唯一收涨、炼厂因 90 天禁令逆跌、RCL 收 -2%、30Y 测 5%）；
  - **RCL×Sandals 三段式**（盘前 +1%→盘中 -5%→收盘 -2%）；**麦当劳 $85 亿计划三次口播**（-4.3%、近四年最低）；**柴油 $6.53/气 $4.47 读数在两档节目完全一致**；
  - Just Capital 的"21%/87%/30%/三分之二"民调与 Surveillance 的"73% 恐惧灾难性 AI"互为补充（口径不同、分别保留）；
  - PG&E 的 UBS 下调（本集 Top Call）与公司 CEO 访谈同集闭环。
