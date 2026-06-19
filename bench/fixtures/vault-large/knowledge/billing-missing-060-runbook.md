---
type: Runbook
title: Billing missing payment runbook
description: Resolve billing not found incidents for payment.
tags: [billing, billing, not-found]
timestamp: 2026-06-19T00:00:00Z
aliases: [absent record, billing ledger, missing payment]
systems: [billing, invoice]
signals: [missing, not found, payment]
---

# Context

The billing workflow reports missing and not found behavior around payment.
Operators use this runbook note when the invoice owner needs a deterministic
diagnosis path. The alternate wording is absent record.

# Diagnosis

Confirm the payment state, compare the latest invoice event, and identify the
customer impact before changing the billing workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this billing incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the billing not found workflow.

# Resolution

Apply the ledger recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the billing
not found finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de billing
e confirmar o sintoma not found antes da escalada.
