---
type: Runbook
title: Mobile deploy 403 after token rotation
description: Fix mobile release deployment failures after mobile signing token rotation.
tags: [bug, deploy, mobile]
timestamp: 2026-06-17T10:09:00Z
aliases: [mobile deploy forbidden, mobile token 403]
systems: [mobile]
signals: [mobile deploy 403, token rotation, forbidden]
---

# Context

Mobile deployment fails with HTTP 403 after rotating the mobile signing token.

# Resolution

Update the mobile release secret, clear the cached signing session, and re-run
the mobile deployment job.
