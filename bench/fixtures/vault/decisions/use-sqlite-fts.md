---
type: Decision
title: Use SQLite FTS for local lexical search
description: Keep Cairn search local-first and dependency-free before optional embedding integrations.
tags: [architecture, search]
timestamp: 2026-06-17T10:05:00Z
aliases: [fts5, bm25, local search]
systems: [cairn]
signals: [sqlite fts, embeddings optional, token budget]
---

# Decision

Use SQLite FTS5 as the default search engine.

# Rationale

Lexical search is deterministic, local, fast, and dependency-free. Embeddings
can be valuable later, but they should be optional and measured against the same
benchmark before becoming part of the core workflow.
