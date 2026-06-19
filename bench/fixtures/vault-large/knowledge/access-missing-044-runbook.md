---
type: Runbook
title: Access missing audit runbook
description: Resolve access not found incidents for audit.
tags: [access, access, not-found]
timestamp: 2026-06-19T00:00:00Z
aliases: [absent record, access breakglass, missing audit]
systems: [access, approval]
signals: [missing, not found, audit]
---

# Context

The access workflow reports missing and not found behavior around audit.
Operators use this runbook note when the approval owner needs a deterministic
diagnosis path. The alternate wording is absent record.

# Diagnosis

Confirm the audit state, compare the latest approval event, and identify the
customer impact before changing the access workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this access incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the access not found workflow.

# Resolution

Apply the breakglass recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the access
not found finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de access
e confirmar o sintoma not found antes da escalada.
