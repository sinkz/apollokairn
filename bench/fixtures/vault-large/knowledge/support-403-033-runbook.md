---
type: Runbook
title: Support 403 escalation runbook
description: Resolve support forbidden incidents for escalation.
tags: [support, support, forbidden]
timestamp: 2026-06-19T00:00:00Z
aliases: [authorization denied, support severity, 403 escalation]
systems: [support, customer]
signals: [403, forbidden, escalation]
---

# Context

The support workflow reports 403 and forbidden behavior around escalation.
Operators use this runbook note when the customer owner needs a deterministic
diagnosis path. The alternate wording is authorization denied.

# Diagnosis

Confirm the escalation state, compare the latest customer event, and identify the
customer impact before changing the support workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this support incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the support forbidden workflow.

# Resolution

Apply the severity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the support
forbidden finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de support
e confirmar o sintoma forbidden antes da escalada.
