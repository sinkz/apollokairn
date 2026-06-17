---
type: Runbook
title: JWT expired because of clock skew
description: Fix authentication failures when tokens appear expired before their expected lifetime.
tags: [bug, auth]
timestamp: 2026-06-17T10:01:00Z
aliases: [jwt expired, token invalid, clock drift]
systems: [auth]
signals: [jwt expired, iat in future, clock skew, unauthorized]
---

# Context

Requests fail with unauthorized responses even though the JWT was issued
recently. Logs show token timestamps slightly in the future or already expired.

# Diagnosis

Compare application server time, identity provider time, and database time.

# Resolution

Fix NTP synchronization, allow a small validation leeway, and rotate affected
sessions only after clocks are stable.
