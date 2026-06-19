---
type: Runbook
title: Database timeout checkout runbook
description: Resolve database latency incidents for checkout.
tags: [database, database, latency]
timestamp: 2026-06-19T00:00:00Z
aliases: [slow response, database connection, timeout checkout]
systems: [database, pool]
signals: [timeout, latency, checkout]
---

# Context

The database workflow reports timeout and latency behavior around checkout.
Operators use this runbook note when the pool owner needs a deterministic
diagnosis path. The alternate wording is slow response.

# Diagnosis

Confirm the checkout state, compare the latest pool event, and identify the
customer impact before changing the database workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this database incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the database latency workflow.

# Resolution

Apply the connection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the database
latency finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de database
e confirmar o sintoma latency antes da escalada.
