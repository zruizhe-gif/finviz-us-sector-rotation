# 11 Evidence and Output Boundaries｜证据、链接与文件边界

## Finviz主统计报告

继续完整执行原日度/周度原因核验标准：

- 公司公告、监管文件、IR、交易所、政府/行业数据、FactSet、Reuters等；
- 给出可点击来源链接和发布日期；
- 严格时间线；
- 区分直接催化、联动/推断、未核实；
- 盘后事件不得解释正常交易时段/本周收盘前价格。

**主统计报告保留链接。**

当前格式与内容基准为 `AI_reports/daily/finviz_2026-08-11_report.md`（2026-09-05起机械产出统一存放于AI_reports）。除一致性优先统计规则保持不变外，沿用其简洁口径、五范围各一张恰好六行的四列表格、Themes一张恰好六行的四列表格、ETF涨跌分表、一致性最终复核和代码文件审计；每只股票的原因在对应表格行内写完，禁止拆成表后模板段；不得擅自增加无用栏目或把同一信息反复展开。

### 逐股催化专项核查

对五范围及Themes每只入选股票分别执行，不能把一批股票合并做一次泛搜：

1. 核对公司法定名称、代码、事件日期和正常交易时段；
2. 依次检查公司公告/IR、SEC及其他监管文件、最新财报与电话会、指引、并购、融资、合同、监管、分析师评级、内部人交易及可靠新闻；
3. 记录发现了什么，以及盘前、盘中、盘后时间线是否能解释当期价格；
4. 找到直接催化时，写事件、时间和关键数据，再写产业/宏观传导；
5. 全部专项核查后仍无匹配事件，才写“暂未找到同日/同周直接催化”，并在同一股票项中写明主要检索边界及该股票特有的板块联动、权重、流动性或经营背景。

禁止让绝大多数股票套用相同的“未找到硬催化”模板；禁止以“获利了结”“市场情绪”“技术性卖盘”等空话替代核查。

## 独立轮动深度报告

- 后台必须完成同等级核验；
- 最终正文删除全部URL、超链接、引用标记、脚注、来源尾注、References/Sources；
- 不设置资料来源章节；
- 删除来源后不能留下残缺括号或半句话。
- 所有非公司板块、行业、子行业、主题与子主题名称统一写中文；英文只保留在公司法定名称、股票代码、ETF代码和必要的指数/数据范围专名中。
- 禁止展示内部生成过程：修改建议、自我纠正、历史同步、作者、ledger、state、强制覆盖、初始性质/建档、审计结果、本地字幕路径、字幕完整性以及“节目/彭博/字幕提到或验证”等措辞。

## Bloomberg内部研究MD

唯一内容输入是从当前 `SKILL.md` 所在目录解析得到的 `script/` 中、按日期和节目名匹配的本地字幕 TXT。内部研究MD必须保留：

- 本地字幕文件绝对路径；
- 节目日期和节目名称；
- 本地字幕全文读取状态；
- 字幕能够确认的研究内容与必要信息缺口。

禁止为节目研究访问 YouTube 获取或判断字幕、Transcript、视频正文、标题简介或片段，也禁止保留视频URL作为内容证据。没有匹配的本地字幕时，节目MD全文只写 `LOCAL_TRANSCRIPT_MISSING`；不得用网络替代内容、标题、简介、旧摘要或零散片段补写节目事实。

这些本地字幕总结是内部研究记录，不是最终发表文章。

## 输出文件

### DAILY

- `AI_reports/daily/finviz_YYYY-MM-DD_report.md`（Finviz主统计报告，保留核验链接；2026-09-05起与AI候选稿同存于AI_reports/daily/，不再写入Skill根目录）
- `AI_reports/daily/finviz_YYYY-MM-DD_stocks.txt`
- `AI_reports/daily/finviz_YYYY-MM-DD_all_codes.txt`
- `AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`（AI轮动候选稿，2026-08-16起新命名，月日不补0；禁止写入 `history/daily/`，禁止放到Skill根目录）

### WEEKLY

- `AI_reports/weekly/finviz_weekly_YYYY-MM-DD_report.md`
- `AI_reports/weekly/finviz_weekly_YYYY-MM-DD_stocks.txt`
- `AI_reports/weekly/finviz_weekly_YYYY-MM-DD_all_codes.txt`
- `AI_reports/weekly/美股板块轮动观察｜YYYY.M.D.md`（AI轮动候选稿，日期取该周最后一个交易日；禁止写入 `history/weekly/`）

两个TXT规则完全按原任务执行。

### 作者正式历史

- 只有作者人工修改或明确确认后的报告才进入 `history/daily/`（或 `history/weekly/`），属于 `AUTHOR_CONFIRMED_HISTORY`；2026-08-16起正式稿命名 `美股板块轮动观察｜YYYY.M.D.md` / `.docx`（月日不补0），旧的 `us_sector_rotation_YYYY-MM-DD.md` 规范命名仍视为正式历史（既有文件不重命名）；
- 第二天行情性质与术语同步只从 `history/` 读取，禁止从 `AI_reports/` 反向更新作者状态；
- 每日催化研究按股票代码去重缓存于 `research/finviz/YYYY-MM-DD/catalyst-cache.json`，同一股票只研究一次（两步研究，命中同日直接事件立即停止；异常样本才深挖）。
