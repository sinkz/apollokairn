from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from cairn.indexer import search, search_passages, show
from cairn.secret_scan import redact_text


CHARS_PER_TOKEN = 4
_RANKERS = {"bm25", "rrf", "auto"}


@dataclass(frozen=True)
class RetrievedSource:
    path: str
    title: str
    type: str
    tags: list[str]
    score: float
    snippet: str
    content: str
    heading: str | None = None
    start_line: int | None = None
    end_line: int | None = None
    truncated: bool = False


@dataclass(frozen=True)
class RetrievalPacket:
    query: str
    mode: str
    requested_ranker: str
    ranker: str
    limit: int
    budget_tokens: int
    used_tokens: int
    source_count: int
    context: str
    sources: list[RetrievedSource]


def approx_tokens(text: str) -> int:
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def _fit(text: str, max_chars: int) -> str:
    if max_chars <= 0:
        return ""
    if len(text) <= max_chars:
        return text
    suffix = "\n[truncated]\n"
    if max_chars <= len(suffix):
        return text[:max_chars]
    return text[: max_chars - len(suffix)].rstrip() + suffix


def _ranker_attempts(ranker: str) -> tuple[str, ...]:
    return ("bm25", "rrf") if ranker == "auto" else (ranker,)


def _retrieve_passages(
    root: Path,
    query: str,
    limit: int,
    max_chars: int,
    type_filter: str | None,
    tag_filters: Sequence[str],
    system_filters: Sequence[str],
    ranker: str,
) -> tuple[str, list[RetrievedSource]]:
    parts: list[str] = []
    sources: list[RetrievedSource] = []
    used_chars = 0
    for result in search_passages(
        root,
        query,
        limit=limit,
        type_filter=type_filter,
        tag_filters=tag_filters,
        system_filters=system_filters,
        ranker=ranker,
    ):
        prefix = (
            f"path: {result.path}\n"
            f"title: {result.title}\n"
            f"type: {result.type}\n"
            f"tags: {', '.join(result.tags)}\n"
            f"heading: {result.heading}\n"
            f"lines: {result.start_line}:{result.end_line}\n"
            f"snippet: {result.snippet}\n"
            "content:\n"
        )
        separator = "\n---\n" if parts else ""
        remaining = max_chars - used_chars - len(separator) - len(prefix)
        if remaining <= 0:
            break
        content = _fit(result.text, remaining)
        redacted_content = redact_text(content)
        block = redact_text(separator + prefix + content)
        parts.append(block)
        sources.append(
            RetrievedSource(
                path=result.path,
                title=result.title,
                type=result.type,
                tags=result.tags,
                score=result.score,
                snippet=redact_text(result.snippet),
                heading=result.heading,
                start_line=result.start_line,
                end_line=result.end_line,
                content=redacted_content,
                truncated=content != result.text,
            )
        )
        used_chars += len(block)
        if used_chars >= max_chars or len(content) < remaining:
            continue
        break
    return "".join(parts), sources


def _retrieve_documents(
    root: Path,
    query: str,
    limit: int,
    max_chars: int,
    type_filter: str | None,
    tag_filters: Sequence[str],
    system_filters: Sequence[str],
    ranker: str,
) -> tuple[str, list[RetrievedSource]]:
    parts: list[str] = []
    sources: list[RetrievedSource] = []
    used_chars = 0
    for result in search(
        root,
        query,
        limit=limit,
        type_filter=type_filter,
        tag_filters=tag_filters,
        system_filters=system_filters,
        ranker=ranker,
    ):
        prefix = (
            f"path: {result.path}\n"
            f"title: {result.title}\n"
            f"type: {result.type}\n"
            f"tags: {', '.join(result.tags)}\n"
            f"snippet: {result.snippet}\n"
            "content:\n"
        )
        separator = "\n---\n" if parts else ""
        remaining = max_chars - used_chars - len(separator) - len(prefix)
        if remaining <= 0:
            break
        full_text = show(root, result.path)
        content = _fit(full_text, remaining)
        redacted_content = redact_text(content)
        block = redact_text(separator + prefix + content)
        parts.append(block)
        sources.append(
            RetrievedSource(
                path=result.path,
                title=result.title,
                type=result.type,
                tags=result.tags,
                score=result.score,
                snippet=redact_text(result.snippet),
                content=redacted_content,
                truncated=content != full_text,
            )
        )
        used_chars += len(block)
        if used_chars >= max_chars or len(content) < remaining:
            continue
        break
    return "".join(parts), sources


def retrieve_packet(
    root: Path,
    query: str,
    limit: int = 3,
    budget_tokens: int = 1000,
    mode: str = "documents",
    type_filter: str | None = None,
    tag_filters: Sequence[str] = (),
    system_filters: Sequence[str] = (),
    ranker: str = "bm25",
) -> RetrievalPacket:
    if limit <= 0:
        raise ValueError("limit must be positive")
    if budget_tokens <= 0:
        raise ValueError("budget must be positive")
    if mode not in {"documents", "passages"}:
        raise ValueError("mode must be 'documents' or 'passages'")
    if ranker not in _RANKERS:
        raise ValueError("ranker must be 'bm25', 'rrf', or 'auto'")

    max_chars = budget_tokens * CHARS_PER_TOKEN

    if mode == "passages":
        for attempt in _ranker_attempts(ranker):
            context, sources = _retrieve_passages(
                root,
                query,
                limit,
                max_chars,
                type_filter,
                tag_filters,
                system_filters,
                attempt,
            )
            if context:
                return RetrievalPacket(
                    query=query,
                    mode=mode,
                    requested_ranker=ranker,
                    ranker=attempt,
                    limit=limit,
                    budget_tokens=budget_tokens,
                    used_tokens=approx_tokens(context),
                    source_count=len(sources),
                    context=context,
                    sources=sources,
                )
        return RetrievalPacket(query, mode, ranker, _ranker_attempts(ranker)[-1], limit, budget_tokens, 0, 0, "", [])

    for attempt in _ranker_attempts(ranker):
        context, sources = _retrieve_documents(
            root,
            query,
            limit,
            max_chars,
            type_filter,
            tag_filters,
            system_filters,
            attempt,
        )
        if context:
            return RetrievalPacket(
                query=query,
                mode=mode,
                requested_ranker=ranker,
                ranker=attempt,
                limit=limit,
                budget_tokens=budget_tokens,
                used_tokens=approx_tokens(context),
                source_count=len(sources),
                context=context,
                sources=sources,
            )
    return RetrievalPacket(query, mode, ranker, _ranker_attempts(ranker)[-1], limit, budget_tokens, 0, 0, "", [])


def retrieve(
    root: Path,
    query: str,
    limit: int = 3,
    budget_tokens: int = 1000,
    mode: str = "documents",
    type_filter: str | None = None,
    tag_filters: Sequence[str] = (),
    system_filters: Sequence[str] = (),
    ranker: str = "bm25",
) -> str:
    return retrieve_packet(
        root,
        query,
        limit=limit,
        budget_tokens=budget_tokens,
        mode=mode,
        type_filter=type_filter,
        tag_filters=tag_filters,
        system_filters=system_filters,
        ranker=ranker,
    ).context
