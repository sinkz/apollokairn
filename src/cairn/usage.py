from __future__ import annotations

import html
import json
from collections import Counter
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Mapping

from cairn.config import load_config
from cairn.ranking import query_tokens
from cairn.secret_scan import redact_text


USAGE_DIR = Path(".cairn") / "usage"
REPORT_DIR = Path(".cairn") / "reports"
EVENTS_FILE = USAGE_DIR / "events.jsonl"
SUMMARY_FILE = REPORT_DIR / "usage-summary.json"
HTML_REPORT_FILE = REPORT_DIR / "usage.html"
EVIDENCE_FILE = REPORT_DIR / "usage-evidence.json"
_PRIVATE_GITIGNORE_LINES = (".cairn/index.db", ".cairn/usage/", ".cairn/reports/")
_OMITTED_KEYS = {"body", "content", "snippet", "append", "append_text"}


@dataclass(frozen=True)
class UsageStatus:
    enabled: bool
    events_path: str
    report_path: str
    event_count: int


@dataclass(frozen=True)
class UsageSummary:
    enabled: bool
    event_count: int
    first_event: str | None
    last_event: str | None
    commands: dict[str, int]
    searches: int
    retrieves: int
    writes: int
    errors: int
    average_duration_ms: float
    total_estimated_tokens: int
    top_query_terms: list[dict[str, object]]
    top_documents: list[dict[str, object]]
    report_path: str | None = None


@dataclass(frozen=True)
class UsageEvidence:
    enabled: bool
    event_count: int
    generated_at: str
    observation_counts: dict[str, int]
    rates: dict[str, float]
    query_examples: list[str]
    top_query_terms: list[dict[str, object]]
    top_documents: list[dict[str, object]]
    decision_notes: dict[str, dict[str, object]]
    privacy: dict[str, object]
    report_path: str | None = None


def usage_enabled(root: Path) -> bool:
    return load_config(Path(root)).usage_tracking


def usage_status(root: Path) -> UsageStatus:
    root = Path(root)
    return UsageStatus(
        enabled=usage_enabled(root),
        events_path=EVENTS_FILE.as_posix(),
        report_path=HTML_REPORT_FILE.as_posix(),
        event_count=len(load_events(root)),
    )


def set_usage_enabled(root: Path, enabled: bool) -> UsageStatus:
    root = Path(root)
    cairn_dir = root / ".cairn"
    cairn_dir.mkdir(parents=True, exist_ok=True)
    path = cairn_dir / "config.json"
    data: dict[str, Any] = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data = loaded
        except (OSError, json.JSONDecodeError):
            data = {}
    data["usage_tracking"] = enabled
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _ensure_private_gitignore(root)
    return usage_status(root)


def record_usage_event(
    root: Path,
    command: str,
    started_at: float,
    data: Mapping[str, Any] | None = None,
    status: str = "ok",
    error: str | None = None,
) -> dict[str, Any] | None:
    root = Path(root)
    if not usage_enabled(root):
        return None
    sanitized = _sanitize(data or {})
    if isinstance(sanitized, dict) and isinstance(sanitized.get("query"), str):
        sanitized["query_terms"] = list(query_tokens(str(sanitized["query"])))
    event: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "status": status,
        "duration_ms": round((perf_counter() - started_at) * 1000, 3),
        "data": sanitized,
    }
    if error:
        event["error"] = redact_text(error)
    path = root / EVENTS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return event


def load_events(root: Path) -> list[dict[str, Any]]:
    path = Path(root) / EVENTS_FILE
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def summarize_usage(root: Path) -> UsageSummary:
    events = load_events(root)
    command_counts: Counter[str] = Counter()
    term_counts: Counter[str] = Counter()
    document_counts: Counter[str] = Counter()
    duration_total = 0.0
    token_total = 0
    errors = 0
    for event in events:
        command = str(event.get("command", "unknown"))
        command_counts[command] += 1
        if event.get("status") != "ok":
            errors += 1
        duration = event.get("duration_ms")
        if isinstance(duration, (int, float)):
            duration_total += float(duration)
        data = event.get("data")
        if not isinstance(data, dict):
            continue
        for term in data.get("query_terms", []):
            if isinstance(term, str) and term:
                term_counts[term.casefold()] += 1
        for document in _documents_from_data(data):
            document_counts[document] += 1
        token_total += _token_value(data)
    first_event = str(events[0].get("timestamp")) if events else None
    last_event = str(events[-1].get("timestamp")) if events else None
    return UsageSummary(
        enabled=usage_enabled(Path(root)),
        event_count=len(events),
        first_event=first_event,
        last_event=last_event,
        commands=dict(sorted(command_counts.items())),
        searches=command_counts.get("search", 0),
        retrieves=command_counts.get("retrieve", 0),
        writes=sum(command_counts.get(command, 0) for command in ("add", "capture", "update")),
        errors=errors,
        average_duration_ms=round(duration_total / len(events), 3) if events else 0.0,
        total_estimated_tokens=token_total,
        top_query_terms=_top(term_counts),
        top_documents=_top(document_counts),
    )


