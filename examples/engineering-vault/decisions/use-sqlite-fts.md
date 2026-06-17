---
type: Decision
title: Use SQLite FTS for local lexical search
description: Keeps search local-first and dependency-free before optional embedding integrations.
tags: [architecture]
timestamp: 2026-06-17T10:10:00Z
aliases: [local search, fts5, bm25]
systems: [cairn]
signals: [token budget, lexical retrieval, offline search]
---

# Decision

Use SQLite FTS5 as the core search backend.

# Rationale

The core workflow should work offline, avoid external services, and stay easy to
audit. FTS5 gives Cairn BM25 ranking, snippets, and compact local indexes with
no runtime dependency beyond Python's standard library.

# Consequences

Embedding search can still be added later as an optional integration, but it
must prove value against deterministic benchmarks before becoming a default.
