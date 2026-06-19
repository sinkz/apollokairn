---
type: Reference
title: Support escalation reference
description: Reference facts for support escalation.
tags: [support, support, skew, reference]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, support severity, drift escalation, customer reference]
systems: [support, customer]
signals: [drift, skew, escalation]
---

# Context

The support workflow reports drift and skew behavior around escalation.
Operators use this reference note when the customer owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the escalation state, compare the latest customer event, and identify the
customer impact before changing the support workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this support incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the support skew workflow.

# Resolution

Apply the severity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the support
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de support
e confirmar o sintoma skew antes da escalada.
