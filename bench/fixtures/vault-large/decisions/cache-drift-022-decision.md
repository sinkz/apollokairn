---
type: Decision
title: Cache skew decision
description: Decision record for cache skew handling.
tags: [cache, cache, skew, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, cache reconnection, drift failover, cache decision]
systems: [cache, worker]
signals: [drift, skew, failover]
---

# Context

The cache workflow reports drift and skew behavior around failover.
Operators use this decision note when the worker owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the failover state, compare the latest worker event, and identify the
customer impact before changing the cache workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this cache incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the cache skew workflow.

# Resolution

Apply the reconnection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the cache
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de cache
e confirmar o sintoma skew antes da escalada.
