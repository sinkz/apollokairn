---
type: Runbook
title: Authentication 403 token runbook
description: Resolve authentication forbidden incidents for token.
tags: [auth, authentication, forbidden]
timestamp: 2026-06-19T00:00:00Z
aliases: [authorization denied, authentication identity, 403 token]
systems: [auth, session]
signals: [403, forbidden, token]
---

# Context

The authentication workflow reports 403 and forbidden behavior around token.
Operators use this runbook note when the session owner needs a deterministic
diagnosis path. The alternate wording is authorization denied.

# Diagnosis

Confirm the token state, compare the latest session event, and identify the
customer impact before changing the authentication workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this authentication incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the authentication forbidden workflow.

# Resolution

Apply the identity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the authentication
forbidden finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de authentication
e confirmar o sintoma forbidden antes da escalada.
