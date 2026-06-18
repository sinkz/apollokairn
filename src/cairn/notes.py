from __future__ import annotations

import re
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from cairn.frontmatter import parse_document
from cairn.schema import SchemaIssue, parse_schema, validate_frontmatter_policy
from cairn.secret_scan import scan_text


_SLUG_CHARS = re.compile(r"[^a-z0-9]+")


class NotePolicyError(ValueError):
    def __init__(self, path: str, issues: Sequence[SchemaIssue]) -> None:
        self.path = path
        self.issues = list(issues)
        message = "; ".join(issue.message for issue in self.issues) or "schema policy failed"
        super().__init__(message)


@dataclass(frozen=True)
class NoteWriteResult:
    path: str
    changed: bool
    would_change: bool = True
    dry_run: bool = False
    reason: str = "updated"
    sha256_before: str | None = None
    sha256_after: str | None = None


@dataclass(frozen=True)
class NotePolicyResult:
    ok: bool
    path: str
    error_count: int
    errors: list[SchemaIssue] = field(default_factory=list)


def slugify(title: str) -> str:
    slug = _SLUG_CHARS.sub("-", title.casefold()).strip("-")
    return slug or "untitled"


def _frontmatter_list(items: Sequence[str]) -> str:
    return "[" + ", ".join(items) + "]"


def _render_body(body: str) -> str:
    stripped = body.strip()
    if not stripped:
        return "# Context\n\n"
    if stripped.startswith("#"):
        return f"{stripped}\n"
    return f"# Context\n\n{stripped}\n"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _secret_issues(path: str, text: str) -> list[SchemaIssue]:
    return [
        SchemaIssue(path, f"potential secret detected: {finding.kind} on line {finding.line}")
        for finding in scan_text(text)
    ]


def _validate_new_note(root: Path, rel: Path, content: str) -> None:
    rel_path = rel.as_posix()
    schema_path = root / "SCHEMA.md"
    if not schema_path.exists():
        raise NotePolicyError(rel_path, [SchemaIssue("SCHEMA.md", "missing schema file")])
    schema = parse_schema(schema_path.read_text(encoding="utf-8"))
    parsed = parse_document(content)
    issues = validate_frontmatter_policy(rel_path, parsed.frontmatter, schema)
    issues.extend(_secret_issues(rel_path, content))
    if issues:
        raise NotePolicyError(rel_path, issues)


def _validate_append(display_path: str, snippet: str) -> None:
    issues = _secret_issues(display_path, snippet)
    if issues:
        raise NotePolicyError(display_path, issues)


def note_policy_payload(exc: NotePolicyError) -> NotePolicyResult:
    return NotePolicyResult(ok=False, path=exc.path, error_count=len(exc.issues), errors=exc.issues)


def create_note(
    root: Path,
    title: str,
    description: str,
    typ: str = "Note",
    tags: Sequence[str] = (),
    folder: str = "knowledge",
    body: str = "",
    aliases: Sequence[str] = (),
    systems: Sequence[str] = (),
    signals: Sequence[str] = (),
    timestamp: str | None = None,
    dry_run: bool = False,
) -> NoteWriteResult:
    root = Path(root)
    if not title.strip():
        raise ValueError("title is required")
    if not description.strip():
        raise ValueError("description is required")
    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    rel = Path(folder) / f"{slugify(title)}.md"
    path = (root / rel).resolve()
    if root.resolve() not in path.parents and path != root.resolve():
        raise ValueError("path must stay inside vault")
    if path.exists():
        raise FileExistsError(rel.as_posix())
    content = (
        "---\n"
        f"type: {typ}\n"
        f"title: {title}\n"
        f"description: {description}\n"
        f"tags: {_frontmatter_list(tags)}\n"
        f"timestamp: {timestamp}\n"
        f"aliases: {_frontmatter_list(aliases)}\n"
        f"systems: {_frontmatter_list(systems)}\n"
        f"signals: {_frontmatter_list(signals)}\n"
        "---\n\n"
        f"{_render_body(body)}"
    )
    _validate_new_note(root, rel, content)
    if dry_run:
        return NoteWriteResult(
            path=rel.as_posix(),
            changed=False,
            would_change=True,
            dry_run=True,
            reason="dry_run",
            sha256_after=None,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return NoteWriteResult(
        path=rel.as_posix(),
        changed=True,
        would_change=True,
        dry_run=False,
        reason="created",
        sha256_after=_sha256_bytes(content.encode("utf-8")),
    )


def _resolve_note_path(root: Path, rel_path: str) -> tuple[Path, str]:
    root_resolved = Path(root).resolve()
    candidate = Path(rel_path)
    path = candidate.resolve() if candidate.is_absolute() else (root_resolved / candidate).resolve()
    if root_resolved not in path.parents and path != root_resolved:
        raise ValueError("path must stay inside vault")
    return path, path.relative_to(root_resolved).as_posix()


def _replace_timestamp(text: str, timestamp: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text

    end_index: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break
    if end_index is None:
        return text

    newline = "\n"
    for line in lines:
        if line.endswith("\r\n"):
            newline = "\r\n"
            break

    for index in range(1, end_index):
        if lines[index].startswith("timestamp:"):
            ending = "\r\n" if lines[index].endswith("\r\n") else "\n" if lines[index].endswith("\n") else ""
            lines[index] = f"timestamp: {timestamp}{ending}"
            return "".join(lines)

    lines.insert(end_index, f"timestamp: {timestamp}{newline}")
    return "".join(lines)


def append_to_note(
    root: Path,
    rel_path: str,
    text: str,
    dry_run: bool = False,
    expected_sha256: str | None = None,
    timestamp: str | None = None,
) -> NoteWriteResult:
    path, display_path = _resolve_note_path(Path(root), rel_path)
    if not path.is_file():
        raise FileNotFoundError(rel_path)
    current_bytes = path.read_bytes()
    current_hash = _sha256_bytes(current_bytes)
    if expected_sha256 and expected_sha256 != current_hash:
        raise ValueError("document modified since expected sha256")
    current = current_bytes.decode("utf-8")
    snippet = text.strip()
    if not snippet:
        raise ValueError("--append must not be empty")
    _validate_append(display_path, snippet)
    if snippet in current:
        return NoteWriteResult(
            path=display_path,
            changed=False,
            would_change=False,
            dry_run=dry_run,
            reason="already_present",
            sha256_before=current_hash,
            sha256_after=current_hash,
        )
    separator = "\n" if current.endswith("\n") else "\n\n"
    touched = _replace_timestamp(current, timestamp or datetime.now(timezone.utc).isoformat())
    updated = touched + separator + snippet + "\n"
    if dry_run:
        return NoteWriteResult(
            path=display_path,
            changed=False,
            would_change=True,
            dry_run=True,
            reason="dry_run",
            sha256_before=current_hash,
            sha256_after=current_hash,
        )
    path.write_text(updated, encoding="utf-8")
    return NoteWriteResult(
        path=display_path,
        changed=True,
        would_change=True,
        dry_run=False,
        reason="updated",
        sha256_before=current_hash,
        sha256_after=_sha256_bytes(updated.encode("utf-8")),
    )
