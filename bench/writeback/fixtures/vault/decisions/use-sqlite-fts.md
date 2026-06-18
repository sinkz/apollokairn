---
type: Decision
title: Use SQLite FTS5 unicode61 tokenizer
description: Use SQLite FTS5 for local lexical search with unicode61 tokenization.
tags: [architecture, library]
timestamp: 2026-06-17T10:00:00Z
systems: [search]
signals: [sqlite fts5, unicode61, remove_diacritics, local index]
---

# Decision

Cairn uses SQLite FTS5 for local search because it is available through the
Python standard library and keeps the core dependency-free.

# Consequence

The index is rebuilt locally and can use unicode61 tokenization for accent
insensitive matching in Portuguese and English notes.
