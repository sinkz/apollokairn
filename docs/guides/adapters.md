# Agent Adapters

Cairn stays agent-agnostic: the vault is Markdown, the index is local, and every
agent talks to the same CLI and JSON contract. Current adapters are generated
instruction files, not separate plugins or separate knowledge stores.

## Supported Targets

| Target | Command | Generated file |
| --- | --- | --- |
| Generic agents | `cairn setup-agent agents --path PATH_TO_VAULT` | `AGENTS.md` |
| Codex | `cairn setup-agent codex --path PATH_TO_VAULT` | `CODEX.md` |
| Claude | `cairn setup-agent claude --path PATH_TO_VAULT` | `CLAUDE.md` |
| OpenCode | `cairn setup-agent opencode --path PATH_TO_VAULT` | `OPENCODE.md` |
| Hermes | `cairn setup-agent hermes --path PATH_TO_VAULT` | `HERMES.md` |
| GitHub Copilot | `cairn setup-agent copilot --path PATH_TO_VAULT` | `.github/copilot-instructions.md` |

Use `--json` when an installer or bootstrap script needs the generated path:

```bash
cairn setup-agent codex --path PATH_TO_VAULT --json
cairn setup-agent copilot --path PATH_TO_VAULT --json
```

The generated guide tells the agent to:

- run `cairn doctor` when vault health is unknown;
- use JSON search before answering;
- prefer passage retrieval with `--ranker auto` before opening full files;
- run `cairn vocab suggest` when vocabulary may differ;
- check `cairn similar` before writing;
- use schema-compatible types and tags;
- use `--body-file` or `--body-stdin` for multi-line Markdown;
- run `cairn validate` and `cairn index` after successful writes.

## Refresh Multiple Guides

`cairn refresh-guides` reads `.cairn/config.json` and rewrites every configured
guide. This is useful when a vault should carry instructions for several
harnesses.

```json
{
  "generated_guides": [
    "AGENTS.md",
    "CODEX.md",
    "CLAUDE.md",
    "OPENCODE.md",
    "HERMES.md",
    ".github/copilot-instructions.md"
  ]
}
```

```bash
cairn refresh-guides --path PATH_TO_VAULT --json
```

Guide paths must stay inside the vault. Generated guide files are ignored by
validation, indexing, search, similar-note checks, and stats.

## What This Is Not

These adapters do not add runtime dependencies and do not require Codex, Claude,
OpenCode, Hermes, or GitHub Copilot to be installed. They are portable
instruction files over the stable CLI/JSON surface. Future plugin packages or
MCP servers should stay optional and outside the dependency-free core.
