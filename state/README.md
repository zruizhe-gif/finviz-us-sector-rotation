# State（作者动态状态层）

本目录保存作者动态状态，属于动态数据，不属于 Skill 规则。

- `market-state-ledger.yaml`：唯一行情性质台账。每个条目记录 `base_state`（五种基础行情性质之一：上涨趋势、下跌趋势、大型震荡、头部、底部）、可选的 `author_exact_state`（作者原话，如“上涨趋势中继”，原样保存）、`as_of`、`source_report` 与状态说明。附带 `sync_checkpoint`（最近一次同步的作者正式报告的日期、路径、sha256、mtime）供增量判定。2026-08-16已一次性并入作者ETF参考池（36个子行业、105只ETF）的全部行情性质；该池不进入日常工作流。
- `author-terminology.yaml`：作者术语与翻译动态表。记录作者对板块/主题/ETF中文名、行业称谓与翻译错误的修正（当前：信息技术固定使用XLK、VGT与XLK高度重复不再在第四部分单列，如正文他处提及VGT仍译为信息技术；Cybersecurity＝网络安全；Biometrics＝生物识别），正式成稿必须沿用。

维护规则：

- 日常运行（DAILY_STATE_UPDATE）允许增量更新本目录；禁止修改 `SKILL.md`、`references/`、`templates/`。
- 同步只从 `history/daily/` 的作者正式报告读取；禁止从 `AI_reports/` 反向更新。
- 同一板块的新作者判断直接覆盖旧判断；作者特殊阶段只能由作者创建、AI 继承、作者新判断覆盖。
- 本目录之外禁止建立第二套状态数据库。
