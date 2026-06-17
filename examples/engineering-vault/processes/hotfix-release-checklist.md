---
type: Process
title: Hotfix release checklist
description: Minimal checklist for releasing urgent production fixes.
tags: [release, deploy]
timestamp: 2026-06-17T10:05:00Z
aliases: [urgent release, production hotfix]
systems: [deployment]
signals: [hotfix, rollback, emergency release]
---

# Entry Criteria

- The defect has a confirmed production impact.
- The proposed fix is scoped and reviewed.
- Rollback instructions are known before deploy starts.

# Checklist

1. Link the incident or support ticket.
2. Run the focused test suite.
3. Build the release artifact.
4. Deploy to the smallest safe environment first.
5. Verify the production signal that motivated the hotfix.
6. Announce completion and rollback status.

# Rollback

Use the previous release artifact unless the incident owner explicitly approves
a forward fix.
