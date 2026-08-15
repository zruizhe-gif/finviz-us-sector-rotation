# 06 Market State Continuity｜行情性质连续性

## 三层边界

### Skill规则层

`SKILL.md`、`references/`、`templates/` 与稳定运行脚本只保存长期规则。日常行情性质、作者对单一板块的最新判断、ETF或主题中文名称修正，不写回Skill规则层。

### 作者动态状态层

`state/market-state-ledger.yaml` 是唯一的行情性质状态表；`state/author-terminology.yaml` 是独立的作者命名与翻译状态表，不构成第二套行情性质数据库。

作者术语字段统一使用 `preferred_zh`。来源优先级为：用户当前明确指令 `AUTHOR_EXPLICIT_INSTRUCTION` 高于 `AUTHOR_CONFIRMED_HISTORY`，更新日期更晚的作者正式报告高于较早报告。

### AI运行结果层

AI自动生成的轮动候选稿只写入：

- `AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`
- `AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`

AI不得自动把候选稿复制、移动或覆盖到 `history/daily/` 或 `history/weekly/`，也不得从 `AI_reports/` 反向更新作者判断、`author_exact_state` 或作者术语。

## AUTHOR_CONFIRMED_HISTORY

`history/daily/` 和 `history/weekly/` 只保存作者人工修改完成或作者明确确认的正式版本。文件扩展名可以是DOCX或规范MD，但“规范命名”本身不构成作者确认；只有人工修改、明确确认或由作者放入正式历史目录后，才属于 `AUTHOR_CONFIRMED_HISTORY`。

同一日期存在多份作者正式版本时：

1. 用户明确指定的版本优先；
2. 否则作者人工修改版优先；
3. 仍无法区分时，以同日最新修改的正式文件优先。

AI候选稿不因文件名规范、内容完整或日期更新而自动升级为正式历史。

## 每日增量同步

每个新交易日或新交易周开始前：

1. 先读取 `state/market-state-ledger.yaml` 与 `state/author-terminology.yaml`；
2. 按本文件的同日版本优先级找到 `history/daily/` 中最新作者正式报告；只读取文件名、报告日期和必要元数据，不先读取正文；
3. 对该文件计算SHA-256，不把原始DOCX或MD正文读入模型；
4. 将报告日期、文件路径和SHA-256分别与 ledger 的 `author_history_as_of`、`latest_author_confirmed_report`、`latest_author_confirmed_report_sha256` 比较；
5. 以下任一条件成立时，重读对应作者正式稿并执行同步：报告日期晚于游标；报告日期等于游标但SHA-256变化；用户明确指定同一交易日另一份更新后的正式文件；
6. 若存在多份日期晚于游标且尚未同步的正式报告，仍按日期从旧到新读取；同日期只同步按优先级选出的正式版本；
7. 从需要同步的正式报告第四部分提取全部最新行情性质，并同步 `author_exact_state` 及其父状态、有效性和来源；同一项目由较新作者判断覆盖较旧判断；
8. 同时提取作者明确修正的板块、Theme、ETF和行业中文名称，只更新 `state/author-terminology.yaml`；其他明确的事实口径、分类、名称、因果或表达修正只按其动态边界继承；
9. 同步完成后，更新 `author_history_as_of`、兼容字段 `as_of`、`latest_author_confirmed_report` 和 `latest_author_confirmed_report_sha256`。同日期修订时日期游标保持不变，只更新实际文件路径和哈希；
10. 同日期重复同步必须幂等：只有字段值真实变化时才更新对应状态，不得仅因重新读取而追加 `change_log`、改变 `base_state_as_of` 或制造虚假行情性质变化。

当日期、路径和哈希均未触发以上条件时，不读取正式稿正文。不得为了确认“没有变化”重新读取全部历史，也不得从AI候选稿推进作者历史同步游标。

## Ledger兼容Schema

顶层字段：

