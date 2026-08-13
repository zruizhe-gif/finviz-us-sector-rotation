from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROXY = "https://r.jina.ai/http://finviz.com/"

MAPS = {
    "sp500": ("sec", "8119.v1.4ebc56c3.js", 10163),
    "dow30": ("sec_dji", "3701.v1.c5931c4b.js", 79341),
    "nasdaq100": ("sec_ndx", "2508.v1.7503c04c.js", 92450),
    "russell2000": ("sec_rut", "6007.v1.adb5ae11.js", 49935),
    "all_stocks": ("sec_all", "7791.v1.9fcfaaa2.js", 20375),
    "themes": ("themes", "6574.v1.c60fdedd.js", 13014),
    "etf": ("etf", "935.v1.701372ba.js", 14651),
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def unwrap_jina(text: str) -> tuple[str, dict[str, str]]:
    marker = "Markdown Content:"
    if marker not in text:
        raise ValueError("Jina wrapper missing Markdown Content marker")
    head, body = text.split(marker, 1)
    meta = {}
    for key in ("Title", "URL Source", "Published Time"):
        m = re.search(rf"(?m)^{re.escape(key)}:\s*(.*)$", head)
        if m:
            meta[key] = m.group(1).strip()
    return body.strip(), meta


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
                    return text[start : i + 1]
    raise ValueError("unbalanced object")


def extract_hierarchy(js: str, module_id: int) -> dict:
    token = f"{module_id}(e){{e.exports="
    i = js.find(token)
    if i < 0:
        # tolerate minifier using another single-letter module argument
        m = re.search(rf"{module_id}\([A-Za-z_$][\w$]*\)\{{[A-Za-z_$][\w$]*\.exports=", js)
        if not m:
            raise ValueError(f"module {module_id} not found")
        i = m.end()
    else:
        i += len(token)
    # If the exact token matched, i already points at the exported object.  For
    # the regex fallback, m.end() also points at the same location.
    j = i if i < len(js) and js[i] == "{" else js.find("{", i)
    literal = balanced_object(js, j)
    # The webpack chunk contains a JSON-compatible JavaScript object literal
    # whose property names are minified without quotes.
    literal = re.sub(r'([\{,])([A-Za-z_$][\w$]*):', r'\1"\2":', literal)
    return json.loads(literal)


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "period": "Finviz 1-Day Performance",
        "trading_date": "2026-08-11",
        "maps": {},
    }
    for key, (t, chunk, module_id) in MAPS.items():
        api_url = PROXY + f"api/map_perf?t={t}&st=d1"
        chunk_url = PROXY + f"assets/dist/{chunk}"
        api_body, api_meta = unwrap_jina(fetch(api_url))
        perf = json.loads(api_body)
        (ROOT / f"{key}_perf.json").write_text(
            json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        chunk_body, chunk_meta = unwrap_jina(fetch(chunk_url))
        hierarchy = extract_hierarchy(chunk_body, module_id)
        (ROOT / f"{key}_hierarchy.json").write_text(
            json.dumps(hierarchy, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        manifest["maps"][key] = {
            "type": t,
            "api_source": f"https://finviz.com/api/map_perf?t={t}&st=d1",
            "api_proxy_source": api_url,
            "api_metadata": api_meta,
            "subtype": perf.get("subtype"),
            "version": perf.get("version"),
            "hash": perf.get("hash"),
            "performance_node_count": len(perf.get("nodes", {})),
            "chunk_source": f"https://finviz.com/assets/dist/{chunk}",
            "chunk_proxy_source": chunk_url,
            "chunk_metadata": chunk_meta,
            "module_id": module_id,
        }
        print(key, len(perf.get("nodes", {})), len(chunk_body), flush=True)
    (ROOT / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
