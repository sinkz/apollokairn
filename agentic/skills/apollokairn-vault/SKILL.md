---
name: apollokairn-vault
description: Use when the user asks to use ApolloKairn, a registered knowledge vault, second brain notes, recurring bug/process memory, or local vault search, retrieval, and writeback.
---

# ApolloKairn Vault

ApolloKairn is a local Markdown knowledge vault. Use the CLI first; avoid reading
the whole vault unless targeted retrieval is not enough.

## Start

1. Check the active vault with `apollokairn vault current --json`.
2. If no active vault exists, run `apollokairn vault list --json` and ask which vault to use.
3. After choosing, pass `--vault NAME` on search, retrieval, and writes.
4. Run `apollokairn doctor --vault NAME` when vault health is unknown.

## Search

- Start with `apollokairn search "<query>" --vault NAME --json --limit 5`.
- For LLM context, use `apollokairn retrieve "<query>" --vault NAME --mode passages --ranker auto --budget 800 --json`.
- If vocabulary may differ, run `apollokairn vocab suggest "<query>" --vault NAME --json`.

## Writeback

- Before creating, run `apollokairn similar "<summary>" --vault NAME --json`.
- Update a related note with `apollokairn update PATH --append-file FILE --vault NAME`.
- Create only reusable knowledge with `apollokairn capture ... --body-file FILE --vault NAME`.
- After writes, run `apollokairn validate --vault NAME` and `apollokairn index --vault NAME`.

Never store secrets, credentials, tokens, private keys, or passwords.
See `references/commands.md` and `references/workflows.md` for concise recipes.
