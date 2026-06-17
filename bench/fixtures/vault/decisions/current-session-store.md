---
type: Decision
title: Current session store uses Redis
description: Current decision for session storage after Postgres lock contention.
tags: [architecture, auth]
timestamp: 2026-06-17T10:10:00Z
aliases: [current session store, redis session decision]
systems: [auth]
signals: [current decision, redis, session store]
---

# Decision

Use Redis for the current session store.

# Rationale

Redis avoids the Postgres lock contention observed during login traffic spikes
and keeps refresh checks low latency.
