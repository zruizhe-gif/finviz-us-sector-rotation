from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAP_LABELS = {
    "all_stocks": "All Stocks",
    "sp500": "S&P 500",
    "dow30": "Dow Jones 30",
    "nasdaq100": "Nasdaq 100",
    "russell2000": "Russell 2000",
}


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def leaves(node):
    children = node.get("children") or []
    if not children:
        yield node
    else:
        for child in children:
            yield from leaves(child)


def sector_rows(key: str):
    hierarchy = load(f"{key}_hierarchy.json")
    perf = load(f"{key}_perf.json")["nodes"]
    rows = []
    for sector in hierarchy["children"]:
        members = []
        for node in leaves(sector):
            ticker = node["name"]
            if ticker in perf and perf[ticker] is not None:
                members.append(
                    {
                        "ticker": ticker,
                        "company": node.get("description", ""),
                        "value": node.get("value", 0),
                        "perf": perf[ticker],
                    }
                )
        up = sum(x["perf"] > 0 for x in members)
        down = sum(x["perf"] < 0 for x in members)
        flat = len(members) - up - down
        denominator = sum(x["value"] for x in members if x["value"] > 0)
        weighted = (
            sum(x["value"] * x["perf"] for x in members if x["value"] > 0)
            / denominator
            if denominator
            else sum(x["perf"] for x in members) / len(members)
        )
        rows.append(
            {
                "name": sector["name"],
                "count": len(members),
                "up": up,
                "down": down,
                "flat": flat,
                "up_pct": 100 * up / len(members),
                "down_pct": 100 * down / len(members),
                "overall_perf": weighted,
                "uniform_up": up == len(members),
                "uniform_down": down == len(members),
                "members": members,
            }
        )
    return rows


def select(rows, direction):
    if direction == "up":
        uniform = sorted(
            (r for r in rows if r["uniform_up"]),
            key=lambda r: r["overall_perf"], reverse=True,
        )
        other = sorted(
            (r for r in rows if not r["uniform_up"]),
            key=lambda r: r["overall_perf"], reverse=True,
        )
    else:
        uniform = sorted(
            (r for r in rows if r["uniform_down"]),
            key=lambda r: r["overall_perf"],
        )
        other = sorted(
            (r for r in rows if not r["uniform_down"]),
            key=lambda r: r["overall_perf"],
        )
    picks = []
    for r in uniform[:3]:
        picks.append({**r, "identity": "清一色优先"})
    for r in other:
        if len(picks) >= 3:
            break
        if r["name"] not in {x["name"] for x in picks}:
            picks.append({**r, "identity": "平均表现补位"})
    for r in picks:
        r["extreme"] = sorted(
            r["members"], key=lambda x: x["perf"], reverse=direction == "up"
        )[:3]
    return uniform, picks


def theme_rows():
    hierarchy = load("themes_hierarchy.json")
    sub_perf = load("themes_perf.json")["nodes"]
    stock_perf = load("all_stocks_perf.json")["nodes"]
    rows = []
    for bucket in hierarchy["children"]:
        for theme in bucket["children"]:
            subthemes = []
            tickers = set()
            for sub in theme.get("children", []):
                name = sub["name"]
                if name in sub_perf and sub_perf[name] is not None:
                    subthemes.append(
                        {
                            "name": name,
                            "display": sub.get("displayName") or sub.get("description") or name,
                            "description": sub.get("description", ""),
                            "perf": sub_perf[name],
                        }
                    )
                for ticker in re.split(r"\s*,\s*", sub.get("extra", "")):
                    if ticker:
                        tickers.add(ticker)
            members = [
                {"ticker": t, "perf": stock_perf[t]}
                for t in sorted(tickers)
                if t in stock_perf and stock_perf[t] is not None
            ]
            up = sum(x["perf"] > 0 for x in subthemes)
            down = sum(x["perf"] < 0 for x in subthemes)
            flat = len(subthemes) - up - down
            rows.append(
                {
                    "name": theme["name"],
                    "count": len(subthemes),
                    "up": up,
                    "down": down,
                    "flat": flat,
                    "up_pct": 100 * up / len(subthemes),
                    "down_pct": 100 * down / len(subthemes),
                    "overall_perf": sum(x["perf"] for x in subthemes) / len(subthemes),
                    "uniform_up": up == len(subthemes),
                    "uniform_down": down == len(subthemes),
                    "subthemes": subthemes,
                    "members": members,
                }
            )
    return rows


