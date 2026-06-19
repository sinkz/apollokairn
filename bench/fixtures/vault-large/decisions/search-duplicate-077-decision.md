---
type: Decision
title: Search repeat decision
description: Decision record for search repeat handling.
tags: [search, search, repeat, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [repeated entry, search ranking, duplicate retrieval, search decision]
systems: [search, index]
signals: [duplicate, repeat, retrieval]
---

# Context

The search workflow reports duplicate and repeat behavior around retrieval.
Operators use this decision note when the index owner needs a deterministic
diagnosis path. The alternate wording is repeated entry.

# Diagnosis

Confirm the retrieval state, compare the latest index event, and identify the
customer impact before changing the search workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this search incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the search repeat workflow.

# Resolution

Apply the ranking recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the search
repeat finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de search
e confirmar o sintoma repeat antes da escalada.
