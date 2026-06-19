---
type: Decision
title: Support pressure decision
description: Decision record for support pressure handling.
tags: [support, support, pressure, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [capacity limit, support severity, saturation escalation, support decision]
systems: [support, customer]
signals: [saturation, pressure, escalation]
---

# Context

The support workflow reports saturation and pressure behavior around escalation.
Operators use this decision note when the customer owner needs a deterministic
diagnosis path. The alternate wording is capacity limit.

# Diagnosis

Confirm the escalation state, compare the latest customer event, and identify the
customer impact before changing the support workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this support incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the support pressure workflow.

# Resolution

Apply the severity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the support
pressure finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de support
e confirmar o sintoma pressure antes da escalada.
