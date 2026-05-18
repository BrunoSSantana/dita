---
id: T03
title: backend.py — js_api exposta ao frontend
status: done
depends_on: [T01, T02]
files_to_create:
  - backend.py
---

## Goal

Implementar `Backend` — classe exposta ao JS via `js_api` do pywebview. Traduz chamadas do frontend em ações no core; sem lógica de negócio própria.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Backend Python"
- API contract: [docs/api-contract.md](../docs/api-contract.md) — **leitura obrigatória**
- Arquitetura: [docs/architecture.md](../docs/architecture.md)

## Interface Esperada

```python
class Backend:
    recording: bool  # espelhado para hotkey.py

    def set_window(self, window) -> None: ...
    def start_recording(self) -> dict: ...
    def stop_recording(self) -> dict: ...
    def get_config(self) -> dict: ...
    def save_language(self, lang: str) -> dict: ...
    def close(self) -> None: ...
```

## Requisitos

- Todo método (exceto `close`) retorna envelope `{"ok": bool, ...}` — ver api-contract.md
- `stop_recording()` chama `pyperclip.copy()` se `auto_copy: True` na config
- `self.recording` deve ser mantido em sincronia — `True` entre `start` e `stop`
- `save_language()` atualiza `self.transcriber.language` além de persistir em config.json
- Nunca levantar exceção não tratada para o JS
- Instanciar `Transcriber` e `AudioRecorder` no `__init__` — não em cada chamada

## Acceptance Criteria

- [ ] Todos os métodos retornam o envelope correto
- [ ] `stop_recording()` retorna `{"ok": true, "data": {"text": str, "duration": float}}`
- [ ] `stop_recording()` retorna `{"ok": true, "data": {"text": "", "duration": float}}` para silêncio (não é erro)
- [ ] `self.recording` é `False` após `stop_recording()`
- [ ] `save_language("auto")` funciona sem erro
- [ ] `close()` chama `self.window.destroy()`

## Notas

- `set_window()` é chamado em `main.py` após criar a janela — o `__init__` não recebe a janela
- Não importar `webview` neste módulo — apenas usar `self.window` que é injetado

---

## Log

| Data | Status | Observação |
|---|---|---|
| 2026-05-18 | `done` | implementado |
