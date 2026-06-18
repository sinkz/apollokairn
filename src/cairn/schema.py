from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CairnSchema:
    profile: str
    types: set[str]
    tags: set[str]


@dataclass(frozen=True)
class SchemaIssue:
    path: str
    message: str


REQUIRED_FIELDS = ("type", "title", "description", "tags", "timestamp")
REQUIRED_SCALAR_FIELDS = ("type", "title", "description", "timestamp")


def parse_schema(text: str) -> CairnSchema:
    profile = "custom"
    types: set[str] = set()
    tags: set[str] = set()
    section: str | None = None

    for raw in text.splitlines():
        line = raw.strip()
        profile_match = re.match(r"Profile:\s*`?([^`]+)`?", line)
        if profile_match:
            profile = profile_match.group(1).strip()
            continue
        if line == "## Types":
            section = "types"
            continue
        if line == "## Tags":
            section = "tags"
            continue
        if line.startswith("- ") and section == "types":
            types.add(line[2:].strip())
        elif line.startswith("- ") and section == "tags":
            tags.add(line[2:].strip())

    return CairnSchema(profile=profile, types=types, tags=tags)


def _is_iso8601(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    candidate = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return True


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_frontmatter_policy(path: str, frontmatter: dict[str, object], schema: CairnSchema) -> list[SchemaIssue]:
    issues: list[SchemaIssue] = []
    for field_name in REQUIRED_FIELDS:
        if field_name not in frontmatter or frontmatter[field_name] in ("", []):
            issues.append(SchemaIssue(path, f"missing required field: {field_name}"))
    for field_name in REQUIRED_SCALAR_FIELDS:
        if (
            field_name in frontmatter
            and frontmatter[field_name] not in ("", [])
            and not _is_non_empty_string(frontmatter[field_name])
        ):
            issues.append(SchemaIssue(path, f"{field_name} must be a non-empty string"))
    typ = frontmatter.get("type")
    if isinstance(typ, str) and typ and typ not in schema.types:
        issues.append(SchemaIssue(path, f"type '{typ}' is not declared in SCHEMA.md"))
    tags = frontmatter.get("tags", [])
    if not isinstance(tags, list):
        issues.append(SchemaIssue(path, "tags must be a list"))
    else:
        for tag in tags:
            if isinstance(tag, str) and tag not in schema.tags:
                issues.append(SchemaIssue(path, f"tag '{tag}' is not declared in SCHEMA.md"))
    timestamp = frontmatter.get("timestamp")
    if _is_non_empty_string(timestamp) and not _is_iso8601(timestamp):
        issues.append(SchemaIssue(path, "timestamp must be ISO 8601"))
    return issues
