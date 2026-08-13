# 2026-08-12 复核工件

- `fetch_and_build.py` 与 `source-manifest.json`：动态发现同一收盘日的七套 Finviz 层级资源，锁定表现接口、层级模块、发布时间、节点数和哈希。
- `calculate.py` 与 `calculated-statistics.json`：按完整有效成分、清一色优先、权重收益/子主题等权收益生成机械统计。
- `generate_outputs.py`：生成主统计报告和两个 TXT，并核验六个范围的四列六行结构、宽度恒等式、逐股原因和代码集合。
- `sec-filing-window.json`、`sec-filing-snippets.json`、`sec-event-exhibits.json` 与 `selected-event-release-text.json`：保存 92 只入选股票的 SEC 专项检索窗口、发布时间和事件材料，用于防止盘后时间线倒置。
- `catalyst-research.md`：逐股核验的可读研究索引。
- `mandatory-rotation-coverage-set.json`：保存六个范围涨3/跌3合并后的17项集合、三项轮入/三项轮出和报告完整性闸门。
- `etf-universe-audit.json`：保存绩效接口与可见 ETF 地图层级的差集、新增代码核验及杠杆/反向排除结果。正式ETF选择严格限于同日地图层级可见叶子。

`report_checks.report_incomplete` 只在正式深度报告、历史副本与 ledger 同步全部完成并通过审计后改为 `false`。

