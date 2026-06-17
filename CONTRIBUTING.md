# Contributing

Thanks for considering a contribution to Cairn.

## Development Setup

```bash
python -m pip install -e .
python -m unittest discover -v
```

The runtime should stay Python standard-library only unless a dependency is
clearly optional and isolated behind an integration boundary.

## Design Principles

- Markdown files remain the source of truth.
- Search should minimize LLM context, not maximize output.
- Local-first behavior must work without a network.
- Agent-facing commands should be deterministic and scriptable.
- Never store or emit secrets in examples, tests, snippets, or fixtures.

## Pull Requests

Before opening a PR:

1. Add focused tests for behavior changes.
2. Run `python -m unittest discover -v`.
3. Update docs when commands or workflows change.
4. Keep unrelated refactors out of the PR.

## Commit Style

Use short imperative messages, for example:

```text
Add budgeted retrieval command
```
