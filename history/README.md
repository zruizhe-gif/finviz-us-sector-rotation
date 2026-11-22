# Historical Rotation Reports（作者正式历史）

- `daily/`：只保存作者人工修改或明确确认的正式日度报告（DOCX 或对应规范 MD）。AI 自动生成的候选稿一律保存在 `../AI_reports/daily/`，AI 不得自行复制进来。不得覆盖或删除不同日期的旧报告。同日多份文件以用户明确指定的人工版优先，否则以最新修改的正式文件优先。2026-08-16起新正式稿命名 `美股板块轮动观察｜YYYY.M.D.md` / `.docx`（月日不补0）；旧的 `us_sector_rotation_YYYY-MM-DD.md` 规范命名仍视为正式历史，既有文件不重命名。
- `weekly/`：同规则，只保存作者正式周度报告；AI 候选稿在 `../AI_reports/weekly/`。

- 本目录内作者人工修改或明确确认的最新报告属于 `AUTHOR_CONFIRMED_HISTORY`，优先级高于 AI_reports 自动稿、旧 state 与 Codex 此前自动判断。
- 每个新交易日开始前只增量检查本目录：只读取日期晚于 `state/market-state-ledger.yaml` 的 `as_of` 的新正式报告，并核对日期等于 `as_of` 的正式文件是否有新修改；不重读全部历史报告。
- 行情性质与术语同步只从本目录读取；禁止从 `AI_reports/` 反向更新 `state/`。
- 新一期日度报告以上一期作者正式报告为连续性基准；新一期周度报告以上一期作者正式周度报告和当周最新日度 state 为基准。
