---
type: Runbook
title: Cache workers disconnected after failover
description: Reconnect workers after Redis cache failover.
tags: [bug, cache]
timestamp: 2026-06-17T10:00:00Z
systems: [redis, workers]
signals: [cache failover, worker reconnect, redis]
---

# Context

After Redis failover, background workers can remain disconnected even though the
new primary is healthy.

# Resolution

Run the reconnection workflow, restart affected workers, and verify queue drain
rate before closing the incident.
