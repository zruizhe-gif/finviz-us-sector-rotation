"""Direct Finviz fetcher (bypasses Jina proxy which returned 403).

Fetches the same 7 datasets as fetch_and_build.py but hits finviz.com
directly. Produces identical output files.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FINVIZ = "https://finviz.com"
TRADING_DATE = "2026-08-26"

MAPS = {
    "sp500": ("sec", 10163, "/assets/dist-legacy/8119.v1.e4b6b726.js"),
    "dow30": ("sec_dji", 79341, "/assets/dist-legacy/3701.v1.3f2be745.js"),
    "nasdaq100": ("sec_ndx", 92450, "/assets/dist-legacy/2508.v1.dfe03cb7.js"),
    "russell2000": ("sec_rut", 49935, "/assets/dist-legacy/6007.v1.9235be48.js"),
    "all_stocks": ("sec_all", 20375, "/assets/dist-legacy/7791.v1.f51c0544.js"),
    "themes": ("themes", 13014, "/assets/dist-legacy/6574.v1.4e9cc00a.js"),
    "etf": ("etf", 14651, "/assets/dist-legacy/935.v1.0dbd2864.js"),
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://finviz.com/map",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def balanced_object(text: str, start: int) -> str:
    if text[start] != "{":
        raise ValueError("object must start with {")
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start: i + 1]
    raise ValueError("unbalanced object")


def extract_hierarchy(js: str, module_id: int) -> dict:
    token = f"{module_id}(e){{e.exports="
    i = js.find(token)
    if i < 0:
        m = re.search(rf"{module_id}\([A-Za-z_$][\w$]*\)\{{[A-Za-z_$][\w$]*\.exports=", js)
        if not m:
            raise ValueError(f"module {module_id} not found")
        i = m.end()
    else:
        i += len(token)
    j = i if i < len(js) and js[i] == "{" else js.find("{", i)
    literal = balanced_object(js, j)
    literal = re.sub(r'([\{,])([A-Za-z_$][\w$]*):', r'\1"\2":', literal)
    return json.loads(literal)


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "period": "Finviz 1-Day Performance",
        "trading_date": TRADING_DATE,
        "maps": {},
        "fetch_mode": "direct_no_proxy",
    }
    for key, (t, module_id, _) in MAPS.items():
        api_url = f"{FINVIZ}/api/map_perf?t={t}&st=d1"
        perf = json.loads(fetch(api_url))
        (ROOT / f"{key}_perf.json").write_text(
            json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # chunk URL: try discovering, fallback to known
        try:
            html = fetch(f"{FINVIZ}/map?t={t}&st=d1")
            m = re.search(
                rf'<link[^>]+href="([^"]+\.js)"[^>]+data-chunk-id="map_base_{re.escape(map_type if (map_type := t) else t)}"',
                html,
            )
            chunk = m.group(1) if m else None
        except Exception:
            chunk = None
        if not chunk:
            # use the perf data's hierarchy if embedded, or skip hierarchy
            # Try fetching chunk from known list
            known = MAPS[key][2]
            chunk = known

        chunk_url = f"{FINVIZ}{chunk}" if chunk.startswith("/") else chunk
        try:
            chunk_js = fetch(chunk_url)
            hierarchy = extract_hierarchy(chunk_js, module_id)
        except Exception as e:
            print(f"WARN: hierarchy fetch failed for {key}: {e}; writing perf only")
            hierarchy = {}

        (ROOT / f"{key}_hierarchy.json").write_text(
            json.dumps(hierarchy, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        manifest["maps"][key] = {
            "type": t,
            "api_source": api_url,
            "performance_node_count": len(perf.get("nodes", {})),
            "module_id": module_id,
        }
        print(key, len(perf.get("nodes", {})), "perf", "hierarchy", len(str(hierarchy)), flush=True)

    (ROOT / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
