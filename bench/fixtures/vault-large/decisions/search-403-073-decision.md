---
type: Decision
title: Search forbidden decision
description: Decision record for search forbidden handling.
tags: [search, search, forbidden, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [authorization denied, search ranking, 403 retrieval, search decision]
systems: [search, index]
signals: [403, forbidden, retrieval]
---

# Context

The search workflow reports 403 and forbidden behavior around retrieval.
Operators use this decision note when the index owner needs a deterministic
diagnosis path. The alternate wording is authorization denied.

# Diagnosis

Confirm the retrieval state, compare the latest index event, and identify the
customer impact before changing the search workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this search incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the search forbidden workflow.

# Resolution

Apply the ranking recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the search
forbidden finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de search
e confirmar o sintoma forbidden antes da escalada.
