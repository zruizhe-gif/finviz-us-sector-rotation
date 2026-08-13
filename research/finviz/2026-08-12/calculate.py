from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAP_LABELS = {
    "all_stocks": "All Stocks",
    "sp500": "S&P 500",
    "dow30": "Dow Jones 30",
    "nasdaq100": "Nasdaq 100",
    "russell2000": "Russell 2000",
}

MAP_KEYS = (*MAP_LABELS, "themes", "etf")

# These products first appeared in the performance API on 2026-08-12 but were
# not yet present in the Finviz ETF map hierarchy.  They are retained here as
# an explicit, auditable exception list instead of being silently ignored.
NEW_OUT_OF_MAP_LEVERAGED_ETFS = {
    "LITG": "Leverage Shares 2X Long LITE Daily ETF",
    "MXLL": "Leverage Shares 2X Long MXL Daily ETF",
    "MRAX": "Tradr 2X Long MRAM Daily ETF",
    "STLL": "Leverage Shares 2X Long STRL Daily ETF",
    "SITX": "Tradr 2X Long SITM Daily ETF",
    "UMCU": "Tradr 2X Long UMC Daily ETF",
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


def hierarchy_coverage(key: str):
    hierarchy = load(f"{key}_hierarchy.json")
    perf = load(f"{key}_perf.json")["nodes"]
    leaf_names = [node["name"] for node in leaves(hierarchy)]
    leaf_counts = Counter(leaf_names)
    unique_leaf_names = set(leaf_names)
    duplicate_leaf_names = sorted(
        name for name, count in leaf_counts.items() if count > 1
    )
    missing_perf = sorted(
        name for name in unique_leaf_names
        if name not in perf or perf[name] is None
    )
    extra_perf = sorted(name for name in perf if name not in unique_leaf_names)
    return {
        "hierarchy_leaf_count": len(leaf_names),
        "hierarchy_unique_leaf_count": len(unique_leaf_names),
        "duplicate_hierarchy_leaf_names": duplicate_leaf_names,
        "performance_node_count": len(perf),
        "matched_leaf_count": len(unique_leaf_names) - len(missing_perf),
        "missing_performance_count": len(missing_perf),
        "missing_performance_nodes": missing_perf,
        "out_of_hierarchy_performance_count": len(extra_perf),
        "out_of_hierarchy_performance_nodes": extra_perf,
    }


def build_coverage_audit():
    ranges = {key: hierarchy_coverage(key) for key in MAP_KEYS}
    return {
        "date": "2026-08-12",
        "status": "source_gaps_present" if any(
            row["missing_performance_count"] for row in ranges.values()
        ) else "complete",
        "policy": (
            "All hierarchy leaves are audited against the same-day performance API. "
            "Missing values are disclosed and excluded from calculations; a group with "
            "no valid members is a hard error."
        ),
        "ranges": ranges,
    }


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
        if not members:
            raise ValueError(f"{key}/{sector['name']}: no members with valid performance")
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
            if not subthemes:
                raise ValueError(f"themes/{theme['name']}: no subthemes with valid performance")
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
    coverage_audit = build_coverage_audit()
    (ROOT / "coverage-audit.json").write_text(
        json.dumps(coverage_audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result = {"date": "2026-08-12", "ranges": {}}
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
    (ROOT / "etf-universe-audit.json").write_text(
        json.dumps(build_etf_universe_audit(result["etf"]), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
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
    path = " ".join(row.get("path", [])).lower()
    if "inverse" in path or "leverage" in path:
        return True
    if re.search(r"(?<![a-z0-9])-?[123](?:\.5)?x(?![a-z0-9])", text):
        return True
    if any(term in text for term in (
        "ultra", "ultrapro", "daily bull", "daily bear", "inverse",
        "double long", "triple long", "double short", "triple short",
        "single-stock leveraged", "bull fund", "bear fund",
    )):
        return True
    # `short` by itself is ambiguous: VIX Short-Term Futures and short-duration
    # bond funds are ordinary long 1x exposures.  Only an explicit short
    # exposure is excluded here.
    neutral_short_phrases = (
        "short-term", "short term", "short duration", "short maturity",
    )
    without_neutral_short = text
    for phrase in neutral_short_phrases:
        without_neutral_short = without_neutral_short.replace(phrase, "")
    return bool(re.search(r"\bshort(?:ing)?\b", without_neutral_short))


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


def build_etf_universe_audit(selection):
    coverage = hierarchy_coverage("etf")
    perf = load("etf_perf.json")["nodes"]
    rows = etf_rows()
    excluded = [row for row in rows if is_leveraged_or_inverse(row)]
    excluded_up = sorted(
        (row for row in excluded if row["perf"] > 0),
        key=lambda row: row["perf"], reverse=True,
    )
    excluded_down = sorted(
        (row for row in excluded if row["perf"] < 0),
        key=lambda row: row["perf"],
    )
    new_out_of_map = []
    for ticker, description in NEW_OUT_OF_MAP_LEVERAGED_ETFS.items():
        new_out_of_map.append(
            {
                "ticker": ticker,
                "description": description,
                "perf": perf.get(ticker),
                "in_hierarchy": False,
                "legal_form": "ETF",
                "leveraged_or_inverse": True,
                "reason": "2x long single-stock daily leveraged ETF",
            }
        )
    return {
        "date": "2026-08-12",
        "contract_universe": "Finviz ETF map hierarchy leaves",
        "hierarchy_leaf_count": coverage["hierarchy_leaf_count"],
        "hierarchy_unique_leaf_count": coverage["hierarchy_unique_leaf_count"],
        "performance_node_count": coverage["performance_node_count"],
        "matched_map_leaf_count": coverage["matched_leaf_count"],
        "missing_map_leaf_performance": coverage["missing_performance_nodes"],
        "out_of_map_performance_node_count": coverage[
            "out_of_hierarchy_performance_count"
        ],
        "eligible_map_leaf_count": len(rows) - len(excluded),
        "excluded_map_leaf_count": len(excluded),
        "highest_positive_map_products_excluded_as_leveraged_or_inverse": excluded_up[:10],
        "lowest_negative_map_products_excluded_as_leveraged_or_inverse": excluded_down[:10],
        "new_out_of_map_leveraged_etfs_checked": new_out_of_map,
        "selected_up": selection["up"],
        "selected_down": selection["down"],
        "notes": [
            "API nodes outside the map hierarchy are not part of the original Finviz map contract universe.",
            "The named new out-of-map products are leveraged and would be excluded even under an expanded universe.",
            "VXX and VIXY are 1x long VIX short-term-futures products; `short-term` does not mean inverse.",
        ],
    }


if __name__ == "__main__":
    main()
