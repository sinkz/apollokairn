# Cairn Engineering Vault Example

This directory is a small example vault for testing Cairn commands and agent
workflows. It contains generic notes only; do not put credentials or private
production data in examples.

Try it from the repository root:

```bash
python -m cairn validate --path examples/engineering-vault
python -m cairn index --path examples/engineering-vault --rebuild
python -m cairn search "deploy 403 token" --path examples/engineering-vault --limit 3
python -m cairn retrieve "hotfix release rollback" --path examples/engineering-vault --budget 600
```
