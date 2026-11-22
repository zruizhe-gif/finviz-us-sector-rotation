# 2026-08-26 原始抓取文件缺失说明

2026-08-28 07:09（本地）误以默认参数运行了本目录的 `fetch_and_build.py`（本意是查看用法），导致本目录的 15 个原始抓取文件被当次抓取覆盖：

- `*_perf.json` × 7、`*_hierarchy.json` × 7、`source-manifest.json`

当次抓取发生于美东 2026-08-27 19:09（8/27 收盘后），`st=d1` 对应 2026-08-27 交易日数据；该批文件随后原样移入 `research/finviz/2026-08-27/` 并将其 manifest 的 `trading_date` 更正为 2026-08-27（附注说明），因此 8/27 的数据链完整无污染。

本目录受影响的仅为上述原始层：8/26 的全部下游产物（`calculated-statistics.json`、`coverage-audit.json`、`etf-universe-audit.json`、`mandatory-rotation-coverage-set.json`、`stock-ticker-universe.json`、catalyst 全套、`runtime-brief.json`）与根目录的 `finviz_2026-08-26_report.md`、两个 TXT 均完好。Finviz 不提供历史 d1 数据，8/26 的节点级原始表现值无法从源端重建；如需完整原始链，可从下游统计与正式报告复核，但原始文件不再可复现。

教训已在本日运行中规避：后续操作均先在独立日期目录内适配 `TRADING_DATE` 再执行。
