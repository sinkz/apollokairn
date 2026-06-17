from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from cairn.indexer import SearchResult, search, show


_TOKEN = re.compile(r"\w+", re.UNICODE)


@dataclass(frozen=True)
class SimilarResult:
    path: str
    title: str
    type: str
    tags: list[str]
    score: float
    snippet: str
    similarity: float


def _tokens(text: str) -> set[str]:
    return {token.casefold() for token in _TOKEN.findall(text)}


def lexical_similarity(query: str, text: str) -> float:
    query_tokens = _tokens(query)
    text_tokens = _tokens(text)
    if not query_tokens or not text_tokens:
        return 0.0
    overlap = len(query_tokens & text_tokens)
    return overlap / len(query_tokens)


def find_similar(
    root: Path,
    query: str,
    limit: int = 5,
    type_filter: str | None = None,
    tag_filters: Sequence[str] = (),
    system_filters: Sequence[str] = (),
) -> list[SimilarResult]:
    results = search(
        root,
        query,
        limit=limit,
        type_filter=type_filter,
        tag_filters=tag_filters,
        system_filters=system_filters,
    )
    out: list[SimilarResult] = []
    for result in results:
        try:
            text = show(root, result.path)
        except (FileNotFoundError, ValueError):
            text = result.title + "\n" + result.snippet
        out.append(
            SimilarResult(
                path=result.path,
                title=result.title,
                type=result.type,
                tags=result.tags,
                score=result.score,
                snippet=result.snippet,
                similarity=round(lexical_similarity(query, text), 4),
            )
        )
    return out


def render_similar(results: Sequence[SimilarResult]) -> str:
    lines: list[str] = []
    for result in results:
        lines.append(
            f"possible duplicate: {result.path} :: {result.title} "
            f"(similarity={result.similarity:.4f})"
        )
        lines.append(result.snippet)
    return "\n".join(lines) + ("\n" if lines else "")
