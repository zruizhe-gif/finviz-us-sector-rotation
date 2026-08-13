以 `finviz-us-sector-rotation-v0.2` 为唯一基线。

1. 先完整读取 `SKILL.md`、`references/01-original-daily-task-verbatim.txt`、`references/02-original-weekly-task-verbatim.txt`、其余全部 references，以及 `examples/legacy/us_sector_rotation_2026-08-05.md`。01/02 是原任务全文，除 `03-current-overrides-and-precedence.md` 明确修改的冲突项外，其余要求一律保留，不得删减。8月5日范文只保留内容深度、分析逻辑和证据标准，冲突的旧技术/结构/持续性规则不得恢复。

2. 日常运行以本Skill内的 `references/09-author-voice-style.md` 与 `references/10-hard-bans.md` 为权威快照。只有用户明确要求维护Skill，且可验证的相邻 `research-publisher` 源存在时，才同步对应最新版；不得让日常分析依赖项目外目录。

3. 重点检查“一致性优先”统计规则已经完整执行：五个股票范围必须先扫描每个板块全部有效成分；Themes先扫描每个大类全部子主题；清一色候选优先于平均表现；每个入选项披露完整宽度和“清一色优先/平均表现补位”；最终单列每个范围清一色上涨/下跌完整候选数、候选名单与最终入选结果。

4. Bloomberg节目内容只扫描当前Skill根目录 `script/` 中的本地TXT；以 `SKILL.md` 所在目录解析路径，不得写死盘符或用户名。按日期和节目名匹配 The Close、Closing Bell、Open Interest、Bloomberg Surveillance，完整读取后按Skill目录每个节目单独保存MD，再生成 `daily-macro-context.md` 和 `week-macro-context.md`。禁止自行访问YouTube寻找或判断字幕、视频正文、简介或替代内容；缺失时只记录 `LOCAL_TRANSCRIPT_MISSING`。

5. 按V0.2完整执行当前prompt指定的目标交易日或交易周：
- 先生成完整Finviz统计主报告和两个TXT；
- 再生成对应日期的独立轮动深度报告；
- 开始前扫描 `history/daily/` 内作者正式DOCX与规范MD，先同步唯一 `state/market-state-ledger.yaml`；没有真实结构变化不得改行情性质；
- 2026-08-12及以后必须先继承8月11日作者正式DOCX中的修订，尤其半导体（XSD）为“头部”；
- 行情性质只能使用上涨趋势、下跌趋势、大型震荡、头部、底部；
- 只有上涨/下跌趋势写趋势维持条件，其他三类不写持续性；
- 禁止高/中高/中/中低/低持续性评级；
- 六个标题严格使用当前规则，第六节只写未来观察点；
- Finviz主统计报告继续保留核验链接；独立轮动深度报告删除来源、超链接、脚注和引用标记。

6. 本轮最高优先级成稿规则：
- 除公司名称、代码和必要指数/范围专名外，板块、行业、子行业、主题与子主题全部统一中文；
- 正式报告禁止出现作者历史、后台同步、ledger/state、强制覆盖、初始性质、修改建议、自我纠正、字幕来源或“节目提到”等内部过程；
- 第二节只选跨六范围涨3/跌3频率最高并经宽度、ETF、权重股复核的轮入3项、轮出3项，相似且底层成分高交叉者合并；严格四列“轮动强度、板块和主题、当日表现情况、轮动分析”；
- 第三节只分析第二节最终六项，不同板块逐项分开，只有实质同类方向可合并；
- Finviz主报告统计规则不变，格式与内容深度以 Skill 根目录内的 `finviz_2026-08-11_report.md` 为基准；每只入选股票分别做催化与时间线专项核查，禁止批量套用“暂未找到”。

7. GitHub发布要求以当前用户prompt为准；不得把旧任务中“一次不上传GitHub”的临时限制延续到新任务。仍不得修改原始01/02任务文件，不运行与本轮无关的测试。

完成后汇报：
- 实际修改/新增文件；
- research-publisher两份规则是否同步成功；
- 本周Bloomberg节目归档清单与缺口；
- 目标日期统计报告、两个TXT、轮动报告路径；
- 一致性优先复核结果；
- state ledger是否变化，如变化说明具体结构证据。
