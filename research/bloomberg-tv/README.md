# Bloomberg TV Archive

Bloomberg 节目内容的唯一字幕输入目录是当前 Skill 根目录的 `script/`。以 `SKILL.md` 所在目录为锚点解析，不依赖工作目录、盘符或用户名。只扫描 `script/` 的直接子文件，不递归扫描子目录；嵌套副本不参与节目匹配。

目标节目为 The Close、Closing Bell、Open Interest、Bloomberg Surveillance。禁止访问 YouTube 获取或判断字幕、Transcript、视频正文、节目简介或片段，也禁止上网寻找替代节目。没有对应本地字幕时，该节目 MD 全文只记录 `LOCAL_TRANSCRIPT_MISSING`；不得用标题、简介、页面说明、旧摘要或零散片段补写节目事实。

## 永久缓存

匹配字幕后先由操作系统计算 SHA-256，不先把全文交给模型。节目 MD 必须保存可机器解析的：

- `program`
- `program_date`
- `source_file`：相对于 Skill 根目录的 `script/<filename>.txt`
- `source_sha256`
- `summary_status`
- `summary_generated_at`

节目 MD 已存在且节目、日期和 `source_sha256` 未变时，运行状态为 `PROGRAM_SUMMARY_CACHE_HIT`。直接复用节目 MD，禁止重新读取原始字幕全文。只有新节目、字幕变化或节目 MD 缺失/元数据不可解析时，才全文读取对应字幕并生成或重建总结。`TRANSCRIPT_DATE_MISMATCH` 同样按来源哈希缓存。

旧节目 MD 不因采用新格式而批量回填或改写。

## 目录与读取层级

目录按 `YYYY-Www/YYYY-MM-DD/` 保存四档节目 MD 和 `daily-macro-context.md`；周目录保存 `week-macro-context.md`。

- 日度宏观综合读取缓存后的节目 MD，生成 `daily-macro-context.md`；日度轮动候选报告主要读取该文件，不再重读四份原始字幕。
- 周度宏观综合只读取本周各交易日的 `daily-macro-context.md`，生成或读取 `week-macro-context.md`；默认不重读周内原始字幕或全部节目 MD。
- 缺少哪一日、哪一档只补哪一项，不重做整周研究。

日度和周度宏观上下文只汇总有有效本地字幕支持的节目内容。

本目录全部属于内部研究层。轮动候选报告只写消化后的宏观事实和市场判断，不得复制字幕路径、缓存命中、读取状态、缺口说明、节目名或“彭博/节目/字幕提到、支持、验证”等来源话术，也不得把单一嘉宾观点直接写成市场事实。
