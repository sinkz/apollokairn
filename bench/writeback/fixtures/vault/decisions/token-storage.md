---
type: Decision
title: Store session tokens in secure cookies
description: Decision about browser session token storage.
tags: [architecture, auth]
timestamp: 2026-06-17T10:00:00Z
systems: [auth, web]
signals: [session token, secure cookie, browser auth]
---

# Decision

Session tokens are stored in secure HTTP-only cookies for browser clients.

# Consequence

Do not store browser session tokens in local storage.
