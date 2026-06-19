---
type: Decision
title: Deployment skew decision
description: Decision record for deployment skew handling.
tags: [deploy, deployment, skew, decision]
timestamp: 2026-06-19T00:00:00Z
aliases: [clock mismatch, deployment rollback, drift artifact, deployment decision]
systems: [deploy, release]
signals: [drift, skew, artifact]
---

# Context

The deployment workflow reports drift and skew behavior around artifact.
Operators use this decision note when the release owner needs a deterministic
diagnosis path. The alternate wording is clock mismatch.

# Diagnosis

Confirm the artifact state, compare the latest release event, and identify the
customer impact before changing the deployment workflow.
The owner triage checklist records customer impact, escalation priority, and the
single accountable owner for this deployment incident.
Cross-document lookup should connect the runbook, decision record, and reference
facts for the deployment skew workflow.

# Resolution

Apply the rollback recovery playbook and the diagnosis resolution checklist.
Then record the owner decision and update the incident log with the deployment
skew finding.

# Atendimento

Para suporte, resolver incidente cliente prioridade usando o playbook de deployment
e confirmar o sintoma skew antes da escalada.
