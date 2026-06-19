---
type: Runbook
title: Observability missing trace runbook
description: Resolve observability not found incidents for trace.
tags: [observability, observability, not-found]
timestamp: 2026-06-19T00:00:00Z
aliases: [absent record, observability dashboard, missing trace]
systems: [observability, alert]
signals: [missing, not found, trace]
---

# Context

The observability workflow reports missing and not found behavior around trace.
Operators use this runbook note when the alert owner needs a deterministic
diagnosis path. The alternate wording is absent record.

# Diagnosis

Confirm the trace state, compare the latest alert event, and identify the
customer impact before changing the observability workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this observability incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the observability not found workflow.

# Resolution

Apply the dashboard recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the observability
not found finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de observability
e confirmar o sintoma not found antes da escalada.
