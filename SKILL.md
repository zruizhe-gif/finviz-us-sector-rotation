---
name: finviz-us-sector-rotation
description: 使用稳定程序完成Finviz美股日度或周度机械统计，并基于增量作者状态、一次性股票催化缓存和Bloomberg本地字幕缓存生成连续性的六部分板块轮动AI候选报告。适用于最新已收盘交易日或完整交易周的Finviz统计、板块轮动分析、作者正式报告后的状态同步，以及用户明确要求时的Skill规则或代码维护。
---

# Finviz US Sector Rotation

## 先判定运行模式

每次任务先读取 `references/14-runtime-modes-and-incremental-workflow.md`，再根据用户当前请求选择模式。

### DAILY_WEEKLY_RUN

这是默认模式。凡用户要求执行日度或周度Finviz统计、轮动分析或正常更新运行数据，且没有明确要求修改Skill、规则或代码，均使用本模式。

只允许更新：

- `state/market-state-ledger.yaml`；
- `state/author-terminology.yaml`；
- 当日或当周 `research/` 运行数据；
- Bloomberg节目摘要与宏观缓存；
- 股票催化缓存；
- Finviz机械统计数据产物；
- `AI_reports/` 中的AI候选稿。

禁止修改Skill规则、templates、稳定脚本、Python代码、validator或manifest；禁止执行全Skill验证、全包哈希审计、GitHub登录、commit或push；禁止重读历史对话、旧负面案例、全部旧报告或未变化的原始字幕；禁止调试正常工作的代码。

### DEVELOPMENT

只有用户当前请求明确包含“修改Skill”“修改规则”“修改代码”“修复长期系统性错误”等要求时才进入本模式。

本模式允许在用户指定范围内维护 `SKILL.md`、`references/`、`templates/`、稳定脚本、Python代码、validator和manifest，但“允许”不等于自动执行。严格服从当前请求的文件范围和禁止项。

GitHub始终需要用户在当前请求中明确授权。仅仅进入DEVELOPMENT，不构成登录、创建仓库、commit、push或修改远端可见性的授权。

## 三层数据边界

### 1. Skill规则层

包括 `SKILL.md`、`references/`、`templates/` 和稳定运行脚本，只保存长期稳定规则。作者对具体板块的新判断、具体ETF或主题的中文名称、某一天的翻译修正及最新正式报告日期不得写入这一层。

### 2. 作者动态状态层

统一位于 `state/`：

- `state/market-state-ledger.yaml` 保存最新基础行情性质、作者精确阶段、日期与来源；
- `state/author-terminology.yaml` 保存作者最新名称与翻译映射。

具体行情判断和术语值只从state与新增作者正式报告读取，不在规则文件中复制一份。

### 3. AI运行结果层

AI自动生成的轮动报告只能写入：

- 日度：`AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`；
- 周度：`AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`。

`AI_reports/` 是AI候选稿。不得自动复制、移动或覆盖 `history/daily/` 与 `history/weekly/` 中的文件，也不得把AI候选稿反向认定为作者正式判断。

## 规则与数据优先级

规则优先级：

1. 用户当前请求中的明确要求；
2. `references/14-runtime-modes-and-incremental-workflow.md`；
3. `references/03-current-overrides-and-precedence.md`；
4. 原日度、周度任务合同；
5. 其他按需加载的reference与模板。

数据优先级：

1. `history/daily/` 中最新选定的 `AUTHOR_CONFIRMED_HISTORY`，包括同日期内容变化或用户明确指定的更新文件；
2. state中保留的作者精确判断与作者术语；
3. state中的五类基础行情性质；
4. `AI_reports/` 候选稿、旧state和Codex此前自动判断。

规范命名本身不能证明一份文件经过作者确认。只有作者人工修改或用户明确确认的报告才能成为 `AUTHOR_CONFIRMED_HISTORY`。

每次DAILY_WEEKLY_RUN开始时，必须定位最新作者正式报告，读取报告日期并计算SHA-256，与 ledger 的 `author_history_as_of`、`latest_author_confirmed_report`、`latest_author_confirmed_report_sha256` 比较。日期更晚、同日期哈希变化或用户明确指定同一交易日另一更新文件时，必须重读并同步；三者均未触发时才复用已有状态而不读正文。同日期重读不得制造虚假基础状态变化记录。

## 按需加载，不做全包预读

DAILY_WEEKLY_RUN不得因为“熟悉规则”而完整读取全部reference、01/02原任务全文、legacy范文或旧负面案例。

正常成稿的主要输入固定为：

1. `research/finviz/YYYY-MM-DD/runtime-brief.json`；
2. `research/finviz/YYYY-MM-DD/catalyst-brief.json`；
3. `daily-macro-context.md` 或一周的日度宏观上下文；
4. 本次需要的 `market-state-ledger` 状态；
5. 最新 `author-terminology`；
6. 最新一期作者正式报告的新增或变更内容；
7. `references/09-author-voice-style.md`；
8. `references/10-hard-bans.md`；
9. 对应报告模板与唯一一次最终审计清单。

