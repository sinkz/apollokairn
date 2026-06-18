# Agent Adapters

ApolloKairn stays agent-agnostic: the vault is Markdown, the index is local, and every
agent talks to the same CLI and JSON contract. Adapters are small instruction
layers over that contract, not separate knowledge stores.

## Global Skills

For Codex and Hermes, install the shared `apollokairn-vault` Agent Skill when
you want the agent to know the ApolloKairn workflow from any repository:

```bash
apollokairn agent install codex
apollokairn agent install hermes
apollokairn agent doctor --json
```

The default mode is `copy`. Use `--mode symlink` only while developing from a
source checkout. The versioned skill source lives in `agentic/skills/`.

## Vault-Local Guides

Use generated guide files when a specific vault should carry instructions for
one or more agent harnesses.

| Target | Command | Generated file |
| --- | --- | --- |
| Generic agents | `apollokairn setup-agent agents --path PATH_TO_VAULT` | `AGENTS.md` |
| Codex | `apollokairn setup-agent codex --path PATH_TO_VAULT` | `CODEX.md` |
| Claude | `apollokairn setup-agent claude --path PATH_TO_VAULT` | `CLAUDE.md` |
| OpenCode | `apollokairn setup-agent opencode --path PATH_TO_VAULT` | `OPENCODE.md` |
| Hermes | `apollokairn setup-agent hermes --path PATH_TO_VAULT` | `HERMES.md` |
| GitHub Copilot | `apollokairn setup-agent copilot --path PATH_TO_VAULT` | `.github/copilot-instructions.md` |

Use `--json` when an installer or bootstrap script needs the generated path:

```bash
apollokairn setup-agent codex --path PATH_TO_VAULT --json
apollokairn setup-agent copilot --path PATH_TO_VAULT --json
```

The generated guide tells the agent to:

- run `apollokairn doctor` when vault health is unknown;
- use JSON search before answering;
- prefer passage retrieval with `--ranker auto` before opening full files;
- run `apollokairn vocab suggest` when vocabulary may differ;
- check `apollokairn similar` before writing;
- use schema-compatible types and tags;
- use `--body-file` or `--body-stdin` for multi-line Markdown;
- run `apollokairn validate` and `apollokairn index` after successful writes.

## Refresh Multiple Vault Guides

`apollokairn refresh-guides` reads `.cairn/config.json` and rewrites every configured
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
apollokairn refresh-guides --path PATH_TO_VAULT --json
```

Guide paths must stay inside the vault. Generated guide files are ignored by
validation, indexing, search, similar-note checks, and stats.

## What This Is Not

These adapters do not add runtime dependencies and do not require Codex, Claude,
OpenCode, Hermes, or GitHub Copilot to be installed. They are portable
instruction files over the stable CLI/JSON surface. Future plugin packages or
MCP servers should stay optional and outside the dependency-free core.
