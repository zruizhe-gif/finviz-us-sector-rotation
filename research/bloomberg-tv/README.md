# Bloomberg TV Archive

Bloomberg 节目内容的唯一字幕输入目录是当前 Skill 根目录的 `script/`。以 `SKILL.md` 所在目录为锚点解析，不依赖工作目录、盘符或用户名。Codex 每次运行扫描该目录，按日期和节目名称匹配 The Close、Closing Bell、Open Interest、Bloomberg Surveillance 的 TXT，完整读取匹配文件全文后生成节目研究MD。

禁止访问 YouTube 获取或判断字幕、Transcript、视频正文、节目简介或节目片段，也禁止上网寻找替代节目。某档没有对应本地字幕时，该节目MD只记录 `LOCAL_TRANSCRIPT_MISSING`；不得用标题、简介、页面说明、旧摘要或零散片段补写节目事实。

目录按 `YYYY-Www/YYYY-MM-DD/` 保存四档节目MD和 `daily-macro-context.md`；周目录保存 `week-macro-context.md`。日度和周度宏观上下文只汇总存在本地字幕支持的节目内容。

本目录全部属于内部研究层。独立轮动深度报告只写消化后的宏观事实和市场判断，不得复制字幕路径、读取状态、缺口说明、节目名或“彭博/节目/字幕提到、支持、验证”等来源话术，也不得把单一嘉宾观点直接写成市场事实。
