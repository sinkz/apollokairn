---
type: Process
title: Hotfix release rollback process
description: Process for production hotfix release rollback when verification fails.
tags: [release, deploy]
timestamp: 2026-06-17T10:12:00Z
aliases: [hotfix rollback, production rollback]
systems: [deployment]
signals: [hotfix, rollback, production release]
---

# Entry Criteria

Use when a hotfix release fails production verification and rollback is safer
than a forward fix.

# Steps

1. Stop the rollout.
2. Redeploy the previous artifact.
3. Verify the original production signal.
4. Announce rollback status.
