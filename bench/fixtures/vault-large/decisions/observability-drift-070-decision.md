---
type: Decision
title: Observability skew decision
description: Decision record for observability skew handling.
tags: [observability, observability, skew, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, observability dashboard, drift trace, observability decision]
systems: [observability, alert]
signals: [drift, skew, trace]
---

# Context

The observability workflow reports drift and skew behavior around trace.
Operators use this decision note when the alert owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the trace state, compare the latest alert event, and identify the
customer impact before changing the observability workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this observability incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the observability skew workflow.

# Resolution

Apply the dashboard recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the observability
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de observability
e confirmar o sintoma skew antes da escalada.
