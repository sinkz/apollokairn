---
type: Runbook
title: Observability timeout trace runbook
description: Resolve observability latency incidents for trace.
tags: [observability, observability, latency]
timestamp: 2026-06-19T00:00:00Z
aliases: [slow response, observability dashboard, timeout trace]
systems: [observability, alert]
signals: [timeout, latency, trace]
---

# Context

The observability workflow reports timeout and latency behavior around trace.
Operators use this runbook note when the alert owner needs a deterministic
diagnosis path. The alternate wording is slow response.

# Diagnosis

Confirm the trace state, compare the latest alert event, and identify the
customer impact before changing the observability workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this observability incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the observability latency workflow.

# Resolution

Apply the dashboard recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the observability
latency finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de observability
e confirmar o sintoma latency antes da escalada.
