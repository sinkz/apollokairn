---
type: Runbook
title: Access drift audit runbook
description: Resolve access skew incidents for audit.
tags: [access, access, skew]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, access breakglass, drift audit]
systems: [access, approval]
signals: [drift, skew, audit]
---

# Context

The access workflow reports drift and skew behavior around audit.
Operators use this runbook note when the approval owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the audit state, compare the latest approval event, and identify the
customer impact before changing the access workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this access incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the access skew workflow.

# Resolution

Apply the breakglass recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the access
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de access
e confirmar o sintoma skew antes da escalada.
