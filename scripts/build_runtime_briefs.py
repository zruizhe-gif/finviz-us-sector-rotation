#!/usr/bin/env python3
"""Build compact LLM runtime inputs from the complete Finviz research artifacts.

The complete hierarchy, performance, calculated-statistics, coverage, ETF audit,
mandatory coverage, ticker universe, and catalyst cache remain the audit record.
This program only creates a loss-bounded read layer for report drafting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
RANGE_KEYS = (
    "all_stocks",
    "sp500",
    "dow30",
    "nasdaq100",
    "russell2000",
    "themes",
)

FIXED_SECTION_FOUR_ROWS = (
    ("信息技术", ("XLK",)),
    ("半导体", ("SOXX", "XSD")),
    ("存储/内存", ("DRAM",)),
    ("软件", ("IGV", "XSW")),
    ("云计算", ("WCLD",)),
    ("网络安全", ("IHAK",)),
    ("通信服务", ("XLC", "RSPC")),
    ("可选消费", ("XLY", "RSPD")),
    ("必需消费", ("XLP",)),
    ("食品饮料", ("PBJ",)),
    ("零售", ("XRT",)),
    ("住宅建筑", ("XHB",)),
    ("能源", ("XLE", "XOP", "AMLP", "CRAK")),
    ("医疗保健", ("XLV",)),
    ("生物科技", ("XBI",)),
    ("金融", ("XLF", "KBE", "KRE", "KIE", "IAI")),
    ("综合工业", ("XLI",)),
    ("航空国防", ("ITA",)),
    ("运输", ("IYT",)),
    ("基础材料", ("XLB",)),
    ("金属矿业", ("XME",)),
    ("房地产/REIT", ("IYR", "RSPR")),
    ("电信", ("IYZ",)),
    ("公用事业", ("XLU",)),
)

COMMODITY_OBSERVATION_ROWS = (
    ("原油", ("BNO",)),
    ("天然气", ("UNG",)),
    ("黄金", ("GLD",)),
    ("白银", ("SLV",)),
    ("工业金属", ("DBB",)),
    ("玉米", ("CORN",)),
)

# Only industries already authorized by references/15 may be appended after the
# fixed 24 rows. Aliases cover the English labels used by Finviz maps.
RELIABLE_APPEND_INDUSTRIES = {
    "Pharmaceuticals": ("制药", ("PPH",), ("XPH",)),
    "Pharmaceutical": ("制药", ("PPH",), ("XPH",)),
    "Medical Devices": ("医疗器械", ("IHI",), ("XHE",)),
    "Medical Equipment": ("医疗器械", ("IHI",), ("XHE",)),
    "Medical Services": ("医疗服务", ("IHF",), ("FXH", "XHS")),
    "Healthcare Providers": ("医疗服务", ("IHF",), ("FXH", "XHS")),
    "US Manufacturing": ("美国制造/工业复兴", ("PAVE",), ("AIRR", "WELD")),
    "Industrial Renaissance": ("美国制造/工业复兴", ("PAVE",), ("AIRR", "WELD")),
}


class BriefError(RuntimeError):
    """Raised when complete inputs cannot support a valid compact brief."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BriefError(f"required input is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BriefError(f"invalid JSON: {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_strings(values: list[str]) -> str:
    payload = "\n".join(values).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_json(payload: Any) -> str:
    serialized = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    return hashlib.sha256(serialized).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def write_lines(path: Path, values: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(values) + "\n", encoding="utf-8")


def require_date(payload: dict[str, Any], expected: str, source: str) -> None:
    actual = payload.get("date") or payload.get("trading_date")
    if actual != expected:
        raise BriefError(f"{source} date mismatch: expected {expected}, got {actual!r}")


def identity(row: dict[str, Any], direction: str) -> str:
    if direction == "up" and row.get("uniform_up") is True:
        return "清一色优先"
    if direction == "down" and row.get("uniform_down") is True:
        return "清一色优先"
    return "平均表现补位"


def selected_expected(rows: list[dict[str, Any]], direction: str) -> list[str]:
    flag = "uniform_up" if direction == "up" else "uniform_down"
    reverse = direction == "up"
    uniform = sorted(
        (row for row in rows if row.get(flag) is True),
        key=lambda row: float(row["overall_perf"]),
        reverse=reverse,
    )
    uniform_names = {row["name"] for row in uniform}
    fallback = sorted(
        (row for row in rows if row["name"] not in uniform_names),
        key=lambda row: float(row["overall_perf"]),
        reverse=reverse,
    )
    return [row["name"] for row in (uniform + fallback)[:3]]


def company_index(calculated: dict[str, Any]) -> dict[str, str]:
    companies: dict[str, str] = {}
    for scope_key in RANGE_KEYS:
        scope = calculated["ranges"][scope_key]
        for row in scope.get("all", []):
            for member in row.get("members", []):
                ticker = member.get("ticker")
                company = member.get("company")
                if ticker and company:
                    companies.setdefault(str(ticker), str(company))
    return companies


def compact_selected_row(
    row: dict[str, Any], direction: str, companies: dict[str, str]
) -> dict[str, Any]:
    extremes = []
    for item in row.get("extreme", []):
        ticker = str(item["ticker"])
        extremes.append(
            {
                "ticker": ticker,
                "company": item.get("company") or companies.get(ticker),
                "perf": item.get("perf"),
            }
        )
    if len(extremes) > 3:
        raise BriefError(f"selected group {row.get('name')} has more than three extremes")

    result = {
        "name": row["name"],
        "component_count": row["count"],
        "up": row["up"],
        "down": row["down"],
        "flat": row["flat"],
        "up_pct": row["up_pct"],
        "down_pct": row["down_pct"],
        "overall_perf": row["overall_perf"],
        "uniform_up": bool(row.get("uniform_up")),
        "uniform_down": bool(row.get("uniform_down")),
        "selection_identity": identity(row, direction),
        "target_stocks": extremes,
    }
    if "subthemes" in row:
        result["subthemes"] = [
            {
                "name": item.get("name"),
                "display": item.get("display"),
                "description": item.get("description"),
                "perf": item.get("perf"),
            }
            for item in row.get("subthemes", [])
        ]
    return result


def build_scope_briefs(
    calculated: dict[str, Any], companies: dict[str, str]
) -> tuple[dict[str, Any], dict[str, Any]]:
    scopes: dict[str, Any] = {}
    audits: dict[str, Any] = {}
    for scope_key in RANGE_KEYS:
        source = calculated["ranges"].get(scope_key)
        if not source:
            raise BriefError(f"calculated statistics missing scope: {scope_key}")
        selected_up = source.get("selected_up", [])
        selected_down = source.get("selected_down", [])
        if len(selected_up) != 3 or len(selected_down) != 3:
            raise BriefError(
                f"{scope_key} must contain exactly three selected up and three selected down groups"
            )

        expected_up = selected_expected(source.get("all", []), "up")
        expected_down = selected_expected(source.get("all", []), "down")
        actual_up = [row["name"] for row in selected_up]
        actual_down = [row["name"] for row in selected_down]
        uniform_up = sorted(
            source.get("uniform_up", []),
            key=lambda row: float(row["overall_perf"]),
            reverse=True,
        )
        uniform_down = sorted(
            source.get("uniform_down", []),
            key=lambda row: float(row["overall_perf"]),
        )
        scope_pass = actual_up == expected_up and actual_down == expected_down
        audits[scope_key] = {
            "status": "PASS" if scope_pass else "FAIL",
            "uniform_up_candidate_count": len(uniform_up),
            "uniform_up_candidates": [row["name"] for row in uniform_up],
            "uniform_down_candidate_count": len(uniform_down),
            "uniform_down_candidates": [row["name"] for row in uniform_down],
            "expected_selected_up": expected_up,
            "actual_selected_up": actual_up,
            "expected_selected_down": expected_down,
            "actual_selected_down": actual_down,
        }
        scopes[scope_key] = {
            "label": source.get("label", scope_key),
            "selected_up": [
                compact_selected_row(row, "up", companies) for row in selected_up
            ],
            "selected_down": [
                compact_selected_row(row, "down", companies) for row in selected_down
            ],
        }
    audits["overall_status"] = (
        "PASS"
        if all(audit["status"] == "PASS" for key, audit in audits.items() if key != "overall_status")
        else "FAIL"
    )
    return scopes, audits


def evidence_row(
    scope_key: str,
    scope_label: str,
    direction: str,
    rank: int,
    row: dict[str, Any],
) -> dict[str, Any]:
    return {
        "scope": scope_label,
        "scope_key": scope_key,
        "direction": direction,
        "rank": rank,
        "name": row["name"],
        "identity": identity(row, direction),
        "component_count": row["count"],
        "up": row["up"],
        "down": row["down"],
        "flat": row["flat"],
        "up_pct": row["up_pct"],
        "down_pct": row["down_pct"],
        "overall_perf": row["overall_perf"],
        "uniform": bool(row.get("uniform_up" if direction == "up" else "uniform_down")),
    }


def build_mandatory(calculated: dict[str, Any], trading_date: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    scopes: dict[str, Any] = {}
    for scope_key in RANGE_KEYS:
        scope = calculated["ranges"][scope_key]
        scope_label = scope.get("label", scope_key)
        scope_payload = {"label": scope_label, "selected_up": [], "selected_down": []}
        for direction in ("up", "down"):
            for rank, row in enumerate(scope[f"selected_{direction}"], start=1):
                evidence = evidence_row(scope_key, scope_label, direction, rank, row)
                grouped[row["name"]].append(evidence)
                scope_payload[f"selected_{direction}"].append(evidence)
        scopes[scope_key] = scope_payload

    items = []
    for name in sorted(grouped):
        evidence = grouped[name]
        up_evidence = [item for item in evidence if item["direction"] == "up"]
        down_evidence = [item for item in evidence if item["direction"] == "down"]
        items.append(
            {
                "name": name,
                "total_frequency": len(evidence),
                "up_frequency": len(up_evidence),
                "down_frequency": len(down_evidence),
                "net_direction_score": len(up_evidence) - len(down_evidence),
                "independent_scope_count": len({item["scope_key"] for item in evidence}),
                "uniform_up_frequency": sum(item["uniform"] for item in up_evidence),
                "uniform_down_frequency": sum(item["uniform"] for item in down_evidence),
                "average_selected_up_perf": (
                    sum(float(item["overall_perf"]) for item in up_evidence) / len(up_evidence)
                    if up_evidence
                    else None
                ),
                "average_selected_down_perf": (
                    sum(float(item["overall_perf"]) for item in down_evidence) / len(down_evidence)
                    if down_evidence
                    else None
                ),
                "evidence": evidence,
            }
        )

    in_ranked = sorted(
        (item for item in items if item["net_direction_score"] > 0),
        key=lambda item: (
            -item["net_direction_score"],
            -item["up_frequency"],
            -item["uniform_up_frequency"],
            -(item["average_selected_up_perf"] or float("-inf")),
            item["name"],
        ),
    )
    out_ranked = sorted(
        (item for item in items if item["net_direction_score"] < 0),
        key=lambda item: (
            item["net_direction_score"],
            -item["down_frequency"],
            -item["uniform_down_frequency"],
            item["average_selected_down_perf"] or float("inf"),
            item["name"],
        ),
    )

    def selected_item(item: dict[str, Any], direction: str) -> dict[str, Any]:
        payload = {
            "name": item["name"],
            "up_frequency": item["up_frequency"],
            "down_frequency": item["down_frequency"],
            "net_direction_score": item["net_direction_score"],
        }
        payload[f"average_selected_{direction}_perf"] = item[
            f"average_selected_{direction}_perf"
        ]
        return payload

    return {
        "date": trading_date,
        "source": "calculated-statistics.json",
        "selection_basis": (
            "All Stocks, S&P 500, Dow Jones 30, Nasdaq 100, Russell 2000 and Themes "
            "each contribute exactly three selected up groups and three selected down groups; "
            "the complete union is preserved before the 3-in/3-out synthesis."
        ),
        "scope_count": len(RANGE_KEYS),
        "scopes": scopes,
        "unique_item_count": len(items),
        "items": items,
        "selected_rotation_3_in_3_out": {
            "method": (
                "Rank by net directional frequency, same-direction frequency, uniform-consistency "
                "frequency and average performance; preserve conflicting scope evidence."
            ),
            "in": [selected_item(item, "up") for item in in_ranked[:3]],
            "out": [selected_item(item, "down") for item in out_ranked[:3]],
        },
    }


def build_ticker_universe(
    calculated: dict[str, Any], trading_date: str, companies: dict[str, str]
) -> dict[str, Any]:
    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for scope_key in RANGE_KEYS:
        scope = calculated["ranges"][scope_key]
        scope_label = scope.get("label", scope_key)
        for direction in ("up", "down"):
            for group_rank, row in enumerate(scope[f"selected_{direction}"], start=1):
                for stock_rank, stock in enumerate(row.get("extreme", []), start=1):
                    ticker = str(stock["ticker"])
                    occurrences[ticker].append(
                        {
                            "scope": scope_label,
                            "scope_key": scope_key,
                            "direction": direction,
                            "group": row["name"],
                            "group_rank": group_rank,
                            "stock_rank": stock_rank,
                            "perf": stock.get("perf"),
                        }
                    )
    tickers = sorted(occurrences)
    items = [
        {
            "ticker": ticker,
            "company": companies.get(ticker),
            "occurrence_count": len(occurrences[ticker]),
            "occurrences": occurrences[ticker],
        }
        for ticker in tickers
    ]
    missing_company = [item["ticker"] for item in items if not item["company"]]
    if missing_company:
        raise BriefError(f"company names missing for selected tickers: {missing_company}")
    return {
        "date": trading_date,
        "source": "calculated-statistics.json selected_up/selected_down extreme stocks",
        "ticker_count": len(tickers),
        "tickers": tickers,
        "items": items,
    }


def compact_etf_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "ticker": row.get("ticker"),
        "description": row.get("description"),
        "perf": row.get("perf"),
        "cluster": row.get("cluster"),
        "primary_exposure": row.get("primary_exposure"),
        "legal_form": row.get("legal_form"),
        "merged_same_exposure": row.get("merged", []),
    }


def coverage_brief(coverage: dict[str, Any]) -> dict[str, Any]:
    ranges: dict[str, Any] = {}
    fatal = []
    all_missing = []
    for scope_key, row in coverage.get("ranges", {}).items():
        missing = list(row.get("missing_performance_nodes", []))
        missing_count = int(row.get("missing_performance_count", len(missing)))
        if missing_count != len(missing):
            fatal.append(f"{scope_key}: missing count/list mismatch")
        if int(row.get("matched_leaf_count", 0)) <= 0:
            fatal.append(f"{scope_key}: zero matched leaves")
        if row.get("duplicate_hierarchy_leaf_names"):
            fatal.append(f"{scope_key}: duplicate hierarchy leaf names")
        all_missing.extend(f"{scope_key}:{ticker}" for ticker in missing)
        ranges[scope_key] = {
            "hierarchy_leaf_count": row.get("hierarchy_leaf_count"),
            "hierarchy_unique_leaf_count": row.get("hierarchy_unique_leaf_count"),
            "performance_node_count": row.get("performance_node_count"),
            "matched_leaf_count": row.get("matched_leaf_count"),
            "missing_performance_count": missing_count,
            "missing_performance_nodes": missing,
            "out_of_hierarchy_performance_count": row.get(
                "out_of_hierarchy_performance_count"
            ),
        }
    return {
        "status": "FAIL" if fatal else "PASS",
        "qualification": "disclosed_source_gaps" if all_missing and not fatal else None,
        "source_status": coverage.get("status"),
        "missing_code_count": len(all_missing),
        "fatal_errors": fatal,
        "ranges": ranges,
    }


def section_four_brief(
    etf_perf: dict[str, Any], mandatory: dict[str, Any]
) -> dict[str, Any]:
    nodes = etf_perf.get("nodes")
    if not isinstance(nodes, dict):
        raise BriefError("etf_perf.json does not contain a nodes mapping")
    fixed_rows = []
    missing = []
    for order, (label, tickers) in enumerate(FIXED_SECTION_FOUR_ROWS, start=1):
        performances = {}
        for ticker in tickers:
            value = nodes.get(ticker)
            if not isinstance(value, (int, float)):
                missing.append(ticker)
                performances[ticker] = None
            else:
                performances[ticker] = value
        fixed_rows.append(
            {
                "order": order,
                "label": label,
                "tickers": list(tickers),
                "performances": performances,
            }
        )
    if missing:
        raise BriefError(f"fixed Section IV ETF performance missing: {sorted(set(missing))}")

    append_candidates = []
    for item in mandatory.get("items", []):
        mapping = RELIABLE_APPEND_INDUSTRIES.get(item.get("name"))
        if not mapping:
            continue
        label, display_tickers, internal_tickers = mapping
        performances = {}
        for ticker in display_tickers:
            value = nodes.get(ticker)
            if not isinstance(value, (int, float)):
                raise BriefError(f"append candidate ETF performance missing: {ticker}")
            performances[ticker] = value
        append_candidates.append(
            {
                "source_group": item["name"],
                "label": label,
                "display_tickers": list(display_tickers),
                "performances": performances,
                "internal_cross_check_only": list(internal_tickers),
                "mandatory_evidence": item,
            }
        )
    return {
        "fixed_row_count": len(fixed_rows),
        "fixed_rows": fixed_rows,
        "append_candidates": append_candidates,
        "prohibited_without_reliable_etf_examples": ["大数据", "金属商品", "生物识别"],
    }


def commodity_brief(etf_perf: dict[str, Any]) -> dict[str, Any]:
    """Keep the six persisted commodity-state proxies needed by Section V."""
    nodes = etf_perf.get("nodes")
    if not isinstance(nodes, dict):
        raise BriefError("etf_perf.json does not contain a nodes mapping")
    rows = []
    missing = []
    for label, tickers in COMMODITY_OBSERVATION_ROWS:
        performances = {}
        for ticker in tickers:
            value = nodes.get(ticker)
            if not isinstance(value, (int, float)):
                missing.append(ticker)
                performances[ticker] = None
            else:
                performances[ticker] = value
        rows.append(
            {
                "label": label,
                "tickers": list(tickers),
                "performances": performances,
            }
        )
    if missing:
        raise BriefError(
            f"commodity observation ETF performance missing: {sorted(set(missing))}"
        )
    return {"row_count": len(rows), "rows": rows, "status": "PASS"}


def build_runtime_brief(
    research_dir: Path,
    trading_date: str,
    calculated: dict[str, Any],
    coverage: dict[str, Any],
    mandatory: dict[str, Any],
    ticker_universe: dict[str, Any],
    etf_audit: dict[str, Any],
    etf_perf: dict[str, Any],
) -> dict[str, Any]:
    companies = company_index(calculated)
    scopes, consistency = build_scope_briefs(calculated, companies)
    coverage_result = coverage_brief(coverage)

    etf_selection = {
        "selected_up": [compact_etf_row(row) for row in calculated["etf"]["up"]],
        "selected_down": [compact_etf_row(row) for row in calculated["etf"]["down"]],
        "same_economic_exposure_audit": etf_audit.get("same_economic_exposure_audit"),
    }
    if len(etf_selection["selected_up"]) != 3 or len(etf_selection["selected_down"]) != 3:
        raise BriefError("ETF selection must contain exactly three up and three down products")
    calculated_etfs = {
        direction: [row["ticker"] for row in etf_selection[f"selected_{direction}"]]
        for direction in ("up", "down")
    }
    audit_etfs = {
        direction: [row.get("ticker") for row in etf_audit.get(f"selected_{direction}", [])]
        for direction in ("up", "down")
    }
    etf_selection["audit_status"] = (
        "PASS" if calculated_etfs == audit_etfs else "FAIL"
    )
    etf_selection["calculated_tickers"] = calculated_etfs
    etf_selection["audit_tickers"] = audit_etfs

    source_files = [
        "calculated-statistics.json",
        "coverage-audit.json",
        "mandatory-rotation-coverage-set.json",
        "etf-universe-audit.json",
        "etf_perf.json",
        "stock-ticker-universe.json",
    ]
    source_hashes = {
        name: sha256_file(research_dir / name)
        for name in source_files
        if (research_dir / name).exists()
    }
    source_hashes.setdefault(
        "mandatory-rotation-coverage-set.json", sha256_json(mandatory)
    )
    source_hashes.setdefault("stock-ticker-universe.json", sha256_json(ticker_universe))
    overall_pass = (
        consistency["overall_status"] == "PASS"
        and coverage_result["status"] == "PASS"
        and etf_selection["audit_status"] == "PASS"
        and mandatory.get("scope_count") == 6
        and ticker_universe.get("ticker_count") == len(ticker_universe.get("tickers", []))
    )
    return {
        "_meta": {
            "schema_version": SCHEMA_VERSION,
            "brief_type": "finviz_runtime_brief",
            "date": trading_date,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "purpose": "LLM drafting input; complete machine artifacts remain authoritative",
            "source_hashes": source_hashes,
            "full_artifacts_preserved": [
                "calculated-statistics.json",
                "coverage-audit.json",
                "mandatory-rotation-coverage-set.json",
                "all hierarchy/performance JSON files",
                "etf-universe-audit.json",
                "stock-ticker-universe.json",
            ],
            "normal_llm_read_policy": (
                "Read this brief, not the full calculated/hierarchy/performance/coverage files; "
                "open a complete artifact only for a named anomaly."
            ),
        },
        "statistics": scopes,
        "consistency_priority_audit": consistency,
        "etf_selection": etf_selection,
        "mandatory_rotation_coverage": mandatory,
        "ticker_universe": {
            "ticker_count": ticker_universe["ticker_count"],
            "ticker_set_sha256": sha256_strings(ticker_universe["tickers"]),
            "tickers": ticker_universe["tickers"],
        },
        "section_four_etf_observation": section_four_brief(etf_perf, mandatory),
        "commodity_observation": commodity_brief(etf_perf),
        "coverage": coverage_result,
        "overall_status": "PASS" if overall_pass else "FAIL",
    }


def build_catalyst_brief(
    cache_path: Path,
    ticker_universe: dict[str, Any],
    trading_date: str,
) -> dict[str, Any]:
    cache = read_json(cache_path)
    records = {key: value for key, value in cache.items() if key != "_meta"}
    expected = list(ticker_universe["tickers"])
    missing = sorted(set(expected) - set(records))
    extra = sorted(set(records) - set(expected))
    incomplete = sorted(
        ticker
        for ticker in expected
        if ticker in records
        and (
            not records[ticker].get("status")
            or not records[ticker].get("output_conclusion")
        )
    )
    if missing or incomplete:
        raise BriefError(
            f"catalyst coverage incomplete: missing={missing}, incomplete={incomplete}"
        )

    universe_items = {item["ticker"]: item for item in ticker_universe["items"]}
    brief_records = []
    for ticker in expected:
        row = records[ticker]
        universe = universe_items[ticker]
        perf_values = sorted(
            {
                occurrence.get("perf")
                for occurrence in universe.get("occurrences", [])
                if isinstance(occurrence.get("perf"), (int, float))
            }
        )
        sources = []
        for index, source in enumerate(row.get("sources", []), start=1):
            sources.append(
                {
                    "id": f"{ticker}-{index}",
                    "title": source.get("title"),
                    "publisher": source.get("publisher"),
                    "published_at": source.get("published_at"),
                    "url": source.get("url"),
                }
            )
        brief_records.append(
            {
                "ticker": ticker,
                "company": row.get("company") or universe.get("company"),
                "perf": perf_values[0] if len(perf_values) == 1 else perf_values,
                "status": row.get("status"),
                "research_level": row.get("research_level"),
                "direct_catalyst": row.get("direct_event"),
                "event_time_et": row.get("event_time_et"),
                "industry_linkage": row.get("confirmed_linkage"),
                "conclusion": row.get("output_conclusion"),
                "evidence_index": sources,
            }
        )

    status_counts = Counter(str(row["status"]) for row in brief_records)
    level_counts = Counter(str(row["research_level"]) for row in brief_records)
    return {
        "_meta": {
            "schema_version": SCHEMA_VERSION,
            "brief_type": "catalyst_brief",
            "date": trading_date,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_file": cache_path.name,
            "source_sha256": sha256_file(cache_path),
            "expected_ticker_count": len(expected),
            "covered_ticker_count": len(brief_records),
            "coverage_pct": 100.0,
            "coverage_status": "PASS",
            "extra_cache_tickers": extra,
            "status_counts": dict(status_counts),
            "research_level_counts": dict(level_counts),
            "normal_llm_read_policy": (
                "Read this brief for drafting; open catalyst-cache.json only for a named ticker anomaly."
            ),
        },
        "records": brief_records,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="Trading date in YYYY-MM-DD form")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Skill project root (defaults to the parent of scripts/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Brief output directory (defaults to research/finviz/YYYY-MM-DD)",
    )
    parser.add_argument(
        "--write-txt",
        action="store_true",
        help="Write the two required ticker TXT files to the project root",
    )
    parser.add_argument(
        "--skip-catalyst",
        action="store_true",
        help="Build only runtime-brief; use before the full catalyst cache is ready",
    )
    parser.add_argument(
        "--require-catalyst",
        action="store_true",
        help="Fail unless catalyst-cache.json exists and covers every selected ticker",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run all available assertions without writing files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        raise BriefError("--date must use YYYY-MM-DD")
    project_root = args.project_root.resolve()
    research_dir = project_root / "research" / "finviz" / args.date
    output_dir = (args.output_dir or research_dir).resolve()

    input_paths = {
        "calculated": research_dir / "calculated-statistics.json",
        "coverage": research_dir / "coverage-audit.json",
        "etf_audit": research_dir / "etf-universe-audit.json",
        "etf_perf": research_dir / "etf_perf.json",
    }
    calculated = read_json(input_paths["calculated"])
    coverage = read_json(input_paths["coverage"])
    etf_audit = read_json(input_paths["etf_audit"])
    etf_perf = read_json(input_paths["etf_perf"])
    for name, payload in (
        ("calculated-statistics.json", calculated),
        ("coverage-audit.json", coverage),
        ("etf-universe-audit.json", etf_audit),
    ):
        require_date(payload, args.date, name)

    companies = company_index(calculated)
    mandatory_path = research_dir / "mandatory-rotation-coverage-set.json"
    ticker_path = research_dir / "stock-ticker-universe.json"
    mandatory = (
        read_json(mandatory_path)
        if mandatory_path.exists()
        else build_mandatory(calculated, args.date)
    )
    ticker_universe = build_ticker_universe(calculated, args.date, companies)
    if ticker_path.exists():
        existing_tickers = read_json(ticker_path)
        if existing_tickers.get("tickers") != ticker_universe["tickers"]:
            raise BriefError("existing stock-ticker-universe.json does not match calculated selections")

    runtime = build_runtime_brief(
        research_dir,
        args.date,
        calculated,
        coverage,
        mandatory,
        ticker_universe,
        etf_audit,
        etf_perf,
    )
    if runtime["overall_status"] != "PASS":
        raise BriefError("runtime brief quality gates failed")

    catalyst_path = research_dir / "catalyst-cache.json"
    catalyst = None
    if not args.skip_catalyst:
        if catalyst_path.exists():
            catalyst = build_catalyst_brief(catalyst_path, ticker_universe, args.date)
        elif args.require_catalyst:
            raise BriefError(f"required input is missing: {catalyst_path}")

    if not args.validate_only:
        if not mandatory_path.exists():
            write_json(mandatory_path, mandatory)
        if not ticker_path.exists():
            write_json(ticker_path, ticker_universe)
        write_json(output_dir / "runtime-brief.json", runtime)
        if catalyst is not None:
            write_json(output_dir / "catalyst-brief.json", catalyst)
        if args.write_txt:
            stock_tickers = ticker_universe["tickers"]
            etf_tickers = [
                row["ticker"]
                for direction in ("up", "down")
                for row in calculated["etf"][direction]
            ]
            all_codes = stock_tickers + [
                ticker for ticker in etf_tickers if ticker not in set(stock_tickers)
            ]
            write_lines(project_root / f"finviz_{args.date}_stocks.txt", stock_tickers)
            write_lines(project_root / f"finviz_{args.date}_all_codes.txt", all_codes)

    result = {
        "date": args.date,
        "runtime_status": runtime["overall_status"],
        "scope_count": len(runtime["statistics"]),
        "selected_group_count": sum(
            len(scope["selected_up"]) + len(scope["selected_down"])
            for scope in runtime["statistics"].values()
        ),
        "selected_etf_count": 6,
        "ticker_count": ticker_universe["ticker_count"],
        "fixed_section_four_row_count": runtime["section_four_etf_observation"][
            "fixed_row_count"
        ],
        "catalyst_brief_built": catalyst is not None,
        "catalyst_coverage_pct": (
            catalyst["_meta"]["coverage_pct"] if catalyst is not None else None
        ),
        "validate_only": args.validate_only,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BriefError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
