---
type: Reference
title: Cache failover reference
description: Reference facts for cache failover.
tags: [cache, cache, latency, reference]
timestamp: 2026-06-19T00:00:00Z
aliases: [slow response, cache reconnection, timeout failover, worker reference]
systems: [cache, worker]
signals: [timeout, latency, failover]
---

# Context

The cache workflow reports timeout and latency behavior around failover.
Operators use this reference note when the worker owner needs a deterministic
diagnosis path. The alternate wording is slow response.

# Diagnosis

Confirm the failover state, compare the latest worker event, and identify the
customer impact before changing the cache workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this cache incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the cache latency workflow.

# Resolution

Apply the reconnection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the cache
latency finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de cache
e confirmar o sintoma latency antes da escalada.
