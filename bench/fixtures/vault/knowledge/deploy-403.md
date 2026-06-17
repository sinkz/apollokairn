---
type: Runbook
title: Deploy 403 after token rotation
description: Fix CI deploy failures caused by stale workspace authorization after token rotation.
tags: [bug, deploy, ci]
timestamp: 2026-06-17T10:00:00Z
aliases: [deploy forbidden, token 403, release denied]
systems: [ci, deployment]
signals: [HTTP 403, forbidden, workspace access, token rotation]
---

# Context

Deployment fails with HTTP 403 shortly after a CI workspace token or service
account secret was rotated.

# Diagnosis

Check whether the deployment provider received the new token. Confirm the
artifact registry still accepts the CI identity.

# Resolution

Update the CI secret, re-run the failed deploy job, and record the rotation
timestamp in the release log.
