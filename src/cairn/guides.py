from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


GUIDE_FILES = {
    "agents": "AGENTS.md",
    "codex": "CODEX.md",
    "claude": "CLAUDE.md",
    "opencode": "OPENCODE.md",
}


@dataclass(frozen=True)
class GuideResult:
    path: str


def _guide_name_from_file(path: str) -> str:
    upper = path.upper()
    if upper == "CODEX.MD":
        return "Codex"
    if upper == "CLAUDE.MD":
        return "Claude"
    if upper == "OPENCODE.MD":
        return "OpenCode"
    return "Agents"


def render_agent_guide(name: str = "Agents") -> str:
    return (
        f"# Cairn Guide for {name}\n\n"
        "Use Cairn as the local knowledge source before solving recurring work.\n\n"
        "## Before Answering\n\n"
        "1. Run `cairn doctor --path <vault>` when vault health is unknown.\n"
        "2. Run `cairn search \"<query>\" --path <vault> --json` for saved knowledge.\n"
        "3. Open at most the top 3 relevant documents.\n"
        "4. Prefer `cairn retrieve \"<query>\" --path <vault> --budget 800` or partial `cairn show` before reading full files.\n\n"
        "## After Solving\n\n"
        "1. Run `cairn similar \"<new knowledge>\" --path <vault>`.\n"
        "2. Prefer `cairn update <path> --append \"<note>\" --path <vault>` when a related note exists.\n"
        "3. Use `cairn add` or `cairn capture` only for reusable knowledge that is not already represented.\n"
        "4. Run `cairn validate --path <vault>` and `cairn index --path <vault>` after edits.\n\n"
        "Never store secrets, credentials, tokens, private keys, or passwords.\n"
    )


def setup_agent(root: Path, agent: str) -> GuideResult:
    root = Path(root)
    key = agent.casefold()
    if key not in GUIDE_FILES:
        known = ", ".join(sorted(GUIDE_FILES))
        raise ValueError(f"unknown agent '{agent}'. Known agents: {known}")
    filename = GUIDE_FILES[key]
    (root / filename).write_text(render_agent_guide(_guide_name_from_file(filename)), encoding="utf-8")
    return GuideResult(path=filename)


def refresh_guides(root: Path) -> list[GuideResult]:
    root = Path(root)
    config_path = root / ".cairn" / "config.json"
    guide_files = ["AGENTS.md"]
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            configured = data.get("generated_guides", guide_files)
            if isinstance(configured, list):
                guide_files = [item for item in configured if isinstance(item, str)]
        except json.JSONDecodeError:
            pass
    results: list[GuideResult] = []
    for filename in guide_files:
        (root / filename).write_text(render_agent_guide(_guide_name_from_file(filename)), encoding="utf-8")
        results.append(GuideResult(path=filename))
    return results
