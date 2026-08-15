#!/usr/bin/env python3
"""Mechanically screen every selected ticker for candidate company events.

This is a first-pass discovery tool, not a factual catalyst adjudicator. It
reduces repeated LLM searches while preserving a 100% ticker coverage gate.
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_module
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from zoneinfo import ZoneInfo


ET = ZoneInfo("America/New_York")
SCHEMA_VERSION = 1
NEWS_TABLE_RE = re.compile(
    r"<table\b[^>]*\bid=[\"']news-table[\"'][^>]*>(.*?)</table>",
    re.IGNORECASE | re.DOTALL,
)
ROW_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
CELL_RE = re.compile(r"<td\b[^>]*>(.*?)</td>", re.IGNORECASE | re.DOTALL)
ANCHOR_RE = re.compile(
    r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)

CATEGORY_PATTERNS = {
    "earnings_guidance": re.compile(
        r"\b(earnings|quarter(?:ly)?|results|revenue|profit|loss|guidance|outlook|forecast|eps)\b",
        re.IGNORECASE,
    ),
    "merger_acquisition": re.compile(
        r"\b(acquir(?:e|es|ed|ing|er)|acquisition|merger|buyout|takeover|strategic alternatives?)\b",
        re.IGNORECASE,
    ),
    "financing_capital_structure": re.compile(
        r"\b(offering|financing|capital raise|convertible|notes?|debt|loan|credit facility|bankruptcy|restructur(?:e|ing))\b",
        re.IGNORECASE,
    ),
    "regulatory_legal": re.compile(
        r"\b(fda|sec\b|regulat(?:or|ory|ion)|approval|clearance|investigation|lawsuit|settlement|antitrust|court)\b",
        re.IGNORECASE,
    ),
    "contract_partnership": re.compile(
        r"\b(contract|award|order|agreement|partnership|collaboration|customer|supplier)\b",
        re.IGNORECASE,
    ),
    "management_governance": re.compile(
        r"\b(appoints?|resigns?|steps down|chief executive|chief financial|\bceo\b|\bcfo\b|board)\b",
        re.IGNORECASE,
    ),
    "capital_return": re.compile(
        r"\b(dividend|buyback|repurchase|split)\b", re.IGNORECASE
    ),
    "analyst_action": re.compile(
        r"\b(upgrade|downgrade|price target|initiates?|rating)\b", re.IGNORECASE
    ),
}


class ScreenError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScreenError(f"required input is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ScreenError(f"invalid JSON: {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def clean_text(raw: str) -> str:
    return " ".join(html_module.unescape(TAG_RE.sub(" ", raw)).split())


def previous_weekday(day: datetime) -> datetime:
    candidate = day - timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate -= timedelta(days=1)
    return candidate


def fetch_quote_html(ticker: str, timeout_seconds: int) -> str:
    curl = shutil.which("curl.exe") or shutil.which("curl")
    if not curl:
        raise ScreenError("curl is required for the stable batch news screen")
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    command = [
        curl,
        "--silent",
        "--show-error",
        "--fail",
        "--location",
        "--http1.1",
        "--connect-timeout",
        "15",
        "--max-time",
        str(timeout_seconds),
        "--retry",
        "2",
        "--retry-delay",
        "1",
        "--user-agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
        url,
    ]
    process = subprocess.run(command, capture_output=True, check=False)
    if process.returncode != 0:
        message = process.stderr.decode("utf-8", "replace").strip()
        raise ScreenError(f"Finviz quote fetch failed for {ticker}: {message}")
    body = process.stdout.decode("utf-8", "replace")
    if "id=\"news-table\"" not in body and "id='news-table'" not in body:
        raise ScreenError(f"Finviz news table missing for {ticker}")
    return body


def parse_row_datetime(
    text: str, inherited_date: datetime | None, target_date: datetime
) -> tuple[datetime | None, datetime | None]:
    normalized = " ".join(text.split())
    patterns = (
        (r"^(\w{3}-\d{2}-\d{2})\s+(\d{1,2}:\d{2}[AP]M)$", "%b-%d-%y %I:%M%p"),
        (r"^Today\s+(\d{1,2}:\d{2}[AP]M)$", None),
        (r"^(\d{1,2}:\d{2}[AP]M)$", None),
    )
    match = re.match(patterns[0][0], normalized, re.IGNORECASE)
    if match:
        value = datetime.strptime(f"{match.group(1)} {match.group(2)}", patterns[0][1]).replace(
            tzinfo=ET
        )
        return value, value
    match = re.match(patterns[1][0], normalized, re.IGNORECASE)
    if match:
        value = datetime.combine(
            target_date.date(), datetime.strptime(match.group(1), "%I:%M%p").time(), ET
        )
        return value, value
    match = re.match(patterns[2][0], normalized, re.IGNORECASE)
    if match and inherited_date is not None:
        value = datetime.combine(
            inherited_date.date(), datetime.strptime(match.group(1), "%I:%M%p").time(), ET
        )
        return value, inherited_date
    return None, inherited_date


def parse_news(
    body: str,
    target_date: datetime,
    window_start: datetime,
    window_end: datetime,
) -> list[dict[str, Any]]:
    table = NEWS_TABLE_RE.search(body)
    if not table:
        raise ScreenError("news table could not be parsed")
    results = []
    inherited_date = None
    for row_html in ROW_RE.findall(table.group(1)):
        cells = CELL_RE.findall(row_html)
        if len(cells) < 2:
            continue
        published, inherited_date = parse_row_datetime(
            clean_text(cells[0]), inherited_date, target_date
        )
        anchor = ANCHOR_RE.search(cells[1])
        if published is None or anchor is None:
            continue
        if not (window_start < published <= window_end):
            continue
        url = urljoin("https://finviz.com/", html_module.unescape(anchor.group(1)))
        title = clean_text(anchor.group(2))
        categories = [
            category for category, pattern in CATEGORY_PATTERNS.items() if pattern.search(title)
        ]
        results.append(
            {
                "published_at_et": published.isoformat(),
                "title": title,
                "url": url,
                "candidate_categories": categories,
                "is_candidate_event": bool(categories),
            }
        )
    return results


def primary_perf(item: dict[str, Any]) -> float | None:
    values = [
        float(row["perf"])
        for row in item.get("occurrences", [])
        if isinstance(row.get("perf"), (int, float))
    ]
    if not values:
        return None
    return max(values, key=abs)


def aligned_with_selected_groups(item: dict[str, Any], perf: float | None) -> bool | None:
    if perf is None or perf == 0:
        return None
    expected = "up" if perf > 0 else "down"
    directions = {row.get("direction") for row in item.get("occurrences", [])}
    return directions == {expected}


def screen_one(
    item: dict[str, Any], target_date: datetime, window_start: datetime, window_end: datetime, timeout: int
) -> dict[str, Any]:
    ticker = item["ticker"]
    body = fetch_quote_html(ticker, timeout)
    news = parse_news(body, target_date, window_start, window_end)
    candidates = [row for row in news if row["is_candidate_event"]]
    perf = primary_perf(item)
    abnormal = perf is not None and abs(perf) >= 8.0
    aligned = aligned_with_selected_groups(item, perf)
    detached = aligned is False
    return {
        "ticker": ticker,
        "company": item.get("company"),
        "occurrences": item.get("occurrences", []),
        "perf": perf,
        "source_status": "OK",
        "news_in_window_count": len(news),
        "candidate_event_count": len(candidates),
        "candidate_events": candidates,
        "abnormal_move": abnormal,
        "aligned_with_selected_groups": aligned,
        "detached_from_selected_groups": detached,
        "requires_model_verification": bool(candidates or abnormal or detached),
        "screen_conclusion": (
            "CANDIDATE_OR_EXCEPTION_REQUIRES_VERIFICATION"
            if candidates or abnormal or detached
            else "NO_CANDIDATE_EVENT_AND_GROUP_ALIGNED"
        ),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="Target trading date YYYY-MM-DD")
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--previous-trading-date", help="Override prior trading date YYYY-MM-DD")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=45)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--only", nargs="*", help="Optional ticker subset for a development smoke test"
    )
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        target = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=ET)
    except ValueError as exc:
        raise ScreenError("--date must use YYYY-MM-DD") from exc
    if args.previous_trading_date:
        try:
            previous = datetime.strptime(args.previous_trading_date, "%Y-%m-%d").replace(tzinfo=ET)
        except ValueError as exc:
            raise ScreenError("--previous-trading-date must use YYYY-MM-DD") from exc
    else:
        previous = previous_weekday(target)
    window_start = datetime.combine(previous.date(), time(16, 0), ET)
    window_end = datetime.combine(target.date(), time(16, 0), ET)

    project_root = args.project_root.resolve()
    research_dir = project_root / "research" / "finviz" / args.date
    universe_path = research_dir / "stock-ticker-universe.json"
    universe = read_json(universe_path)
    if universe.get("date") != args.date:
        raise ScreenError("stock ticker universe date mismatch")
    items = list(universe.get("items", []))
    if args.only:
        requested = set(args.only)
        items = [item for item in items if item.get("ticker") in requested]
        absent = sorted(requested - {item.get("ticker") for item in items})
        if absent:
            raise ScreenError(f"requested smoke-test tickers absent from universe: {absent}")
    if not items:
        raise ScreenError("ticker universe is empty")

    records: dict[str, Any] = {}
    failures: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as executor:
        future_map = {
            executor.submit(
                screen_one, item, target, window_start, window_end, args.timeout_seconds
            ): item["ticker"]
            for item in items
        }
        for future in as_completed(future_map):
            ticker = future_map[future]
            try:
                records[ticker] = future.result()
            except Exception as exc:  # every source failure must remain explicit
                failures[ticker] = str(exc)

    expected_tickers = sorted(item["ticker"] for item in items)
    covered_tickers = sorted(records)
    status = "PASS" if not failures and covered_tickers == expected_tickers else "FAIL"
    payload = {
        "_meta": {
            "schema_version": SCHEMA_VERSION,
            "date": args.date,
            "previous_trading_date": previous.date().isoformat(),
            "research_window_et": f"{window_start.isoformat()} / {window_end.isoformat()}",
            "source": "Finviz quote news tables; mechanical candidate screen only",
            "source_ticker_universe": str(universe_path.relative_to(project_root)).replace("\\", "/"),
            "source_ticker_universe_sha256": sha256_file(universe_path),
            "expected_ticker_count": len(expected_tickers),
            "covered_ticker_count": len(covered_tickers),
            "coverage_pct": round(100 * len(covered_tickers) / len(expected_tickers), 6),
            "status": status,
            "failed_tickers": failures,
            "candidate_ticker_count": sum(
                row["candidate_event_count"] > 0 for row in records.values()
            ),
            "model_verification_ticker_count": sum(
                row["requires_model_verification"] for row in records.values()
            ),
            "generated_at": datetime.now(ET).isoformat(),
        },
        "records": {ticker: records[ticker] for ticker in sorted(records)},
    }
    if not args.validate_only:
        output = args.output or (research_dir / "catalyst-screen.json")
        write_json(output.resolve(), payload)
    print(json.dumps(payload["_meta"], ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScreenError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
