---
type: Runbook
title: Access 403 audit runbook
description: Resolve access forbidden incidents for audit.
tags: [access, access, forbidden]
timestamp: 2026-06-19T00:00:00Z
aliases: [authorization denied, access breakglass, 403 audit]
systems: [access, approval]
signals: [403, forbidden, audit]
---

# Context

The access workflow reports 403 and forbidden behavior around audit.
Operators use this runbook note when the approval owner needs a deterministic
diagnosis path. The alternate wording is authorization denied.

# Diagnosis

Confirm the audit state, compare the latest approval event, and identify the
customer impact before changing the access workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this access incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the access forbidden workflow.

# Resolution

Apply the breakglass recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the access
forbidden finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de access
e confirmar o sintoma forbidden antes da escalada.
