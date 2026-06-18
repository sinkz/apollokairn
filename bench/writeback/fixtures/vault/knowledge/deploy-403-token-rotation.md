---
type: Runbook
title: Deploy 403 after CI token rotation
description: Fix deploy failures when CI token rotation leaves workspace access stale.
tags: [bug, deploy]
timestamp: 2026-06-17T10:00:00Z
systems: [ci, deployment]
signals: [http 403, token rotation, workspace access, ci secret]
---

# Context

Deploy can fail with HTTP 403 immediately after CI token rotation because the
workspace access secret still points at the old token.

# Diagnosis

The deployment job reaches the provider but receives forbidden responses. The
failure mentions workspace access, stale token, or CI secret permission.

# Resolution

Update the CI secret with the rotated token, verify workspace access, and rerun
the failed deployment job.

# Extra Checks

Also verify namespace-specific Kubernetes secret.
