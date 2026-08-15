# README-CODEX

V0.2采用稳定规则、作者动态状态和AI候选稿三层分离。

- `SKILL.md`、`references/`、`templates/` 与稳定脚本只保存长期规则；
- `state/` 保存最新行情性质、作者精确阶段、作者术语、日期与来源；
- `AI_reports/` 保存AI自动候选稿；
- `history/` 只保存作者人工修改或明确确认的正式版本。

默认运行模式是 `DAILY_WEEKLY_RUN`：先读state，按报告日期、正式文件路径和SHA-256同步新增或同日期已修改的作者正式报告，运行稳定Finviz程序，复用ticker催化缓存和Bloomberg字幕哈希缓存，再从整理好的中间结果生成AI候选稿。正常运行不修改Skill、代码、模板或manifest，不重读未变化的旧历史和旧负面案例，不调试正常代码，不执行全包审计或GitHub操作。

只有用户明确要求修改Skill、规则、代码或修复长期系统性错误时才进入 `DEVELOPMENT`。GitHub始终需要当前请求中的单独明确授权。

详细流程见 `references/14-runtime-modes-and-incremental-workflow.md`。
