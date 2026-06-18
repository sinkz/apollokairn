# Cairn Examples

This directory contains vaults you can run locally to understand Cairn before
creating your own vault.

## Available Examples

| Path | Purpose |
| --- | --- |
| `examples/engineering-vault` | Small engineering vault with a deploy runbook, a hotfix process, and a search decision |

## Run The Engineering Example

From the repository root:

```bash
python -m pip install -e .
cairn validate --path examples/engineering-vault
cairn index --path examples/engineering-vault --rebuild
cairn doctor --path examples/engineering-vault
```

Search the example:

```bash
cairn search "deploy 403 token" --path examples/engineering-vault --limit 3
cairn search "release denied workspace access" --path examples/engineering-vault --limit 3
```

Retrieve compact context:

```bash
cairn retrieve "deploy 403 token" --path examples/engineering-vault --budget 500
cairn retrieve "hotfix release rollback" --path examples/engineering-vault --mode passages --budget 300
```

Open only the part you need:

```bash
cairn show knowledge/deploy-403.md --path examples/engineering-vault --section Resolution
cairn show processes/hotfix-release-checklist.md --path examples/engineering-vault --snippet rollback
```

Check for duplicate knowledge:

```bash
cairn similar "deploy forbidden after token rotation" --path examples/engineering-vault
```

## Create A Disposable Copy

If you want to edit the example, copy it first:

```bash
cp -R examples/engineering-vault PATH_TO_TEST_VAULT
cairn index --path PATH_TO_TEST_VAULT --rebuild
```

PowerShell:

```powershell
Copy-Item -Recurse examples\engineering-vault PATH_TO_TEST_VAULT
cairn index --path PATH_TO_TEST_VAULT --rebuild
```

## What To Look For

- Each note has required frontmatter: `type`, `title`, `description`, `tags`,
  and `timestamp`.
- `aliases`, `systems`, and `signals` make old knowledge easier to find when
  the future query uses different words.
- Search returns snippets and paths first.
- `retrieve --mode passages` returns smaller context packets than full
  documents.
- `.cairn/index.db` is generated and can be rebuilt; Markdown files are the
  source of truth.
