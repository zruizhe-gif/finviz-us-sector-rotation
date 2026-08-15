# 14 Runtime Modes and Incremental Workflow｜运行模式与增量工作流

本文件是日度、周度正常运行和Skill开发维护的统一入口。目标是在不降低Finviz统计完整性和轮动分析质量的前提下，只读取本次真正新增或缺失的材料。

## 目录

1. 先选择模式
2. 三层目录职责
3. 日常启动时的增量作者同步
4. 行情性质数据模型
5. 作者术语增量表
6. Finviz机械统计
7. 股票催化一次去重缓存
8. Bloomberg字幕永久缓存
9. 轮动成稿的固定输入
10. AI报告与正式历史隔离
11. 唯一一次最终审计
12. DAILY_WEEKLY_RUN中永久删除的操作

## 1. 先选择模式

### DAILY_WEEKLY_RUN

默认模式。用于：

- 最新已完成正常收盘交易日的日度任务；
- 最新完整交易周的周度任务；
- 正常更新state、research、缓存和AI候选报告。

本模式允许写入：

- `state/market-state-ledger.yaml`；
- `state/author-terminology.yaml`；
- 当期 `research/finviz/`；
- 当期 `research/bloomberg-tv/`；
- Finviz机械统计报告和TXT数据产物；
- `AI_reports/daily/` 或 `AI_reports/weekly/`。

本模式禁止：

- 修改 `SKILL.md`、references、templates；
- 修改Python或其他稳定程序；
- 修改validator或manifest；
- 运行全Skill validator或全包hash审计；
- GitHub登录、创建仓库、commit、push或远端配置修改；
- 重读历史对话、01/02原任务全文、legacy范文、旧负面案例和全部旧报告；
- 重读哈希未变化的Bloomberg原始字幕；
- 重复研究已有缓存的ticker；
- 调试正常工作的代码。

### DEVELOPMENT

只有用户当前请求明确要求修改Skill、修改规则、修改代码或修复长期系统性错误时使用。

只修改用户当前授权范围。DEVELOPMENT只是允许维护规则或代码的模式门，不自动授权manifest重建、全包验证或GitHub操作。GitHub始终要求用户在当前请求中明确授权。

## 2. 三层目录职责

### Skill规则层

`SKILL.md`、`references/`、`templates/` 和稳定程序只保存跨日期长期有效的规则。不得写入具体板块的最新状态、某次作者判断、具体术语映射或最新正式报告日期。

### 作者动态状态层

`state/` 保存：

- 最新五类基础行情性质；
- 作者明确给出的特殊阶段原话；
- 作者最新名称与翻译；
- 作者正式历史同步日期；
- 每条状态的来源与日期。

### AI运行结果层

AI自动轮动稿保存为：

- `AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`；
- `AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`。

`history/daily/` 和 `history/weekly/` 仅存作者人工修改或明确确认的正式报告。文件名规范不能单独证明作者确认。

## 3. 日常启动时的增量作者同步

按以下顺序执行一次：

1. 读取 `state/market-state-ledger.yaml`；
2. 读取 `state/author-terminology.yaml`；
3. 按作者正式版本优先级找到 `history/daily/` 中最新正式报告，只取得文件名、报告日期与必要元数据；
4. 计算该文件的SHA-256，并与 ledger 的 `author_history_as_of`、`latest_author_confirmed_report`、`latest_author_confirmed_report_sha256` 比较；
5. 日期更晚、同日期SHA-256变化，或用户明确指定同一交易日另一份更新后的正式文件时，必须重新读取对应正式稿；其余情况不读取正文；
6. 有多个未同步的较新交易日报告时，按日期从旧到新读取；同日期只选优先级最高的正式版本；
7. 从需同步报告第四部分提取全部最新行情性质，并同步作者精确阶段的父状态、有效性和来源；
8. 同时提取作者明确修正的名称、翻译和其他明确的事实口径、分类、因果或表达错误；术语只更新 `state/author-terminology.yaml`，动态修正不写回Skill；
9. 同步完成后更新真实来源文件与SHA-256；日期更晚时推进 `author_history_as_of` 与兼容字段 `as_of`，同日期修订时日期游标保持不变；
10. 同日期重读必须幂等，不得仅因重新同步制造行情性质变化记录；
11. 为轮动成稿只读取最新一期作者正式报告一份，不回放全部历史。

