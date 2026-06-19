---
type: Runbook
title: Cache mismatch failover runbook
description: Resolve cache inconsistent incidents for failover.
tags: [cache, cache, inconsistent]
timestamp: 2026-06-19T00:00:00Z
aliases: [contract difference, cache reconnection, mismatch failover]
systems: [cache, worker]
signals: [mismatch, inconsistent, failover]
---

# Context

The cache workflow reports mismatch and inconsistent behavior around failover.
Operators use this runbook note when the worker owner needs a deterministic
diagnosis path. The alternate wording is contract difference.

# Diagnosis

Confirm the failover state, compare the latest worker event, and identify the
customer impact before changing the cache workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this cache incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the cache inconsistent workflow.

# Resolution

Apply the reconnection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the cache
inconsistent finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de cache
e confirmar o sintoma inconsistent antes da escalada.
