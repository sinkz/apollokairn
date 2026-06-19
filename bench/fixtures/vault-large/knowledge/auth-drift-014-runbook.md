---
type: Runbook
title: Authentication drift token runbook
description: Resolve authentication skew incidents for token.
tags: [auth, authentication, skew]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, authentication identity, drift token]
systems: [auth, session]
signals: [drift, skew, token]
---

# Context

The authentication workflow reports drift and skew behavior around token.
Operators use this runbook note when the session owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the token state, compare the latest session event, and identify the
customer impact before changing the authentication workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this authentication incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the authentication skew workflow.

# Resolution

Apply the identity recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the authentication
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de authentication
e confirmar o sintoma skew antes da escalada.
