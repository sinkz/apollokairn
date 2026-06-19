---
type: Reference
title: Observability trace reference
description: Reference facts for observability trace.
tags: [observability, observability, pressure, reference]
timestamp: 2026-06-19T00:00:00Z
aliases: [capacity limit, observability dashboard, saturation trace, alert reference]
systems: [observability, alert]
signals: [saturation, pressure, trace]
---

# Context

The observability workflow reports saturation and pressure behavior around trace.
Operators use this reference note when the alert owner needs a deterministic
diagnosis path. The alternate wording is capacity limit.

# Diagnosis

Confirm the trace state, compare the latest alert event, and identify the
customer impact before changing the observability workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this observability incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the observability pressure workflow.

# Resolution

Apply the dashboard recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the observability
pressure finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de observability
e confirmar o sintoma pressure antes da escalada.
