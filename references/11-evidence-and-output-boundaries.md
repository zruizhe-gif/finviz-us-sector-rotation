# 11 Evidence and Output Boundaries｜证据、缓存与文件边界

## Finviz 机械统计报告

Finviz 统计固定使用现有稳定代码完成，模型不得为了再次确认而手工遍历全部股票。机械层继续保留：

- 五个股票范围、Themes 与 ETF；
- 一致性优先、清一色优先、不足三项才按平均表现补位；
- ETF 去杠杆、反向和相同经济敞口；
- calculated statistics、coverage audit、mandatory rotation coverage set、股票去重集合、ETF 结果与两个 TXT；
- 准确涨跌幅、严格时间线、直接催化与联动/推断的区分；
- 主统计报告中的可点击来源链接和发布日期。

五个股票范围与 Themes 各保留恰好六行四列表格，股票原因写在对应表格行内。正常日度运行不得修改或调试正常工作的 `fetch_and_build.py`、`calculate.py`、`generate_outputs.py`；程序真实报错时停止并报告，不得在 DAILY_WEEKLY_RUN 中现场改代码。

## 股票催化一次去重缓存

当日机械统计完成后，先从其入选股票建立唯一 ticker 集合。跨指数、Themes 或板块重复出现的同一股票只研究一次，随后由所有出现位置共同复用该 ticker 的缓存结论。

缓存固定保存于：

`research/finviz/YYYY-MM-DD/catalyst-cache.json`

以股票代码为 key。结构遵守 `templates/catalyst-cache.json`，至少保存公司名称、全部入选位置、涨跌幅、研究层级、结论状态、直接事件及时间线、必要来源、已确认联动、停止原因和完成时间。缓存元数据保存来源统计文件及其 SHA-256、唯一 ticker 数和 ticker 集合指纹。

同一交易日期内，ticker 记录完整且来源统计仍覆盖该股票时，直接记为 `CATALYST_CACHE_HIT`，禁止重复搜索。统计集合变化时只研究新增或未完成 ticker；已经完成的记录继续复用。

### 普通股票固定两步

普通股票只执行以下顺序：

1. 搜索“公司名/股票代码 + 日期 + 当日新闻/财报/公告”；
2. 第一步结果含糊、需要确认原始披露或确有必要时，再检查公司 IR 或 SEC/其他对应监管来源。

发现能够解释当期正常交易时段的明确直接事件后立即停止继续搜索，保存事件、发布时间、关键数据与时间线。不得为了让材料显得更完整继续穷举其他表单或新闻。

两步仍没有独立事件时，固定记录：

- 日报：`暂未找到同日直接催化`
- 周报：`暂未找到同周直接催化`

随后依据已经由机械统计、板块宽度、行业事实或宏观上下文确认的联动，给出该股票的具体解释。不得用“获利了结”“技术性卖盘”“市场情绪”等空话，也不得为了证明“没有事件”继续穷举 SEC 表单、评级、内部人交易、融资、合同和监管信息。

### 深度升级的唯一条件

只有以下情况才进入完整事件调查，并在缓存中保存 `research_level: deep` 与明确的 `deep_research_reason`：

- 异常大涨或大跌；
- 财报或重大指引变化；
- 并购；
- 监管事件；
- 融资或资本结构冲击；
- 重大合同；
- 股价明显脱离已确认的板块方向；
- 信息互相冲突。

没有命中上述条件时，不得自行升级研究深度。直接事件一经确认仍执行“找到即停”。

## Bloomberg 内部研究缓存

Bloomberg 的唯一字幕输入、直接子目录扫描、SHA-256 判定、节目 MD 元数据、`PROGRAM_SUMMARY_CACHE_HIT`、日度和周度宏观读取边界统一遵守 `references/08-bloomberg-tv-macro-context.md` 与 `templates/bloomberg-program-note.md`。

节目 MD 的 `source_file` 必须是 Skill 根目录相对路径，并保存 `source_sha256`。相同哈希命中缓存时禁止重新读取原始字幕全文。日度报告主要读取 `daily-macro-context.md`；周度报告只读取本周各日 `daily-macro-context.md` 并使用 `week-macro-context.md`，默认不得回到周内原始字幕。

## 独立轮动候选报告的固定输入

成稿阶段只读取已经整理好的中间结果：

1. 当日/当周 calculated statistics；
2. mandatory rotation coverage set；
3. catalyst cache；
4. daily macro context 或 week macro context；
5. 最新 market-state-ledger；
6. 最新 author-terminology；
7. 上一期作者正式报告；
8. Voice Style；
9. Hard Bans。
10. `references/15-fixed-section-four-etf-pool.md` 中已经固化的第四部分观察池与去重关系。

成稿阶段不得重新抓 Finviz、全网重查所有股票、重读 Bloomberg 原始字幕或重读全部历史报告。缺什么只补什么。

正式候选报告删除全部 URL、超链接、引用标记、脚注、来源尾注和 References/Sources；删除来源后不得留下残缺括号或半句话。所有非公司板块、行业、子行业和主题名称按作者术语表统一写中文。禁止展示缓存、历史同步、ledger、state、强制覆盖、字幕来源或审计过程。

## 输出文件边界

Finviz 机械统计报告与 TXT 继续按现有数据产物结构保存：

### DAILY

- `finviz_YYYY-MM-DD_report.md`
- `finviz_YYYY-MM-DD_stocks.txt`
- `finviz_YYYY-MM-DD_all_codes.txt`
- `AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`

### WEEKLY

- `finviz_weekly_YYYY-MM-DD_report.md`
- `finviz_weekly_YYYY-MM-DD_stocks.txt`
- `finviz_weekly_YYYY-MM-DD_all_codes.txt`
- `AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`

`AI_reports/` 只保存 AI 候选稿。AI 不得自行复制、移动或覆盖 `history/daily/`；只有作者人工修改或明确确认的版本才进入正式历史。
