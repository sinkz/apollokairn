---
type: Runbook
title: Sessão expira após autenticação
description: Corrige expiração de sessão depois da renovação do token de autenticação.
tags: [bug, auth, support]
timestamp: 2026-06-17T10:00:00Z
systems: [support-portal, auth]
signals: [sessao expira, renovacao token, autenticacao]
---

# Contexto

Usuários podem perder a sessão logo após autenticação quando o token renovado não
é propagado para o cookie ativo.

# Solução

Forçar renovação do cookie de sessão e validar se o serviço de autenticação
publicou o token mais recente.