`calculated-statistics.json`、coverage、mandatory coverage、hierarchy/perf、ETF audit与完整 `catalyst-cache.json` 永久保留为机器底稿。稳定后处理程序 `scripts/build_runtime_briefs.py` 在不改变任何统计结果的前提下生成两个brief。正常DAILY_WEEKLY_RUN中，LLM不得全文读取这些大型底稿；只有brief指出具体异常或终审某一项失败时，才定点打开对应文件或ticker记录。详细边界见 `references/16-runtime-briefs-and-batch-catalysts.md`。

只有发生明确缺口时才读取对应reference或原始材料：字幕摘要缺失或哈希变化时读取原字幕；ticker催化缓存缺失时补该ticker；稳定程序真实报错时停止并报告。缺什么只补什么。

## Finviz机械统计不可简化

使用项目现有稳定抓取、计算和输出程序生成机械统计，不让模型手工遍历全部股票或重新计算已有中间结果。保持以下规则完整生效：

- All Stocks、S&P 500、Dow Jones 30、Nasdaq 100、Russell 2000五个股票范围；
- Themes与ETFs；
- 一致性优先、清一色候选优先、不足3项时才按平均表现补位；
- 板块与主题宽度、准确收益、涨3/跌3和完整性审计；
- ETF排除杠杆与反向产品，并按相同经济敞口去重；
- 股票去重集合与两个TXT。

完整机械底稿生成后运行 `scripts/build_runtime_briefs.py`。它只建立LLM读取层，不替代、删减或重算Finviz核心逻辑；其一致性、coverage、ETF、固定观察池和ticker覆盖断言失败时，停止成稿并定点核查完整底稿。

原日度与周度任务全文继续保留为机械统计合同，但DAILY_WEEKLY_RUN不重复全文读取。DEVELOPMENT修改机械规则或稳定程序时，才按需读取原合同与 `references/04-consistency-first-statistics.md`。

正常运行不得修改 `fetch_and_build.py`、`calculate.py` 或 `generate_outputs.py`。程序真实报错时停止并报告，不在日常任务中顺手调试或重写代码。

股票催化第一轮必须由 `scripts/batch_catalyst_screen.py` 一次覆盖全部唯一ticker，不得为每只普通股票启动独立高推理工作线。只有候选事件、异常涨跌、财报/指引、并购、融资或资本结构、监管、重大合同、明显脱离板块或证据冲突才进入模型定点深度核验；无候选事件且与板块方向一致的ticker完成必要机械核查后立即记录“暂未找到同日直接催化”。

## 行情性质与作者精确阶段

AI能够自主创建的 `base_state` 只有：上涨趋势、下跌趋势、大型震荡、头部、底部。

作者正式报告可以给出更具体的 `author_exact_state`。创建时同时记录其五类父状态 `author_exact_base_state`、来源 `author_exact_source_report`，并将 `author_exact_active` 设为 `true`。只有 `author_exact_active: true` 且当前 `base_state` 等于 `author_exact_base_state` 时，才在正式报告中逐字展示作者精确阶段。AI只能继承，不能创造、扩展、压缩或改写作者精确阶段，也不能把它复制给其他板块。

作者精确阶段不是第六种AI基础分类；state必须同时保留五类 `base_state` 与作者原话及来源。若真实结构证据使 `base_state` 离开其父状态，机械地将 `author_exact_active` 设为 `false`，保留作者原话、日期、父状态和来源作为历史记录，正式报告改为显示新的 `base_state`。以后即使 `base_state` 返回旧父状态也不得自动复活旧精确阶段，只有较新的作者明确重申才可重新激活。

## 轮动报告固定边界

Finviz机械统计完成后建立去重的 `MANDATORY_ROTATION_COVERAGE_SET`。第二部分只精选三项轮入与三项轮出；第三部分只分析这六项；第四部分固定按 `references/15-fixed-section-four-etf-pool.md` 的顺序写24行ETF观察池，只有当天涨3/跌3中存在可靠代表ETF的其他行业才追加；无可靠代表ETF的Theme不得进入第四部分。该展示边界不改变Finviz机械统计、mandatory coverage或涨3/跌3规则。

第四部分固定三列：`板块/ETF`、`当天表现`、`行情性质及说明`。指定的双ETF行必须同时取得两只ETF表现并解释方向或幅度分化；能源与金融各自合并为一行。状态从唯一 ledger 的ETF状态与作者连续性字段读取，不从一次性外部参考池重复读取。

日度轮动报告标题固定为 `美股板块轮动观察｜YYYY.M.D`，月份和日期不补0。Markdown成稿的标题与六个部分标题全部使用普通正文加粗，不得使用 `#`、`##`、`###` Heading语法；DOCX标题使用加粗正文段落且不设置大纲级别，表格字体比正文字体小一号。

独立轮动报告固定六部分，使用全中文板块与主题名称；具体译名从 `state/author-terminology.yaml` 读取。正文不得展示内部同步、缓存、审计、字幕来源或状态数据库过程，不得含超链接、技术指标或投资建议。公司名称必须带股票代码。

## 完成条件

只执行一次最终综合审计。优先使用两个brief中的完整性断言；通过后立即结束。发现问题时只修正失败项并定点回查对应大型底稿或ticker，不重新开始第二轮或第三轮全量审计。

DAILY_WEEKLY_RUN完成后，不修改Skill、不重建manifest、不运行全Skill validator、不执行全包hash审计，也不访问GitHub。
