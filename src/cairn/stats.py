from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from cairn.frontmatter import FrontmatterError, parse_document
from cairn.indexer import _concept_files
from cairn.retriever import approx_tokens


@dataclass(frozen=True)
class VaultStats:
    documents: int
    types: dict[str, int]
    tags: dict[str, int]
    chars: int
    estimated_tokens: int


def collect_stats(root: Path) -> VaultStats:
    root = Path(root)
    type_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    chars = 0
    documents = 0
    for path in _concept_files(root):
        text = path.read_text(encoding="utf-8")
        try:
            parsed = parse_document(text)
        except FrontmatterError:
            continue
        documents += 1
        chars += len(text)
        typ = parsed.frontmatter.get("type")
        if isinstance(typ, str) and typ:
            type_counts[typ] += 1
        tags = parsed.frontmatter.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str) and tag:
                    tag_counts[tag] += 1
    return VaultStats(
        documents=documents,
        types=dict(sorted(type_counts.items())),
        tags=dict(sorted(tag_counts.items())),
        chars=chars,
        estimated_tokens=approx_tokens("x" * chars),
    )


def render_stats(stats: VaultStats) -> str:
    lines = [
        f"documents: {stats.documents}",
        f"chars: {stats.chars}",
        f"estimated_tokens: {stats.estimated_tokens}",
        "types:",
    ]
    lines.extend(f"  {key}: {value}" for key, value in stats.types.items())
    lines.append("tags:")
    lines.extend(f"  {key}: {value}" for key, value in stats.tags.items())
    return "\n".join(lines) + "\n"
