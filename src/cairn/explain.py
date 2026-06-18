from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from cairn.frontmatter import FrontmatterError, parse_document
from cairn.ranking import query_tokens
from cairn.vocabulary import expanded_query_tokens


SCORE_NOTE = "Ranking score is diagnostic metadata, not confidence."


@dataclass(frozen=True)
class MatchedTerm:
    term: str
    fields: list[str]


@dataclass(frozen=True)
class RankingExplanation:
    path: str
    ranker: str
    score: float
    score_note: str
    matched_terms: list[MatchedTerm]
    matched_fields: list[str]
    heading: str | None = None
    start_line: int | None = None
    end_line: int | None = None


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _as_text(value: object) -> str:
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return "" if value is None else str(value)


def _field_map(root: Path, rel_path: str, passage_text: str = "") -> dict[str, str]:
    path = Path(root) / rel_path
    try:
        parsed = parse_document(path.read_text(encoding="utf-8"))
    except (OSError, FrontmatterError):
        return {"passage": passage_text} if passage_text else {}
    fields = {
        "title": _as_text(parsed.frontmatter.get("title")),
        "description": _as_text(parsed.frontmatter.get("description")),
        "tags": _as_text(parsed.frontmatter.get("tags")),
        "aliases": _as_text(parsed.frontmatter.get("aliases")),
        "systems": _as_text(parsed.frontmatter.get("systems")),
        "signals": _as_text(parsed.frontmatter.get("signals")),
        "body": parsed.body,
    }
    if passage_text:
        fields["passage"] = passage_text
    return fields


def _diagnostic_terms(root: Path, query: str) -> list[str]:
    terms = list(query_tokens(query))
    expanded = expanded_query_tokens(root, query)
    if expanded:
        terms.extend(expanded)
    out: list[str] = []
    seen: set[str] = set()
    for term in terms:
        key = _normalize(term)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(term)
    return out


def _matched_terms(terms: Sequence[str], fields: dict[str, str]) -> list[MatchedTerm]:
    out: list[MatchedTerm] = []
    normalized_fields = {name: _normalize(text) for name, text in fields.items() if text}
    for term in terms:
        norm = _normalize(term)
        matches = sorted(name for name, text in normalized_fields.items() if norm and norm in text)
        if matches:
            out.append(MatchedTerm(term=term, fields=matches))
    return out


def _matched_fields(terms: Iterable[MatchedTerm]) -> list[str]:
    fields: set[str] = set()
    for term in terms:
        fields.update(term.fields)
    return sorted(fields)


def explain_result(
    root: Path,
    query: str,
    rel_path: str,
    score: float,
    ranker: str,
    passage_text: str = "",
    heading: str | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
) -> RankingExplanation:
    matches = _matched_terms(_diagnostic_terms(root, query), _field_map(root, rel_path, passage_text=passage_text))
    return RankingExplanation(
        path=rel_path,
        ranker=ranker,
        score=score,
        score_note=SCORE_NOTE,
        matched_terms=matches,
        matched_fields=_matched_fields(matches),
        heading=heading,
        start_line=start_line,
        end_line=end_line,
    )


def explain_search_results(root: Path, query: str, results: Sequence[object], ranker: str) -> list[RankingExplanation]:
    return [
        explain_result(root, query, result.path, result.score, ranker)
        for result in results
    ]


def explain_retrieval_sources(root: Path, query: str, sources: Sequence[object], ranker: str) -> list[RankingExplanation]:
    return [
        explain_result(
            root,
            query,
            source.path,
            source.score,
            ranker,
            passage_text=source.content,
            heading=source.heading,
            start_line=source.start_line,
            end_line=source.end_line,
        )
        for source in sources
    ]
