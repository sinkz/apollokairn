---
type: Decision
title: Database skew decision
description: Decision record for database skew handling.
tags: [database, database, skew, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, database connection, drift checkout, database decision]
systems: [database, pool]
signals: [drift, skew, checkout]
---

# Context

The database workflow reports drift and skew behavior around checkout.
Operators use this decision note when the pool owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the checkout state, compare the latest pool event, and identify the
customer impact before changing the database workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this database incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the database skew workflow.

# Resolution

Apply the connection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the database
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de database
e confirmar o sintoma skew antes da escalada.
