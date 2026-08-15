#!/usr/bin/env python3
"""Merge the mechanical ticker screen with bounded model adjudications.

The screen covers every selected ticker once.  Only records marked for model
verification need an adjudication.  The resulting catalyst-cache.json remains
the complete research record; build_runtime_briefs.py creates the compact LLM
read layer after this gate passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
DIRECT = "DIRECT_SAME_DAY_CATALYST"
NO_DIRECT = "NO_SAME_DAY_DIRECT_CATALYST"


class CacheError(RuntimeError):
    """Raised when the complete cache cannot be built safely."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CacheError(f"required input is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CacheError(f"invalid JSON: {path}: {exc}") from exc


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


def linkage_text(record: dict[str, Any]) -> str:
    occurrences = record.get("occurrences", [])
    labels: list[str] = []
    directions: list[str] = []
    for item in occurrences:
        group = str(item.get("group", "")).strip()
        if group and group not in labels:
            labels.append(group)
        direction = item.get("direction")
        if direction in {"up", "down"} and direction not in directions:
            directions.append(direction)
    side = {"up": "偏强", "down": "偏弱"}
    direction_text = "/".join(side[value] for value in directions) or "入选"
    group_text = ", ".join(labels) or "selected market group"
    return f"该股与当日所选 {group_text} 的{direction_text}方向一致。"


def source_from_candidate(
    record: dict[str, Any], title_fragment: str
) -> dict[str, Any]:
    matches = [
        item
        for item in record.get("candidate_events", [])
        if title_fragment.casefold() in str(item.get("title", "")).casefold()
    ]
    if len(matches) != 1:
        raise CacheError(
            f"{record['ticker']}: candidate source fragment {title_fragment!r} "
            f"matched {len(matches)} events"
        )
    match = matches[0]
    return {
        "title": match["title"],
        "url": match["url"],
        "publisher": "Finviz-linked source",
        "published_at": match["published_at_et"],
        "time_semantics": "publication_time_et",
    }


def build_sources(
    ticker: str, record: dict[str, Any], adjudication: dict[str, Any], cutoff: str
) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for fragment in adjudication.get("candidate_title_contains", []):
        sources.append(source_from_candidate(record, str(fragment)))
    for item in adjudication.get("custom_sources", []):
        required = {"title", "url", "publisher", "published_at"}
        missing = required - set(item)
        if missing:
            raise CacheError(f"{ticker}: custom source missing {sorted(missing)}")
        sources.append(
            {
                **item,
                "time_semantics": item.get(
                    "time_semantics", "publication_time_et"
                ),
            }
        )
    if not sources:
        sources.append(
            {
                "title": f"Finviz {ticker} quote-news feed checked through the regular-session close",
                "url": f"https://finviz.com/quote.ashx?t={ticker}&p=d",
                "publisher": "Finviz news aggregation",
                "published_at": cutoff,
                "time_semantics": "research_cutoff_not_article_publication_time",
            }
        )
    return sources