def render_usage_summary(summary: UsageSummary) -> str:
    lines = [
        f"enabled: {str(summary.enabled).lower()}",
        f"events: {summary.event_count}",
        f"searches: {summary.searches}",
        f"retrieves: {summary.retrieves}",
        f"writes: {summary.writes}",
        f"errors: {summary.errors}",
        f"average_duration_ms: {summary.average_duration_ms}",
        f"total_estimated_tokens: {summary.total_estimated_tokens}",
        "top_query_terms:",
    ]
    lines.extend(f"  {item['value']}: {item['count']}" for item in summary.top_query_terms)
    lines.append("top_documents:")
    lines.extend(f"  {item['value']}: {item['count']}" for item in summary.top_documents)
    if summary.report_path:
        lines.append(f"report: {summary.report_path}")
    return "\n".join(lines) + "\n"


def write_usage_report(root: Path, output: str | None = None) -> UsageSummary:
    root = Path(root)
    summary = summarize_usage(root)
    report_path = _report_output_path(root, output)
    summary_path = root / SUMMARY_FILE
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(_summary_payload(summary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_usage_html(summary), encoding="utf-8")
    return replace(summary, report_path=_display_path(root, report_path))


def write_usage_evidence(root: Path, output: str | None = None) -> UsageEvidence:
    root = Path(root)
    evidence = summarize_usage_evidence(root)
    report_path = _evidence_output_path(root, output)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    evidence = replace(evidence, report_path=_display_path(root, report_path))
    report_path.write_text(json.dumps(_evidence_payload(evidence), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return evidence


def summarize_usage_evidence(root: Path) -> UsageEvidence:
    root = Path(root)
    events = load_events(root)
    summary = summarize_usage(root)
    searches = _count_events(events, "search")
    retrieves = _count_events(events, "retrieve")
    writes = sum(_count_events(events, command) for command in ("add", "capture", "update"))
    zero_result_searches = _count_matching(events, "search", "result_count", 0)
    zero_source_retrieves = _count_matching(events, "retrieve", "source_count", 0)
    passage_retrieves = _count_matching(events, "retrieve", "mode", "passages")
    auto_ranker_retrieves = _count_matching(events, "retrieve", "requested_ranker", "auto")
    rrf_searches = _count_matching(events, "search", "ranker", "rrf")
    errors = sum(1 for event in events if event.get("status") != "ok")
    observation_counts = {
        "events": len(events),
        "searches": searches,
        "retrieves": retrieves,
        "writes": writes,
        "errors": errors,
        "zero_result_searches": zero_result_searches,
        "zero_source_retrieves": zero_source_retrieves,
        "passage_retrieves": passage_retrieves,
        "auto_ranker_retrieves": auto_ranker_retrieves,
        "rrf_searches": rrf_searches,
    }
    rates = {
        "zero_result_search_rate": _rate(zero_result_searches, searches),
        "zero_source_retrieve_rate": _rate(zero_source_retrieves, retrieves),
        "retrieve_per_search_rate": _rate(retrieves, searches),
        "passage_retrieve_rate": _rate(passage_retrieves, retrieves),
        "error_rate": _rate(errors, len(events)),
    }
    return UsageEvidence(
        enabled=usage_enabled(root),
        event_count=len(events),
        generated_at=datetime.now(timezone.utc).isoformat(),
        observation_counts=observation_counts,
        rates=rates,
        query_examples=_query_examples(events),
        top_query_terms=summary.top_query_terms,
        top_documents=summary.top_documents,
        decision_notes=_decision_notes(observation_counts, rates),
        privacy={
            "stores_note_bodies": False,
            "stores_snippets": False,
            "stores_raw_context": False,
            "source": EVENTS_FILE.as_posix(),
            "artifact_scope": "aggregates plus redacted query examples",
        },
    )


def render_usage_evidence(evidence: UsageEvidence) -> str:
    lines = [
        f"events: {evidence.event_count}",
        f"searches: {evidence.observation_counts['searches']}",
        f"retrieves: {evidence.observation_counts['retrieves']}",
        f"writes: {evidence.observation_counts['writes']}",
        f"zero_result_search_rate: {evidence.rates['zero_result_search_rate']}",
        f"zero_source_retrieve_rate: {evidence.rates['zero_source_retrieve_rate']}",
        f"retrieve_per_search_rate: {evidence.rates['retrieve_per_search_rate']}",
        "decision_notes:",
    ]
    for key, note in evidence.decision_notes.items():
        lines.append(f"  {key}: {note['status']} - {note['rationale']}")
    if evidence.report_path:
        lines.append(f"report: {evidence.report_path}")
    return "\n".join(lines) + "\n"


def render_usage_html(summary: UsageSummary) -> str:
    commands = _bar_list(summary.commands)
    terms = _bar_list({str(item["value"]): int(item["count"]) for item in summary.top_query_terms})
    documents = _bar_list({str(item["value"]): int(item["count"]) for item in summary.top_documents})
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ApolloKairn Usage Report</title>
  <style>
    :root {{ color-scheme: light; --ink:#1f2933; --muted:#687385; --line:#d9dee7; --fill:#2f6f4e; --soft:#f7f3ea; }}
    body {{ margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:#fbfaf7; }}
    main {{ max-width:1040px; margin:0 auto; padding:40px 20px 56px; }}
    h1 {{ margin:0 0 8px; font-size:clamp(2rem, 4vw, 3.4rem); letter-spacing:0; }}
    h2 {{ margin:0 0 16px; font-size:1rem; text-transform:uppercase; color:var(--muted); letter-spacing:.08em; }}
    .lead {{ margin:0 0 28px; color:var(--muted); max-width:760px; line-height:1.55; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:12px; margin:24px 0; }}
    .metric, section {{ border:1px solid var(--line); background:white; border-radius:8px; }}
    .metric {{ padding:16px; }}
    .metric strong {{ display:block; font-size:1.8rem; }}
    .metric span {{ color:var(--muted); font-size:.9rem; }}
    section {{ padding:20px; margin-top:16px; }}
    .row {{ display:grid; grid-template-columns:minmax(120px, 1fr) 70px 2fr; gap:12px; align-items:center; margin:10px 0; }}
    .label {{ overflow-wrap:anywhere; }}
    .bar {{ height:10px; background:var(--soft); border-radius:999px; overflow:hidden; }}
    .bar i {{ display:block; height:100%; background:var(--fill); }}
    .empty {{ color:var(--muted); }}
    footer {{ color:var(--muted); margin-top:24px; font-size:.9rem; }}
  </style>
</head>
<body>
<main>
  <h1>ApolloKairn Usage Report</h1>
  <p class="lead">Local opt-in metrics from this vault. Query text is redacted for common secret-like values, and note bodies/snippets are not stored in usage events.</p>
  <div class="grid">
    <div class="metric"><strong>{summary.event_count}</strong><span>events</span></div>
    <div class="metric"><strong>{summary.searches}</strong><span>searches</span></div>
    <div class="metric"><strong>{summary.retrieves}</strong><span>retrievals</span></div>
    <div class="metric"><strong>{summary.writes}</strong><span>writes</span></div>
    <div class="metric"><strong>{summary.total_estimated_tokens}</strong><span>estimated tokens</span></div>
    <div class="metric"><strong>{summary.average_duration_ms}</strong><span>avg ms</span></div>
  </div>
  <section><h2>Commands</h2>{commands}</section>
  <section><h2>Query Terms</h2>{terms}</section>
  <section><h2>Documents</h2>{documents}</section>
  <footer>First event: {html.escape(summary.first_event or "n/a")} · Last event: {html.escape(summary.last_event or "n/a")}</footer>
</main>
</body>
</html>
"""


def _sanitize(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Mapping):
        return {
            str(key): _sanitize(item)
            for key, item in value.items()
            if str(key).casefold() not in _OMITTED_KEYS
        }
    if isinstance(value, (list, tuple)):
        return [_sanitize(item) for item in value]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return redact_text(str(value))


def _ensure_private_gitignore(root: Path) -> None:
    path = Path(root) / ".gitignore"
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    normalized = {line.strip() for line in existing}
    changed = False
    for line in _PRIVATE_GITIGNORE_LINES:
        if line not in normalized:
            existing.append(line)
            changed = True
    if changed:
        path.write_text("\n".join(existing).rstrip() + "\n", encoding="utf-8")


def _documents_from_data(data: Mapping[str, Any]) -> list[str]:
    out: list[str] = []
    for key in ("result_paths", "source_paths"):
        value = data.get(key)
        if isinstance(value, list):
            out.extend(str(item) for item in value if isinstance(item, str) and item)
    for key in ("path", "document"):
        value = data.get(key)
        if isinstance(value, str) and value:
            out.append(value)
    return out


def _token_value(data: Mapping[str, Any]) -> int:
    for key in ("used_tokens", "tokens", "estimated_tokens"):
        value = data.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
    return 0


def _top(counter: Counter[str], limit: int = 10) -> list[dict[str, object]]:
    return [{"value": value, "count": count} for value, count in counter.most_common(limit)]


def _summary_payload(summary: UsageSummary) -> dict[str, Any]:
    return {
        "enabled": summary.enabled,
        "event_count": summary.event_count,
        "first_event": summary.first_event,
        "last_event": summary.last_event,
        "commands": summary.commands,
        "searches": summary.searches,
        "retrieves": summary.retrieves,
        "writes": summary.writes,
        "errors": summary.errors,
        "average_duration_ms": summary.average_duration_ms,
        "total_estimated_tokens": summary.total_estimated_tokens,
        "top_query_terms": summary.top_query_terms,
        "top_documents": summary.top_documents,
        "report_path": summary.report_path,
    }


def _evidence_payload(evidence: UsageEvidence) -> dict[str, Any]:
    return {
        "enabled": evidence.enabled,
        "event_count": evidence.event_count,
        "generated_at": evidence.generated_at,
        "observation_counts": evidence.observation_counts,
        "rates": evidence.rates,
        "query_examples": evidence.query_examples,
        "top_query_terms": evidence.top_query_terms,
        "top_documents": evidence.top_documents,
        "decision_notes": evidence.decision_notes,
        "privacy": evidence.privacy,
        "report_path": evidence.report_path,
    }


def _report_output_path(root: Path, output: str | None) -> Path:
    if output:
        path = Path(output)
        return path if path.is_absolute() else Path(root) / path
    return Path(root) / HTML_REPORT_FILE


def _evidence_output_path(root: Path, output: str | None) -> Path:
    if output:
        path = Path(output)
        return path if path.is_absolute() else Path(root) / path
    return Path(root) / EVIDENCE_FILE


def _display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _bar_list(values: Mapping[str, int]) -> str:
    if not values:
        return '<p class="empty">No data yet.</p>'
    max_value = max(values.values()) or 1
    rows = []
    for label, count in values.items():
        width = max(4, round((count / max_value) * 100))
        rows.append(
            '<div class="row">'
            f'<div class="label">{html.escape(str(label))}</div>'
            f"<strong>{count}</strong>"
            f'<div class="bar"><i style="width:{width}%"></i></div>'
            "</div>"
        )
    return "\n".join(rows)


def _count_events(events: list[dict[str, Any]], command: str) -> int:
    return sum(1 for event in events if event.get("command") == command)


def _count_matching(events: list[dict[str, Any]], command: str, key: str, expected: object) -> int:
    count = 0
    for event in events:
        if event.get("command") != command:
            continue
        data = event.get("data")
        if isinstance(data, Mapping) and data.get(key) == expected:
            count += 1
    return count


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _query_examples(events: list[dict[str, Any]], limit: int = 10) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for event in events:
        data = event.get("data")
        if not isinstance(data, Mapping):
            continue
        query = data.get("query")
        if not isinstance(query, str) or not query:
            continue
        if query in seen:
            continue
        seen.add(query)
        out.append(query)
        if len(out) >= limit:
            break
    return out


def _decision_notes(observation_counts: Mapping[str, int], rates: Mapping[str, float]) -> dict[str, dict[str, object]]:
    events = observation_counts["events"]
    searches = observation_counts["searches"]
    retrieves = observation_counts["retrieves"]
    enough_usage = events >= 30 and searches >= 10 and retrieves >= 5
    ranker_status = "ready_for_review" if enough_usage else "needs_more_usage"
    ranker_rationale = (
        "enough local search/retrieve usage exists to review ranking or embedding changes"
        if enough_usage
        else "collect at least 30 events, 10 searches, and 5 retrieves before tuning ranking or embeddings"
    )
    no_answer_status = "watch" if rates["zero_result_search_rate"] >= 0.2 or rates["zero_source_retrieve_rate"] >= 0.2 else "ok"
    no_answer_rationale = (
        "no-answer or zero-source cases are frequent enough to prioritize abstention/no-signal slices"
        if no_answer_status == "watch"
        else "no-answer rates are not elevated in the current local sample"
    )
    return {
        "ranker_or_embedding_decision": {
            "status": ranker_status,
            "rationale": ranker_rationale,
            "minimum_events": 30,
            "minimum_searches": 10,
            "minimum_retrieves": 5,
        },
        "no_answer_and_abstention": {
            "status": no_answer_status,
            "rationale": no_answer_rationale,
        },
    }