“日期没有变化”不等于“作者判断没有变化”。作者历史识别由报告日期、正式文件路径和SHA-256共同完成。AI运行日期、AI候选稿和AI基础状态更新不得推进作者历史游标或改写最新正式报告哈希。

## 4. 行情性质数据模型

AI可自主创建的 `base_state` 仅允许：

1. 上涨趋势；
2. 下跌趋势；
3. 大型震荡；
4. 头部；
5. 底部。

作者可以在正式报告中给出更具体阶段。state至少同时保存：

```yaml
base_state: <五类之一>
base_state_as_of: YYYY-MM-DD
author_exact_state: <作者原话或null>
author_exact_state_as_of: YYYY-MM-DD
author_exact_base_state: <五类父状态或null>
author_exact_active: <true或false>
author_exact_source_report: <真实作者正式文件或null>
source: <真实来源>
source_report: <真实作者正式文件；当前明确指令则不伪造路径>
```

执行规则：

- `author_exact_state` 只能由作者正式报告创建或由较新作者正式报告覆盖；
- 作者创建或重申精确阶段时，必须记录兼容的 `author_exact_base_state` 和独立来源，并将 `author_exact_active` 设为 `true`；
- AI只能继承作者原话，不能自行发明、扩展、缩写或改写；
- AI不得把某个项目的作者精确阶段复制给其他项目；
- 只有 active 为 true 且当前 `base_state` 等于父状态时，下一期报告才继续使用作者原话；
- 真正结构破坏允许AI更新五类 `base_state`；一旦离开父状态，必须机械地将旧精确阶段设为 inactive，但不得删除或改写其作者原话、日期、父状态和来源；
- `base_state` 后来返回旧父状态也不得自动复活旧精确阶段，只有较新作者明确重申才可重新激活；
- 趋势维持与破坏条件始终按 `base_state` 判断；
- AI报告不得反向把正文措辞写成新的作者精确状态。

首次出现且需要分类的项目由AI从五类 `base_state` 中选择，记录运行证据与来源；不得创造第六种基础类别。

## 5. 作者术语增量表

具体名称和翻译只保存在 `state/author-terminology.yaml`。每条至少记录：

```yaml
preferred_zh: <作者用词>
as_of: YYYY-MM-DD
source: <用户明确要求或作者正式报告>
source_report: <适用时填写>
```

可按需要记录禁用别名或原始源标签。运行时遵守：

- 作者新正式报告中的明确修正覆盖旧映射；
- 不根据当日ETF成分、代表股票或临时表现重新命名；
- 不把相近但独立的源标签合并；
- AI报告只能读取并执行映射，不能从AI候选稿反向更新作者术语；
- 单个术语修正属于 `DAILY_STATE_UPDATE`，只更新state，不修改Skill规则。

## 6. Finviz机械统计

每天或每周只做：

1. 获取目标日期或交易周的最新Finviz map数据；
2. 运行项目现有稳定抓取、计算和输出程序；
3. 生成 calculated statistics；
4. 生成 coverage audit；
5. 生成 `MANDATORY_ROTATION_COVERAGE_SET`；
6. 生成股票去重集合、ETF结果和两个TXT。

稳定程序必须继续实现：

- 五个股票范围；
- Themes；
- ETFs；
- 一致性优先；
- 清一色优先；
- 清一色不足3项才按平均表现补位；
- ETF排除杠杆和反向产品；
- 相同经济敞口去重；
- 完整性审计。

模型不得为了再次确认而手工遍历全部股票。正常运行禁止修改 `fetch_and_build.py`、`calculate.py`、`generate_outputs.py`。程序真实报错时立即停止并报告；需要修复时由用户另行授权进入DEVELOPMENT。

## 7. 股票催化一次去重缓存

使用：

`research/finviz/YYYY-MM-DD/catalyst-cache.json`

ticker为key。同一股票无论出现在多少指数、主题或板块，只研究一次，后续直接复用缓存。

普通股票研究顺序：

1. 搜索公司名或ticker、目标日期和当日新闻、财报或公告；
2. 只有必要时检查公司IR或SEC；
3. 找到明确同日直接事件后立即停止继续搜索；
4. 两步仍没有独立事件时，记录“暂未找到同日直接催化”，再依据已经确认的板块、行业或宏观联动解释。

