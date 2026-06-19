---
type: Decision
title: Cache forbidden decision
description: Decision record for cache forbidden handling.
tags: [cache, cache, forbidden, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [authorization denied, cache reconnection, 403 failover, cache decision]
systems: [cache, worker]
signals: [403, forbidden, failover]
---

# Context

The cache workflow reports 403 and forbidden behavior around failover.
Operators use this decision note when the worker owner needs a deterministic
diagnosis path. The alternate wording is authorization denied.

# Diagnosis

Confirm the failover state, compare the latest worker event, and identify the
customer impact before changing the cache workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this cache incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the cache forbidden workflow.

# Resolution

Apply the reconnection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the cache
forbidden finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de cache
e confirmar o sintoma forbidden antes da escalada.
