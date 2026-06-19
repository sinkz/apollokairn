---
type: Runbook
title: Database saturation checkout runbook
description: Resolve database pressure incidents for checkout.
tags: [database, database, pressure]
timestamp: 2026-06-19T00:00:00Z
aliases: [capacity limit, database connection, saturation checkout]
systems: [database, pool]
signals: [saturation, pressure, checkout]
---

# Context

The database workflow reports saturation and pressure behavior around checkout.
Operators use this runbook note when the pool owner needs a deterministic
diagnosis path. The alternate wording is capacity limit.

# Diagnosis

Confirm the checkout state, compare the latest pool event, and identify the
customer impact before changing the database workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this database incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the database pressure workflow.

# Resolution

Apply the connection recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the database
pressure finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de database
e confirmar o sintoma pressure antes da escalada.
