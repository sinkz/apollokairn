---
type: Reference
title: Search retrieval reference
description: Reference facts for search retrieval.
tags: [search, search, stale, reference]
timestamp: 2026-06-19T00:00:00Z
aliases: [invalid state, search ranking, expired retrieval, index reference]
systems: [search, index]
signals: [expired, stale, retrieval]
---

# Context

The search workflow reports expired and stale behavior around retrieval.
Operators use this reference note when the index owner needs a deterministic
diagnosis path. The alternate wording is invalid state.

# Diagnosis

Confirm the retrieval state, compare the latest index event, and identify the
customer impact before changing the search workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this search incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the search stale workflow.

# Resolution

Apply the ranking recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the search
stale finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de search
e confirmar o sintoma stale antes da escalada.
