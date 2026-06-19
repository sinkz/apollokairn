---
type: Decision
title: Cache stale decision
description: Decision record for cache stale handling.
tags: [cache, cache, stale, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [invalid state, cache reconnection, expired failover, cache decision]
systems: [cache, worker]
signals: [expired, stale, failover]
---

# Context

The cache workflow reports expired and stale behavior around failover.
Operators use this decision note when the worker owner needs a deterministic
diagnosis path. The alternate wording is invalid state.

# Diagnosis

Confirm the failover state, compare the latest worker event, and identify the
customer impact before changing the cache workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this cache incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the cache stale workflow.

# Resolution

Apply the reconnection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the cache
stale finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de cache
e confirmar o sintoma stale antes da escalada.
