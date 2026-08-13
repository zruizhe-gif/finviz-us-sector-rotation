---
name: finviz-us-sector-rotation
description: Finviz美股日度/周度板块统计与连续性轮动分析。完整保留原日度与周度任务，以当前覆盖规则只修改明确冲突项；先执行一致性优先的Finviz机械统计与逐股催化核查，再用历史行情性质和本地宏观节目研究在后台生成全中文、三项轮入与三项轮出的六部分轮动深度报告。
---

# Finviz US Sector Rotation

## 核心原则

这个 Skill 是原 Finviz 日度任务与周度任务的合并升级版。

**原任务不是参考资料，而是仍然生效的任务合同。**

每次运行必须完整读取：

1. `references/01-original-daily-task-verbatim.txt`
2. `references/02-original-weekly-task-verbatim.txt`
3. `references/03-current-overrides-and-precedence.md`
4. `references/04-consistency-first-statistics.md`
5. `references/05-rotation-report-current.md`
6. `references/06-market-state-continuity.md`
7. `references/07-persistence-and-commodities.md`
8. `references/08-bloomberg-tv-macro-context.md`
9. `references/09-author-voice-style.md`
10. `references/10-hard-bans.md`
11. `references/11-evidence-and-output-boundaries.md`
12. `references/12-quality-audit.md`
13. `references/13-negative-example-lessons.md`
14. `examples/legacy/us_sector_rotation_2026-08-05.md`（只学习内容深度、分析逻辑和证据标准；与当前规则冲突处以03为准）
15. `state/market-state-ledger.yaml`

### 规则优先级

1. 用户当前prompt中的明确新要求；
2. `03-current-overrides-and-precedence.md` 中列出的明确覆盖项；
3. 原日度/周度任务全文；
4. 其他辅助reference与模板。

**凡 `03` 没有明确否定、替换或修改的原任务条款，一律原样继续生效。不得因为SKILL.md没有重写一遍，就视为失效。**

## 两阶段工作流

### A. Finviz机械统计

严格按原任务全部要求执行，尤其是“一致性优先”的涨3/跌3筛选。统计阶段不能被轮动分析简化或替代。

### B. 独立轮动深度报告

统计完成后再写轮动分析。轮动报告使用新的六部分结构、五种行情性质、历史连续性、趋势条件规则和宏观节目研究。

正式成稿只呈现市场事实与分析结论。所有非公司板块、行业、子行业和主题名称统一写中文；英文源标签只用于后台匹配。禁止把历史同步、state ledger、强制覆盖、审计、纠错、建档、本地字幕来源、Bloomberg节目如何形成判断等内部过程写入正式报告。

术语必须先按源标签核对再翻译：`Cybersecurity` 只能写“网络安全”，`Biometrics` 只能写“生物识别”。二者是两个独立主题，不得依据代表ETF、个股业务或子主题相似性互换名称。

### C. AUTHOR_CONFIRMED_HISTORY 与唯一状态台账

`history/daily/` 内由作者人工修改或明确确认的日度DOCX，以及规范命名的 `us_sector_rotation_YYYY-MM-DD.md`，统一视为 `AUTHOR_CONFIRMED_HISTORY`。同一交易日同时存在多份时，以用户明确指定的人工版优先；没有明确指定时，以最新修改的正式文件优先。必须读取其第四部分“行情性质”，并可为机器读取保留规范MD镜像，但台账来源必须指向真实的作者正式文件。`state/market-state-ledger.yaml` 是唯一的各板块/主题最新行情性质总表，禁止另建第二套状态数据库。

每个新交易日开始前，必须先扫描 `history/daily/`，按日期从旧到新读取所有晚于 ledger `as_of` 的正式报告，并提取第四部分“行情性质”同步到 ledger；同一项目以最新日期的作者判断为准。还必须重新读取日期等于 ledger `as_of` 的最新正式报告，以捕捉作者对同日文件的人工修改。完成同步后才能进行当天 Finviz 统计与轮动分析。

每期报告完成并保存到 `history/daily/` 后，必须再按正式报告同步 ledger，并把 ledger 总体 `as_of` 和最新基准来源推进到该报告日期；即使没有任何行情性质变化也必须推进日期，不得伪造状态改变。每个条目至少记录名称、代表ETF、当前行情性质、`as_of`、`source_report` 和一句必要的状态说明。

### D. Bloomberg 本地字幕唯一输入

Bloomberg 节目内容的唯一字幕输入目录是本 Skill 根目录内的 `script/`。运行时先以当前 `SKILL.md` 所在目录解析 Skill 根目录，再访问其直接子目录 `script/`；不得依赖工作目录、盘符、用户名或外部绝对路径。每次运行只扫描该目录，按日期与节目名称匹配 The Close、Closing Bell、Open Interest、Bloomberg Surveillance 的 TXT，完整读取对应文件全文后生成节目研究MD。

禁止为 Bloomberg 节目自行访问 YouTube 获取或判断字幕、Transcript、视频正文、节目简介或替代片段。某档节目没有对应本地字幕时，只记录 `LOCAL_TRANSCRIPT_MISSING`；不得上网寻找替代节目，不得根据标题、简介或零散片段补写节目事实。详细流程见 `references/08-bloomberg-tv-macro-context.md`。

### E. MANDATORY_ROTATION_COVERAGE_SET

