# Adapters Para Agentes

Cairn permanece agnóstico de agentes: o vault é Markdown, o índice é local, e
todo agente usa o mesmo contrato de CLI e JSON. Os adapters atuais são arquivos
de instrução gerados, não plugins separados nem bases de conhecimento separadas.

## Targets Suportados

| Target | Comando | Arquivo gerado |
| --- | --- | --- |
| Agentes genéricos | `cairn setup-agent agents --path CAMINHO_DO_VAULT` | `AGENTS.md` |
| Codex | `cairn setup-agent codex --path CAMINHO_DO_VAULT` | `CODEX.md` |
| Claude | `cairn setup-agent claude --path CAMINHO_DO_VAULT` | `CLAUDE.md` |
| OpenCode | `cairn setup-agent opencode --path CAMINHO_DO_VAULT` | `OPENCODE.md` |
| Hermes | `cairn setup-agent hermes --path CAMINHO_DO_VAULT` | `HERMES.md` |
| GitHub Copilot | `cairn setup-agent copilot --path CAMINHO_DO_VAULT` | `.github/copilot-instructions.md` |

Use `--json` quando um instalador ou script de bootstrap precisa do caminho
gerado:

```bash
cairn setup-agent codex --path CAMINHO_DO_VAULT --json
cairn setup-agent copilot --path CAMINHO_DO_VAULT --json
```

O guia gerado orienta o agente a:

- rodar `cairn doctor` quando a saúde do vault for desconhecida;
- usar busca JSON antes de responder;
- preferir recuperação por passagens com `--ranker auto` antes de abrir arquivos completos;
- rodar `cairn vocab suggest` quando o vocabulário pode ser diferente;
- checar `cairn similar` antes de escrever;
- usar types e tags compatíveis com `SCHEMA.md`;
- usar `--body-file` ou `--body-stdin` para Markdown multi-linha;
- rodar `cairn validate` e `cairn index` depois de escritas bem-sucedidas.

## Atualizar Vários Guias

`cairn refresh-guides` lê `.cairn/config.json` e reescreve todos os guias
configurados. Isso é útil quando o mesmo vault deve carregar instruções para
vários harnesses.

```json
{
  "generated_guides": [
    "AGENTS.md",
    "CODEX.md",
    "CLAUDE.md",
    "OPENCODE.md",
    "HERMES.md",
    ".github/copilot-instructions.md"
  ]
}
```

```bash
cairn refresh-guides --path CAMINHO_DO_VAULT --json
```

Os caminhos dos guias precisam ficar dentro do vault. Arquivos de guia gerados
são ignorados por validação, indexação, busca, similaridade e stats.

## O Que Isto Não É

Esses adapters não adicionam dependências de runtime e não exigem Codex, Claude,
OpenCode, Hermes ou GitHub Copilot instalados. Eles são arquivos de instrução
portáveis sobre a superfície estável de CLI/JSON. Pacotes de plugin ou servidores
MCP futuros devem continuar opcionais e fora do core sem dependências.
