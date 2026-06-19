---
type: Decision
title: Mobile skew decision
description: Decision record for mobile skew handling.
tags: [mobile, mobile, skew, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, mobile release, drift store, mobile decision]
systems: [mobile, build]
signals: [drift, skew, store]
---

# Context

The mobile workflow reports drift and skew behavior around store.
Operators use this decision note when the build owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the store state, compare the latest build event, and identify the
customer impact before changing the mobile workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this mobile incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the mobile skew workflow.

# Resolution

Apply the release recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the mobile
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de mobile
e confirmar o sintoma skew antes da escalada.
