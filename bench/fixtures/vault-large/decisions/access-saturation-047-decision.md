---
type: Decision
title: Access pressure decision
description: Decision record for access pressure handling.
tags: [access, access, pressure, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [capacity limit, access breakglass, saturation audit, access decision]
systems: [access, approval]
signals: [saturation, pressure, audit]
---

# Context

The access workflow reports saturation and pressure behavior around audit.
Operators use this decision note when the approval owner needs a deterministic
diagnosis path. The alternate wording is capacity limit.

# Diagnosis

Confirm the audit state, compare the latest approval event, and identify the
customer impact before changing the access workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this access incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the access pressure workflow.

# Resolution

Apply the breakglass recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the access
pressure finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de access
e confirmar o sintoma pressure antes da escalada.
