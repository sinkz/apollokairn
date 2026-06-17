---
type: Runbook
title: ERR_DB_POOL_EXHAUSTED during checkout
description: Fix checkout failures when the database connection pool is exhausted.
tags: [bug, database]
timestamp: 2026-06-17T10:07:00Z
aliases: [database pool exhausted, checkout db pool]
systems: [checkout, database]
signals: [ERR_DB_POOL_EXHAUSTED, pool exhausted, checkout failure]
---

# Context

Checkout requests fail with `ERR_DB_POOL_EXHAUSTED` when workers hold database
connections too long during a traffic spike.

# Resolution

Lower checkout worker concurrency, inspect slow transactions, and restart only
the affected worker group after connection pressure drops.
