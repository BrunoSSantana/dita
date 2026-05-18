---
id: T05
title: frontend/index.html — estrutura HTML
status: done
depends_on: []
files_to_create:
  - frontend/index.html
---

## Goal

Implementar o HTML da interface — estrutura semântica mínima que o `app.js` e o `style.css` esperam.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Frontend / index.html"
- `frontend/style.css` já implementado — IDs e classes devem estar alinhados

## IDs e Classes Requeridos pelo CSS e JS

| Elemento | ID/Classe | Tipo |
|---|---|---|
| Wrapper externo | `#overlay` | div |
| Container principal | `#app` | div |
| Header | `#header` | div |
| Botão de idioma | `#lang-btn` | button |
| Waveform | `#waveform` | div (barras geradas por JS) |
| Caixa de texto | `#text-box` | div |
| Placeholder | `#placeholder` | span |
| Transcrição | `#transcript` | span |
| Ícone de check | `#check-icon` | i |
| Linha de status | `#status-row` | div |
| Status | `#status` | span |
| Timer | `#timer` | span |
| Controles | `#controls` | div |
| Botão limpar | `#clear-btn` | button |
| Botão gravar | `#rec-btn` | button |
| Ícone gravar | `#rec-icon` | i |
| Botão copiar | `#copy-btn` | button |

## Requisitos

- Carregar Tabler Icons via CDN (para os ícones `ti-*`)
- Carregar `style.css` no `<head>`
- Carregar `app.js` no final do `<body>`
- `lang="pt-BR"`, charset UTF-8
- Botões usam classes `.icon-btn` exceto `#rec-btn` (tem classe própria)
- Ícones: `ti-trash` (clear), `ti-microphone` (rec), `ti-copy` (copy), `ti-check` (check)

## Acceptance Criteria

- [ ] Todos os IDs da tabela acima presentes
- [ ] Tabler Icons carrega (verificar CDN no `<head>`)
- [ ] `app.js` e `style.css` referenciados com caminhos relativos corretos
- [ ] Página válida com `lang` e `charset`

---

## Log

| Data | Status | Observação |
|---|---|---|
| 2026-05-18 | `done` | Implementado |
