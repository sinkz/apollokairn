---
type: Reference
title: Observability trace reference
description: Reference facts for observability trace.
tags: [observability, observability, forbidden, reference]
timestamp: 2026-06-19T00:00:00Z
aliases: [authorization denied, observability dashboard, 403 trace, alert reference]
systems: [observability, alert]
signals: [403, forbidden, trace]
---

# Context

The observability workflow reports 403 and forbidden behavior around trace.
Operators use this reference note when the alert owner needs a deterministic
diagnosis path. The alternate wording is authorization denied.

# Diagnosis

Confirm the trace state, compare the latest alert event, and identify the
customer impact before changing the observability workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this observability incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the observability forbidden workflow.

# Resolution

Apply the dashboard recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the observability
forbidden finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de observability
e confirmar o sintoma forbidden antes da escalada.
