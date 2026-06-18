from __future__ import annotations

import fnmatch
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CairnConfig:
    exclude: tuple[str, ...] = ()
    usage_tracking: bool = False


def validate_config(root: Path) -> list[str]:
    path = Path(root) / ".cairn" / "config.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"config invalid JSON: {exc}"]
    errors: list[str] = []
    exclude = data.get("exclude", [])
    if not isinstance(exclude, list) or any(not isinstance(item, str) for item in exclude):
        errors.append("config exclude must be a list of strings")
    guides = data.get("generated_guides", [])
    if not isinstance(guides, list) or any(not isinstance(item, str) for item in guides):
        errors.append("config generated_guides must be a list of strings")
    search_limit = data.get("search_limit")
    if search_limit is not None and (not isinstance(search_limit, int) or search_limit <= 0):
        errors.append("config search_limit must be a positive integer")
    usage_tracking = data.get("usage_tracking")
    if usage_tracking is not None and not isinstance(usage_tracking, bool):
        errors.append("config usage_tracking must be a boolean")
    return errors


def load_config(root: Path) -> CairnConfig:
    path = Path(root) / ".cairn" / "config.json"
    if not path.exists():
        return CairnConfig()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return CairnConfig()
    exclude = data.get("exclude", [])
    if not isinstance(exclude, list):
        return CairnConfig()
    return CairnConfig(
        exclude=tuple(item for item in exclude if isinstance(item, str) and item.strip()),
        usage_tracking=data.get("usage_tracking") is True,
    )


def is_excluded(root: Path, path: Path, config: CairnConfig | None = None) -> bool:
    root = Path(root)
    config = load_config(root) if config is None else config
    rel = path.relative_to(root).as_posix()
    parts = rel.split("/")
    for raw_pattern in config.exclude:
        pattern = raw_pattern.strip().replace("\\", "/").strip("/")
        if not pattern:
            continue
        if rel == pattern or rel.startswith(pattern + "/"):
            return True
        if pattern in parts:
            return True
        if fnmatch.fnmatch(rel, pattern) or any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True
    return False
