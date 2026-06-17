---
type: Runbook
title: Consolidated deploy forbidden token fix
description: Consolidated note for duplicate deploy forbidden token incidents.
tags: [bug, deploy, duplicate]
timestamp: 2026-06-17T10:11:00Z
aliases: [deploy forbidden token duplicate, consolidated deploy 403]
systems: [ci]
signals: [deploy forbidden, token duplicate, HTTP 403]
---

# Context

Several daily notes described the same deploy forbidden token failure. This
consolidated note is the canonical fix.

# Resolution

Update the CI token, verify workspace access, and merge duplicate observations
into this note.
