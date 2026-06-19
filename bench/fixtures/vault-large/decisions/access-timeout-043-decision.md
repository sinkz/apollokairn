---
type: Decision
title: Access latency decision
description: Decision record for access latency handling.
tags: [access, access, latency, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [slow response, access breakglass, timeout audit, access decision]
systems: [access, approval]
signals: [timeout, latency, audit]
---

# Context

The access workflow reports timeout and latency behavior around audit.
Operators use this decision note when the approval owner needs a deterministic
diagnosis path. The alternate wording is slow response.

# Diagnosis

Confirm the audit state, compare the latest approval event, and identify the
customer impact before changing the access workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this access incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the access latency workflow.

# Resolution

Apply the breakglass recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the access
latency finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de access
e confirmar o sintoma latency antes da escalada.
