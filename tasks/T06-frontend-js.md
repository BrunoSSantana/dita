---
id: T06
title: frontend/app.js — lógica JS e bridge pywebview
status: done
depends_on: [T03, T05]
files_to_create:
  - frontend/app.js
---

## Goal

Implementar toda a lógica do frontend: máquina de estados, animações, bridge JS↔Python e função `handleHotkey()` que o `hotkey.py` aciona via `evaluate_js`.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Frontend / app.js"
- API contract: [docs/api-contract.md](../docs/api-contract.md) — **leitura obrigatória**
- `hotkey.py` chama `window.evaluate_js("handleHotkey()")` — esta função deve existir no escopo global

## Máquina de Estados

```
idle ──[gravar / handleHotkey]──→ recording
recording ──[parar / handleHotkey]──→ processing
processing ──[texto ok]──→ done
processing ──[sem áudio]──→ idle
done ──[gravar]──→ recording
```

`handleHotkey()` deve respeitar o estado atual:
- `idle` → `startRecording()`
- `recording` → `stopRecording()`
- `processing` → ignorar
- `done` → `startRecording()` (limpa resultado anterior)

## Funções Requeridas

| Função | Descrição |
|---|---|
| `handleHotkey()` | Entry point do atalho global — **deve ser global (não `const`/`let`)** |
| `toggleRecord()` | Usado pelo botão #rec-btn |
| `startRecording()` | Chama `api.start_recording()`, atualiza UI |
| `stopRecording()` | Atualiza UI para "processando", chama `api.stop_recording()` |
| `cycleLang()` | Cicla idioma e chama `api.save_language()` |
| `clearAll()` | Reset completo da UI e estado |
| `copyManual()` | Copia transcript atual via `navigator.clipboard.writeText()` |
| `typeText(text, onDone)` | Efeito typewriter 22ms/char |
| `showCheck()` | Exibe ícone de check por 2s |
| `scheduleClose()` | Busca config e fecha após `auto_close_after` s |
| `setStatus(text)` | Atualiza `#status` |
| `setBars(mode)` | Aplica classe `idle`/`active`/`done` nas barras |
| `resetUi()` | Reseta todos os elementos para estado inicial |

## Requisitos

- `handleHotkey` deve ser declarada com `function` (não `const`) para ser acessível via `evaluate_js`
- Waveform: gerar 40 barras no carregamento com `--hi`, `--hlo`, `--d` aleatórios
- Timer: formato `MM:SS` com `setInterval` — limpar interval em `stopRecording()`
- `copyManual()` usa `navigator.clipboard.writeText()` — não assume que pyperclip já copiou
- `stopRecording()` atualiza status para "processando" **antes** de chamar a API (a call bloqueia 2-10s)
- Fechar com `Esc`: listener em `document.addEventListener('keydown')`

## Acceptance Criteria

- [ ] `handleHotkey` acessível globalmente
- [ ] Máquina de estados sem transições inválidas
- [ ] Timer limpo ao parar gravação
- [ ] `stopRecording()` desabilita `#rec-btn` durante processamento e reabilita após
- [ ] `scheduleClose()` não fecha se `auto_close_after === 0`
- [ ] `copyManual()` funciona mesmo se `auto_copy` for false na config
- [ ] Tecla `Esc` chama `api.close()`

## Notas

- `window.pywebview` pode não estar disponível imediatamente no carregamento — aguardar evento `pywebviewready` se necessário
- `navigator.clipboard` requer contexto seguro; no pywebview isso é garantido

---

## Log

| Data | Status | Observação |
|---|---|---|
| 2026-05-18 | `done` | implementado |
