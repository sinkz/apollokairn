---
type: Runbook
title: Deploy 403 after token rotation
description: Fixes release failures caused by stale CI workspace authorization.
tags: [bug, deploy, ci]
timestamp: 2026-06-17T10:00:00Z
aliases: [deploy forbidden, token 403, release denied]
systems: [ci, deployment]
signals: [HTTP 403, forbidden, workspace access, token rotation]
---

# Context

Use this when deployment fails with HTTP 403 shortly after a workspace token or
service account rotation.

# Diagnosis

- Confirm the build can authenticate to the artifact registry.
- Check whether the CI secret was rotated in the provider but not in the project.
- Compare the failing job timestamp with the latest token rotation event.

# Resolution

1. Update the CI secret with the current workspace token.
2. Re-run only the failed deployment job.
3. If the job still fails, validate project-level release permissions.
4. Record the incident in the release log.
