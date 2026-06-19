---
type: Runbook
title: Search missing retrieval runbook
description: Resolve search not found incidents for retrieval.
tags: [search, search, not-found]
timestamp: 2026-06-19T00:00:00Z
aliases: [absent record, search ranking, missing retrieval]
systems: [search, index]
signals: [missing, not found, retrieval]
---

# Context

The search workflow reports missing and not found behavior around retrieval.
Operators use this runbook note when the index owner needs a deterministic
diagnosis path. The alternate wording is absent record.

# Diagnosis

Confirm the retrieval state, compare the latest index event, and identify the
customer impact before changing the search workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this search incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the search not found workflow.

# Resolution

Apply the ranking recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the search
not found finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de search
e confirmar o sintoma not found antes da escalada.
