# Historical Rotation Reports

## AUTHOR_CONFIRMED_HISTORY

`history/` 只保存作者人工修改完成或作者明确确认的正式报告：

- `daily/`：作者正式日度报告，可以是DOCX或作者确认的规范MD；
- `weekly/`：作者正式周度报告，可以是DOCX或作者确认的规范MD。

文件名规范、六部分结构完整或AI已经完成审计，都不等于作者确认。AI自动生成的候选稿必须保存到：

- `AI_reports/daily/美股板块轮动观察｜YYYY.M.D.md`
- `AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`

AI不得自行把候选稿复制、移动或覆盖到 `history/`。只有作者人工修改或明确确认后的版本才可进入本目录；不同日期的正式历史不得覆盖或删除。

同一日期存在多份正式文件时，以用户明确指定版本优先；没有明确指定时，作者人工修改版优先，再按最新修改时间确定。新一期报告以上一期作者正式报告作为连续性基准。

每天开始前定位最新作者正式报告，读取报告日期并计算SHA-256，与 `state/market-state-ledger.yaml` 中的 `author_history_as_of`、`latest_author_confirmed_report` 和 `latest_author_confirmed_report_sha256` 比较。日期更晚、同日期哈希变化，或用户明确指定同一交易日另一份更新后的正式文件时，必须重读该正式稿并同步行情性质、作者精确阶段、术语和其他明确修正；否则不重读正文。“日期没有变化”不等于“作者判断没有变化”。

`AI_reports/` 永远不能反向更新 `author_exact_state`、作者术语或作者历史同步游标。

新日度正式报告的正文标题与建议文件基名统一为 `美股板块轮动观察｜YYYY.M.D`，月份和日期不补0；既有作者正式历史不追溯重命名或重写。
