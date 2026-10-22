# 16 Runtime Briefs and Batch Catalysts｜轻量运行输入与批量催化

本文件定义机器底稿与LLM成稿输入之间的稳定隔离层。目标仅是减少重复读取、搜索和推理；任何统计范围、涨3跌3、ticker覆盖、证据标准、Bloomberg研究、行情性质或报告内容均不得削减。

## 1. 完整机器底稿永久保留

每期继续生成并保留：

- `calculated-statistics.json`；
- `coverage-audit.json`；
- `mandatory-rotation-coverage-set.json`；
- 全部hierarchy与performance JSON；
- `etf-universe-audit.json`；
- `stock-ticker-universe.json`；
- 完整 `catalyst-cache.json`；
- 机械统计报告与两个TXT。

这些文件是计算、审计和追溯依据。不得删除、截断或用brief反向覆盖。

## 2. runtime-brief

完整机械底稿生成后执行：

```powershell
python scripts/build_runtime_briefs.py --date YYYY-MM-DD --skip-catalyst --write-txt
```

程序生成 `research/finviz/YYYY-MM-DD/runtime-brief.json`，只保留：

- 五个股票范围与Themes各自完整涨3跌3；
- 每项成分/子主题涨跌平、方向占比、整体收益及清一色/补位身份；
- 每项三只目标股票、公司名称、代码与涨跌幅；
- 每个范围清一色候选完整名称及一致性优先PASS/FAIL；
- 最终涨3跌3 ETF、同敞口合并结果与ETF audit一致性；
- 完整mandatory coverage与最终轮入/轮出机械候选；
- 固定24行所需全部ETF表现及获准追加项目；
- 商品分析所需原油、天然气、黄金、白银、工业金属与玉米代理ETF表现；
- coverage匹配数量、缺失代码摘要、披露资格与PASS/FAIL；
- 唯一ticker集合及来源文件SHA-256。

程序必须断言六个范围各恰好3涨3跌、固定观察池24行完整、ETF各3只、TXT集合可重建且一致性优先未被破坏。失败时停止成稿并定点检查对应机器底稿。

## 3. 全ticker批量初筛

完整唯一ticker集合生成后，执行：

```powershell
python scripts/batch_catalyst_screen.py --date YYYY-MM-DD --previous-trading-date YYYY-MM-DD
```

程序对全部ticker执行一次批量机械候选事件扫描，并保留 `catalyst-screen.json`。该扫描只回答：目标正常交易时段能够使用的前一交易日盘后至当日收盘前，是否存在候选公司事件；同时标记异常涨跌、与入选板块方向脱离及证据冲突。它不是最终催化判断，候选项仍按证据标准定点核验。

批量扫描覆盖率必须为100%，并为每个ticker保留：公司、全部出现位置、涨跌幅、扫描时间窗、候选标题/时间/链接、异常与板块一致性标记。网络或来源失败的ticker不得伪装成“无事件”，必须进入待补或FAIL。

模型只处理以下ticker：

- 有候选事件；
- 财报或指引；
- 并购；
- 融资或资本结构；
- 监管；
- 重大合同；
- 异常涨跌；
- 明显脱离板块；
- 证据冲突。

没有候选事件、批量扫描成功且表现与所属板块一致的股票，完成必要核查后直接记录“暂未找到同日直接催化”，并使用已经确认的板块、行业或宏观联动；不得扩展成逐ticker全网穷举。

## 4. catalyst-brief

全部ticker记录完成并写入完整 `catalyst-cache.json` 后执行：

```powershell
python scripts/build_runtime_briefs.py --date YYYY-MM-DD --require-catalyst --write-txt
```

程序只有在完整cache覆盖率为100%时才生成 `catalyst-brief.json`。每个ticker只保留：公司名称、涨跌幅、结论状态、研究层级、直接催化、事件时间、行业联动、成稿结论与必要证据索引。任何ticker缺失或缺少结论都必须FAIL。

## 5. LLM读取纪律

正常DAILY_WEEKLY_RUN的成稿阶段只读取：

1. 最新作者正式稿的新增或变更内容；
2. 本次需要的market-state-ledger状态；
3. author terminology；
4. `runtime-brief.json`；
5. `catalyst-brief.json`；
6. `daily-macro-context.md`；
7. 当前报告模板；
8. Voice Style与Hard Bans所需规则。

禁止全文读取calculated、coverage、hierarchy/perf、ETF audit或完整catalyst cache；禁止成稿后重新抓数据或重复研究ticker。只有brief中的具名异常、证据冲突或唯一终审失败项，才允许定点打开相关原文件。

最终仍执行一次完整审计。brief是完整底稿的受检索投影，不是降低质量标准的摘要替代品。若出现context compaction，先检查是否误载大型底稿，并记录本次发生次数；不得通过删除研究或报告要求解决。
