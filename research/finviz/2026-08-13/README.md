# Finviz 2026-08-13 raw-data cache

This directory contains the exact public Finviz map inputs used to reproduce the
2026-08-13 1-Day Performance report. `fetch_and_build.py` records source URLs,
retrieval metadata, raw API responses, and the same-close hierarchy chunks before
performing breadth and consistency-first calculations offline.

- `fetch_and_build.py` / `source-manifest.json`：动态发现同一收盘日的七套 Finviz 层级资源，锁定表现接口、层级模块、发布时间、节点数和哈希。
- `calculate.py` / `calculated-statistics.json`：按完整有效成分、清一色优先、权重收益/子主题等权收益生成机械统计。
- `coverage-audit.json` / `etf-universe-audit.json`：源覆盖审计与 ETF 母集审计。
- `mandatory-rotation-coverage-set.json`：六个范围涨3/跌3合并后的 16 项集合、三项轮入/三项轮出、ETF 最终敞口去重结果与报告完整性闸门。
- `catalyst-cache.json`：按股票代码去重的一次性催化研究缓存（两步研究，命中同日直接事件即止）。
- `generate_outputs.py`：生成主统计报告和两个 TXT，并核验六个范围的四列六行结构、宽度恒等式、逐股原因和代码集合。

ETF 绩效接口暴露的产品母集大于可见 ETF 地图层级；正式选择严格限于同日地图层级可见叶子，并按底层经济敞口去重。
