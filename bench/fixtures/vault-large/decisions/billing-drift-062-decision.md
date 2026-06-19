---
type: Decision
title: Billing skew decision
description: Decision record for billing skew handling.
tags: [billing, billing, skew, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, billing ledger, drift payment, billing decision]
systems: [billing, invoice]
signals: [drift, skew, payment]
---

# Context

The billing workflow reports drift and skew behavior around payment.
Operators use this decision note when the invoice owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the payment state, compare the latest invoice event, and identify the
customer impact before changing the billing workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this billing incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the billing skew workflow.

# Resolution

Apply the ledger recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the billing
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de billing
e confirmar o sintoma skew antes da escalada.
