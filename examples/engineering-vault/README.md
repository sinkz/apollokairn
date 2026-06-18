# Engineering Vault Example

This is a small Cairn vault for trying the CLI. It contains generic engineering
knowledge only:

- `knowledge/deploy-403.md`: a runbook for deploy failures after token rotation.
- `processes/hotfix-release-checklist.md`: a hotfix release process.
- `decisions/use-sqlite-fts.md`: a decision note explaining local lexical search.

Do not put credentials, private production data, or real customer data in
examples.

## Validate And Index

Run these commands from the repository root:

```bash
python -m pip install -e .
cairn validate --path examples/engineering-vault
cairn index --path examples/engineering-vault --rebuild
cairn doctor --path examples/engineering-vault
```

Expected result:

- `validate` prints no errors.
- `index` creates `examples/engineering-vault/.cairn/index.db`.
- `doctor` reports that the vault and index are healthy.

## Search

```bash
cairn search "deploy 403 token" --path examples/engineering-vault --limit 3
```

Expected top result:

```text
knowledge/deploy-403.md :: Deploy 403 after token rotation
```

Try an alias-style query:

```bash
cairn search "release denied workspace access" --path examples/engineering-vault --limit 3
```

The deploy runbook should still be found because its frontmatter contains
aliases and signals for those terms.

## Retrieve Context For An Agent

Full-document retrieval under a budget:

```bash
cairn retrieve "deploy 403 token" --path examples/engineering-vault --budget 500
```

Passage retrieval for smaller context:

```bash
cairn retrieve "hotfix release rollback" --path examples/engineering-vault --mode passages --budget 300
```

Passage output includes the source path, heading, line range, snippet, and the
matching section text.

## Open Specific Context

```bash
cairn show knowledge/deploy-403.md --path examples/engineering-vault --section Resolution
cairn show knowledge/deploy-403.md --path examples/engineering-vault --snippet "workspace access" --context 2
cairn show processes/hotfix-release-checklist.md --path examples/engineering-vault --lines 18:24
```

Use these after search when you know which document matters and want to avoid
opening unnecessary context.

## Duplicate Check

```bash
cairn similar "deploy forbidden after token rotation" --path examples/engineering-vault
```

The deploy runbook should appear as a related note. In a real vault, update that
note instead of creating another note about the same issue.

## Add A Test Note In A Copy

Copy the example before editing it:

```bash
cp -R examples/engineering-vault PATH_TO_TEST_VAULT
cairn capture --path PATH_TO_TEST_VAULT \
  --title "Webhook 400 after schema change" \
  --description "Fix webhook calls that fail when the payload schema changes." \
  --type Runbook \
  --tag bug \
  --system webhook \
  --signal "HTTP 400" \
  --body "Webhook requests started returning HTTP 400 after the schema changed. Compare the outgoing payload with the provider schema and remove unknown fields."
cairn index --path PATH_TO_TEST_VAULT
cairn search "webhook 400 schema" --path PATH_TO_TEST_VAULT
```

For a real note, open the created Markdown file and add structured sections such
as `# Diagnosis`, `# Resolution`, and `# Follow-up`.