def main():
    result = {"date": "2026-08-11", "ranges": {}}
    for key, label in MAP_LABELS.items():
        rows = sector_rows(key)
        uniform_up, up = select(rows, "up")
        uniform_down, down = select(rows, "down")
        result["ranges"][key] = {
            "label": label,
            "all": rows,
            "uniform_up": uniform_up,
            "uniform_down": uniform_down,
            "selected_up": up,
            "selected_down": down,
        }
    rows = theme_rows()
    uniform_up, up = select(rows, "up")
    uniform_down, down = select(rows, "down")
    result["ranges"]["themes"] = {
        "label": "Themes",
        "all": rows,
        "uniform_up": uniform_up,
        "uniform_down": uniform_down,
        "selected_up": up,
        "selected_down": down,
    }
    result["etf"] = etf_selection()
    (ROOT / "calculated-statistics.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for key, r in result["ranges"].items():
        print(
            r["label"],
            "groups", len(r["all"]),
            "uniform_up", [x["name"] for x in r["uniform_up"]],
            "uniform_down", [x["name"] for x in r["uniform_down"]],
            "selected_up", [(x["name"], x["identity"]) for x in r["selected_up"]],
            "selected_down", [(x["name"], x["identity"]) for x in r["selected_down"]],
        )
    print("ETF", [(x["ticker"], x["perf"], x["cluster"]) for x in result["etf"]["up"]], [(x["ticker"], x["perf"], x["cluster"]) for x in result["etf"]["down"]])


def is_leveraged_or_inverse(row):
    text = " ".join(
        [row["ticker"], row.get("description", ""), " ".join(row.get("path", []))]
    ).lower()
    terms = (
        "2x", "3x", "-1x", "-2x", "-3x", "ultra", "ultrapro",
        "daily bull", "daily bear", "short", "inverse", "leverage",
    )
    return any(term in text for term in terms)


def etf_rows():
    hierarchy = load("etf_hierarchy.json")
    perf = load("etf_perf.json")["nodes"]
    rows = []

    def walk(node, path=()):
        children = node.get("children") or []
        if not children:
            ticker = node["name"]
            if ticker in perf and perf[ticker] is not None:
                rows.append(
                    {
                        "ticker": ticker,
                        "description": node.get("description", ""),
                        "perf": perf[ticker],
                        "path": list(path),
                    }
                )
        else:
            for child in children:
                walk(child, path + ((node["name"],) if node["name"] != "Root" else ()))

    walk(hierarchy)
    return rows


def exposure_cluster(row):
    t = row["ticker"]
    desc = row["description"].lower()
    path = " ".join(row["path"]).lower()
    if t in {"BNO", "USO", "DBO"} or "crude oil" in desc:
        return "原油期货"
    if t in {"PSI", "DRAM", "FTXL", "SOXX", "SMH", "XSD"} or "semiconductor" in desc:
        return "半导体股票"
    if "south korea" in desc or t == "EWY":
        return "韩国股票"
    if "singapore" in desc or t == "EWS":
        return "新加坡股票"
    if "home construction" in desc or "homebuilders" in desc or t in {"ITB", "XHB"}:
        return "美国住宅建筑"
    if "brazil" in desc or t in {"EWZ", "BRF"}:
        return "巴西股票"
    if "china" in desc or "ftse china" in desc or t in {"MCHI", "FXI", "GXC", "PGJ"}:
        return "中国股票"
    if "healthcare providers" in desc or "health care services" in desc or t in {"XHS", "IHF"}:
        return "美国医疗服务"
    if "real estate" in desc or "reit" in desc:
        return "房地产股票"
    if "silver" in desc or t in {"SLV", "SIVR"}:
        return "白银现货信托"
    if "vix" in desc:
        return "VIX期货"
    if "energy" in desc and "fixed income" not in path:
        return "能源生产商股票"
    return f"{path}｜{desc}"


def etf_selection():
    eligible = [r for r in etf_rows() if not is_leveraged_or_inverse(r)]
    result = {}
    for direction in ("up", "down"):
        ordered = sorted(eligible, key=lambda r: r["perf"], reverse=direction == "up")
        clusters = {}
        for row in ordered:
            cluster = exposure_cluster(row)
            row = {**row, "cluster": cluster}
            clusters.setdefault(cluster, []).append(row)
        selected = []
        for row in ordered:
            cluster = exposure_cluster(row)
            if cluster not in {x["cluster"] for x in selected}:
                selected.append({**row, "cluster": cluster})
            if len(selected) == 3:
                break
        for row in selected:
            row["merged"] = [
                x for x in clusters[row["cluster"]] if x["ticker"] != row["ticker"]
            ][:5]
        result[direction] = selected
    return result


if __name__ == "__main__":
    main()