Finviz 机械统计完成后，必须先建立 `MANDATORY_ROTATION_COVERAGE_SET`：纳入 All Stocks、S&P 500、Dow Jones 30、Nasdaq 100、Russell 2000 各自涨3与跌3，以及 Themes 涨3与跌3；跨范围同名项目去重，但保留其在每个范围的证据。

集合只用于后台研究与完整性审计，不得作为正式报告的栏目或叙述对象：

- 第二部分不机械罗列全集合。先统计六个范围涨3/跌3出现频率，合并名称相近、个股交叉度高且经济敞口实质相同的方向，严格精选轮入3项和轮出3项；
- 第二部分表格严格只有四列：`轮动强度`、`板块和主题`、`当日表现情况`、`轮动分析`（周报把“当日”改为“本周”）；
- 第三部分仅分析第二部分最终筛出的三项轮入与三项轮出，每个不同板块/主题分别设小标题；只有实质相同的方向可以合并，例如能源与能源商品；
- 第四部分覆盖集合中具有板块/主题意义的项目并完成五种行情性质分类；
- 全部相关项目已存在于 ledger，或在后台完成状态补建后写入 ledger。

历史无记录不是省略理由。后台对新项目结合历史资料和近期真实价格结构完成分类并写入状态台账；正式报告只写最终“行情性质”，禁止写“初始性质”“建档”“作者历史”等过程话术。核心结论只能是一段高信息密度文字。

## DAILY

- 使用 Finviz 1-Day Performance。
- 最新一个已完成正常收盘的美股交易日。
- 无新交易日：只报告“没有新交易日”，不重复旧报告。
- 输出文件名遵守原日度任务与 `11-evidence-and-output-boundaries.md`。

## WEEKLY

- 使用 Finviz 1-Week Performance。
- 以该周最后一个正常交易日为数据日期。
- 无新的完整交易周：只报告“没有新的完整交易周”。
- 周度统计仍完整执行原周度任务，不得退化成日度报告汇总。

## 强制执行顺序

1. 确认 DAILY / WEEKLY、目标日期与是否有新数据；
2. 读取原任务全文和当前覆盖规则；
3. 扫描 `history/daily/`，把 `AUTHOR_CONFIRMED_HISTORY` 按日期从旧到新同步进唯一 ledger，并复核同日人工修订；
4. 从当前 Skill 根目录解析并扫描 `script/`，完整读取目标日期/当周可用的四档 Bloomberg 本地字幕并完成研究归档；缺失只记 `LOCAL_TRANSCRIPT_MISSING`；
5. 完成五个股票范围、Themes、ETFs的完整机械统计；
6. 由五个股票范围及 Themes 的涨3/跌3建立去重后的 `MANDATORY_ROTATION_COVERAGE_SET`；
7. 逐只入选股票专项核查公司公告、财报、监管、合同、评级及可靠新闻与发布时间；按桌面旧版主报告的格式、内容组织和深度生成主统计报告与两个TXT；
8. 读取最近一期轮动报告与同步后的状态台账，判断是否发生真正结构变化；首次出现的覆盖项目必须在后台从五种合法行情性质中完成分类并写入台账；
9. 研究集合内全部项目的直接驱动、盈利预期、宏观背景和商品基本面；
10. 按跨范围频率、宽度、ETF与权重股印证，选出第二节轮入3和轮出3；第三节只逐项分析这六项；第四节覆盖内部涨3/跌3集合中具有板块意义的项目；
11. 执行统计完整性、连续性、Hard Bans、来源边界、格式和 `MANDATORY_ROTATION_COVERAGE_SET` 逐项审计；
12. 只有 `REPORT_INCOMPLETE = FALSE` 才能保存与交付报告；
13. 保存正式历史报告到 `history/daily/`；
14. 从保存后的正式报告再次同步唯一 ledger；即使没有状态变化，也推进总体 `as_of`、条目确认日期与来源报告。

## 禁止的捷径

- 禁止只按板块平均涨跌幅选前三；
- 禁止只看极端三只股票判断板块方向；
- 禁止删掉原任务中的任何市场、Themes、ETF、TXT、驱动核验或复核环节；
- 禁止为了新轮动写作规则而修改机械统计规则；
- 禁止把单日/单周涨跌直接改写为新的行情性质；
- 禁止把没有热点的交易日硬写成“轮动主线丰富”。
- 禁止因 ledger/历史没有记录、补位、样本噪声或“不是真热点”而删除 `MANDATORY_ROTATION_COVERAGE_SET` 中的项目；
- 禁止把后台覆盖集合全部机械塞入第二节；第二节只能写频率与证据排序后的3项轮入和3项轮出；
- 禁止给第二节增加第五列，或把规定四列改名；
- 禁止把无实质关系的板块合并分析；
- 禁止正式成稿混用中英文板块/主题名称；
- 禁止把修改建议、自我纠正、作者历史、ledger、强制覆盖、初始性质、字幕来源或“节目提到”等内部话术写入正式报告；
- 禁止用一次泛搜和模板化“暂未找到”替代每只入选股票的专项催化核查；
- 禁止使用本地 TXT 之外的 YouTube 字幕、Transcript、视频正文、简介或片段生成 Bloomberg 节目内容；
- 禁止在 `state/market-state-ledger.yaml` 之外建立另一套行情性质状态数据库。
