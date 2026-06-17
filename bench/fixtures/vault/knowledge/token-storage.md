---
type: Reference
title: Token storage policy
description: General notes about token storage, unrelated to deploy failures.
tags: [auth]
timestamp: 2026-06-17T10:02:00Z
aliases: [secret storage, credential storage]
systems: [auth]
signals: [token, secret]
---

# Notes

Store service credentials in the approved secret manager. This document mentions
tokens but does not explain deploy 403 failures or JWT clock skew.
