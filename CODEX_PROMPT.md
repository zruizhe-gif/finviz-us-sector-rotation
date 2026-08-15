# Codex运行入口

以当前目录中的 `finviz-us-sector-rotation-v0.2` 为唯一基线。

1. 先读取 `SKILL.md` 和 `references/14-runtime-modes-and-incremental-workflow.md`，根据用户当前请求判定 `DAILY_WEEKLY_RUN` 或 `DEVELOPMENT`。
2. 默认使用 `DAILY_WEEKLY_RUN`。不要完整预读所有references、01/02原任务、历史对话、legacy范文、旧负面案例、全部历史报告或全部原始字幕。
3. 日度或周度运行先读state，再定位 `history/daily/` 中最新 `AUTHOR_CONFIRMED_HISTORY`，计算其SHA-256并与 `author_history_as_of`、`latest_author_confirmed_report`、`latest_author_confirmed_report_sha256` 比较。日期更晚、同日期哈希变化或用户明确指定同日另一更新文件时都必须重读并同步；否则不重读正文。具体行情判断和术语只更新state，不修改Skill规则。
4. Finviz机械统计固定由项目现有稳定程序完成。保持五个股票范围、Themes、ETFs、一致性优先、清一色优先、不足3项才补位、ETF去杠杆/反向/相同经济敞口和完整性审计，不让模型手工重算全部股票。
5. 同一ticker的催化只研究一次并写入当日缓存；已有缓存直接复用。Bloomberg节目摘要按 `source_sha256` 复用；哈希未变化时不得重读原字幕。
6. 轮动成稿只读取已经整理好的统计、coverage、催化缓存、宏观上下文、state、最新一期作者正式报告、Voice Style、Hard Bans和模板。缺什么只补什么。
7. AI自动稿只能写入 `AI_reports/daily/` 或 `AI_reports/weekly/`，不得写入或覆盖 `history/`。只有作者人工修改或明确确认的版本才能进入正式历史并更新作者状态。
8. 最终只执行一次综合审计。通过后立即结束；不得进行第二轮、第三轮全量复核。
9. `DEVELOPMENT` 只在用户明确要求修改Skill、规则、代码或修复系统性问题时使用，并严格遵守当前请求的文件范围。GitHub登录、commit、push或可见性修改仍需用户在当前请求中明确授权。

完成后只汇报当前请求要求的文件、状态、目录结构和验证结果，不主动运行额外Finviz任务、全Skill validator、manifest重建、全包hash审计或GitHub操作。
