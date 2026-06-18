# Roadmap

Cairn is built around one constraint: useful retrieval should cost less context
than opening everything. The roadmap is organized by product maturity, not by
implementation history.

## Shipped

- Local Markdown vault with frontmatter schema, profiles, validation, and
  rebuildable SQLite FTS index.
- Agent-agnostic CLI workflow: search, retrieve, show partial context, capture,
  update, validate, doctor, stats, export, and import.
- Budgeted retrieval for LLM context packets, including passage-level retrieval
  for smaller prompts.
- Deterministic search benchmark with qrels, golden checks, ranking metrics,
  token budgets, and passage-vs-document context reduction.
- BM25 default ranking plus opt-in RRF and `retrieve --ranker auto` fallback.
- Secret-safety checks for validation, retrieval, and export.
- Similar-note detection with fingerprint fallback and `duplicate_candidate` /
  `related` labels.
- Markdown writeback ergonomics through `--body-file`, `--body-stdin`,
  `--append-file`, and `--append-stdin`.
- Public documentation, example vault, changelog, contribution guide, and GitHub
  Pages overview.

## Now

- Build a deterministic writeback suite that exercises agent-style vault
  behavior: duplicate prevention, note updates, recurring bugs, process notes,
  access notes, library references, and token cost.
- Add benchmark history and comparison data to the public site so regressions are
  visible over time.
- Tighten evaluation around `similar` thresholds and update-vs-create decisions.
- Keep README, usage guides, examples, and the public page aligned with actual
  commands.

## Next

- Optional adapters or plugin packages for Codex, Claude, GitHub Copilot,
  OpenCode, and other agent harnesses.
- Team workflows for reviewing shared vault changes before they become common
  knowledge.
- Better benchmark slices by role and domain, such as engineering, support,
  product, and personal notes.
- More import paths from existing Markdown or Obsidian-style knowledge bases.

## Later

- Optional embedding backend behind a strict integration boundary.
- UI or TUI for browsing, reviewing, and curating notes.
- Richer analytics for vault health, duplication, stale notes, and coverage gaps.

## Non-goals

- Replacing Markdown as the source of truth.
- Requiring cloud services for local search.
- Making embeddings mandatory for the core workflow.
- Storing credentials, private keys, tokens, or secrets.
