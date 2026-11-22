# AI Reports（AI 运行结果层）

本目录保存 AI 自动生成的正式候选轮动报告，属于 AI 运行结果层——不是 Skill 规则，也不是作者状态。

- 日度：`daily/美股板块轮动观察｜YYYY.M.D.md`（2026-08-16起新命名，月日不补0，如 美股板块轮动观察｜2026.8.14）
- 周度：`weekly/美股板块轮动观察｜YYYY.M.D.md`（日期取该周最后一个交易日）
- 旧命名 `us_sector_rotation_YYYY-MM-DD.md` 已废止；既有历史文件不重命名。报告不得放到Skill根目录。

分离规则：

- 只有作者人工修改或明确确认后的报告才进入 `history/daily/`（或 `history/weekly/`），属于 `AUTHOR_CONFIRMED_HISTORY`；
- AI 不得自行把本目录中的文件复制进 `history/`；
- 第二天行情性质与术语同步只从 `history/daily/` 读取；禁止从本目录反向更新 `state/`；
- 优先级：作者正式历史 > 本目录自动稿 > 旧 state > Codex 此前自动判断；
- Finviz 机械统计主报告与两个 TXT 仍按现有数据产物结构保存在 Skill 根目录。
