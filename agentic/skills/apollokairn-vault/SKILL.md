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
- Update with `--append-file FILE` or `--append-stdin`; create with `--body-file FILE` or `--body-stdin`.
- After writes, run `apollokairn validate --vault NAME` and `apollokairn index --vault NAME`.

## Usage Evidence

- When asked to evaluate real vault behavior, first make sure usage metrics are explicitly enabled with `apollokairn usage status --vault NAME --json`.
- Generate local evidence with `apollokairn usage evidence --vault NAME --json`; use it to discuss no-result rates, no-source retrieves, passage usage, and whether ranking/RRF/embeddings have enough evidence for review.
- Do not treat usage logs as success labels unless explicit user feedback is recorded.

Never store secrets, credentials, tokens, private keys, or passwords.
See `references/commands.md` and `references/workflows.md` for concise recipes.
