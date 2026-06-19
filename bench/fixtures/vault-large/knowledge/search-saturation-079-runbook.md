---
type: Runbook
title: Search saturation retrieval runbook
description: Resolve search pressure incidents for retrieval.
tags: [search, search, pressure]
timestamp: 2026-06-19T00:00:00Z
aliases: [capacity limit, search ranking, saturation retrieval]
systems: [search, index]
signals: [saturation, pressure, retrieval]
---

# Context

The search workflow reports saturation and pressure behavior around retrieval.
Operators use this runbook note when the index owner needs a deterministic
diagnosis path. The alternate wording is capacity limit.

# Diagnosis

Confirm the retrieval state, compare the latest index event, and identify the
customer impact before changing the search workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this search incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the search pressure workflow.

# Resolution

Apply the ranking recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the search
pressure finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de search
e confirmar o sintoma pressure antes da escalada.
