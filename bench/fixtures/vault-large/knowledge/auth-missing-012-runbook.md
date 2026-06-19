---
type: Runbook
title: Authentication missing token runbook
description: Resolve authentication not found incidents for token.
tags: [auth, authentication, not-found]
timestamp: 2026-06-19T00:00:00Z
aliases: [absent record, authentication identity, missing token]
systems: [auth, session]
signals: [missing, not found, token]
---

# Context

The authentication workflow reports missing and not found behavior around token.
Operators use this runbook note when the session owner needs a deterministic
diagnosis path. The alternate wording is absent record.

# Diagnosis

Confirm the token state, compare the latest session event, and identify the
customer impact before changing the authentication workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this authentication incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the authentication not found workflow.

# Resolution

Apply the identity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the authentication
not found finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de authentication
e confirmar o sintoma not found antes da escalada.
