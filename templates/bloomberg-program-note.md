---
program: "{Program}"
program_date: "YYYY-MM-DD"
source_file: "script/{transcript-file}.txt"
source_sha256: "{SHA256}"
summary_status: "OK"
summary_generated_at: "YYYY-MM-DDTHH:MM:SSZ"
---

# {Program}｜YYYY-MM-DD

> 使用前先由操作系统计算匹配字幕的 SHA-256。若对应节目 MD 已存在，且节目、日期和 `source_sha256` 一致，运行状态为 `PROGRAM_SUMMARY_CACHE_HIT`：直接复用既有节目 MD，禁止重新读取原始字幕全文，也不使用本模板重写总结。

> 本模板只用于新节目、字幕哈希变化或节目 MD 缺失/元数据不可解析的情况。历史节目 MD 不因本模板升级而批量回填。

> 缺失分支：没有匹配的直接子目录字幕时，不使用本模板；整个节目 MD 只写一行 `LOCAL_TRANSCRIPT_MISSING`，不得添加标题、元数据、旧内容或任何推断。

> `source_file` 必须是相对于 Skill 根目录的路径，只能指向 `script/` 直接子文件，不得写盘符、用户名或绝对路径。日期错配时把 `summary_status` 改为 `TRANSCRIPT_DATE_MISMATCH`，保存错配证据；同一哈希以后直接继承该结论。

> 本文件是内部研究记录。轮动候选报告只使用消化后的事实和宏观判断，禁止复制节目名称、字幕路径、缓存状态、读取状态、完整性说明或“彭博/节目/字幕提到、支持、验证”等来源话术。

- 本地字幕读取状态：`FULL_TEXT_READ_FOR_SUMMARY_REBUILD`

## 主要主题

### {主题一}

- 核心内容：
- 主要论据与重要数据：

## 主要嘉宾、身份与核心判断

- {字幕可确认姓名}｜{字幕可确认身份}：{核心判断}
- 无法由字幕确认的姓名或身份不得猜测。

## 主持人与嘉宾的重要分歧

## 与当天美股/利率/美元/商品/轮动相关内容

## 信息缺口
