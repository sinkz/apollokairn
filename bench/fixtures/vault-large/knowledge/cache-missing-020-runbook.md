---
type: Runbook
title: Cache missing failover runbook
description: Resolve cache not found incidents for failover.
tags: [cache, cache, not-found]
timestamp: 2026-06-19T00:00:00Z
aliases: [absent record, cache reconnection, missing failover]
systems: [cache, worker]
signals: [missing, not found, failover]
---

# Context

The cache workflow reports missing and not found behavior around failover.
Operators use this runbook note when the worker owner needs a deterministic
diagnosis path. The alternate wording is absent record.

# Diagnosis

Confirm the failover state, compare the latest worker event, and identify the
customer impact before changing the cache workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this cache incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the cache not found workflow.

# Resolution

Apply the reconnection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the cache
not found finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de cache
e confirmar o sintoma not found antes da escalada.