不得为了证明“没有事件”继续穷举所有SEC表单、评级、内部人交易、融资、合同和监管信息。

只有以下情况升级完整事件调查：异常大涨大跌、财报、并购、监管、融资、重大合同、明显脱离板块或信息互相冲突。

## 8. Bloomberg字幕永久缓存

原始字幕只来自Skill根目录直接子目录 `script/`。禁止自行访问YouTube或其他网站寻找替代字幕、Transcript、视频正文、简介或片段。

每个节目研究MD必须记录：

```yaml
source_file: script/...
source_sha256: <sha256>
```

处理顺序：

1. 计算匹配字幕的SHA-256；
2. 检查节目MD是否存在且 `source_sha256` 相同；
3. 相同则记录或识别 `PROGRAM_SUMMARY_CACHE_HIT`，禁止重新读取原字幕全文；
4. 仅在新节目、字幕哈希变化或summary缺失时读取原字幕并重建节目MD；
5. 某档节目没有本地字幕时只记录 `LOCAL_TRANSCRIPT_MISSING`，不得寻找网络替代内容；
6. 从有效节目MD生成或更新 `daily-macro-context.md`。

日度轮动报告主要读取 `daily-macro-context.md`，不得在成稿阶段重读四份字幕或四份节目MD。

周度报告读取过去一周的 `daily-macro-context.md` 并生成周度宏观上下文，默认禁止重新读取周内原始字幕或全部节目MD。

## 9. 轮动成稿的固定输入

成稿阶段只读取：

1. 当期 calculated statistics；
2. mandatory rotation coverage；
3. catalyst cache；
4. daily macro context或一周的日度宏观上下文；
5. 最新market-state-ledger；
6. 最新author-terminology；
7. 最新一期作者正式报告一份；
8. `09-author-voice-style.md`；
9. `10-hard-bans.md`；
10. 对应报告模板。

日度第四部分另按 `references/15-fixed-section-four-etf-pool.md` 读取已经固化的24行、去重关系和多ETF交叉验证规则，并从唯一 `market-state-ledger.yaml` 的 `etf_states.states` 读取ETF状态。建立该ledger域时使用的一次性外部参考池不属于日常输入，不得再次读取。

成稿阶段禁止重新抓取Finviz、全网重查所有股票、重读Bloomberg原始字幕或重读全部历史报告。缺少哪一项，只回到对应阶段补哪一项。

## 10. AI报告与正式历史隔离

- 日度AI候选稿写入 `AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`；标题同样为 `美股板块轮动观察｜YYYY.M.D`，月份和日期不补0；
- 周度AI候选稿写入 `AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`；
- AI不得自动写入、复制或覆盖 `history/daily/` 与 `history/weekly/`；
- 作者人工修改或明确确认后，由作者正式版本进入history；
- 下一次作者状态同步只读取history中的新增正式报告；
- 不得从AI_reports反向更新 `author_exact_state`、作者术语或作者同步游标。

Finviz机械统计报告和TXT继续按现有数据产物结构保存，不迁入 `AI_reports/`。

## 11. 唯一一次最终审计

完成草稿和出版清理后，只执行一次综合审计，检查：

- 涨3/跌3完整性；
- 一致性优先；
- TXT代码集合；
- 当期重要方向是否进入分析；
- 五类 `base_state` 合法；
- `author_exact_state` 是否原样继承；
- 作者术语映射是否执行；
- 历史连续性；
- 非趋势状态没有持续性分析；
- 六部分结构；
- Hard Bans；
- 无超链接；
- 无技术指标；
- 无投资建议；
- 所有公司名称带股票代码。

通过后立即结束。若存在失败项，只修正该项并定点复查，不重新运行第二轮或第三轮全量审计。

## 12. DAILY_WEEKLY_RUN中永久删除的操作

- 全文重读原日度、周度合同；
- 重读历史对话；
- 重读旧负面案例和legacy范文；
- 回放全部历史报告；
- 重读哈希未变化的字幕；
- 对同一ticker重复研究；
- 为证明无催化而穷举所有事件类型；
- 模型手工重新遍历全部Finviz股票；
- 调试或修改正常代码；
- 修改Skill、references、templates；
- 重建manifest；
- 运行全Skill validator；
- 全包hash审计；
- GitHub登录、commit或push；
- 第二轮、第三轮全量复核。
