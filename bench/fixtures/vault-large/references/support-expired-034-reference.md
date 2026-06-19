---
type: Reference
title: Support escalation reference
description: Reference facts for support escalation.
tags: [support, support, stale, reference]
timestamp: 2026-06-19T00:00:00Z
aliases: [invalid state, support severity, expired escalation, customer reference]
systems: [support, customer]
signals: [expired, stale, escalation]
---

# Context

The support workflow reports expired and stale behavior around escalation.
Operators use this reference note when the customer owner needs a deterministic
diagnosis path. The alternate wording is invalid state.

# Diagnosis

Confirm the escalation state, compare the latest customer event, and identify the
customer impact before changing the support workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this support incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the support stale workflow.

# Resolution

Apply the severity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the support
stale finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de support
e confirmar o sintoma stale antes da escalada.
