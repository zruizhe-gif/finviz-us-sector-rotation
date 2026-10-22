# README-CODEX

V0.2 的核心修复是：**把原日度和原周度任务全文原样放回Skill，并建立“原任务默认继续生效、只有当前覆盖文件可以修改冲突项”的优先级。** V0.3 在此之上建立了稳定日常运行模式：三层结构（Skill规则／作者动态状态 `state/`／AI运行结果 `AI_reports/`）、增量状态同步、催化与Bloomberg字幕缓存、AI报告与作者正式历史分离、两种运行模式（`DAILY_WEEKLY_RUN` 默认／`DEVELOPMENT`）。详细协议见 `references/14-daily-workflow-and-caching.md`。

Codex不要再根据精简版SKILL.md猜原任务。

每次运行：

1. 先判断模式：默认 `DAILY_WEEKLY_RUN`；只有用户明确要求修改Skill/规则/代码才进入 `DEVELOPMENT`；
2. DEVELOPMENT/首装完整读取01/02与全部覆盖规则；日常运行只读固定输入集（统计产物、覆盖集合、催化缓存、当日宏观上下文、两个state文件、上一期作者正式报告、Voice Style、Hard Bans），禁止重读全部历史报告与原始字幕；
3. Finviz机械统计由 `fetch_and_build.py` → `calculate.py` → `generate_outputs.py` 固定执行（一致性优先、清一色优先、不足3补位、ETF去杠杆/反向/敞口去重）；禁止模型手工遍历全股票复核，禁止修改脚本；
4. 状态同步为增量：只读 `history/daily/` 中晚于 ledger `as_of` 的新作者正式报告；作者特殊阶段（如“上涨趋势中继”）作为 `AUTHOR_EXACT_STATE` 原样保存并沿用；术语修正写入 `state/author-terminology.yaml`（VGT＝信息技术；Cybersecurity＝网络安全；Biometrics＝生物识别）；禁止从 `AI_reports/` 反向更新 state；
5. Bloomberg研究只读当前Skill根目录的 `script/` 本地字幕，节目MD带 `source_sha256` 永久缓存；命中且hash未变禁止重读字幕；日度只读当日 `daily-macro-context.md`；
6. 催化研究按股票代码一次去重缓存（两步研究，命中同日直接事件立即停止，异常样本才深挖）；
7. 轮动报告七部分结构（第六节宏观讨论、第七节未来观察点；BAN-010语气纪律）：第二节严格选三项轮入与三项轮出、固定四列六行；第三节只分析这六项，不同板块逐项分开；AI候选稿只写入 `AI_reports/daily/`（或weekly），禁止写入 `history/`；只有作者人工修改或确认后才进入 history；
8. 除公司名称、代码和必要指数/范围专名外，所有板块、主题和子行业名称统一中文，术语以 `state/author-terminology.yaml` 为准；
9. 正式报告不得出现作者历史、后台同步、ledger/state、强制覆盖、初始性质、审计、字幕来源或“节目提到”等内部过程；
10. 审计只做一次（15项清单），通过后立即结束。
