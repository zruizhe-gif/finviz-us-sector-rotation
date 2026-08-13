# Finviz 2026-08-12 raw-data cache

This directory contains the exact public Finviz map inputs used to reproduce the
2026-08-12 1-Day Performance report. `fetch_and_build.py` records source URLs,
retrieval metadata, raw API responses, and the same-close hierarchy chunks before
performing breadth and consistency-first calculations offline.

The ETF performance API exposes a broader symbol universe than the visible ETF map
hierarchy. The report follows the original contract's Finviz ETF map scope: only
products present as leaves in the same-close hierarchy are eligible. The API versus
hierarchy difference and newly observed tickers are retained in audit artifacts so
that a map-bundle change cannot silently alter the selection universe.

