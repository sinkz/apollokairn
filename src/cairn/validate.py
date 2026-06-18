from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from cairn.config import is_excluded, load_config
from cairn.frontmatter import FrontmatterError, parse_document
from cairn.schema import parse_schema, validate_frontmatter_policy
from cairn.secret_scan import scan_text


RESERVED_NAMES = {
    "index.md",
    "log.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CODEX.md",
    "copilot-instructions.md",
    "glossary.md",
    "HERMES.md",
    "OPENCODE.md",
    "SCHEMA.md",
}
@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


@dataclass
class ValidationReport:
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)


def _concept_files(root: Path) -> list[Path]:
    ignored_parts = {".cairn", "_templates"}
    config = load_config(root)
    out: list[Path] = []
    for path in root.rglob("*.md"):
        if path.name in RESERVED_NAMES:
            continue
        if any(part in ignored_parts for part in path.relative_to(root).parts):
            continue
        if is_excluded(root, path, config):
            continue
        out.append(path)
    return sorted(out)


def validate_vault(root: Path) -> ValidationReport:
    root = Path(root)
    report = ValidationReport()
    schema_path = root / "SCHEMA.md"
    if not schema_path.exists():
        report.errors.append(ValidationIssue("SCHEMA.md", "missing schema file"))
        return report

    schema = parse_schema(schema_path.read_text(encoding="utf-8"))

    for path in _concept_files(root):
        rel = path.relative_to(root).as_posix()
        raw = path.read_text(encoding="utf-8")
        for finding in scan_text(raw):
            report.errors.append(
                ValidationIssue(
                    rel,
                    f"potential secret detected: {finding.kind} on line {finding.line}",
                )
            )
        try:
            doc = parse_document(raw)
        except FrontmatterError as exc:
            report.errors.append(ValidationIssue(rel, str(exc)))
            continue
        for issue in validate_frontmatter_policy(rel, doc.frontmatter, schema):
            report.errors.append(ValidationIssue(issue.path, issue.message))

    return report