- `schema_version`：当前为3；
- `author_history_as_of`：已同步的最新作者正式报告日期；
- `as_of`：向后兼容别名，必须与 `author_history_as_of` 同值，并具有相同的作者历史同步游标语义；
- `latest_author_confirmed_report`：真实存在的最新作者正式文件；
- `latest_author_confirmed_report_sha256`：上述文件同步时的SHA-256，使用64位十六进制字符串；
- `latest_source_report`、`baseline_source`：兼容旧读取器的来源别名；
- `allowed_states`：只约束AI可创建的五种基础行情性质。

同一 `state/market-state-ledger.yaml` 还可包含 `etf_states` 域，用于保存作者明确给出的ETF级状态。它属于唯一ledger，不是第二份状态文件：

- `etf_states.as_of`、`source` 和 `source_description` 记录整批作者状态的日期与来源；
- `etf_states.states.<ticker>` 保存该ETF的 `base_state`、`author_exact_state`、`author_exact_base_state` 与 `author_exact_active`；
- 作者精确阶段的日期由该批次 `etf_states.as_of` 记录；
- 同一ticker同时出现在 `sectors_and_themes` 与 `etf_states.states` 时，日期更新且来源优先级更高的作者ETF状态是第四部分的当前权威值；旧板块条目继续保留兼容性和历史，不得与ETF域并列成为两个当前结论；
- 一次性外部ETF参考池在合并后不再读取，日常运行只读取本ledger与 `references/15-fixed-section-four-etf-pool.md` 已固化的展示关系。

每个板块、主题或商品条目至少包含：

- `label`
- `representative_etf`
- `state`：向后兼容别名，必须等于 `base_state`
- `base_state`
- `base_state_as_of`
- `author_exact_state`
- `author_exact_state_as_of`
- `author_exact_base_state`：作者精确阶段创建或重申时对应的五类父状态
- `author_exact_active`：当前是否允许展示该作者精确阶段
- `author_exact_source_report`：作者精确阶段的独立来源；即使当前基础状态后来改变也不得覆盖
- `source`
- `as_of`
- `source_report`
- `note`

当前由作者正式历史同步的条目使用 `source: AUTHOR_CONFIRMED_HISTORY`。若未来AI基于真正结构破坏更新 `base_state`，必须记录实际结构证据与日期，不得把 `AI_reports/` 候选稿伪装成作者来源。

## 五种基础行情性质

AI只能创建或修改以下 `base_state`：

1. 上涨趋势
2. 下跌趋势
3. 大型震荡
4. 头部
5. 底部

`state` 必须与 `base_state` 完全相同。AI不得创建“上涨趋势中继”“下跌趋势中继”“主升浪”“二次启动”“强趋势”“弱趋势”“修复趋势”或其他第六种基础分类。

## AUTHOR_EXACT_STATE

作者在最新正式报告或当前明确指令中使用更具体的行情阶段时：

- `base_state` 保存其对应的五类基础状态；
- `author_exact_state` 原样保存作者用词；
- `author_exact_state_as_of` 记录作者判断日期；
- `author_exact_base_state` 记录该精确阶段的五类父状态，例如“上涨趋势中继”的父状态只能是“上涨趋势”；
- `author_exact_active` 设为 `true`；
- `author_exact_source_report` 独立记录创建或重申该精确阶段的真实作者正式文件；
- 正式历史来源使用 `source: AUTHOR_CONFIRMED_HISTORY`；当前用户明确指令使用 `source: AUTHOR_EXPLICIT_INSTRUCTION`，且优先级更高；
- `source_report` 只指向真实作者正式文件；若来源为当前明确指令，则使用日期与状态说明记录，不伪造文件路径。

AI不得自行创建、改写、缩写、标准化、降级或清除 `author_exact_state`，也不得把某个板块的作者特殊阶段复制给其他板块。

正式报告的行情性质显示顺序为：

1. 仅当 `author_exact_state` 非空、`author_exact_active: true` 且当前 `base_state == author_exact_base_state` 时，原样显示作者精确阶段；
2. 否则显示 `base_state`。

