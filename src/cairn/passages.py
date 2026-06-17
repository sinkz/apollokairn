from __future__ import annotations

import re
from dataclasses import dataclass

from cairn.frontmatter import parse_document


_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class Passage:
    path: str
    heading: str
    start_line: int
    end_line: int
    text: str


def _body_start_line(document: str) -> int:
    lines = document.splitlines()
    for idx, line in enumerate(lines, start=1):
        if idx > 1 and line.strip() == "---":
            return idx + 2 if idx < len(lines) and lines[idx].strip() == "" else idx + 1
    return 1


def split_passages(path: str, document: str) -> list[Passage]:
    parsed = parse_document(document)
    body_lines = parsed.body.splitlines()
    base_line = _body_start_line(document)
    passages: list[Passage] = []
    heading = "Document"
    start_line = base_line
    current: list[str] = []

    def flush(end_line: int) -> None:
        text = "\n".join(current).strip()
        if text:
            passages.append(
                Passage(
                    path=path,
                    heading=heading,
                    start_line=start_line,
                    end_line=end_line,
                    text=text,
                )
            )

    for body_index, line in enumerate(body_lines, start=0):
        full_line = base_line + body_index
        match = _HEADING.match(line)
        if match:
            flush(full_line - 1)
            heading = match.group(2).strip()
            start_line = full_line
            current = [line]
            continue
        current.append(line)
    flush(base_line + len(body_lines) - 1)
    return passages
