---
id: T08
title: tests/ — testes de config.py
status: done
depends_on: []
files_to_create:
  - tests/__init__.py
  - tests/test_config.py
---

## Goal

Testar `config.py` — único módulo com lógica própria suficiente para justificar testes. `audio.py` e `transcriber.py` são melhor validados rodando a app; `backend.py`, `hotkey.py` e `main.py` exigiriam mocks de pywebview/pynput sem retorno proporcional.

## Contexto

- Convenções: [docs/conventions.md](../docs/conventions.md)

## Casos a cobrir

- `load_config()` retorna defaults quando `config.json` não existe
- `load_config()` faz merge com defaults quando `config.json` tem campos parciais
- `load_config()` retorna defaults quando `config.json` está corrompido (JSON inválido)
- `save_config(patch)` persiste somente os campos do patch, mantém os demais
- `save_config` + `load_config` round-trip: o que se salva é o que se lê

## Acceptance Criteria

- [ ] `pytest tests/` passa sem nenhuma dependência externa instalada
- [ ] `tmp_path` do pytest isola cada teste — sem tocar no `config.json` real
- [ ] Sem imports de qualquer módulo além de `config` e stdlib

---

## Log

| Data | Status | Observação |
|---|---|---|
| — | `pending` | — |
