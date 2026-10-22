以 `finviz-us-sector-rotation-v0.2` 为唯一基线（当前工作流版本 v0.3）。

0. 先判断运行模式。默认进入 `DAILY_WEEKLY_RUN`；只有用户明确要求修改Skill/规则/代码/长期系统性错误时才是 `DEVELOPMENT`。本轮是否处于 DEVELOPMENT 由用户本轮指令决定，不得自行切换。

1. DEVELOPMENT / 首次安装：完整读取 `SKILL.md`、`references/01`～`references/14`、`examples/legacy/us_sector_rotation_2026-08-05.md`、全部 templates 与 `state/` 两个文件。01/02 是原任务全文，除 `03`（含2026-08-14工作流改造节）明确修改的冲突项外一律保留；8月5日范文只保留内容深度、分析逻辑和证据标准，旧技术/结构/持续性规则不得恢复。
   DAILY_WEEKLY_RUN：只读固定输入集——当日 calculated statistics 与 mandatory rotation coverage set、当日 catalyst cache、当日 daily-macro-context、`state/market-state-ledger.yaml`、`state/author-terminology.yaml`、上一期作者正式报告（只取第四部分与术语）、`references/09`、`references/10`、`SKILL.md`。禁止重读全部历史报告、旧负面案例与原始字幕全文。

2. 日常运行以本Skill内的 `references/09-author-voice-style.md` 与 `references/10-hard-bans.md` 为权威快照。只有用户明确要求维护Skill且可验证的相邻源存在时才同步最新版；不得让日常分析依赖项目外目录。

3. 状态同步为增量：读 `state/market-state-ledger.yaml`，扫描 `history/daily/`，只读取日期晚于 ledger `as_of` 的新作者正式报告，并核对日期等于 `as_of` 的正式文件是否有新修改（sha256/mtime 与 `sync_checkpoint` 比对）；只提取第四部分，新作者判断直接覆盖旧判断。行情性质：AI 自主判断只有五种（上涨趋势、下跌趋势、大型震荡、头部、底部）；作者明确写出的更具体阶段（如“上涨趋势中继”）作为 `AUTHOR_EXACT_STATE` 原样保存（base_state + author_exact_state），正式报告沿用作者原话，AI 不得自创、改回或套用他板块。术语修正写入 `state/author-terminology.yaml`（当前：VGT＝信息技术；Cybersecurity＝网络安全；Biometrics＝生物识别）。禁止从 `AI_reports/` 反向更新 state。

4. 一致性优先统计规则必须完整执行：五个股票范围先扫描每个板块全部有效成分；Themes 先扫描每个大类全部子主题；清一色候选优先于平均表现；每个入选项披露完整宽度和“清一色优先/平均表现补位”；最终单列每个范围清一色上涨/下跌完整候选数、候选名单与最终入选结果。机械统计由 `fetch_and_build.py` → `calculate.py` → `generate_outputs.py` 固定执行，程序真实报错才停止并报告；禁止模型手工遍历全股票复核，禁止修改脚本。

5. Bloomberg 节目内容只扫描当前Skill根目录 `script/` 的本地 TXT（以 `SKILL.md` 所在目录解析路径，不得写死盘符或用户名）。节目MD记录 `source_file` 与 `source_sha256`；MD存在且 hash 未变 → `PROGRAM_SUMMARY_CACHE_HIT`，禁止重读原始字幕全文；只有新节目、字幕变化、summary 缺失才全文读取并生成节目MD与 `daily-macro-context.md`。日度只读当日 daily-macro-context；周度读整周 daily-macro-context，默认禁止重读周内字幕。缺失只记 `LOCAL_TRANSCRIPT_MISSING`；禁止访问YouTube或替代节目。

6. 催化研究使用 `research/finviz/YYYY-MM-DD/catalyst-cache.json` 一次去重缓存（股票代码为 key）：普通股票两步研究（公司名/代码+日期+当日新闻/财报/公告；必要时查 IR/SEC），命中同日直接事件立即停止；两步仍无独立事件才记“暂未找到同日直接催化”加已确认联动，禁止穷举 SEC 表单、评级、内部人、融资、合同、监管。只有异常大涨大跌、财报、并购、监管、融资、重大合同、明显脱离板块、信息冲突才做完整事件调查。

7. 轮动深度报告：七部分固定结构（2026-10-16起新增第六节“宏观讨论”，未来观察点顺延为第七节；全文执行BAN-010语气纪律）；第二节按六范围涨3/跌3频率精选三项轮入与三项轮出，严格四列六行；第三节只分析这六项，不同板块逐项分开，只有实质同类方向可合并；第四节覆盖内部涨3/跌3去重集合中具有板块/主题意义的项目；第五节商品涨跌驱动判断；第六节宏观讨论；第七节只写未来观察点。只有上涨/下跌趋势写趋势维持与破坏条件，其他三类不写持续性；禁止高/中/低持续性评级；除公司名称、代码和必要指数/范围专名外全部统一中文，术语以 `state/author-terminology.yaml` 为准；Finviz主统计报告保留核验链接，独立轮动深度报告删除来源、超链接、脚注和引用标记；正式报告禁止出现作者历史、后台同步、ledger/state、强制覆盖、初始性质、审计、字幕来源或“节目提到”等内部过程。

8. 输出与分离：Finviz 主报告与两个 TXT 按现有数据产物结构保存于 Skill 根目录；AI 轮动候选稿保存到 `AI_reports/daily/us_sector_rotation_YYYY-MM-DD.md`（周度 `AI_reports/weekly/us_sector_rotation_week_YYYY-MM-DD.md`）；禁止 AI 写入或覆盖 `history/daily/`、`history/weekly/`；AI_reports 自动稿不更新 ledger。

9. 审计只做一次（`references/14` 第七节15项清单），通过后立即结束，禁止第二轮、第三轮全量复核。

10. GitHub 发布要求以当前用户prompt为准；日常运行默认不登录、不 commit、不 push，不重建 manifest，不运行全 Skill validator，不做全包 hash 审计。仍不得修改原始01/02任务文件，不运行与本轮无关的测试。

完成后汇报：
- 实际修改/新增文件；
- 模式（DAILY_WEEKLY_RUN / DEVELOPMENT）；
- 增量状态同步结果（是否读取新作者报告、哪些条目变化、AUTHOR_EXACT_STATE 与术语是否更新）；
- Bloomberg 缓存命中/缺失清单（不报告字幕内容细节）；
- 目标日期统计报告、两个TXT、AI轮动候选稿路径；
- 一致性优先复核结果；
- 一次性审计结果。
