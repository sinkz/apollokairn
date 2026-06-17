---
type: Runbook
title: Session cookie rotation causes login refresh failure
description: Fix login token refresh failures caused by stale session cookie rotation state.
tags: [bug, auth]
timestamp: 2026-06-17T10:08:00Z
aliases: [login token refresh, session cookie rotation, refresh token]
systems: [auth]
signals: [login refresh failed, session cookie, token refresh]
---

# Context

Users are redirected to login after a session cookie rotation. The access token
refresh succeeds in the identity provider but the application still reads the
old cookie state.

# Resolution

Invalidate the stale cookie namespace and force a one-time refresh of the
session metadata cache.