def build_record(
    ticker: str,
    screened: dict[str, Any],
    adjudication: dict[str, Any] | None,
    cutoff: str,
    timeline_note: str,
    completed_at: str,
) -> dict[str, Any]:
    requires_review = bool(screened.get("requires_model_verification"))
    if requires_review and adjudication is None:
        raise CacheError(f"{ticker}: required model adjudication is missing")
    if not requires_review and adjudication is not None:
        raise CacheError(f"{ticker}: unnecessary adjudication would duplicate research")

    if adjudication is None:
        adjudication = {"status": "none", "research_level": "normal"}

    status_value = adjudication.get("status")
    if status_value not in {"direct", "none"}:
        raise CacheError(f"{ticker}: status must be direct or none")
    status = DIRECT if status_value == "direct" else NO_DIRECT
    direct_event = adjudication.get("direct_event")
    event_time = adjudication.get("event_time_et")
    if status == DIRECT and (not direct_event or not event_time):
        raise CacheError(f"{ticker}: direct event and event time are required")
    if status == NO_DIRECT and (direct_event is not None or event_time is not None):
        raise CacheError(f"{ticker}: no-direct record cannot contain a direct event")

    level = adjudication.get("research_level", "deep" if requires_review else "normal")
    if level not in {"normal", "deep"}:
        raise CacheError(f"{ticker}: invalid research level {level!r}")
    linkage = adjudication.get("confirmed_linkage") or linkage_text(screened)
    sources = build_sources(ticker, screened, adjudication, cutoff)
    conclusion = (
        str(direct_event)
        if status == DIRECT
        else f"暂未找到同日直接催化；{linkage}"
    )
    return {
        "company": screened.get("company"),
        "occurrences": screened.get("occurrences", []),
        "performance_pct": screened.get("perf"),
        "research_level": level,
        "deep_research_reason": adjudication.get("deep_research_reason"),
        "status": status,
        "mechanical_screen": {
            "news_in_window_count": screened.get("news_in_window_count"),
            "candidate_event_count": screened.get("candidate_event_count"),
            "abnormal_move": screened.get("abnormal_move"),
            "aligned_with_selected_groups": screened.get(
                "aligned_with_selected_groups"
            ),
            "result": screened.get("screen_conclusion"),
        },
        "model_adjudication": {
            "performed": requires_review,
            "result": "direct_event_confirmed" if status == DIRECT else "no_qualifying_event_found",
        },
        "direct_event": direct_event,
        "event_time_et": event_time,
        "event_within_price_window": True if status == DIRECT else None,
        "sources": sources,
        "confirmed_linkage": linkage,
        "output_conclusion": conclusion,
        "evidence_conflict": False,
        "timeline_note": timeline_note,
        "stop_reason": (
            "DIRECT_EVENT_FOUND_STOP"
            if status == DIRECT
            else (
                "DEEP_RESEARCH_COMPLETED_NO_DIRECT_EVENT"
                if level == "deep"
                else "BATCH_SCREEN_NO_CANDIDATE_AND_GROUP_ALIGNED"
            )
        ),
        "completed_at": completed_at,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="Trading date in YYYY-MM-DD")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    research = root / "research" / "finviz" / args.date
    screen_path = research / "catalyst-screen.json"
    adjudication_path = research / "catalyst-adjudications.json"
    universe_path = research / "stock-ticker-universe.json"
    screen = read_json(screen_path)
    adjudications = read_json(adjudication_path)
    universe = read_json(universe_path)

    screen_meta = screen.get("_meta", {})
    if screen_meta.get("date") != args.date or screen_meta.get("status") != "PASS":
        raise CacheError("mechanical screen date/status gate failed")
    if adjudications.get("_meta", {}).get("date") != args.date:
        raise CacheError("adjudication date mismatch")
    records = screen.get("records", {})
    expected = sorted(
        item["ticker"] if isinstance(item, dict) else str(item)
        for item in universe.get("tickers", [])
    )
    if sorted(records) != expected:
        raise CacheError("mechanical screen does not cover the complete ticker universe")

    review_expected = sorted(
        ticker
        for ticker, record in records.items()
        if record.get("requires_model_verification")
    )
    adjudicated = sorted(key for key in adjudications if key != "_meta")
    if review_expected != adjudicated:
        missing = sorted(set(review_expected) - set(adjudicated))
        extra = sorted(set(adjudicated) - set(review_expected))
        raise CacheError(f"adjudication coverage mismatch; missing={missing}, extra={extra}")

    cutoff = f"{args.date}T16:00:00-04:00"
    previous_date = screen_meta.get("previous_trading_date")
    timeline_note = (
        f"The scan covered {previous_date} after close through {args.date} 16:00 ET; "
        f"later {args.date} items were excluded from causal attribution."
    )
    completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    output: dict[str, Any] = {
        "_meta": {
            "schema_version": SCHEMA_VERSION,
            "period": "DAILY",
            "date": args.date,
            "trading_date": args.date,
            "research_window_et": screen_meta.get("research_window_et"),
            "normal_session_cutoff_et": cutoff,
            "source_screen": str(screen_path.relative_to(root)).replace("\\", "/"),
            "source_screen_sha256": sha256_file(screen_path),
            "source_adjudications": str(adjudication_path.relative_to(root)).replace("\\", "/"),
            "source_adjudications_sha256": sha256_file(adjudication_path),
            "selected_ticker_set": str(universe_path.relative_to(root)).replace("\\", "/"),
            "selected_ticker_source_sha256": sha256_file(universe_path),
            "unique_count": len(expected),
            "unique_ticker_count": len(expected),
            "batch_screen_coverage_pct": 100.0,
            "model_verification_ticker_count": len(review_expected),
            "ordinary_research_order": [
                "batch_mechanical_company_event_screen",
                "model_verification_only_for_candidates_or_exceptions",
            ],
            "completed_at": completed_at,
            "generated_at": completed_at,
        }
    }
    for ticker in expected:
        output[ticker] = build_record(
            ticker,
            records[ticker],
            adjudications.get(ticker),
            cutoff,
            timeline_note,
            completed_at,
        )

    if len(output) - 1 != len(expected):
        raise CacheError("final cache coverage gate failed")
    if not args.validate_only:
        write_json(research / "catalyst-cache.json", output)
    direct_count = sum(
        item.get("status") == DIRECT for key, item in output.items() if key != "_meta"
    )
    print(
        f"catalyst cache PASS: {len(expected)}/{len(expected)} tickers; "
        f"direct={direct_count}; no_direct={len(expected) - direct_count}; "
        f"model_verified={len(review_expected)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CacheError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