下一交易日没有作者新判断、且 `base_state` 仍与父状态一致时，必须继续显示作者原话。若真正结构证据使 `base_state` 离开 `author_exact_base_state`，AI只执行机械失活：把 `author_exact_active` 设为 `false`，保留 `author_exact_state`、`author_exact_state_as_of`、`author_exact_base_state` 和 `author_exact_source_report` 作为历史作者判断，正式报告显示新的 `base_state`。以后 `base_state` 即使返回旧父状态也不得自动重新激活，只有较新的作者明确重申才能更新来源并将其重新设为 active。持续性权限始终按 `base_state` 判断，不能根据 `author_exact_state` 另造规则。

## 日度与周度连续性

### 日度

- 读取同步后的两个state文件；
- 读取上一期作者正式报告作为内容连续性基准；
- 以上一期 `base_state` 和兼容且有效的 `author_exact_state` 为默认值；
- 当天涨跌、宽度和单一事件只能影响当日轮动判断，不能自动改变跨期结构。
- 第四部分按 `references/15-fixed-section-four-etf-pool.md` 的固定24行读取 `etf_states.states`；无可靠代表ETF的主题状态仍可保留在ledger，但不得进入第四部分。

### 周度

- 读取同步后的两个state文件；
- 读取上一期作者正式周报（如已有）与当周最新日度状态；
- 周度标签必须与最新日度结构兼容，不能用一周涨跌幅重新发明状态；
- 周度AI候选稿仍只写入 `AI_reports/weekly/`。

## 结构变更门槛

只有价格结构发生足以改变原状态的真实变化，AI才允许更新 `base_state`，例如：

- 大型震荡真正脱离原大区间并完成有效突破或破位；
- 上涨趋势的高低点结构被破坏并进入大型震荡、头部或下跌趋势；
- 下跌趋势结构被破坏并进入大型震荡、底部或上涨趋势；
- 头部或底部完成向趋势或大型震荡的结构转换。

以下理由不能单独改变 `base_state`：

- 单日大涨或大跌；
- 单周涨跌；
- 一次公司财报；
- 板块突然进入涨3或跌3；
- 一天宽度改善；
- 宏观叙事听起来发生变化。

## 首次出现项目

`MANDATORY_ROTATION_COVERAGE_SET` 中首次出现而 ledger 尚无记录的板块或主题，必须依据已经整理好的近期真实价格结构，从五种合法 `base_state` 中完成分类并写入 ledger。AI不得为该项目创造 `author_exact_state`，不得重读全部历史报告，也不得把后台建档过程写入正式报告。

## 状态更新记录

真正的基础状态改变继续记录：

- `previous_state`
- `new_state`
- `effective_date`
- `evidence_summary`
- `source_report`

这里的 `previous_state` 与 `new_state` 均指五类 `base_state`。没有变化时不写伪更新；同日期作者稿因哈希或指定文件变化而重读，也不能仅凭“重新同步”追加记录。作者特殊阶段的创建、重申、覆盖或机械失活只更新其专用字段，不伪装成AI基础状态变化。

## 游标推进边界

日期更晚的 `AUTHOR_CONFIRMED_HISTORY` 可以推进顶层 `author_history_as_of` 与 `as_of`。同日期正式稿SHA-256变化，或用户明确指定同日另一更新文件时，日期游标不变，但必须更新 `latest_author_confirmed_report` 和 `latest_author_confirmed_report_sha256` 并重新同步正文修订。

以下操作不得推进作者历史同步游标：

- 生成或修改 `AI_reports/` 候选稿；
- 完成Finviz机械统计；
- AI基于当天证据更新运行数据；
- 在日期、文件和哈希均未变化时重新打开旧报告；
- 对旧报告进行重复审计。

作者人工修改或明确确认AI候选稿后，正式版本进入 `history/`；下一次运行再按新增作者正式报告同步state。
